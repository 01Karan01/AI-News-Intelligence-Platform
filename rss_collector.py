import feedparser
import pandas as pd
from datetime import datetime

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

    print(f"\nCollecting from {source}...")

    feed = feedparser.parse(url)

    # Skip feed if it cannot be parsed
    if feed.bozo:
        print(f"Could not read {source}")
        continue

    print(f"Articles Found: {len(feed.entries)}")

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
print("\n===================================")
print("NEWS COLLECTION COMPLETED")
print("===================================")

print(f"\nTotal Unique Articles: {len(df)}")

print("\nArticles Per Source:\n")
print(df["source"].value_counts())

print("\nDataset saved as news.csv")