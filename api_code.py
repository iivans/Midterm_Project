# api_code.py
import requests

API_KEY = '7da1efeeea871e2ca9596dea6307724a'
BASE_URL = 'https://api.themoviedb.org/3/'
actor_cache = {}  # Cache to reduce redundant API calls


def get_actor_movies(actor_id):
    if actor_id in actor_cache:
        return actor_cache[actor_id]

    print(f"Getting movies for actor ID {actor_id}...")
    url = f"{BASE_URL}person/{actor_id}/movie_credits?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movie_data = data['cast']
        print(f"Found {len(movie_data)} movies for actor ID {actor_id}.")
        actor_cache[actor_id] = movie_data
        return movie_data
    else:
        raise ValueError(f"Error getting data for actor ID {actor_id}.")


def get_movie_actors(movie_id):
    try:
        print(f"Getting actors for movie ID {movie_id}...")
        movie_url = f"{BASE_URL}movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(movie_url)

        if response.status_code == 200:
            data = response.json()
            return data['cast']
        else:
            raise ValueError(f"Error getting movie data for movie ID {movie_id}")

    except Exception as e:
        print(f"Skipping movie ID {movie_id} due to an error: {e}")
        return []  # Return an empty list if there's an error


def search_actor_by_name(name):
    url = f"{BASE_URL}search/person?api_key={API_KEY}&query={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data['results']
        if len(results) == 0:
            print(f"No results found for {name}.")
            return None

        for idx, actor in enumerate(results):
            print(f"{idx + 1}. {actor['name']} (ID: {actor['id']})")

        while True:  # Input loop to handle invalid indices
            try:
                choice = int(input("Choose the actor by entering the corresponding number: ")) - 1
                if 0 <= choice < len(results):
                    return results[choice]['id']
                else:
                    print(f"Invalid selection. Please choose a number between 1 and {len(results)}.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        raise ValueError(f"Error searching for actor name: {name}")


def get_actor_name(actor_id):
    url = f"{BASE_URL}person/{actor_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        raise ValueError(f"Error getting data for actor ID {actor_id}.")
