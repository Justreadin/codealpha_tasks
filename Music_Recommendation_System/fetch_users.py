import psycopg2
from api.db_config import DATABASE_CONFIG  # Import the database configuration

def get_all_users():
    try:
        # Connect to PostgreSQL using the imported configuration
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Query to fetch all users
        query = "SELECT * FROM platform;"  # Replace 'users' with your table name
        cursor.execute(query)

        # Fetch and display all rows
        users = cursor.fetchall()
        print("\nAll Users in the Database:\n")
        for user in users:
            print(user)  # Each user is a tuple

        # Close cursor and connection
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("Error:", e)

# Call the function
if __name__ == "__main__":
    get_all_users()
