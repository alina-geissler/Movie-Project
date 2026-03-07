import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

REQUEST_DATA_URL = f'https://www.omdbapi.com/?apikey={API_KEY}&t='


def fetch_data(movie_title):
    # TODO: Docstring!
    # TODO: absichern gegen KeyErrors...
    try:
        res = requests.get(REQUEST_DATA_URL + f'{movie_title}')
    except Exception as e:
        print("*** API is not accessible ***\nError: ", e)
        return False, False, False, False
    movie_info = res.json()
    if movie_info.get("Error") == "Movie not found!":
        return None, None, None, None
    title = movie_info['Title']
    year = movie_info['Year']
    rating = movie_info['imdbRating']
    poster_image_url = movie_info['Poster']
    return title, year, rating, poster_image_url





