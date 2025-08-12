import requests

url = "https://api.themoviedb.org/3/search/movie"
genre_url = "https://api.themoviedb.org/3/genre/movie/list"

params = { 
    "query": "13 Going On 30",
    "include_adult": "false",
    "language": "en-US",
    "page": 1
}

headers = {
    "accept": "application/json",
    "Authorization": API_KEY
}

response = requests.get(url, headers=headers, params=params)
genre_response = requests.get(genre_url, headers=headers)

data = response.json()
genres = genre_response.json()['genres']

genre_dict = {g['id']: g['name'] for g in genres}

if data['results']:
    movie = data['results'][0] 
    print(f"TITLE: {movie['title']}")
    print(f"POSTER PATH: https://image.tmdb.org/t/p/w500{movie['poster_path']}")
    
    genre_names = [genre_dict[g] for g in movie['genre_ids']]
    print(f"GENRES: {', '.join(genre_names)}")
    print(f"OVERVIEW: {movie['overview']}")
else: 
    print("No results found.")

