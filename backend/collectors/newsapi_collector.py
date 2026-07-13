import os
import pathlib

import requests
import pandas as pd

from backend.utils.logger import logger

_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]


def _load_api_key():
    """Try to load the NewsAPI key from environment or .env file."""

    api_key = os.getenv("API_KEY")
    if api_key:
        return api_key

    env_path = _BACKEND_DIR / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "API_KEY":
                        return v.strip().strip('"').strip("'")
        except Exception as e:
            logger.exception("Failed reading .env file: %s", e)

    return None


def collect():
    """Collect top headlines from NewsAPI. Returns a DataFrame.

    Returns an empty DataFrame if no API key is available (graceful skip).
    """

    api_key = _load_api_key()

    if not api_key:
        logger.warning(
            "No NewsAPI key found — skipping NewsAPI collection. "
            "Set API_KEY in your environment or backend/.env to enable this."
        )
        return pd.DataFrame()

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&pageSize=100&apiKey={api_key}"
    )

    logger.info("Fetching articles from NewsAPI...")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.exception("HTTP request to NewsAPI failed: %s", e)
        return pd.DataFrame()
    except ValueError as e:
        logger.exception("Invalid JSON received from NewsAPI: %s", e)
        return pd.DataFrame()

    status = data.get("status")
    if status is None:
        logger.error("No 'status' field in NewsAPI response: %s", data)
        return pd.DataFrame()
    elif status != "ok":
        logger.error("NewsAPI returned non-ok status: %s", data)
        return pd.DataFrame()

    articles_list = data.get("articles", [])
    logger.info("Articles found from NewsAPI: %d", len(articles_list))

    articles = []
    for article in articles_list:
        source = None
        if isinstance(article.get("source"), dict):
            source = article["source"].get("name")

        articles.append(
            {
                "source": source,
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "author": article.get("author"),
                "publishedAt": article.get("publishedAt"),
                "url": article.get("url"),
            }
        )

    df = pd.DataFrame(articles)
    logger.info("NewsAPI collection completed — %d articles", len(df))
    return df


# Allow standalone execution for testing
if __name__ == "__main__":
    result = collect()
    if not result.empty:
        result.to_csv("newsapi_articles.csv", index=False)
        logger.info("Saved %d articles to newsapi_articles.csv", len(result))
    else:
        logger.info("No articles collected.")