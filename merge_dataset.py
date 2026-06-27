import pandas as pd

rss = pd.read_csv("news.csv")
api = pd.read_csv("newsapi_articles.csv")

# Rename NewsAPI columns to match RSS
api = api.rename(columns={
    "description": "summary",
    "url": "link",
    "publishedAt": "published"
})

# Keep only common columns
rss = rss[["source", "title", "summary", "link", "published"]]
api = api[["source", "title", "summary", "link", "published"]]

# Merge
merged = pd.concat([rss, api], ignore_index=True)

# Remove duplicate titles
merged.drop_duplicates(subset=["title"], inplace=True)

merged.to_csv("master_news.csv", index=False)

print("Total Articles:", len(merged))