# Lyrical - AI Music Recommendation System

## Overview
Lyrical is an AI-powered music recommendation system that integrates advanced machine learning with full-stack development. Designed to deliver personalized music experiences, Lyrical provides song recommendations, trending music insights, playlist management, and an interactive chat feature. It is powered by **Spotify's dataset**, tracking user listening behavior to predict song preferences.

## Key Features
✅ **Personalized Recommendations** – AI-driven music suggestions based on user listening history.
✅ **Multi-Device Optimization** – Recommends music based on the user's device type.
✅ **Trending Music** – Displays trending songs dynamically.
✅ **Smart Search** – Find music with an intelligent search engine.
✅ **Playlist Management** – Users can create and manage their playlists.
✅ **Interactive Chat System** – Engage with an AI-powered chat assistant for music discovery.
✅ **Real-Time API Responses** – FastAPI backend ensures smooth interaction.
✅ **Visually Stunning UI** – Vue.js frontend with 3D animations and modern aesthetics.

## Tech Stack
- **Frontend:** Vue.js, TailwindCSS, Three.js (for 3D visuals)
- **Backend:** FastAPI, PostgreSQL, SQLAlchemy
- **Machine Learning:** Scikit-learn (Gradient Boosting Classifier)
- **Database:** PostgreSQL
- **Deployment:** Docker, Uvicorn, Nginx

---

## Project Structure
```
Lyrical/
│
├── data/                # Datasets
├── models/              # Trained ML models
├── notebooks/           # Jupyter notebooks for experimentation
├── api/                 # FastAPI-based API
│   ├── recommendation_api.py  # API for music recommendations
├── scripts/             # Helper scripts
│   ├── db_connection.py   # Database connection setup
│   ├── data_preprocessing.py # Data cleaning and processing
│   ├── train_model.py    # Model training script
├── main.py              # Application entry point
│
├── frontend/            # Vue.js frontend
│   ├── components/      # UI components
│   ├── views/           # Pages and views
│   ├── store/           # Vuex state management
│   ├── App.vue          # Main Vue component
│   ├── main.js          # Entry point
│
└── docker/              # Deployment configuration
```

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Vue.js (installed globally)

### Backend Setup
```sh
# Clone the repository
git clone https://github.com/Justreadin/codealpha_task/Lyrical.git
cd Lyrical

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up the database
python scripts/db_connection.py

# Train the model (optional if pre-trained model is available)
python scripts/train_model.py

# Run FastAPI
uvicorn api.recommendation_api:app --host 0.0.0.0 --port 1200 --reload
```

### Frontend Setup
```sh
cd frontend
npm install
npm run dev
```

---

## API Endpoints
### Get Recommendations
**Endpoint:** `/recommend/{user_id}`

**Method:** `GET`

**Response:**
```json
{
  "user_id": "Windows 10",
  "recommended_tracks": ["Song A", "Song B"]
}
```

---

## Model Training Workflow

1. **Database Connection Setup**
   - Location: `scripts/db_connection.py`
   - Establishes a connection to PostgreSQL.

2. **Data Preprocessing**
   - Location: `scripts/data_preprocessing.py`
   - Cleans and prepares the dataset.

3. **Model Training**
   - Location: `scripts/train_model.py`
   - Trains a **Gradient Boosting Classifier** on user listening behavior.

4. **Saving the Model**
   - Location: `models/`
   - Saves the trained model using `joblib`.

5. **Serving the Model**
   - Location: `api/api.py`
   - Provides RESTful API endpoints for recommendations.

6. **Frontend Integration**
   - Location: `frontend/`
   - Builds the Vue.js application with search, playlists, and chat features.

---

## Next Steps
1. **Fine-tune the Machine Learning Model** – Improve accuracy with additional features.
2. **Optimize API Performance** – Reduce latency and increase scalability.
3. **Enhance UI/UX** – Add more animations and make interactions seamless.
4. **Deploy on Cloud** – Host on AWS/GCP/Azure with Dockerized containers.
5. **Implement User Authentication** – Allow users to save preferences.

---

## Contributions
We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-new-feature`).
3. Commit your changes.
4. Open a pull request.

---

## Acknowledgments
Special thanks to **CodeAlpha** for this incredible opportunity!

---

### 🚀 Let’s make music discovery smarter with Lyrical! 🎶

