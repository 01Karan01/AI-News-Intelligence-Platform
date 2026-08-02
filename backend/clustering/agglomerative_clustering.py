import sys
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.db import get_connection

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent

    print("Loading articles from database...")
    conn = get_connection()
    # Must order by id to match embeddings ordering
    df = pd.read_sql_query("SELECT id, title FROM articles ORDER BY id", conn)
    
    embeddings_path = BASE_DIR / "embeddings" / "news_embeddings.npy"
    if not embeddings_path.exists():
        print(f"Embeddings file not found at {embeddings_path}. Please run generate_embeddings.py first.")
        conn.close()
        return

    embeddings = np.load(embeddings_path)

    print("Articles in DB:", len(df))
    print("Embedding Shape:", embeddings.shape)

    if len(df) != embeddings.shape[0]:
        print("ERROR: Dimension mismatch! The number of articles in DB does not match embeddings shape.")
        conn.close()
        return

    # Compute cosine similarity matrix
    print("Computing cosine similarity matrix...")
    similarity_matrix = cosine_similarity(embeddings)

    # Perform Agglomerative Clustering
    print("Running Agglomerative Clustering...")
    try:
        clustering = AgglomerativeClustering(
            n_clusters=min(30, len(df)),  # Handle cases with fewer than 30 articles
            metric="precomputed",
            linkage="average"
        )
    except TypeError:
        clustering = AgglomerativeClustering(
            n_clusters=min(30, len(df)),
            affinity="precomputed",
            linkage="average"
        )
    labels = clustering.fit_predict(1 - similarity_matrix)
    df["cluster"] = labels

    # Update database with cluster_id
    print("Updating cluster IDs in database...")
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "UPDATE articles SET cluster_id = ? WHERE id = ?",
            (int(row["cluster"]), int(row["id"]))
        )
    conn.commit()
    conn.close()

    print("Clustering completed successfully!")
    print("\nCluster Counts:")
    print(df["cluster"].value_counts().sort_index())

if __name__ == "__main__":
    main()
