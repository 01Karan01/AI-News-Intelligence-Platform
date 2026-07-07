import sys
from pathlib import Path
import pandas as pd
from keybert import KeyBERT

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.db import get_connection

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

def main():
    print("Loading KeyBERT model...")
    kw_model = KeyBERT()
    print("Model Loaded!\n")

    print("Loading articles from database...")
    conn = get_connection()
    df = pd.read_sql_query("SELECT title, cluster_id FROM articles WHERE cluster_id IS NOT NULL", conn)

    if df.empty:
        print("No clustered articles found in database. Exiting.")
        conn.close()
        return

    clusters = sorted(df["cluster_id"].unique())
    event_titles = []

    for cluster in clusters:
        cluster_df = df[df["cluster_id"] == cluster]
        
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
            "cluster": int(cluster),
            "title": clean_title(best_keyword),
            "keywords": ", ".join(keyword_list)
        })

    # Clear events table and insert new events
    print("Saving event titles to database...")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events")
    
    for event in event_titles:
        cursor.execute(
            "INSERT INTO events (id, title, keywords) VALUES (?, ?, ?)",
            (event["cluster"], event["title"], event["keywords"])
        )
        
    conn.commit()
    conn.close()
    
    print("Event titles generation completed successfully!")
    print(pd.DataFrame(event_titles))

if __name__ == "__main__":
    main()
