import pandas as pd
from keybert import KeyBERT

print("Loading KeyBERT model...")

kw_model = KeyBERT()

print("Model Loaded!\n")

# -----------------------
# Load clustered news
# -----------------------

df = pd.read_csv("clustering/clustered_news.csv")

clusters = sorted(df["cluster"].unique())

event_titles = []

for cluster in clusters:

    cluster_df = df[df["cluster"] == cluster]

    # Combine first few headlines
    text = " ".join(cluster_df["title"].head(5).tolist())

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=5
    )

    keyword_list = [k[0] for k in keywords]

    event_titles.append({
        "cluster": cluster,
        "keywords": ", ".join(keyword_list)
    })

event_df = pd.DataFrame(event_titles)

event_df.to_csv("data/event_titles.csv", index=False)

print(event_df)

print("\nSaved as data/event_titles.csv")