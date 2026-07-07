import sys
from pathlib import Path

import pandas as pd
from transformers import pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.utils.csv_utils import read_csv_safely


BASE_DIR = Path(__file__).resolve().parents[1]
BAD_ENTITIES = {"bbc", "cnn", "npr", "com", "news", "reuters"}


def clean_entity(value):
    cleaned = str(value).replace("##", "").strip(" ,.;:!?()[]{}\"'")
    if len(cleaned) <= 2:
        return ""
    if cleaned.lower() in BAD_ENTITIES:
        return ""
    if cleaned[0].islower():
        return ""
    if cleaned.islower():
        return ""
    return cleaned


print("Loading NER model...")

ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

print("Model Loaded!")

# -----------------------
# Load clustered dataset
# -----------------------

df = read_csv_safely("clustering/clustered_news.csv")

people = []
organizations = []
locations = []

print("Extracting entities...\n")

for text in (
    df["title"].fillna("") + " " +
    df["summary"].fillna("")
):

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

    people.append(", ".join(sorted(set(person))))
    organizations.append(", ".join(sorted(set(org))))
    locations.append(", ".join(sorted(set(loc))))

df["people"] = people
df["organizations"] = organizations
df["locations"] = locations

df.to_csv(BASE_DIR / "data" / "news_with_entities.csv", index=False)

print("\nDone!")
print("Saved as news_with_entities.csv")
