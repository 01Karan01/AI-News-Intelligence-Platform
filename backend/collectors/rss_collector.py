import feedparser
import pandas as pd
from datetime import datetime
from backend.utils.logger import logger

# ─────────────────────────────────────────────
# RSS Feed Sources (expanded)
# ─────────────────────────────────────────────
RSS_FEEDS = {
    # ── BBC ──
    "BBC Main": "https://feeds.bbci.co.uk/news/rss.xml",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "BBC Science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",

    # ── NPR ──
    "NPR": "https://feeds.npr.org/1001/rss.xml",

    # ── TechCrunch ──
    "TechCrunch": "https://techcrunch.com/feed/",

    # ── Reuters ──
    "Reuters World": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
    "Reuters Business": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    "Reuters Tech": "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best",

    # ── The Guardian ──
    "Guardian World": "https://www.theguardian.com/world/rss",
    "Guardian Tech": "https://www.theguardian.com/uk/technology/rss",
    "Guardian Science": "https://www.theguardian.com/science/rss",

    # ── Al Jazeera ──
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",

    # ── The Verge ──
    "The Verge": "https://www.theverge.com/rss/index.xml",

    # ── Ars Technica ──
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",

    # ── Wired ──
    "Wired": "https://www.wired.com/feed/rss",

    # ── ABC News ──
    "ABC News": "https://abcnews.go.com/abcnews/topstories",

    # ── New York Times ──
    "NYT Home": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NYT World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

    # ── CBS News ──
    "CBS News": "https://www.cbsnews.com/latest/rss/main",

    # ── Associated Press ──
    "AP News": "https://rsshub.app/apnews/topics/apf-topnews",
}


def collect():
    """Collect articles from all RSS feeds. Returns a pandas DataFrame."""

    logger.info("Starting RSS collection from %d feeds...", len(RSS_FEEDS))
    articles = []

    for source, url in RSS_FEEDS.items():
        logger.info("Collecting from %s", source)

        try:
            feed = feedparser.parse(url)
        except Exception as e:
            logger.exception("Failed to parse feed for %s: %s", source, e)
            continue

        # Skip feed if it cannot be parsed
        if feed.bozo:
            logger.warning(
                "Could not read %s: %s",
                source,
                getattr(feed, "bozo_exception", "parse error"),
            )
            continue

        logger.info("Articles found from %s: %d", source, len(feed.entries))

        for entry in feed.entries:
            articles.append(
                {
                    "source": source,
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "author": entry.get("author", ""),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    df = pd.DataFrame(articles)

    # Remove duplicate articles
    if not df.empty:
        df.drop_duplicates(subset=["title"], inplace=True)

    logger.info("RSS COLLECTION COMPLETED")
    logger.info("Total unique articles: %d", len(df))
    if not df.empty:
        logger.info(
            "Articles per source:\n%s", df["source"].value_counts().to_string()
        )

    return df


# Allow standalone execution for testing
if __name__ == "__main__":
    result = collect()
    result.to_csv("news.csv", index=False)
    logger.info("Dataset saved as news.csv")