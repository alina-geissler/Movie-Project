import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

REQUEST_DATA_URL = f'https://www.omdbapi.com/?apikey={API_KEY}&t='


def fetch_data(movie_title):
    """
    Fetch information about a specific movie from the API.
    :param movie_title: movie user wants to add to the database
    :return: title, release year, IMDb rating and URL to the movie poster if a valid one was found
    """
    try:
        res = requests.get(REQUEST_DATA_URL + f'{movie_title}')
    except Exception as e:
        print("*** API is not accessible ***\nError: ", e)
        return False, False, False, False
    movie_info = res.json()
    if movie_info.get("Error") == "Movie not found!":
        return None, None, None, None
    title = movie_info.get('Title')
    year = movie_info.get('Year')
    rating = movie_info.get('imdbRating')
    if rating in ("N/A", None):
        rating = 0
    poster_image_url = movie_info.get('Poster')
    valid_poster_url = is_valid_poster_url(poster_image_url)

    return title, year, rating, valid_poster_url


def is_valid_poster_url(url):
    """
    Check if a URL returned from the API is valid and directs to the movie poster.
    :param url: URL to a specific movie poster
    :return: valid URL or 'N/A' to insert into database
    """
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






