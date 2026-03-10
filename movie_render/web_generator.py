TEMPLATE_PATH = 'static/index_template.html'
OUTPUT_HTML_PATH = 'index.html'
PLACEHOLDER_MOVIE_GRID = '__TEMPLATE_MOVIE_GRID__'
POSTER_REPLACEMENT_PATH = 'static/missing_poster_replacement.png'


def load_template(file_path):
    """
    Load HTML template.
    :param file_path: source of the template
    :return: HTML template
    """
    with open(file_path, "r") as handle:
        return handle.read()


def create_movie_card(title, year, rating, poster_image_url):
    """
    Create HTML movie card element for given movie.
    :params title, year, rating, poster_image_url: record of a single movie in the database
    :return: complete <div class="movie"> HTML card markup for given movie
    """
    output = '<li>\n'
    output += '<div class="movie">\n'
    if poster_image_url == 'N/A':
        output += f'<img class="movie-poster" src={POSTER_REPLACEMENT_PATH} title>\n'
    else:
        output += f'<img class="movie-poster" src={poster_image_url} title>\n'
    output += f'<div class="movie-title">{title}</div>\n'
    output += f'<div class="movie-year">{year}</div>\n'
    output += f'<div class="movie-rating">Rating: {rating}</div>\n'
    try:
        num_stars = int(rating)
    except ValueError:
        num_stars = 0

    output += f'<div class="star-rating">{'&#11088 ' * num_stars}</div>'
    output += '</div>\n'
    output += '</li>\n'
    return output


def create_html_file(movie_data):
    """
    Generate HTML file showcasing the movies in the database.
    :param movie_data: dictionary containing the movies from the database
    """
    template = load_template(TEMPLATE_PATH)
    if not movie_data:
        output = '<li>\n'
        output += ('<p style="font-weight: bold; color: #629480FF; font-size: 16pt; text-align: center;">'
                   'No movies in the database yet</p>\n')
        output += ('<p style="color: #629480FF; font-size: 16pt; text-align: center;">'
                   'So start collecting your favorites!</p>\n')
        output += '</li>\n'
    else:
        output = ''
        for movie in movie_data:
            output += create_movie_card(movie,
                                        movie_data[movie].get("year"),
                                        movie_data[movie].get("rating"),
                                        movie_data[movie].get("movie_poster_url"))
    html_with_data = template.replace(PLACEHOLDER_MOVIE_GRID, output)
    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as handle:
        handle.write(html_with_data)
