import os
import sys
import pathlib
import requests
import pandas as pd

try:
    from utils.logger import logger
except ModuleNotFoundError:
    # When running the script directly (python collectors\newsapi_collector.py),
    # Python's sys.path[0] is the collectors folder, so sibling package 'utils'
    # isn't found. Add project root to sys.path as a fallback so imports work.
    ROOT = pathlib.Path(__file__).resolve().parents[1]
    sys.path.append(str(ROOT))
    from utils.logger import logger

API_KEY = os.getenv("API_KEY")

# If API key not in env, try loading from a .env file at project root (simple parser)
if not API_KEY:
    env_path = pathlib.Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "API_KEY":
                        API_KEY = v.strip().strip('"').strip("'")
                        break
        except Exception as e:
            logger.exception("Failed reading .env file: %s", e)

#Raise error if API key is still not set
if not API_KEY:
    logger.error("API_KEY environment variable not set and no API_KEY in .env")
    raise SystemExit("Missing API_KEY environment variable; set it or place API_KEY in a .env file")

url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=100&apiKey={API_KEY}"
)
#Recieve responses from NewsAPI
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    logger.exception("HTTP request to NewsAPI failed: %s", e)
    data = {}
except ValueError as e:
    logger.exception("Invalid JSON received from NewsAPI: %s", e)
    data = {}

status = data.get("status")
if status is None:
    logger.error("No 'status' field in NewsAPI response: %s", data)
elif status != "ok":
    logger.error("NewsAPI returned non-ok status: %s", data)

articles_list = data.get("articles", [])
logger.info("Articles found: %d", len(articles_list))

articles = []
for article in articles_list:
    source = None
    if isinstance(article.get("source"), dict):
        source = article.get("source", {}).get("name")

    articles.append({
        "source": source,
        "title": article.get("title"),
        "description": article.get("description"),
        "content": article.get("content"),
        "author": article.get("author"),
        "publishedAt": article.get("publishedAt"),
        "url": article.get("url")
    })

df = pd.DataFrame(articles)
out_file = "newsapi_articles.csv"
try:
    df.to_csv(out_file, index=False)
    logger.info("Saved %d articles to %s", len(df), out_file)
except Exception as e:
    logger.exception("Failed to save articles to CSV: %s", e)