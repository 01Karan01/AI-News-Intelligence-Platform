from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

files = {
    "master_news": BASE_DIR / "data" / "master_news.csv",
    "clustered_news": BASE_DIR / "clustering" / "clustered_news.csv",
    "news_with_entities": BASE_DIR / "data" / "news_with_entities.csv",
    "event_titles": BASE_DIR / "data" / "event_titles.csv",
}

for name, path in files.items():
    print("=" * 60)
    print(name)
    print(path)

    df = pd.read_csv(path)

    print(df.columns.tolist())
    print(df.head(2))