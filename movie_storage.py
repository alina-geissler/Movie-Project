import json


def get_movies():
    """
    Loads the information for all movies from the JSON file.
    :return: a dictionary of dictionaries containing the information from the database
    """
    with open("data.json", "r") as movie_data:
        data = json.loads(movie_data.read())
        return data


def save_movies(movies):
    """
    Saves the information for all movies in the JSON file.
    :param movies: information to save

    """
    json_str = json.dumps(movies)
    with open("data.json", "w") as file_updater:
        file_updater.write(json_str)


def add_movie(title, year, rating):
    """
    Adds a new movie to the movie database.
    Loads the information from the JSON file and saves it after adding the new movie.
    :param title: new movie title
    :param year: new movie year
    :param rating: new movie rating
    """
    with open("data.json", "r") as movie_data:
        data = json.loads(movie_data.read())
    data[title] = {"year": year, "rating": rating}
    save_movies(data)


def delete_movie(title):
    """
    Deletes a movie from the movie database.
    Loads the information from the JSON file and saves it after deleting the movie.
    :param title: movie title to delete
    """
    with open("data.json", "r") as movie_data:
        data = json.loads(movie_data.read())
    if data:
        del data[title]
        save_movies(data)


def update_movie(title, rating):
    """
    Updates a movie from the movie database.
    Loads the information from the JSON file and saves it after updating the movie.
    :param title: movie title to update
    :param rating: updated movie rating
    """
    with open("data.json", "r") as movie_data:
        data = json.loads(movie_data.read())
    if data:
        data[title]["rating"] = rating
        save_movies(data)
