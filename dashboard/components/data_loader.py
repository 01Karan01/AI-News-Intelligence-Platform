import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.db import get_connection

def load_data():
    conn = get_connection()
    try:
        # Load articles with valid clusters
        df = pd.read_sql_query("SELECT * FROM articles WHERE cluster_id IS NOT NULL", conn)
        # Load events mapping table
        titles_df = pd.read_sql_query("SELECT id as cluster, title, keywords FROM events", conn)
    except Exception as e:
        print(f"Error loading data from database: {e}")
        df = pd.DataFrame(columns=["source", "title", "summary", "link", "published", "author", "collected_at", "cluster", "people", "organizations", "locations"])
        titles_df = pd.DataFrame(columns=["cluster", "title", "keywords"])
    finally:
        conn.close()

    # Align DB column 'cluster_id' with expected dataframe column 'cluster'
    if "cluster_id" in df.columns:
        df = df.rename(columns={"cluster_id": "cluster"})

    # Set default types
    df["cluster"] = df["cluster"].astype(int)
    titles_df["cluster"] = titles_df["cluster"].astype(int)

    return df, titles_df