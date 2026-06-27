import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("master_news.csv")

print(f"Loaded {len(df)} articles")

# -----------------------------
# Combine title and summary
# -----------------------------
texts = (
    df["title"].fillna("") + " " +
    df["summary"].fillna("")
).tolist()

# -----------------------------
# Load Embedding Model
# -----------------------------
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")

# -----------------------------
# Generate Embeddings
# -----------------------------
print("Generating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=32,
    convert_to_numpy=True
)

print("Embeddings generated!")

# -----------------------------
# Display Shape
# -----------------------------
print("\nEmbedding Shape:", embeddings.shape)

# -----------------------------
# Save Embeddings
# -----------------------------
np.save("news_embeddings.npy", embeddings)

print("Embeddings saved as news_embeddings.npy")

# -----------------------------
# Save Dataset
# -----------------------------
df.to_csv("embedded_news.csv", index=False)

print("Dataset saved as embedded_news.csv")