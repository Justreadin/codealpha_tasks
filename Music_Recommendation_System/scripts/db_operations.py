# 2. scripts/db_operations.py
import psycopg2
from api.db_config import DATABASE_CONFIG
import pandas as pd
import datetime


def connect_to_db():
    """
    Establish a database connection using credentials from db_config.
    """
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            port=DATABASE_CONFIG['port']
        )
        print("Database connection successful.")
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None



def insert_data(df):
    """
    Insert rows from a DataFrame into the database.
    """
    conn = connect_to_db()
    if conn:
        try:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    try:
                        # Convert offline_timestamp (Unix timestamp) to datetime
                        if pd.notna(row['offline_timestamp']):
                            # Check if the timestamp is in seconds or milliseconds
                            if row['offline_timestamp'] > 10000000000:  # likely in milliseconds
                                offline_timestamp = datetime.datetime.utcfromtimestamp(row['offline_timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                offline_timestamp = datetime.datetime.utcfromtimestamp(row['offline_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            offline_timestamp = None

                        print(f"Inserting row with offline_timestamp: {offline_timestamp}")  # Debugging print

                        cur.execute(
                            """
                            INSERT INTO spotify_tracks (
                                ts, platform, ms_played, conn_country, master_metadata_track_name,
                                master_metadata_album_artist_name, master_metadata_album_album_name,
                                spotify_track_uri, reason_start, reason_end, shuffle, offline,
                                offline_timestamp, incognito_mode
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                row['ts'], row['platform'], row['ms_played'], row['conn_country'],
                                row['master_metadata_track_name'], row['master_metadata_album_artist_name'],
                                row['master_metadata_album_album_name'], row['spotify_track_uri'],
                                row['reason_start'], row['reason_end'], row['shuffle'], row['offline'],
                                offline_timestamp, row['incognito_mode']
                            )
                        )
                    except Exception as e:
                        print(f"Error inserting row: {e}")
                        print(f"Row causing issue: {row}")  # Log the problematic row
                        continue  # Skip the problematic row and continue with the rest of the data

                conn.commit()
            print("Data insertion successful.")
        except Exception as e:
            print("Error inserting data:", e)
        finally:
            conn.close()



def fetch_data():
    """
    Fetch data from the database for further analysis or model training.
    """
    conn = connect_to_db()
    if conn:
        try:
            query = "SELECT * FROM spotify_tracks;"
            df = pd.read_sql_query(query, conn)

            # Check if the data is empty and provide a message
            if df.empty:
                print("No data found in the 'spotify_tracks' table.")
                return None
            
            print(f"Data fetched successfully. Shape: {df.shape}")
            return df
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Database connection failed.")

