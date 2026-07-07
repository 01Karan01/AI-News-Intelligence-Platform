import sys
from pathlib import Path
import pandas as pd
from transformers import pipeline

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.db import get_connection

BAD_ENTITIES = {"bbc", "cnn", "npr", "com", "news", "reuters"}

def clean_entity(value):
    cleaned = str(value).replace("##", "").strip(" ,.;:!?()[]{}\"'")
    if len(cleaned) <= 2:
        return ""
    if cleaned.lower() in BAD_ENTITIES:
        return ""
    if cleaned.islower() or cleaned[0].islower():
        return ""
    return cleaned

def main():
    print("Loading NER model...")
    ner = pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )
    print("Model Loaded!")

    print("Loading articles from database...")
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, title, summary FROM articles ORDER BY id", conn)

    if df.empty:
        print("No articles found in database. Exiting.")
        conn.close()
        return

    print(f"Extracting entities for {len(df)} articles...\n")
    cursor = conn.cursor()

    for idx, row in df.iterrows():
        text = str(row["title"] or "") + " " + str(row["summary"] or "")
        entities = ner(text[:512])

        person = []
        org = []
        loc = []

        for entity in entities:
            label = entity["entity_group"]
            cleaned = clean_entity(entity["word"])

            if not cleaned:
                continue

            if label == "PER":
                person.append(cleaned)
            elif label == "ORG":
                org.append(cleaned)
            elif label == "LOC":
                loc.append(cleaned)

        people_str = ", ".join(sorted(set(person)))
        org_str = ", ".join(sorted(set(org)))
        loc_str = ", ".join(sorted(set(loc)))

        cursor.execute(
            "UPDATE articles SET people = ?, organizations = ?, locations = ? WHERE id = ?",
            (people_str, org_str, loc_str, int(row["id"]))
        )

        if idx % 10 == 0:
            print(f"Processed {idx}/{len(df)} articles...")

    conn.commit()
    conn.close()
    print("\nNER extraction and database enrichment completed successfully!")

if __name__ == "__main__":
    main()
