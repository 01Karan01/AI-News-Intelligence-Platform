import feedparser
import pandas as pd

feeds = {
    "BBC Main": "https://feeds.bbci.co.uk/news/rss.xml",
    "BBC Tech": "https://feeds.bbci.co.uk/news/technology/rss.xml"
}

articles = []

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries:
        articles.append({
            "source": source,
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")
        })

df = pd.DataFrame(articles)

df.to_csv("news.csv", index=False)

print("Total articles:", len(df))