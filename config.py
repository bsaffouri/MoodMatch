import os
import json
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import requests

# --- Load environment variables ---
load_dotenv("project.env")
API_KEY = os.getenv("API_KEY")
print("Loaded API_KEY:", API_KEY)

# --- TMDB API endpoints ---
DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
GENRES_URL = "https://api.themoviedb.org/3/genre/movie/list"
HEADERS = {"accept": "application/json"}

# --- Load mood mappings ---
with open("mood_mappings.json", "r") as f:
    maps_to_moods = json.load(f)

# --- Load tokenizer and model ---
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# --- Utility: embed text using mean pooling ---
def embed_text(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Mean pooling
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings
