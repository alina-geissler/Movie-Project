import movie_storage.movie_storage_sql as storage
import movie_fetch.data_fetcher as data_fetcher
import movie_render.web_generator as web_generator

import random
import datetime
import colorama

colorama.init(autoreset=True)


# Show menu and get menu choice by user

def show_menu():
    """
    Print the menu on the screen.
    """
    print(colorama.Fore.BLACK + colorama.Back.GREEN + "---------------------------")
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "Menu:")
    print(colorama.Fore.GREEN +
          "0.\tExit\n"
          "1.\tList movies\n"
          "2.\tAdd movie\n"
          "3.\tDelete movie\n"
          "4.\tUpdate movie\n"
          "5.\tStats\n"
          "6.\tRandom movie\n"
          "7.\tSearch movie\n"
          "8.\tMovies sorted by rating\n"
          "9.\tMovies sorted by year\n" 
          "10.\tFilter movies\n"                                        
          "11.\tCreate rating histogram\n"
          "12.\tGenerate Website")
    print(colorama.Fore.BLACK + colorama.Back.GREEN + "---------------------------")
    print()


def get_choice_by_user():
    """
    Ask the user for the desired menu item.
    Accept a valid choice as input and open the corresponding function.
    """
    while True:
        try:
            user_choice = int(input(colorama.Fore.BLUE + "Enter choice (0-12): "))
        except ValueError:
            print(colorama.Style.BRIGHT + colorama.Fore.RED + "Invalid choice\n")
            show_menu()
            continue
        if user_choice not in range(13):
            print(colorama.Style.BRIGHT + colorama.Fore.RED + "Invalid choice\n")
            show_menu()
        else:
            print()
            return user_choice


# Functions for all menu choices

def list_movies():
    """
    List all movies from the database with release year and rating.
    """
    movie_dict = storage.get_movies()
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + f"{len(movie_dict)} movies in total")
    for movie in movie_dict:
        print(colorama.Fore.CYAN + f"{movie} ({movie_dict[movie]["year"]}): "
                                   f"{movie_dict[movie]["rating"]}")


def add_movie():
    """
    Ask the user for a new movie title to add to the database.
    Accept valid options as input and call function 'data_fetcher.fetch_data' to get year, IMDb rating
    and URL to the movie poster.
    Call function 'storage.add_new_movie' to add the new movie with accompanying information to the database.
    """
    movie_dict = storage.get_movies()
    while True:
        new_movie = input(colorama.Fore.BLUE + "Enter new movie name: ")
        if not new_movie:
            print(colorama.Fore.RED + "Movie title can't be empty\n")
            continue
        else:
            break
    if new_movie in movie_dict:
        print(colorama.Fore.RED + f"Movie '{new_movie}' already exists")
    else:
        new_movie = check_for_similar_title(new_movie)
        if new_movie not in movie_dict:
            new_title, new_year, new_rating, new_poster_url = data_fetcher.fetch_data(new_movie)
            if new_title is False:
                return
            if new_title is None:
                print(colorama.Fore.RED + f"No movie '{new_movie}' found.")
            else:
                storage.add_new_movie(new_title, new_year, new_rating, new_poster_url)
                print(colorama.Fore.CYAN + f"\nMovie '{new_title}' from {new_year} "
                                           f"(with rating {new_rating}) successfully added")


def check_for_similar_title(title_to_search_for):
    """
    Check if the same title with different upper and lower case already exists in the database.
    :param title_to_search_for: movie user wants to add to the database
    :return: similar title if found, otherwise initial user input
    """
    movie_dict = storage.get_movies()
    similar_title = ""
    for movie in movie_dict:
        if title_to_search_for.lower() in movie.lower():
            similar_title = movie
    if similar_title:
        print(colorama.Fore.RED + f"Did you mean '{similar_title}'? "
                                  f"(Movie '{similar_title}' already exists)")
        while True:
            add_anyway = input(colorama.Fore.BLUE +
                               "\nDo you still want to add the movie? (Y/N): ").upper()
            if add_anyway not in ("Y", "YES", "N", "NO"):
                print(colorama.Fore.RED + "Please enter 'Y' or 'N'")
            else:
                if add_anyway in ("Y", "YES"):
                    return title_to_search_for
                else:
                    return similar_title
    else:
        return title_to_search_for


