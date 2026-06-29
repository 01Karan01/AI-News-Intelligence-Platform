import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/embedded_news.csv")

embeddings = np.load("embeddings/news_embeddings.npy")

print("Articles:", len(df))
print("Embedding Shape:", embeddings.shape)

# -----------------------------
# Cosine similarity matrix
# -----------------------------
similarity_matrix = cosine_similarity(embeddings)

# -----------------------------
# Agglomerative Clustering
# -----------------------------
clustering = clustering = AgglomerativeClustering(
    n_clusters=30,
    affinity="precomputed",
    linkage="average"
)

labels = clustering.fit_predict(1 - similarity_matrix)

df["cluster"] = labels

# -----------------------------
# Save results
# -----------------------------
df.to_csv("clustered_news.csv", index=False)

print("\nCluster Counts:\n")
print(df["cluster"].value_counts().sort_index())

print("\nSample Results:\n")
print(df[["cluster", "title"]].head(30))