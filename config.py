import os 
import requests
from dotenv import load_dotenv

load_dotenv("project.env")

#the api key loaded 
API_KEY = os.getenv("API_KEY")
print("Loaded API_KEY:", API_KEY)

#api endpoints 
discover_url = "https://api.themoviedb.org/3/discover/movie"
genres_url = "https://api.themoviedb.org/3/genre/movie/list"

#api auth header 
headers = {
    "accept": "application/json",
}

def get_genres():
    params = {"api_key": API_KEY}

    response = requests.get(genres_url, headers= headers, params=params)
    response.raise_for_status()
    genres = response.json().get("genres", [])
    return {g['id']: g['name'] for g in genres}


#getting genre id's and names from tmbd 
genre_response = requests.get(genres_url, headers=headers, params = {"api_key": API_KEY})
genre_dict = {g['id']: g['name'] for g in genre_response.json().get('genres', [])}
genre_response.raise_for_status()


#mapping moods to genres? or genre id's 
maps_to_moods = {
    "scarefest": [27], #horror
    "mother daughter relationship": [10751], #family
    "3 am melancholy":[18], #drama
    "you just finished your first year of college": [], #young adult #drama #keyword "college"

 }
#defining function to fetch up to 5 movies after given a list of genre id's

def get_movies_by_genres(mood,num_results = 5):

    if mood not in maps_to_moods:
       print (f" {mood} not found :( ")
       return []

    genre_ids = maps_to_moods[mood]
    params = { 
        "api_key": API_KEY,
        "with_genres": ",".join(str(g) for g in genre_ids),
        "language": "en-US",
        "sort_by" : "popularity.desc", 
        "page":1
    }

    response = requests.get(discover_url, headers=headers, params=params)
 
    if response.status_code != 200: 
        print ("Error:", response.json())
        return []

    data = response.json().get("results", [])
    return data[:num_results]


#this is an example test
if __name__ == "__main__":
    mood = "mother daughter relationship"
    movies = get_movies_by_genres(mood)

    print(f"\nMovies for mood: {mood}")
    for m in movies:
        genre_names = [genre_dict.get(gid, "") for gid in m['genre_ids']]
        print(f"- {m['title']} | Genres: {', '.join(genre_names)}")
