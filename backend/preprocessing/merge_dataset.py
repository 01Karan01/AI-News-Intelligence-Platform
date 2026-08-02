import sys
from pathlib import Path
from datetime import datetime
from html import unescape
import re

import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.csv_utils import read_csv_safely
from backend.utils.db import init_db, save_articles_to_db
from backend.utils.logger import logger


def clean_text(value):
    if value is None:
        return ""

    text = str(value)
    if not text.strip():
        return ""

    try:
        repaired = text.encode("latin1").decode("utf-8")
        if "�" not in repaired:
            text = repaired
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    text = unescape(text)
    text = re.sub(r"<\s*br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"</\s*(p|li|div|h\d)\s*>", ". ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\bContinue reading\.{0,3}\s*$", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip(" .")


def main(rss_df=None, api_df=None):
    """Merge RSS and NewsAPI data into the database.

    Args:
        rss_df: Optional DataFrame from RSS collector. Falls back to CSV if None.
        api_df: Optional DataFrame from NewsAPI collector. Falls back to CSV if None.
    """

    logger.info("Initializing database...")
    init_db()

    # Load data — prefer passed-in DataFrames, fall back to CSVs
    if rss_df is None:
        logger.info("Loading RSS data from CSV...")
        rss = read_csv_safely("news.csv")
    else:
        rss = rss_df.copy()
        logger.info("Using %d articles from RSS collector", len(rss))

    if api_df is None:
        api_csv = Path(__file__).resolve().parent.parent / "newsapi_articles.csv"
        if api_csv.exists():
            logger.info("Loading NewsAPI data from CSV...")
            api = read_csv_safely(str(api_csv))
        else:
            logger.info("No NewsAPI CSV found — skipping.")
            api = pd.DataFrame()
    else:
        api = api_df.copy()
        if not api.empty:
            logger.info("Using %d articles from NewsAPI collector", len(api))
        else:
            logger.info("NewsAPI returned no articles — skipping.")

    # Normalize NewsAPI column names
    if not api.empty:
        api = api.rename(
            columns={
                "description": "summary",
                "url": "link",
                "publishedAt": "published",
            }
        )

    # Add missing columns
    for df in [rss, api]:
        if df.empty:
            continue
        if "author" not in df.columns:
            df["author"] = ""
        if "collected_at" not in df.columns:
            df["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Select standard columns
    cols = ["source", "title", "summary", "link", "published", "author", "collected_at"]
    if not rss.empty:
        rss = rss.reindex(columns=cols)
    if not api.empty:
        api = api.reindex(columns=cols)

    # Merge
    frames = [df for df in [rss, api] if not df.empty]
    if not frames:
        logger.warning("No articles to merge — both sources are empty.")
        return

    merged = pd.concat(frames, ignore_index=True)
    for column in ["source", "title", "summary", "author"]:
        if column in merged.columns:
            merged[column] = merged[column].apply(clean_text)
    merged.drop_duplicates(subset=["title"], inplace=True)

    logger.info("Upserting %d unique articles into database...", len(merged))
    save_articles_to_db(merged)

    logger.info("Merge completed successfully!")


if __name__ == "__main__":
    main()