def delete_movie():
    """
    Ask the user for a movie title to delete from the database.
    Call function storage.delete_existing_movie to delete the movie if title was found.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    movie_to_delete = input(colorama.Fore.BLUE + "Enter movie name to delete: ")
    if movie_to_delete not in movie_dict:
        print(colorama.Fore.RED + f"Movie '{movie_to_delete}' doesn't exist")
    else:
        storage.delete_existing_movie(movie_to_delete)
        print(colorama.Fore.CYAN + f"\nMovie '{movie_to_delete}' successfully deleted")


def update_movie():
    """
    Ask the user for a movie title to update and the updated rating.
    Accept valid options as input.
    Call function confirm_similar_title if a movie with different upper and lower case is in the database.
    Call function storage.delete_existing_movie to updates the movie rating in the database if title was found.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    movie_to_update = input(colorama.Fore.BLUE + "Enter movie name: ")
    similar_title = ""
    for movie in movie_dict:
        if movie != movie_to_update and movie.lower() == movie_to_update.lower():
            similar_title = movie
    if similar_title:
        movie_to_update = confirm_similar_title(movie_to_update, similar_title)
    elif movie_to_update not in movie_dict:
        print(colorama.Fore.RED + f"Movie '{movie_to_update}' doesn't exist")
    if movie_to_update in movie_dict:
        updated_rating = get_valid_rating()
        storage.update_existing_movie(movie_to_update, updated_rating)
        print(colorama.Fore.CYAN + f"\nMovie '{movie_to_update}' successfully updated")


def confirm_similar_title(similar_movie, movie_in_database):
    """

    :param similar_movie: movie title user entered
    :param movie_in_database: same movie as similar_movie but different upper and lower case
    :return: movie in database if user wants to update this movie, otherwise initial user input
    """
    print(colorama.Fore.RED + f"No movie '{similar_movie}' found.")
    while True:
        add_anyway = input(colorama.Fore.BLUE +
                           f"Did you mean '{movie_in_database}' and want to update this movie? (Y/N): ").upper()
        if add_anyway not in ("Y", "YES", "N", "NO"):
            print(colorama.Fore.RED + "Please enter 'Y' or 'N'")
        else:
            if add_anyway in ("Y", "YES"):
                return movie_in_database
            else:
                return similar_movie


def get_valid_rating():
    """
    Prompt user for new movie rating, accept valid options.
    :return: rating to update in the database
    """
    while True:
        try:
            rating = float(input(colorama.Fore.BLUE +
                                 "Enter new movie rating (1-10): "))
        except ValueError:
            print(colorama.Fore.RED + "Please enter a valid rating")
            continue
        if not 1 <= rating <= 10:
            print(colorama.Fore.RED + "Please enter a valid rating")
        else:
            return rating


def show_stats():
    """
    Show the average and median rating of all movies in the database
    and list the best and worst movie(s).
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return

    ratings = [movie_dict[movie]["rating"] for movie in movie_dict]
    average_rating = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    if len(ratings) % 2 == 0:
        median_rating = (sorted_ratings[len(sorted_ratings) // 2] +
                         sorted_ratings[len(sorted_ratings) // 2 - 1]) / 2
    else:
        median_rating = sorted_ratings[len(sorted_ratings) // 2]
    worst_rating = sorted_ratings[0]
    best_rating = sorted_ratings[-1]

    worst_movies = [movie for movie in movie_dict
                    if movie_dict[movie]["rating"] == worst_rating]
    best_movies = [movie for movie in movie_dict
                   if movie_dict[movie]["rating"] == best_rating]

    print(colorama.Fore.CYAN + f"Average rating: {round(average_rating, 1)}\n"
                               f"Median rating: {round(median_rating, 1)}\n")
    print(colorama.Fore.CYAN + "Best movie(s):")
    for movie in best_movies:
        print(colorama.Fore.CYAN + f"{movie}, {best_rating}")
    print(colorama.Fore.CYAN + "\nWorst movie(s):")
    for movie in worst_movies:
        print(colorama.Fore.CYAN + f"{movie}, {worst_rating}")


def get_random_movie():
    """
    Select a random movie from all movies in the database.
    Print it on the screen with release year and rating.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    movie_titles = list(movie_dict)
    random_movie = random.choice(movie_titles)
    print(colorama.Fore.CYAN + f"Your movie for tonight: {random_movie} "
                               f"(from {movie_dict[random_movie]['year']}), "
                               f"it's rated {movie_dict[random_movie]['rating']}")


