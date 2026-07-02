import pandas as pd
from utils.csv_utils import read_csv_safely


def load_data():
    df = read_csv_safely("clustering/clustered_news.csv")
    titles_df = pd.read_csv("data/event_titles.csv")

    df["cluster"] = df["cluster"].astype(int)
    titles_df["cluster"] = titles_df["cluster"].astype(int)

    return df, titles_df