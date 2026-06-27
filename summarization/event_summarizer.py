import pandas as pd
from transformers import pipeline

print("Loading summarization model...")

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

print("Model Loaded!")

# ---------------------------
# Load clustered dataset
# ---------------------------

df = pd.read_csv("clustered_news.csv")

clusters = sorted(df["cluster"].unique())

for cluster in clusters:

    print("\n")
    print("=" * 70)
    print(f"EVENT {cluster}")
    print("=" * 70)

    cluster_df = df[df["cluster"] == cluster]

    # Merge titles into one document
    text = ". ".join(cluster_df["title"].tolist())

    # BART has input length limits
    text = text[:1000]

    summary = summarizer(
        text,
        max_length=80,
        min_length=30,
        do_sample=False
    )

    print(summary[0]["summary_text"])