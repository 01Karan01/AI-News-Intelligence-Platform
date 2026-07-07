import pandas as pd
import numpy as np
import sys
from pathlib import Path
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.csv_utils import read_csv_safely


BASE_DIR = Path(__file__).resolve().parents[1]

# -----------------------------
# Load data
# -----------------------------
df = read_csv_safely("data/embedded_news.csv")

embeddings = np.load(BASE_DIR / "embeddings" / "news_embeddings.npy")

print("Articles:", len(df))
print("Embedding Shape:", embeddings.shape)

# -----------------------------
# Cosine similarity matrix
# -----------------------------
similarity_matrix = cosine_similarity(embeddings)

# -----------------------------
# Agglomerative Clustering
# -----------------------------
clustering = AgglomerativeClustering(
    n_clusters=30,
    metric="precomputed",
    linkage="average"
)

labels = clustering.fit_predict(1 - similarity_matrix)

df["cluster"] = labels

# -----------------------------
# Save results
# -----------------------------
df.to_csv(BASE_DIR / "clustering" / "clustered_news.csv", index=False)

print("\nCluster Counts:\n")
print(df["cluster"].value_counts().sort_index())

print("\nSample Results:\n")
print(df[["cluster", "title"]].head(30))
