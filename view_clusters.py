import pandas as pd

df = pd.read_csv("clustered_news.csv")

for cluster in sorted(df["cluster"].unique()):
    print("=" * 70)
    print(f"CLUSTER {cluster}")
    print("=" * 70)

    cluster_df = df[df["cluster"] == cluster]

    for title in cluster_df["title"]:
        print("-", title)

    print()