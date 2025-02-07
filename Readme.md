# CodeAlpha Tasks Repository

This repository contains projects completed during my Machine Learning Internship at CodeAlpha. Each project in this repository focuses on real-world applications of machine learning, AI, and software engineering.

## Projects

### 1. Music Recommendation System
**Description:**
A music recommendation system powered by machine learning that predicts a user's likelihood of repeatedly listening to a song within a set timeframe. Using a dataset where a value of 1 indicates repeated plays within a month, the system tracks user song histories and timestamps to generate personalized song recommendations.

#### Project Structure
```
Music_Recommendation_System/
│
├── data/                # Raw and processed datasets
├── models/              # Trained machine learning models
├── notebooks/           # Jupyter notebooks for experimentation
├── api/                 # API code for serving recommendations
├── scripts/             # Helper scripts for preprocessing, training, etc.
└── main.py              # Main application entry point
```

#### Key Components & Steps
1. **Database Connection Setup**
   - Location: `scripts/db_connection.py`
   - Establishes connection to PostgreSQL for data retrieval.
   - Example:
     ```python
     from sqlalchemy import create_engine
     DATABASE_URL = "postgresql://username:password@localhost:5432/music_recommendation"
     engine = create_engine(DATABASE_URL)
     def get_db_engine():
         return engine
     ```

2. **Data Preprocessing**
   - Location: `scripts/data_preprocessing.py`
   - Cleans and prepares data for model training.
   - Example:
     ```python
     import pandas as pd
     def clean_data(data_path):
         data = pd.read_json(data_path)
         data = data.dropna(subset=['track_name', 'artist_name'])
         data['played_at'] = pd.to_datetime(data['played_at'])
         return data
     cleaned_data = clean_data("../data/spotify_million_playlist.json")
     cleaned_data.to_csv("../data/cleaned_data.csv", index=False)
     ```

3. **Model Training**
   - Location: `scripts/train_model.py`
   - Trains a machine learning model to predict repeated plays.
   - Example:
     ```python
     from sklearn.model_selection import train_test_split
     from sklearn.ensemble import GradientBoostingClassifier
     def train_model(data_path):
         data = pd.read_csv(data_path)
         X = data[['duration_ms', 'play_count']]
         y = data['repeat_play']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         model = GradientBoostingClassifier()
         model.fit(X_train, y_train)
         return model
     model = train_model("../data/cleaned_data.csv")
     ```

4. **Saving Models**
   - Location: `models/`
   - Saves the trained model for inference.
   - Example:
     ```python
     import joblib
     joblib.dump(model, "../models/music_recommendation_model.pkl")
     ```

5. **API for Recommendations**
   - Location: `api/recommendation_api.py`
   - Provides RESTful API endpoints using FastAPI.
   - Example:
     ```python
     from fastapi import FastAPI
     import joblib
     app = FastAPI()
     model = joblib.load("../models/music_recommendation_model.pkl")
     @app.get("/recommend/{user_id}")
     def recommend(user_id: int):
         return {"user_id": user_id, "recommended_tracks": ["Track A", "Track B"]}
     ```

6. **Main Application**
   - Location: `main.py`
   - Runs the application, including API, database setup, and data pipeline.
   - Example:
     ```python
     import uvicorn
     if __name__ == "__main__":
         uvicorn.run("api.recommendation_api:app", host="0.0.0.0", port=1200, reload=True)
     ```

#### Next Steps
- Data Preparation: Load and preprocess the dataset.
- Model Development: Train and evaluate models.
- API Integration: Deploy the API.
- Testing: Validate data flow and recommendation accuracy.
- Deployment: Serve recommendations through API endpoints.

---

## Contributing
This repository is for my internship tasks at CodeAlpha. If you have suggestions, feel free to open an issue or fork the project for experimentation.

## License
This project is for educational purposes under my internship and follows an open learning approach. License details will be updated based on final deployment considerations.

