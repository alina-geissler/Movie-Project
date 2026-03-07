from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


def get_movies():
    """
    Retrieve all movies from the database.
    :return: a dictionary of dictionaries containing the information for each movie
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_new_movie(title, year, rating):
    """
    Add a new movie to the database.
    :param title: new movie title
    :param year: new movie year
    :param rating: new movie rating
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text("INSERT OR IGNORE INTO movies (title, year, rating) "
                                             "VALUES (:title, :year, :rating)"),
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            rows_changed = result.rowcount
            if rows_changed > 0:
                print(f"Movie '{title}' successfully added.")
            else:
                print(f"Movie '{title}' already exists.")
        except Exception as e:
            print(f"Error: {e}")


def delete_existing_movie(title):
    """
    Delete a movie from the database.
    :param title: movie title to delete
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()
            rows_changed = result.rowcount
            if rows_changed > 0:
                print(f"Movie '{title}' successfully deleted.")
            else:
                print(f"No movie '{title}' found.")
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
            result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                                        {"title": title, "rating": rating})
            connection.commit()
            rows_changed = result.rowcount
            if rows_changed > 0:
                print(f"Movie '{title}' successfully updated.")
            else:
                print(f"No movie '{title}' found.")
        except Exception as e:
            print(f"Error: {e}")

print(get_movies())
add_new_movie("Inception", 2010, 8.8)
add_new_movie("Test", 2010, 8.8)
print(get_movies())
update_existing_movie("Inception", 5.5)
print(get_movies())
delete_existing_movie("Inception")
delete_existing_movie("Test")
print(get_movies())