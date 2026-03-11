# :clapper: Movie-Project - CineStash

**CLI Movie Collection Manager with Static Website Export**

A command-line application to manage your personal movie collection. 
Add movies via API, store them in SQLite, perform CRUD operations, 
search for and filter movies, show stats, create rating histograms, get a random movie suggestion
and generate a responsive HTML website to showcase your curated movie treasure trove with one click!

## :sparkles: Features

- **CRUD Operations**: Add, list, update and delete movies
- **Search & Analytics**: Sort / filter / search for movies, show stats, 
create rating histogram and save it to a file
- **Data Lookup**: Enter title and auto-fetch year of publication,
IMDb rating and movie poster from external API with .env key
- **Poster Handling**: Auto-fallback for broken or missing URLs
- **Storage**: SQLite database with auto-migration (data/movies.db)
- **Website Export**: Static website with responsive grid layout

## :file_folder: Project Structure

```
Movie-Project/
├── data/
│   └── movies.db
├── static/
│   ├── index_template.html
│   ├── style.css
│   └── missing_poster_replacement.png
├── movie_fetch/
│   └── data_fetcher.py
├── movie_storage/
│   └── movie_storage_sql.py
├── movie_render/
│   └── web_generator.py
├── main.py
├── README.md
├── requirements.txt
├── .env
└── index.html           # generated website 
```

## :wrench: Setup & Usage

1. **Clone the repository**   
`git clone ...`
2. **Install virtual env**  
Windows: `python -m venv .venv`  
Linux / macOS: `python3 -m venv .venv`
3. **Create file '.env'**
4. **Get API key from https://www.omdbapi.com/ and add it to '.env'**
`API_KEY='your_key_here'`
5. **Install dependencies**   
Windows: `pip install -r requirements.txt`  
Linux / macOS: `pip3 install -r requirements.txt`
6. **Run the application**  
Windows: `python main.py`  
Linux / macOS: `python3 main.py`

## :clipboard: Commands

Main menu commands overview - navigate with numbers:

| Command | Description                  |
|---------|------------------------------|
| 0       | Exit                         |
| 1       | List all movies              |
| 2       | Add new movie                |
| 3       | Delete movie                 |
| 4       | Update movie                 |
| 5       | Show stats                   |
| 6       | Get random movie suggestion  |
| 7       | Search for movie             |
| 8       | List movies sorted by rating |
| 9       | List movies sorted by year   |
| 10      | Filter movies                |
| 11      | Create rating histogram      |
| 12      | Generate HTML website        |


## :package: Dependencies

`colorama` - generates rating histograms
`matplotlib` - enables colored terminal output for better CLI readability

`sqlalchemy` - object-relational mapper for SQLite database operations
`requests` - sends HTTP calls to the API and parses the JSON responses
`dotenv` - loads the API key from '.env' into environment variables



