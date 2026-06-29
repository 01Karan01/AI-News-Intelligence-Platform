import feedparser
import pandas as pd
from datetime import datetime
from utils.logger import logger

# -----------------------------
# RSS Feed Sources
# -----------------------------
RSS_FEEDS = {
    # BBC
    "BBC Main": "https://feeds.bbci.co.uk/news/rss.xml",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC Science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",

    # NPR
    "NPR": "https://feeds.npr.org/1001/rss.xml",

    # TechCrunch
    "TechCrunch": "https://techcrunch.com/feed/",
}

# -----------------------------
# Store all collected articles
# -----------------------------
articles = []

# -----------------------------
# Collect articles
# -----------------------------
for source, url in RSS_FEEDS.items():

    logger.info("Collecting from %s", source)

    try:
        feed = feedparser.parse(url)
    except Exception as e:
        logger.exception("Failed to parse feed for %s: %s", source, e)
        continue

    # Skip feed if it cannot be parsed
    if feed.bozo:
        logger.warning("Could not read %s: %s", source, getattr(feed, 'bozo_exception', 'parse error'))
        continue

    logger.info("Articles Found from %s: %d", source, len(feed.entries))

    for entry in feed.entries:

        articles.append({
            "source": source,
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "author": entry.get("author", ""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(articles)

# -----------------------------
# Remove duplicate articles
# -----------------------------
df.drop_duplicates(subset=["title"], inplace=True)

# -----------------------------
# Save dataset
# -----------------------------
df.to_csv("news.csv", index=False)

# -----------------------------
# Print Summary
# -----------------------------
logger.info("NEWS COLLECTION COMPLETED")
logger.info("Total Unique Articles: %d", len(df))
logger.info("Articles Per Source:\n%s", df["source"].value_counts().to_string())
logger.info("Dataset saved as news.csv")