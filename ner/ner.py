import pandas as pd
from transformers import pipeline

from utils.csv_utils import read_csv_safely

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

        if label == "PER":
            person.append(entity["word"])

        elif label == "ORG":
            org.append(entity["word"])

        elif label == "LOC":
            loc.append(entity["word"])

    people.append(", ".join(sorted(set(person))))
    organizations.append(", ".join(sorted(set(org))))
    locations.append(", ".join(sorted(set(loc))))

df["people"] = people
df["organizations"] = organizations
df["locations"] = locations

df.to_csv("data/news_with_entities.csv", index=False)

print("\nDone!")
print("Saved as news_with_entities.csv")