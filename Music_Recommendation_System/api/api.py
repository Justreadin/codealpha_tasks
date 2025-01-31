from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD, Dataset, Reader
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/music_recommendation_ai")
conn = psycopg2.connect(DATABASE_URL)

# Spotify OAuth configuration
sp_oauth = SpotifyOAuth(
    client_id="0d148e213e894056afe71f928b7500b3",
    client_secret="cc302a12c30b4ace9ae3e847c4247426",
    redirect_uri="http://localhost:8000/callback",
    scope="user-library-read user-top-read playlist-read-private"
)

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Initialize FastAPI app
app = FastAPI(
    name="Lyrical AI",
    title="Music Recommendation API",
    description="Hybrid Filtering for Personalized Music Recommendations"
)

# Load cleaned data
df = pd.read_csv('./data/cleaned_data.csv')

# Ensure 'platform' represents unique users or create mock user IDs
if 'platform' not in df.columns:
    df['platform'] = 'user_' + (df.index // 10).astype(str)

# Create the User-Item matrix
user_item_matrix = df.pivot_table(
    index='platform',
    columns='master_metadata_track_name',
    values='play_count',
    aggfunc='sum',
    fill_value=0
)

# Calculate cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Train or load the SVD model
try:
    with open('models/svd_model.pkl', 'rb') as model_file:
        svd = pickle.load(model_file)
except FileNotFoundError:
    reader = Reader(rating_scale=(0, user_item_matrix.max().max()))
    data = Dataset.load_from_df(df[['platform', 'master_metadata_track_name', 'play_count']], reader)
    trainset = data.build_full_trainset()
    svd = SVD()
    svd.fit(trainset)
    with open('models/svd_model.pkl', 'wb') as model_file:
        pickle.dump(svd, model_file)

# Models for API requests
class User(BaseModel):
    phone_model: str
    name: str

class PlatformData(BaseModel):
    platform: str
    ts: datetime
    ms_played: int
    conn_country: str
    track_name: str
    album_name: str
    artist_name: str
    spotify_track_uri: str
    reason_start: str
    reason_end: str
    shuffle: bool
    offline: bool
    offline_timestamp: datetime
    incognito_mode: bool

class BatchRecommendationRequest(BaseModel):
    user_ids: List[str]
    top_n: int = 5

# Helper function: Insert data into database
def insert_data_to_db(data: PlatformData):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO spotify_tracks (
                    ts, platform, ms_played, conn_country, 
                    master_metadata_track_name, master_metadata_album_album_name, 
                    master_metadata_album_artist_name, spotify_track_uri, 
                    reason_start, reason_end, shuffle, offline, 
                    offline_timestamp, incognito_mode
                ) VALUES (
                    %(ts)s, %(platform)s, %(ms_played)s, %(conn_country)s, 
                    %(track_name)s, %(album_name)s, %(artist_name)s, %(spotify_track_uri)s, 
                    %(reason_start)s, %(reason_end)s, %(shuffle)s, %(offline)s, 
                    %(offline_timestamp)s, %(incognito_mode)s
                )
                ON CONFLICT (spotify_track_uri) DO NOTHING;
            """, data.dict())
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Endpoint: Fetch all available users
@app.get("/users/", response_model=List[str])
async def get_users():
    available_users = user_item_matrix.index.tolist()
    return available_users

@app.get("/home-data")
async def get_home_data():
    try:
        app_logger.info("Fetching home data")
        # Example response
        data = {"message": "Welcome to the home view"}
        app_logger.info("Successfully fetched home data")
        return data
    except Exception as e:
        error_logger.error(f"Error in /home-data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint: Register a new user
@app.post("/user/register")
async def register_user(user: User):
    try:
        # Check if the user already exists in the database
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM spotify_tracks WHERE platform = %s LIMIT 1", (user.phone_model,))
            existing_user = cur.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists with this phone model.")

        # Insert a new placeholder record for the user
        placeholder_data = PlatformData(
            platform=user.phone_model,
            ts=datetime.now(),
            ms_played=0,
            conn_country="unknown",
            track_name="unknown",
            album_name="unknown",
            artist_name="unknown",
            spotify_track_uri="unknown",
            reason_start="unknown",
            reason_end="unknown",
            shuffle=False,
            offline=False,
            offline_timestamp=datetime.now(),
            incognito_mode=False,
        )
        insert_data_to_db(placeholder_data)

        return {"message": f"User '{user.name}' registered successfully with phone model '{user.phone_model}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

# Endpoint: Add new platform data
@app.post("/platform/add")
async def add_platform_data(data: PlatformData):
    try:
        insert_data_to_db(data)
        return {"message": f"Platform data for {data.platform} added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding platform data: {e}")

# Endpoint: Fetch Spotify data for a platform
@app.get("/platform/{platform_id}/spotify_data")
async def fetch_spotify_data(platform_id: str):
    try:
        user_top_tracks = sp.current_user_top_tracks(limit=10)
        return {
            "platform_id": platform_id,
            "spotify_top_tracks": [
                {"name": track["name"], "artist": track["artists"][0]["name"], "uri": track["uri"]}
                for track in user_top_tracks["items"]
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Spotify data: {e}")


#@app.get("/recommend/user/{user_id}")
#async def recommend_user_based(user_id: str, top_n: int = 5):
#    if user_id not in user_similarity_df.index:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found.")
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).iloc[1:top_n+1].index
    recommended_songs = user_item_matrix.loc[similar_users].sum().sort_values(ascending=False)
#    already_played_songs = user_item_matrix.loc[user_id] > 0
#    recommended_songs = recommended_songs[~recommended_songs.index.isin(user_item_matrix.columns[already_played_songs])]
#    return recommended_songs.head(top_n).to_dict()

@app.get("/recommend/combined/{user_id}")
async def recommend_combined(user_id: str, top_n: int = 5):
    # Personalized song recommendations
    user_songs = df[df['platform'] == user_id]['master_metadata_track_name']
    all_songs = df['master_metadata_track_name'].unique()

    svd_recommendations = []
    for song in all_songs:
        if song not in user_songs.values:
            est_play_count = svd.predict(user_id, song).est
            svd_recommendations.append((song, est_play_count))

    svd_recommendations.sort(key=lambda x: x[1], reverse=True)
    svd_recommendations = [song for song, _ in svd_recommendations[:top_n]]

    # Spotify new releases
    results_new_releases = sp.new_releases(country="US", limit=top_n)
    new_releases = results_new_releases['albums']['items']

    spotify_recommendations = [
        {
            "name": release['name'],
            "artist": ', '.join(artist['name'] for artist in release['artists']),
            "url": release['external_urls']['spotify']
        } for release in new_releases
    ]

    # Return combined recommendations
    combined_recommendations = {
        "personalized_recommendations": svd_recommendations,
        "spotify_recommendations": spotify_recommendations
    }

    return combined_recommendations


@app.get("/recommend/new_releases/")
async def recommend_new_releases(top_n: int = 5):
    results = sp.new_releases(country="US", limit=top_n)
    new_releases = results['albums']['items']

    recommendations = []
    for release in new_releases:
        recommendations.append({
            "name": release['name'],
            "artist": ', '.join(artist['name'] for artist in release['artists']),
            "url": release['external_urls']['spotify']
        })

    return {"recommendations": recommendations}

@app.get("/evaluate/") 
async def evaluate_model():
    true_ratings = []
    predicted_ratings = []

    for user in user_item_matrix.index:
        similar_users = user_similarity_df[user].sort_values(ascending=False).iloc[1:6].index
        recommended_songs = user_item_matrix.loc[similar_users].sum().sort_values(ascending=False)
        already_played_songs = user_item_matrix.loc[user] > 0
        recommended_songs = recommended_songs[~recommended_songs.index.isin(user_item_matrix.columns[already_played_songs])]

        for song in recommended_songs.index:
            true_rating = user_item_matrix.loc[user, song]
            predicted_rating = recommended_songs[song]
            true_ratings.append(true_rating)
            predicted_ratings.append(predicted_rating)

    mae = np.mean(np.abs(np.array(true_ratings) - np.array(predicted_ratings)))
    rmse = np.sqrt(np.mean((np.array(true_ratings) - np.array(predicted_ratings)) ** 2))

    return {"mae": mae, "rmse": rmse}

@app.get("/recommend/similar_songs/{song_name}")
async def recommend_similar_songs(song_name: str, top_n: int = 5):
    if song_name not in df['master_metadata_track_name'].values:
        raise HTTPException(status_code=404, detail="Song not found.")
    song_vector = user_item_matrix[song_name].values.reshape(1, -1)
    similarity_scores = cosine_similarity(song_vector, user_item_matrix.T)[0]
    top_similar_songs = np.argsort(similarity_scores)[-top_n - 1:-1][::-1]
    return [{"song": user_item_matrix.columns[idx]} for idx in top_similar_songs]

@app.get("/recommend/trending/")
async def get_trending_songs(top_n: int = 10):
    results = sp.new_releases(country="US", limit=top_n)
    return [{"name": album['name'], "artist": album['artists'][0]['name']} for album in results['albums']['items']]

@app.get("/user/{user_id}/generate_playlist/")
async def generate_playlist(user_id: str, top_n: int = 10):
    if user_id not in user_similarity_df.index:
        raise HTTPException(status_code=404, detail="User not found.")
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).iloc[1:top_n + 1].index
    recommended_songs = user_item_matrix.loc[similar_users].sum().sort_values(ascending=False)
    already_played_songs = user_item_matrix.loc[user_id] > 0
    playlist_songs = recommended_songs[~recommended_songs.index.isin(user_item_matrix.columns[already_played_songs])]
    return {"playlist": playlist_songs.head(top_n).index.tolist()}

@app.get("/search/")
async def search(query: str, top_n: int = 5):
    # Search songs
    songs_results = df[df['master_metadata_track_name'].str.contains(query, case=False, na=False)]
    song_names = songs_results['master_metadata_track_name'].unique()[:top_n]
    
    # Search artists
    artist_results = df[df['artist_name'].str.contains(query, case=False, na=False)]
    artists = artist_results['artist_name'].unique()[:top_n]

    # Search albums
    album_results = df[df['album_name'].str.contains(query, case=False, na=False)]
    albums = album_results['album_name'].unique()[:top_n]

    return {"songs": song_names.tolist(), "artists": artists.tolist(), "albums": albums.tolist()}

@app.post("/user/{user_id}/create_playlist/")
async def create_playlist(user_id: str, song_names: List[str]):
    if user_id not in user_similarity_df.index:
        raise HTTPException(status_code=404, detail="User not found.")

    # Add playlist creation logic, for example, saving it in the user record or a new database table
    playlist_name = f"{user_id}_playlist"
    playlist_songs = {
        "playlist_name": playlist_name,
        "songs": song_names
    }

    return {"message": f"Playlist '{playlist_name}' created successfully with {len(song_names)} songs.", "playlist": playlist_songs}

@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    query = chat_request.query.lower()
    user_id = chat_request.user_id
    top_n = chat_request.top_n

    if "recommend" in query and "user" in query:
        if user_id:
            response = call_recommend_user_based(user_id, top_n)
            return {"reply": f"Here are personalized recommendations based on user {user_id}: {response}"}
        else:
            return {"reply": "Please provide a user ID for recommendations."}

    elif "recommend" in query and "combined" in query:
        if user_id:
            response = call_recommend_combined(user_id, top_n)
            return {"reply": f"Here are combined recommendations (personalized + new releases): {response}"}
        else:
            return {"reply": "Please provide a user ID for combined recommendations."}

    elif "new releases" in query:
        response = call_new_releases(top_n)
        return {"reply": f"Here are the latest music releases: {response}"}

    elif "trending" in query:
        response = call_trending_songs(top_n)
        return {"reply": f"Check out these trending songs: {response}"}

    elif "search" in query:
        response = call_search(query, top_n)
        return {"reply": f"Here are the search results for '{query}': {response}"}

    elif "generate playlist" in query:
        if user_id:
            response = call_generate_playlist(user_id, top_n)
            return {"reply": f"Here’s your generated playlist: {response}"}
        else:
            return {"reply": "Please provide a user ID to generate a playlist."}

    elif "register" in query:
        if user_id:
            name = query.split("register ")[-1].strip()
            user = User(phone_model="unknown", name=name)
            response = call_register_user(user)
            return {"reply": f"User {name} registered successfully: {response}"}
        else:
            return {"reply": "Please provide your name to register."}

    else:
        return {"reply": "Sorry, I didn't quite understand your request. Please ask for music recommendations, trending music, new releases, or create a playlist."}

    
# Close database connection on shutdown
@app.on_event("shutdown")
def shutdown_event():
    conn.close()