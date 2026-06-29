import os
import requests
import pandas as pd

API_KEY = os.getenv("API_KEY")

url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=100&apiKey={API_KEY}"
)

response = requests.get(url)

data = response.json()

print(data["status"])
print("Articles:", len(data["articles"]))

articles = []

for article in data["articles"]:

    articles.append({
        "source": article["source"]["name"],
        "title": article["title"],
        "description": article["description"],
        "content": article["content"],
        "author": article["author"],
        "publishedAt": article["publishedAt"],
        "url": article["url"]
    })

df = pd.DataFrame(articles)

df.to_csv("newsapi_articles.csv", index=False)

print("Saved", len(df), "articles")