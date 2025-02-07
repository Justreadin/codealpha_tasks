# Music Recommendation System

## Overview
Spotify's recommendation system, powered by machine learning, predicts a user's likelihood of repeatedly listening to a song within a set timeframe. Using a dataset with 1 indicating repeated plays within a month, it tracks user song histories and timestamps to generate personalized song recommendations.

## Features
- **Personalized Recommendations**: Predicts songs users are likely to replay.
- **Machine Learning Model**: Uses Gradient Boosting for classification.
- **FastAPI Backend**: Exposes recommendations via API.
- **Vue.js Frontend**: A visually impressive UI with 3D visuals, animations, and a stunning design.
- **Database Integration**: Uses PostgreSQL for storing user history.
- **Chat System**: Integrated floating chat for user interaction.

---
## Project Structure

### Backend
```
Music_Recommendation_System/
│
├── data/                # Datasets
├── models/              # Saved ML models
├── notebooks/           # Jupyter notebooks for experimentation
├── api/                 # FastAPI-based API
├── scripts/             # Helper scripts
│   ├── db_connection.py   # Database connection setup
│   ├── data_preprocessing.py # Data cleaning and processing
│   ├── train_model.py    # Model training script
├── main.py              # Application entry point
```

### Frontend
```
src/
├── assets/                # Static assets
├── components/            # Vue components
│   ├── Chat.vue           # Chat system component
│   ├── Header.vue         # Search bar
│   ├── IconBar.vue        # Navigation bar
│   ├── Recommendations.vue # Recommended songs
│   ├── DeviceSpecific.vue # Device-specific API recommendations
│   ├── Visual3D.vue       # 3D visualization using Three.js
│   ├── Playlist.vue       # Playlist creation and management
│   ├── Trending.vue       # Trending songs display
│   ├── SearchBar.vue      # Search input
├── views/                 # Application views
│   ├── HomeView.vue       # Main home page
│   ├── RecommendationsView.vue # Recommendations page
│   ├── PlaylistView.vue   # Playlists management
│   ├── SearchView.vue     # Search results page
├── store/                 # Vuex/Pinia state management
│   ├── index.js           # Global state
│   ├── modules/
│       ├── user.js        # User state
│       ├── recommendations.js # Recommendation state
│       ├── playlists.js   # Playlist state
├── App.vue                # Main Vue component
├── main.js                # Entry point
public/
└── index.html             # Main HTML file
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
git clone https://github.com/Justreadin/codealpha_task/Music_Recommendation_System.git
cd Music_Recommendation_System

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

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
  "user_id": Windows 10,
  "recommended_tracks": ["Song A", "Song B"]
}
```

---
## Next Steps
1. **Data Preparation**: Load and preprocess the dataset.
2. **Model Development**: Train and evaluate machine learning models.
3. **API Integration**: Deploy the API for recommendations.
4. **Frontend Enhancement**: Improve UI/UX with animations and 3D visuals.
5. **Testing**: Validate data flow and recommendation accuracy.
6. **Deployment**: Deploy both frontend and backend services.

---
## Contributions
Feel free to contribute to this project by submitting issues or pull requests.

---
## Acknowlegdement:
CodeAlpha

