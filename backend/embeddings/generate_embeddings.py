import sys
from pathlib import Path
import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.db import get_connection, DB_PATH

def main():
    print("Loading articles from database...")
    conn = get_connection()
    # Sort by ID to ensure consistent 1-to-1 matching with index
    df = pd.read_sql_query("SELECT id, title, summary FROM articles ORDER BY id", conn)
    conn.close()

    print(f"Loaded {len(df)} articles")
    if df.empty:
        print("No articles found in database. Exiting.")
        return

    # Combine title and summary
    texts = (
        df["title"].fillna("") + " " +
        df["summary"].fillna("")
    ).tolist()

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded successfully!")

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32,
        convert_to_numpy=True
    )
    print("Embeddings generated!")
    print("Embedding Shape:", embeddings.shape)

    # Save embeddings to the embeddings folder
    embeddings_dir = Path(__file__).resolve().parent
    embeddings_dir.mkdir(parents=True, exist_ok=True)
    np.save(embeddings_dir / "news_embeddings.npy", embeddings)
    print(f"Embeddings saved to {embeddings_dir / 'news_embeddings.npy'}")

if __name__ == "__main__":
    main()