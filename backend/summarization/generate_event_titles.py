from pathlib import Path

import pandas as pd
from keybert import KeyBERT


BASE_DIR = Path(__file__).resolve().parents[1]
BAD_TITLE_WORDS = {
    "bbc",
    "cnn",
    "npr",
    "news",
    "video",
    "watch",
    "reuters",
    "ap",
    "the",
    "and",
}


def clean_title(text):
    words = []
    for raw_word in str(text).replace("-", " ").replace(":", " ").split():
        word = raw_word.strip(" ,.;:!?()[]{}\"'")
        if not word or word.lower() in BAD_TITLE_WORDS:
            continue
        words.append(word)

    return " ".join(words[:5]).title() or "Untitled Event"


print("Loading KeyBERT model...")

kw_model = KeyBERT()

print("Model Loaded!\n")

# -----------------------
# Load clustered news
# -----------------------

df = pd.read_csv(BASE_DIR / "clustering" / "clustered_news.csv")

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
    best_keyword = keyword_list[0] if keyword_list else cluster_df["title"].iloc[0]

    event_titles.append({
        "cluster": cluster,
        "title": clean_title(best_keyword),
        "keywords": ", ".join(keyword_list)
    })

event_df = pd.DataFrame(event_titles)

event_df.to_csv(BASE_DIR / "data" / "event_titles.csv", index=False)

print(event_df)

print("\nSaved as data/event_titles.csv")