def search_for_movie():
    """
    Ask the user for part of a movie title.
    Print it on the screen with release year and rating if movie was found in the database.
    If a similar title was found, print this movie with accompanying information.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    key_term = input(colorama.Fore.BLUE + "Enter part of movie name: ")
    term_found = False
    for movie in movie_dict:
        if key_term.lower() in movie.lower():
            demanded_movie = movie
            print(colorama.Fore.CYAN + f"\n{demanded_movie} ({movie_dict[demanded_movie]["year"]}), "
                                       f"{movie_dict[demanded_movie]["rating"]}")
            term_found = True
    if not term_found:
        print(colorama.Fore.RED + f"No movie '{key_term}' found")
        words_in_key_term = key_term.lower().split()
        for movie in movie_dict:
            important_words_in_movie = clean_title_for_checking_similarity(movie)
            great_similarity = check_terms_for_similarity(words_in_key_term,
                                                          important_words_in_movie)
            suggested_movie = movie
            if great_similarity:
                print(colorama.Fore.CYAN + f"\nDid you mean '{suggested_movie}'?\n"
                                           f"{suggested_movie} (from {movie_dict[suggested_movie]["year"]}) "
                                           f"is rated {movie_dict[suggested_movie]["rating"]}")


def clean_title_for_checking_similarity(movie_title):
    """
    Remove the articles from a movie title to compare it with the search term
    provided by the user.
    :param movie_title: movie title to clean
    :return: important words of the movie title
    """
    words_to_ignore = ["the", "a", "an", "and"]
    words_in_movie_title = movie_title.lower().split()
    important_words_in_title = " ".join(
        [word for word in words_in_movie_title if word not in words_to_ignore])
    return important_words_in_title.split()


def check_terms_for_similarity(words, words_to_compare_with):
    """
    Check whether two terms are similar.
    :param words: a list of words from the first term
    :param words_to_compare_with: a list of words from the second term
    :return: whether the terms are similar
    """
    is_similar = False
    for word in words:
        for word_to_compare in words_to_compare_with:
            if calc_edit_distance(word, word_to_compare) <= 2:
                is_similar = True
    return is_similar


def calc_edit_distance(string_1, string_2):
    """
    Calculate the editing distance between two strings.
    :param string_1: any string
    :param string_2: second string to compare with first one
    :return: the editing distance
    """
    dp = []  # initialize matrix ("dynamic programming")
    for i in range(len(string_1) + 1):
        dp.append([0] * (len(string_2) + 1))
    for i in range(1, len(string_1) + 1):
        dp[i][0] = i  # insert base case for first string into matrix
        for j in range(1, len(string_2) + 1):
            dp[0][j] = j  # insert base case for second string into matrix
            if string_1[i - 1].lower() == string_2[j - 1].lower():  # same letter means no costs
                dp[i][j] = dp[i - 1][j - 1]  # transfer the value of the cell in the upper left diagonal
            else:  # replacing, deleting or inserting a letter costs +1
                first_increase = dp[i - 1][j - 1] + 1  # value of the cell in the upper left diagonal + 1
                second_increase = dp[i][j - 1] + 1  # value of the cell on the left + 1
                third_increase = dp[i - 1][j] + 1  # value of the cell above + 1
                dp[i][j] = min(first_increase, second_increase, third_increase)
    edit_distance = dp[len(string_1)][len(string_2)]  # accesses the cell at the bottom right
    return edit_distance


def list_movies_sorted_by_rating():
    """
    List all movies from the database with accompanying information, sorted by rating.
    Show the highest rated first.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    movies_listed = [(movie, movie_dict[movie]["year"],
                      movie_dict[movie]["rating"]) for movie in movie_dict]
    movies_sorted_by_rating = sorted(movies_listed, key=lambda x: x[2], reverse=True)
    for movie, year, rating in movies_sorted_by_rating:
        print(colorama.Fore.CYAN + f"{movie} ({year}), {rating}")


