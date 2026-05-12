import pandas as pd
import requests
from dotenv import load_dotenv
import os
import time
from tqdm import tqdm
from pathlib import Path

# --- SETUP PATHS ---
# This finds the 'MovieMind' folder regardless of where you run the script from
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

# Load the environment variables
load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# --- DEBUGGING ---
print(f"Current Working Directory: {os.getcwd()}")
print(f"Looking for .env at: {ENV_PATH}")
print(f"DEBUG: API Key loaded = {'Yes' if API_KEY and len(API_KEY)>10 else 'No'}")

if not API_KEY or len(API_KEY) < 20:
    print("❌ API Key still not loading!")
    print(f"Check if the file exists here: {ENV_PATH}")
    exit()

# --- FUNCTIONS ---
def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'append_to_response': 'credits,keywords'
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for movie {movie_id}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# --- MAIN EXECUTION ---
def main():
    print("🚀 Starting data collection...")

    popular_movies = []
    # Collect list of popular movies
    for page in tqdm(range(1, 100), desc="Fetching Movie List"):  # Reduced to 5 pages for a quick test
        url = f"{BASE_URL}/movie/popular"
        params = {
            'api_key': API_KEY,
            'language': 'en-US',
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            popular_movies.extend(response.json()['results'])
        time.sleep(0.2)

    print(f"\nFound {len(popular_movies)} movies. Fetching detailed data...")

    detailed_movies = []
    # Fetch details for each movie (limiting to first 100 for safety)
    for movie in tqdm(popular_movies[:1981], desc="Processing Details"):
        details = get_movie_details(movie['id'])
        if details:
            movie_data = {
                'id': details.get('id'),
                'title': details.get('title'),
                'genres': [g['name'] for g in details.get('genres', [])],
                'vote_average': details.get('vote_average'),
                'vote_count': details.get('vote_count'),
                'popularity': details.get('popularity'),
                'release_date': details.get('release_date'),
                'budget': details.get('budget'),
                'revenue': details.get('revenue'),
                'cast': [c['name'] for c in details.get('credits', {}).get('cast', [])[:6]],
                'keywords': [k['name'] for k in details.get('keywords', {}).get('keywords', [])[:8]],
            }
            detailed_movies.append(movie_data)
        time.sleep(0.2)

    # Save Data
    if detailed_movies:
        df = pd.DataFrame(detailed_movies)
        
        # Ensure 'data' folder exists
        os.makedirs(BASE_DIR / 'data', exist_ok=True)
        
        save_path = BASE_DIR / 'data' / 'raw_movies.csv'
        df.to_csv(save_path, index=False)
        print(f"\n✅ SUCCESS! Saved {len(df)} movies to {save_path}")
    else:
        print("\n⚠️ No data collected.")

if __name__ == "__main__":
    main()