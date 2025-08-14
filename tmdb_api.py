import requests
import torch
import torch.nn.functional as F
from config import API_KEY, DISCOVER_URL, GENRES_URL, HEADERS, maps_to_moods, embed_text

# --- Fetch genres from TMDB ---
def get_genres():
    params = {"api_key": API_KEY}
    response = requests.get(GENRES_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    genres = response.json().get("genres", [])
    return {g['id']: g['name'] for g in genres}

# --- Genre dictionary (fetched once) ---
genre_dict = get_genres()

# --- Get movies by mood ---
def get_movies_by_mood(mood, num_results=20, top_k=5):
    # Normalize mood
    mood_key = mood.lower().strip()
    normalized_maps = {k.lower().strip(): v for k, v in maps_to_moods.items()}

    if mood_key not in normalized_maps:
        print(f"{mood} not found :(")
        return []

    mood_data = normalized_maps[mood_key]
    genre_ids = mood_data.get("genres", [])
    keywords = mood_data.get("keywords", [])

    # TMDB API params
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1
    }
    if genre_ids:
        params["with_genres"] = ",".join(str(g) for g in genre_ids)

    # Fetch movies from TMDB
    response = requests.get(DISCOVER_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print("Error:", response.json())
        return []

    movies = response.json().get("results", [])[:num_results]

    # --- NLP filter using embeddings ---
    if keywords:
        keyword_embedding = embed_text([" ".join(keywords)])
        movie_overviews = [m.get("overview", "") for m in movies]
        overview_embeddings = embed_text(movie_overviews)

        # Cosine similarity
        cos_sim = F.cosine_similarity(overview_embeddings, keyword_embedding)
        top_indices = torch.topk(cos_sim, k=min(top_k, len(movies))).indices.tolist()
        movies = [movies[i] for i in top_indices]

    return movies