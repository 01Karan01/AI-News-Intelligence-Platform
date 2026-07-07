import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add project root to sys.path if not present
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.csv_utils import read_csv_safely
from backend.utils.db import init_db, save_articles_to_db

def main():
    print("Initializing database...")
    init_db()

    print("Loading raw files...")
    rss = read_csv_safely("news.csv")
    api = read_csv_safely("newsapi_articles.csv")

    # Normalize NewsAPI column names
    api = api.rename(columns={
        "description": "summary",
        "url": "link",
        "publishedAt": "published"
    })

    # Add missing columns
    if "author" not in rss.columns:
        rss["author"] = ""
    if "collected_at" not in rss.columns:
        rss["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "author" not in api.columns:
        api["author"] = ""
    api["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Select standard columns
    cols = ["source", "title", "summary", "link", "published", "author", "collected_at"]
    rss = rss[[c for c in cols if c in rss.columns]].reindex(columns=cols)
    api = api[[c for c in cols if c in api.columns]].reindex(columns=cols)

    # Merge
    merged = pd.concat([rss, api], ignore_index=True)
    merged.drop_duplicates(subset=["title"], inplace=True)

    print(f"Upserting {len(merged)} unique articles into database...")
    save_articles_to_db(merged)

    print("Consolidation Completed successfully!")

if __name__ == "__main__":
    main()