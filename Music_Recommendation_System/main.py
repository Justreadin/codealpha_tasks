from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import logging
from scripts.db_operations import insert_data, fetch_data
from scripts.collaborative_filtering import recommend_songs, prepare_user_item_matrix
import uvicorn
from logger import logger  # Import the logger

app = FastAPI()

# Enable CORS for Vue.js frontend
origins = [
    "http://localhost:8081",  # Vue.js development server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the Vue.js `dist` folder
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

@app.get("/")
async def serve_vue_app():
    """
    Serve the Vue.js application.
    """
    return FileResponse("frontend/dist/index.html")

@app.post("/log/error")
async def log_error(request: Request):
    """
    Receive logs from the frontend and log them using the backend's logger.
    """
    data = await request.json()  # Get the JSON data from the frontend
    message = data.get('message')
    error = data.get('error')
    stack = data.get('stack', None)

    # Log the received error using the backend logger
    if message and error:
        logger.error(f"Frontend error: {message} - Error: {error} - Stack Trace: {stack if stack else 'No stack trace provided'}")
        return {"status": "error logged successfully"}, 200
    else:
        logger.warning("Received incomplete log data from frontend.")
        return {"status": "incomplete data"}, 400

def load_and_insert_data():
    try:
        # Load cleaned data
        cleaned_data_path = "./data/cleaned_data.csv"
        logger.info(f"Loading cleaned data from {cleaned_data_path}...")
        cleaned_data = pd.read_csv(cleaned_data_path)

        # Ensure data is not empty before insertion
        if cleaned_data.empty:
            logger.warning("No data found to insert. Please check the cleaned data file.")
            return

        # Insert data into PostgreSQL
        logger.info("Inserting data into the database...")
        insert_data(cleaned_data)
        logger.info("Data insertion complete.")
    except FileNotFoundError:
        logger.error(f"Error: File not found at {cleaned_data_path}. Ensure the file path is correct.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

def explore_data():
    try:
        logger.info("Fetching data from the database...")
        data = fetch_data()

        logger.info("Data Sample:")
        logger.info(data.head())
        logger.info("\nMissing Values Summary:")
        logger.info(data.isnull().sum())
    except Exception as e:
        logger.exception(f"Error during data exploration: {e}")

def generate_recommendations(user):
    try:
        logger.info("Fetching data for collaborative filtering...")
        data = fetch_data()
        user_item_matrix, user_similarity_df = prepare_user_item_matrix(data)

        recommendations = recommend_songs(user, user_item_matrix, user_similarity_df, top_n=5)
        logger.info(f"\nTop 5 recommendations for user '{user}':")
        logger.info(recommendations)
    except Exception as e:
        logger.exception(f"Error generating recommendations: {e}")

if __name__ == "__main__":
    logger.info("Music Recommendation System\n")

    # Step 1: Load and insert data into the database
    load_and_insert_data()

    # Step 2: Explore the data in the database
    explore_data()

    # Step 3: Generate song recommendations for a sample user
    sample_user = 'iOS 15.2 (iPhone12,1)'  # Replace with a valid user ID for testing
    generate_recommendations(sample_user)

    # Run the FastAPI app on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
