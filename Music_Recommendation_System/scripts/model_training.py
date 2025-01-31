import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load cleaned data
data_path = "../data/cleaned_data.csv"
data = pd.read_csv(data_path)

# Feature Engineering
data['hour'] = pd.to_datetime(data['ts']).dt.hour  # Extracting hour if not already done
label_encoders = {}
categorical_columns = ['platform', 'conn_country', 'reason_start', 'reason_end']

# Encode categorical features
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

# Target variable: Predict repeated plays within a month (binary classification)
data['repeat_play'] = np.where(data['play_count'] > 1, 1, 0)

# Feature selection
features = ['ms_played', 'hour', 'shuffle', 'offline', 'incognito_mode', 'platform', 
            'conn_country', 'reason_start', 'reason_end']
target = 'repeat_play'

X = data[features]
y = data[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Evaluation:\n", classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(model, "../models/spotify_recommendation_model.pkl")
joblib.dump(label_encoders, "../models/label_encoders.pkl")
print("Model and encoders saved successfully.")
