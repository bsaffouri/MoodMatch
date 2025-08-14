from tmdb_api import get_movies_by_mood, genre_dict
from config import embed_text
import torch
import torch.nn.functional as F

def cosine_similarity(a, b):
    # Compute cosine similarity between two sets of embeddings
    return F.cosine_similarity(a, b, dim=1)

def rank_movies_by_mood(mood):
    movies = get_movies_by_mood(mood, num_results=20)
    if not movies:
        return []

    # Embed user mood
    mood_embedding = embed_text([mood])

    # Embed movie overviews
    overviews = [m["overview"] if m.get("overview") else "" for m in movies]
    movie_embeddings = embed_text(overviews)

    # Compute cosine similarity
    similarities = cosine_similarity(mood_embedding, movie_embeddings)

    # Sort movies by similarity
    sorted_movies = [m for _, m in sorted(zip(similarities.tolist(), movies), reverse=True)]
    return sorted_movies[:5]

if __name__ == "__main__":
    mood = "3 am feeling melancholic and sentimental"
    ranked_movies = rank_movies_by_mood(mood)

    print(f"\nTop movies for mood: {mood}")
    for m in ranked_movies:
        genre_names = [genre_dict.get(gid, "") for gid in m['genre_ids']]
        print(f"- {m['title']} | Genres: {', '.join(genre_names)}")