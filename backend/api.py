from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AI News Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _read_csv(path):
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Missing data file: {path.name}")

    return pd.read_csv(path, engine="python", on_bad_lines="skip").fillna("")


def _split_values(value):
    if not isinstance(value, str) or not value.strip():
        return []

    values = []
    for item in value.split(","):
        cleaned = item.strip()
        if (
            cleaned
            and len(cleaned) > 2
            and not cleaned.startswith("##")
            and not cleaned.islower()
            and cleaned.lower() not in {"bbc", "cnn", "npr", "com", "news", "reuters"}
            and cleaned not in values
        ):
            values.append(cleaned)
    return values


def _parse_date(value):
    parsed = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(parsed):
        return datetime.now(timezone.utc)
    return parsed.to_pydatetime()


def _event_title(cluster_id, titles_df, cluster_df):
    if not titles_df.empty and "cluster" in titles_df.columns:
        title_row = titles_df[titles_df["cluster"].astype(str) == str(cluster_id)]
    else:
        title_row = pd.DataFrame()

    if not title_row.empty:
        title = str(title_row.iloc[0].get("title", "")).strip()
        if title:
            return title

        keywords = str(title_row.iloc[0].get("keywords", "")).strip()
        if keywords:
            return keywords.split(",")[0].strip().title()

    return str(cluster_df.iloc[0].get("title", f"Event Cluster {cluster_id}"))


def _category_for(text):
    lowered = text.lower()
    categories = {
        "Technology": ["ai", "openai", "tech", "software", "chip", "semiconductor", "gta", "nasa"],
        "Geopolitics": [
            "iran",
            "us",
            "russia",
            "ukraine",
            "china",
            "war",
            "sanction",
            "conflict",
            "refugee",
            "asylum",
            "minister",
        ],
        "Climate": ["heat", "heatwave", "climate", "weather", "storm", "flood", "earthquake", "earthquakes"],
        "Business": ["market", "stock", "company", "business", "economy", "trade"],
        "Politics": ["election", "minister", "court", "government", "president", "campaign"],
        "Health": ["health", "hospital", "disease", "doctor", "vaccine"],
    }

    scores = {}
    for category, keywords in categories.items():
        scores[category] = sum(
            len(re.findall(rf"\b{re.escape(keyword)}\b", lowered)) for keyword in keywords
        )

    category, score = max(scores.items(), key=lambda item: item[1])
    return category if score else "World News"


def _unique_from_column(cluster_df, column, limit=8):
    if column not in cluster_df.columns:
        return []

    counter = Counter()
    for value in cluster_df[column].tolist():
        counter.update(_split_values(value))
    return [item for item, _ in counter.most_common(limit)]


def _source_articles(cluster_df):
    articles = []
    for index, row in cluster_df.head(10).iterrows():
        published = _parse_date(row.get("published", ""))
        articles.append(
            {
                "id": f"article-{row.get('cluster', 'x')}-{index}",
                "headline": row.get("title", "Untitled article"),
                "source": row.get("source", "Unknown source"),
                "publishedAt": published.isoformat(),
                "url": row.get("link", ""),
            }
        )
    return articles


def _event_timeline(cluster_df):
    items = []
    sorted_df = cluster_df.copy()
    sorted_df["_published_dt"] = sorted_df["published"].apply(_parse_date)
    sorted_df = sorted_df.sort_values("_published_dt")

    for _, row in sorted_df.head(5).iterrows():
        published = row["_published_dt"]
        items.append(
            {
                "time": published.strftime("%H:%M"),
                "label": row.get("title", "Article published"),
            }
        )
    return items


