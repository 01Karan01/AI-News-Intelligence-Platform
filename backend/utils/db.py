import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "news_intelligence.db"

def get_connection():
    """Return a sqlite3 Connection object pointing to our local news database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create events and articles tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            title TEXT,
            keywords TEXT
        )
    """)
    
    # Create articles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT UNIQUE,
            summary TEXT,
            link TEXT,
            published TEXT,
            author TEXT,
            collected_at TEXT,
            cluster_id INTEGER,
            people TEXT,
            organizations TEXT,
            locations TEXT,
            FOREIGN KEY(cluster_id) REFERENCES events(id)
        )
    """)
    
    conn.commit()
    conn.close()

def save_articles_to_db(df: pd.DataFrame):
    """Upsert articles into the database, avoiding title duplicates."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure columns exist and fillna
    columns = ["source", "title", "summary", "link", "published", "author", "collected_at"]
    df_db = df.reindex(columns=columns).fillna("")
    
    for _, row in df_db.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO articles (source, title, summary, link, published, author, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(row["source"]),
            str(row["title"]),
            str(row["summary"]),
            str(row["link"]),
            str(row["published"]),
            str(row["author"]),
            str(row["collected_at"])
        ))
        
    conn.commit()
    conn.close()
