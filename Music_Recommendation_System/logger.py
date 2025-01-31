import logging

# Configure the logger
logger = logging.getLogger("music_recommendation_system")
logger.setLevel(logging.DEBUG)

# Create file handler to log in a file
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.DEBUG)

# Create a console handler for real-time logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Export the logger for use in other parts of the app