def list_movies_sorted_by_year():
    """
    Ask the user whether the latest movie should be displayed first.
    Accept valid options as input.
    List all movies from the database with accompanying information, sorted by release year.
    Show the movies in the desired order.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    movies_listed = [(movie, movie_dict[movie]["year"], movie_dict[movie]["rating"])
                     for movie in movie_dict]
    while True:
        latest_first = input(colorama.Fore.BLUE +
                             "Do you want the latest movies first? (Y/N): ").upper()
        if latest_first not in ("Y", "YES", "N", "NO"):
            print(colorama.Fore.RED + "Please enter 'Y' or 'N'")
        else:
            break
    if latest_first in ("Y", "YES"):
        movies_sorted_by_year = sorted(movies_listed, key=lambda x: x[1], reverse=True)
    else:
        movies_sorted_by_year = sorted(movies_listed, key=lambda x: x[1])
    print()
    for movie, year, rating in movies_sorted_by_year:
        print(colorama.Fore.CYAN + f"{movie} ({year}), {rating}")


def filter_movies():
    """
    Ask the user for their desired filter criteria.
    A minimum rating, a start year and an end year can be specified.
    All three are optional.
    Call functions for each criterion to prompt user and list all movies from the database
    that meet the desired criteria.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    current_year = datetime.date.today().year
    min_rating = get_min_rating()
    start_year = get_start_year(current_year)
    end_year = get_end_year(current_year, start_year)
    matching_movies = []
    for movie in movie_dict:
        if (movie_dict[movie]["rating"] >= min_rating and
                start_year <= movie_dict[movie]["year"] <= end_year):
            matching_movies.append(movie)
    if len(matching_movies) == 0:
        print(colorama.Fore.RED + "No matching movies found")
    else:
        print()
        for movie in matching_movies:
            print(colorama.Fore.CYAN + f"{movie} ({movie_dict[movie]["year"]}): "
                                       f"{movie_dict[movie]["rating"]}")


def get_min_rating():
    """
    Prompt user for minimum rating to filter the movies accordingly.
    Accept valid options or no input for no minimum rating.
    :return: user input or 1 if no minimum rating has been entered
    """
    while True:
        min_rating = input(colorama.Fore.BLUE +
                           "Enter minimum rating (leave blank for no minimum rating): ")
        if min_rating == "":
            return 1
        else:
            try:
                min_rating = float(min_rating)
            except ValueError:
                print(colorama.Fore.RED + "Please enter a valid rating (1-10)")
                continue
            if not 1 <= min_rating <= 10:
                print(colorama.Fore.RED + "Please enter a valid rating (1-10)")
            else:
                return min_rating


def get_start_year(current_year):
    """
    Prompt user for start year to filter the movies accordingly.
    Accept valid options or no input for no start year.
    :param current_year: current year to validate input
    :return: user input or 1888 if no start year has been entered
    """
    while True:
        start_year = input(colorama.Fore.BLUE +
                           "Enter start year (leave blank for no start year): ")
        if start_year == "":
            return 1888
        else:
            try:
                start_year = int(start_year)
            except ValueError:
                print(colorama.Fore.RED + "Please enter a valid year")
                continue
            if start_year < 1888:
                print(colorama.Fore.RED +
                      "Please enter a valid start year (the first existing movie is from 1888)")
            elif start_year > current_year:
                print(colorama.Fore.RED +
                      f"Please enter a valid start year (come back in {start_year - current_year}"
                      f" year(s) for movies from {start_year})")
            else:
                return start_year


