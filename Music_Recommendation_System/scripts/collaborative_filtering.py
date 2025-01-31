import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_absolute_error, mean_squared_error
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate
import os

# Ensure models directory exists for saving
os.makedirs('./models', exist_ok=True)

# Load the cleaned data
df = pd.read_csv('./data/cleaned_data.csv')

# Display unique user identifiers (e.g., 'platform')
print("Available User Identifiers:", df['platform'].unique())

# Ensure 'platform' represents unique users or create a mock user ID if necessary
if 'platform' not in df.columns:
    df['platform'] = 'user_' + (df.index // 10).astype(str)  # Mock user IDs based on index if necessary

def prepare_user_item_matrix(df):
    """
    Prepares the user-item matrix from the input DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing columns: 'platform', 'master_metadata_track_name', 'play_count'.

    Returns:
    pd.DataFrame: User-Item matrix.
    """
    user_item_matrix = df.pivot_table(
        index='platform',
        columns='master_metadata_track_name',
        values='play_count',
        aggfunc='sum',
        fill_value=0
    )
    return user_item_matrix


# Create the User-Item matrix
user_item_matrix = prepare_user_item_matrix(df)

# Save User-Item Matrix to CSV
user_item_matrix.to_csv('./models/user_item_matrix.csv')
print("User-item matrix saved successfully!")

# Calculate the cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)

# Convert to DataFrame for easier reading
user_similarity_df = pd.DataFrame(user_similarity, 
                                  index=user_item_matrix.index, 
                                  columns=user_item_matrix.index)

# Save User Similarity Matrix
user_similarity_df.to_csv('./models/user_similarity_matrix.csv')
print("User similarity matrix saved successfully!")

# Function to recommend songs based on similar users
def recommend_songs(user, user_item_matrix, user_similarity_df, top_n=5):
    """
    Recommend songs based on collaborative filtering (user-based).
    """
    if user not in user_similarity_df.index:
        print(f"Error: User '{user}' not found in the user similarity matrix.")
        return pd.Series([], dtype=float)  # Return an empty series if the user is not found

    # Get the most similar users (excluding the target user itself)
    similar_users = user_similarity_df[user].sort_values(ascending=False).iloc[1:top_n+1].index

    # Get the songs that the similar users have played
    recommended_songs = user_item_matrix.loc[similar_users].sum().sort_values(ascending=False)

    # Filter out songs the user has already played
    already_played_songs = user_item_matrix.loc[user] > 0
    recommended_songs = recommended_songs[~recommended_songs.index.isin(user_item_matrix.columns[already_played_songs])]

    # Return top N recommended songs
    return recommended_songs.head(top_n)

# SVD-based Matrix Factorization
def svd_recommend(user, df, n_recommendations=5):
    reader = Reader(rating_scale=(0, user_item_matrix.max().max()))
    data = Dataset.load_from_df(df[['platform', 'master_metadata_track_name', 'play_count']], reader)

    svd = SVD()
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    trainset = data.build_full_trainset()
    svd.fit(trainset)

    # Save the trained SVD model
    with open('./models/svd_model.pkl', 'wb') as model_file:
        pickle.dump(svd, model_file)
    print("SVD model saved successfully!")

    all_songs = df['master_metadata_track_name'].unique()
    user_songs = df[df['platform'] == user]['master_metadata_track_name']

    recommendations = []
    for song in all_songs:
        if song not in user_songs.values:
            est_play_count = svd.predict(user, song).est
            recommendations.append((song, est_play_count))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [song for song, _ in recommendations[:n_recommendations]]

# Evaluation Metrics: Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE)
def evaluate_model(user_item_matrix, user_similarity_df, top_n=5):
    true_ratings = []
    predicted_ratings = []

    for user in user_item_matrix.index:
        recommended_songs = recommend_songs(user, user_item_matrix, user_similarity_df, top_n)

        # Collect true ratings and predicted ratings
        for song in recommended_songs.index:
            true_rating = user_item_matrix.loc[user, song]
            predicted_rating = recommended_songs[song]

            true_ratings.append(true_rating)
            predicted_ratings.append(predicted_rating)

    mae = mean_absolute_error(true_ratings, predicted_ratings)
    rmse = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
    return mae, rmse

# Example: Recommend songs for a user
user = 'Windows 10 (10.0.22000; x64; AppX)'  # Replace with a valid user ID from your data
if user in user_item_matrix.index:
    recommended_songs = recommend_songs(user, user_item_matrix, user_similarity_df, top_n=5)
    print(f"\nRecommended songs for {user}:")
    print(recommended_songs)

    svd_recommendations = svd_recommend(user, df, n_recommendations=5)
    print(f"\nSVD Recommendations for {user}:")
    print(svd_recommendations)
else:
    print(f"\nUser '{user}' not found in the user-item matrix.")

# Evaluate the model
mae, rmse = evaluate_model(user_item_matrix, user_similarity_df, top_n=5)
print(f"\nModel Evaluation:\nMean Absolute Error (MAE): {mae}\nRoot Mean Squared Error (RMSE): {rmse}")
