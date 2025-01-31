import os
import pandas as pd
import numpy as np

# Define the data path (absolute path)
data_path = "C:/Users/USER/OneDrive/Desktop/Python/Music_Recommendation_System/data/clean_data.json"
output_dir = "C:/Users/USER/OneDrive/Desktop/Python/Music_Recommendation_System/data/"

# Check if the data path exists
print("Data path exists:", os.path.exists(data_path))

def clean_and_engineer_features(data_path):
    try:
        # Load data
        print("Loading data from:", data_path)
        data = pd.read_json(data_path)
        print(f"Data loaded successfully. Shape of the data: {data.shape}")

        # Handle missing values and duplicates
        print("Cleaning data (removing missing values and duplicates)...")
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        print(f"Data after cleaning. Shape: {data.shape}")

        # Convert timestamp to datetime
        print("Converting timestamp to datetime...")
        data['ts'] = pd.to_datetime(data['ts'])
        print("Timestamp conversion complete.")

        # Extract date-based features
        print("Extracting date-based features...")
        data['hour'] = data['ts'].dt.hour
        data['day_of_week'] = data['ts'].dt.day_name()
        data['is_weekend'] = data['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
        print("Feature extraction complete.")

        # Filter out short plays (< 30 seconds)
        print("Filtering short plays (< 30 seconds)...")
        data = data[data['ms_played'] > 30000]
        print(f"Data after filtering: {data.shape}")

        # Calculate track play counts
        print("Calculating track play counts...")
        track_play_counts = data.groupby('master_metadata_track_name')['ms_played'].count().reset_index()
        track_play_counts.columns = ['track_name', 'play_count']
        print(f"Track play counts calculated. Sample:\n{track_play_counts.head()}")

        # Merge play counts back into the dataset
        print("Merging play counts back into the dataset...")
        processed_data = data.merge(track_play_counts, left_on='master_metadata_track_name', right_on='track_name', how='left')

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            print(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)

        # Save cleaned and processed data
        processed_data_path = os.path.join(output_dir, "cleaned_data.csv")
        print(f"Saving processed data to {processed_data_path}...")
        processed_data.to_csv(processed_data_path, index=False)
        print("Processed data saved successfully!")

        return processed_data

    except Exception as e:
        print(f"Error during processing: {e}")

# Call the function
clean_and_engineer_features(data_path)