def get_end_year(current_year, start_year):
    """
    Prompt user for end year to filter the movies accordingly.
    Accept valid options or no input for no end year.
    :param current_year: current year to validate input
    :param start_year: chosen start year to validate input
    :return: user input or current year if no end year has been entered
    """
    while True:
        end_year = input(colorama.Fore.BLUE + "Enter end year (leave blank for no end year): ")
        if end_year == "":
            return current_year
        else:
            try:
                end_year = int(end_year)
            except ValueError:
                print(colorama.Fore.RED + "Please enter a valid year")
                continue
            if end_year < start_year:
                print(colorama.Fore.RED +
                      f"Please enter a valid end year (your start year is {start_year})")
            elif end_year > current_year:
                print(colorama.Fore.RED +
                      f"Please enter a valid end year (come back in {end_year - current_year} "
                      f"year(s) for movies from {end_year})")
            else:
                return end_year


def create_rating_histogram():
    """
    Create a rating histogram with the ratings of all movies in the database.
    Call a function to ask the user how it should be saved and save it in the desired manner.
    Ask the user whether the histogram should be displayed and do so depending on the answer.
    """
    import matplotlib.pyplot as plt

    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        return
    ratings = [movie_dict[movie]["rating"] for movie in movie_dict]
    plt.hist(ratings, bins=list(range(0, 11)))
    plt.hist(ratings, bins=list(range(0, 11)), edgecolor='black')
    plt.title("Histogram of movie ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    file_type = get_valid_file_type()
    plt.savefig(f'histogram_of_movie_ratings.{file_type}')
    print(colorama.Fore.CYAN + f"\nHistogram successfully created and saved")
    while True:
        show_histogram = input(colorama.Fore.BLUE + "Show histogram? (Y/N): ").upper()
        if show_histogram not in ("Y", "YES", "N", "NO"):
            print(colorama.Fore.RED + "Please enter 'Y' or 'N'")
        else:
            break
    if show_histogram in ("Y", "YES"):
        plt.show()


def get_valid_file_type():
    """
    Prompt user for file type to save the rating histogram accordingly.
    Accept valid options.
    :return: desired file type
    """
    while True:
        file_type = input(colorama.Fore.BLUE + "Save file as (PNG / PDF / JPEG): ").upper()
        if file_type not in ("PNG", "PDF", "JPEG", "JPG"):
            print(colorama.Fore.RED + "Invalid file type")
        elif file_type == "PNG":
            return "png"
        elif file_type == "PDF":
            return "pdf"
        elif file_type in ("JPEG", "JPG"):
            return "jpg"


def generate_website():
    """
    Call function to create HTML file showcasing the movies in the database.
    If database is empty, ask user if website should be generated anyway.
    """
    movie_dict = storage.get_movies()
    if not movie_dict:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "No movies in the database")
        while True:
            create_website = input(colorama.Fore.BLUE + "Generate website anyway? (Y/N): ").upper()
            if create_website not in ("Y", "YES", "N", "NO"):
                print(colorama.Fore.RED + "Please enter 'Y' or 'N'")
            else:
                break
    if movie_dict or create_website in ("Y", "YES"):
        web_generator.create_html_file(movie_dict)
        print(colorama.Fore.CYAN + f"\nWebsite successfully generated")


def main():
    """
    Main function:
    Welcomes the user. Then calls up the menu, asks the user for their choice
    and carries out the desired tasks until the user exits the program.
    """
    storage.create_table()
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN +
          "\n********** CineStash **********")
    print(colorama.Fore.GREEN +
          "Your cureated movie treasure trove\n")

    dispatch = {
        1: list_movies,
        2: add_movie,
        3: delete_movie,
        4: update_movie,
        5: show_stats,
        6: get_random_movie,
        7: search_for_movie,
        8: list_movies_sorted_by_rating,
        9: list_movies_sorted_by_year,
        10: filter_movies,
        11: create_rating_histogram,
        12: generate_website
    }

    while True:
        show_menu()
        menu_choice = get_choice_by_user()
        if menu_choice == 0:
            print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "Bye!")
            break
        else:
            dispatch[menu_choice]()
            print()
            input(colorama.Fore.BLUE + "Press enter to continue ")
            print()


if __name__ == "__main__":
    main()
