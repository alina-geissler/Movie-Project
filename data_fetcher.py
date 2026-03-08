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
    valid_poster_url = is_valid_poster_url(poster_image_url)

    return title, year, rating, valid_poster_url


def is_valid_poster_url(url):
    if "http" not in url:
        return "N/A"
    else:
        try:
            res = requests.head(url)
        except Exception:
            return "N/A"
        if res.status_code != 200:
            return "N/A"
        else:
            return url






