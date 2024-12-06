import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

CLIENT_ID = ''
CLIENT_SECRET = ''

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="http:/localhost:8888/callback",
                                               scope="user-library-read"))


def get_artist_genres(artist_name):
    """
    Retrieve genres for a given artist name
    
    Args:
        artist_name (str): Name of the artist
    
    Returns:
        list: List of genres associated with the artist
    """
    try:
        # Search for the artist
        results = sp.search(q='artist:' + artist_name, type='artist')
        
        # Get the first artist result
        if results['artists']['items']:
            artist = results['artists']['items'][0]
            return artist['genres']
        return []
    except Exception as e:
        print(f"Error fetching genres for {artist_name}: {e}")
        return []

def process_csv_files(directory):
    """
    Process all CSV files in a directory
    
    Args:
        directory (str): Path to directory containing CSV files
    
    Returns:
        pandas.DataFrame: Consolidated dataframe with artist genres
    """
    all_artists_genres = []
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    for file in csv_files:
        file_path = os.path.join(directory, file)
        
        # Read CSV, skipping first row
        df = pd.read_csv(file_path, skiprows=1, header=None)
        
        # Assuming artists are in the first column
        artists = df.iloc[:, 0].tolist()
        
        # Process each artist
        for artist in artists:
            genres = get_artist_genres(artist)
            all_artists_genres.append({
                'artist': artist,
                'genres': ', '.join(genres) if genres else 'No genres found'
            })
            
            # Respect Spotify API rate limits
            time.sleep(0.2)  # Add a small delay between requests
    
    # Convert to DataFrame
    return pd.DataFrame(all_artists_genres)

# Usage
directory_path = 'C:/Users/billy/Repositories/Pre-Commit-Development/SpotifyMLProject/GenreMatching'
artists_genres_df = process_csv_files(directory_path)

# Save results to a CSV
artists_genres_df.to_csv('artists_genres.csv', index=False)

print("Genre retrieval complete. Results saved to artists_genres.csv")