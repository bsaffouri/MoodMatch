from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# Load pre-trained sentence transformer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(texts):
    """Return sentence embeddings for a list of texts."""
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Mean pooling
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings

def cosine_similarity(a, b):
    return F.cosine_similarity(a, b, dim=1)