def _load_events():
    from backend.utils.db import get_connection, DB_PATH
    if not DB_PATH.exists():
        return []

    conn = get_connection()
    try:
        news_df = pd.read_sql_query(
            "SELECT * FROM articles WHERE cluster_id IS NOT NULL", conn
        )
        news_df = news_df.rename(columns={"cluster_id": "cluster"})
        titles_df = pd.read_sql_query(
            "SELECT id as cluster, title, keywords FROM events", conn
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database read failed: {e}")
    finally:
        conn.close()

    if news_df.empty:
        return []

    events = []
    for cluster_id, cluster_df in news_df.groupby("cluster"):
        cluster_df = cluster_df.copy()
        cluster_df["_published_dt"] = cluster_df["published"].apply(_parse_date)
        cluster_df = cluster_df.sort_values("_published_dt", ascending=False)

        title = _event_title(cluster_id, titles_df, cluster_df)
        top_row = cluster_df.iloc[0]
        summaries = [str(value).strip() for value in cluster_df["summary"].tolist() if str(value).strip()]
        summary = summaries[0] if summaries else "No summary is available for this event cluster."
        article_count = len(cluster_df)
        source_count = cluster_df["source"].nunique() if "source" in cluster_df.columns else 0
        confidence = min(98, max(72, 72 + article_count + source_count * 2))

        people = _unique_from_column(cluster_df, "people")
        organizations = _unique_from_column(cluster_df, "organizations")
        locations = _unique_from_column(cluster_df, "locations")
        category_text = " ".join([title, summary, " ".join(cluster_df["title"].head(5).tolist())])

        events.append(
            {
                "id": str(cluster_id),
                "title": title,
                "summary": summary,
                "date": top_row["_published_dt"].isoformat(),
                "category": _category_for(category_text),
                "confidence": confidence,
                "articleCount": article_count,
                "globalImpact": (
                    f"This cluster connects {article_count} related articles from "
                    f"{source_count} source{'s' if source_count != 1 else ''}, helping surface a broader event "
                    "instead of isolated headlines."
                ),
                "people": people,
                "organizations": organizations,
                "locations": locations,
                "sources": _source_articles(cluster_df),
                "timeline": _event_timeline(cluster_df),
            }
        )

    return sorted(events, key=lambda event: event["date"], reverse=True)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/events")
def get_events():
    return _load_events()


@app.get("/api/events/search")
def search_events(q: str = Query(default="")):
    term = q.lower().strip()
    events = _load_events()

    if not term:
        return events

    return [
        event
        for event in events
        if term
        in " ".join(
            [
                event["title"],
                event["summary"],
                event["category"],
                " ".join(event["people"]),
                " ".join(event["organizations"]),
                " ".join(event["locations"]),
            ]
        ).lower()
    ]


@app.get("/api/events/{event_id}")
def get_event(event_id: str):
    for event in _load_events():
        if event["id"] == event_id:
            return event

    raise HTTPException(status_code=404, detail="Event not found")


@app.get("/api/statistics")
def get_statistics():
    from backend.utils.db import get_connection, DB_PATH
    if not DB_PATH.exists():
        return {
            "articles": 0,
            "events": 0,
            "sources": 0,
            "countries": 0,
        }

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as articles, COUNT(DISTINCT cluster_id) as events, COUNT(DISTINCT source) as sources FROM articles")
        stats_row = cursor.fetchone()
        articles_count = stats_row["articles"]
        events_count = stats_row["events"]
        sources_count = stats_row["sources"]

        cursor.execute("SELECT locations FROM articles WHERE locations IS NOT NULL AND locations != ''")
        loc_rows = cursor.fetchall()
        locations = Counter()
        for row in loc_rows:
            locations.update(_split_values(row["locations"]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database statistics query failed: {e}")
    finally:
        conn.close()

    return {
        "articles": articles_count,
        "events": events_count,
        "sources": sources_count,
        "countries": len(locations),
    }


@app.get("/api/timeline")
def get_timeline():
    events = _load_events()
    if not events:
        return []

    latest = max(_parse_date(event["date"]) for event in events).date()
    groups = []

    for days_ago in range(6):
        target_date = latest - pd.Timedelta(days=days_ago)
        label = "Latest" if days_ago == 0 else f"{days_ago} Day{'s' if days_ago != 1 else ''} Earlier"
        groups.append(
            {
                "daysAgo": days_ago,
                "label": label,
                "events": [
                    event
                    for event in events
                    if _parse_date(event["date"]).date() == target_date
                ],
            }
        )

    return groups
