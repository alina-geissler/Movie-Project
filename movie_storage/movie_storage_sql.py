from sqlalchemy import create_engine, text

DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)


def create_table():
    """
    Create the movies table if it does not exist in the database yet.
    """
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_image_url TEXT NOT NULL
            )
        """))
        connection.commit()


def get_movies():
    """
    Retrieve all movies from the database.
    :return: a dictionary of dictionaries containing the information for each movie
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_image_url FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "movie_poster_url": row[3]} for row in movies}


def add_new_movie(title, year, rating, poster_image_url):
    """
    Add a new movie to the database.
    :param title: new movie title
    :param year: new movie year
    :param rating: new movie rating
    :param poster_image_url: URL to the movie poster
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT OR IGNORE INTO movies (title, year, rating, poster_image_url) "
                                    "VALUES (:title, :year, :rating, :poster_image_url)"),
                               {"title": title, "year": year, "rating": rating, "poster_image_url": poster_image_url})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_existing_movie(title):
    """
    Delete a movie from the database.
    :param title: movie title to delete
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def update_existing_movie(title, rating):
    """
    Update a movie's rating in the database.
    :param title: movie title to update
    :param rating: updated movie rating
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                                        {"title": title, "rating": rating})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
