# 🧠 AI News Intelligence Platform

An end-to-end AI-powered news intelligence platform that **collects, clusters, and analyzes** breaking news from 20+ sources in real time. Uses NLP techniques including sentence embeddings, agglomerative clustering, named entity recognition, and keyword extraction to surface emerging events from raw news feeds.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface&logoColor=black)

---

## ✨ Features

- **20+ RSS Feed Sources** — BBC, Reuters, The Guardian, Al Jazeera, NYT, TechCrunch, Wired, and more
- **Automated Pipeline** — One command to collect → embed → cluster → extract entities → generate titles
- **Sentence Embeddings** — `all-MiniLM-L6-v2` via Sentence-Transformers
- **Agglomerative Clustering** — Groups related articles into events using cosine similarity
- **Named Entity Recognition** — Extracts people, organizations, and locations using `bert-base-NER`
- **Event Title Generation** — KeyBERT-based keyword extraction for cluster labeling
- **REST API** — FastAPI backend serving events, search, statistics, and timeline endpoints
- **React Dashboard** — Interactive frontend with event cards, entity views, search, and timeline

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA COLLECTION                          │
│  RSS Feeds (20+ sources)  ·  NewsAPI (optional, needs API key)  │
└────────────────────────────────┬────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PREPROCESSING                             │
│         Merge · Deduplicate · Normalize → SQLite DB             │
└────────────────────────────────┬────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                       NLP PIPELINE                              │
│  Embeddings → Clustering → NER → Event Title Generation         │
└────────────────────────────────┬────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                         SERVING                                 │
│            FastAPI REST API  ←→  React Dashboard                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-News-Intelligence-Platform.git
cd AI-News-Intelligence-Platform
```

### 2. Set Up the Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Pipeline

```bash
# From the project root directory
python -m backend.pipeline
```

This single command will:
1. Collect articles from 20+ RSS feeds
2. Merge and deduplicate into SQLite
3. Generate sentence embeddings
4. Cluster related articles into events
5. Extract named entities (people, orgs, locations)
6. Generate event titles with keyword extraction

> **Note:** The first run downloads ~500MB of ML models (Sentence-Transformers, BERT-NER, KeyBERT). Subsequent runs use the cached models.

#### Pipeline Flags

```bash
python -m backend.pipeline --skip-collect   # Re-process existing data without re-fetching
python -m backend.pipeline --skip-ml        # Collect articles only, skip ML pipeline
```

### 4. Start the API

```bash
uvicorn backend.api:app --reload
```

The API will be available at `http://localhost:8000`. Key endpoints:
- `GET /api/events` — All clustered events
- `GET /api/events/search?q=climate` — Search events
- `GET /api/events/{id}` — Single event detail
- `GET /api/statistics` — Dashboard statistics
- `GET /api/timeline` — Timeline view

### 5. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to view the dashboard.

---

## 🔑 Optional: NewsAPI Integration

For additional article coverage, you can add a [NewsAPI](https://newsapi.org/) key:

```bash
# Create backend/.env
echo API_KEY=your_newsapi_key_here > backend/.env
```

The pipeline works perfectly without it — it will use RSS feeds only.

---

## 📁 Project Structure

```
AI-News-Intelligence-Platform/
├── backend/
│   ├── pipeline.py                # ← Main entry point — runs everything
│   ├── api.py                     # FastAPI REST API
│   ├── collectors/
│   │   ├── rss_collector.py       # 20+ RSS feed collector
│   │   └── newsapi_collector.py   # NewsAPI collector (optional)
│   ├── preprocessing/
│   │   └── merge_dataset.py       # Merge & deduplicate into SQLite
│   ├── embeddings/
│   │   └── generate_embeddings.py # Sentence-Transformer embeddings
│   ├── clustering/
│   │   └── agglomerative_clustering.py  # Cosine similarity clustering
│   ├── ner/
│   │   └── ner.py                 # Named Entity Recognition
│   ├── summarization/
│   │   ├── event_summarizer.py    # BART summarization
│   │   └── generate_event_titles.py # KeyBERT event labeling
│   ├── utils/
│   │   ├── db.py                  # SQLite database utilities
│   │   ├── csv_utils.py           # CSV reading helpers
│   │   └── logger.py              # Logging configuration
│   └── requirements.txt
├── frontend/                      # React + Vite dashboard
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Home, Event, About pages
│   │   ├── services/              # API client
│   │   └── context/               # React context
│   └── package.json
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Collection** | `feedparser`, `requests`, NewsAPI |
| **NLP** | `sentence-transformers`, `scikit-learn`, `transformers`, `keybert` |
| **Database** | SQLite via `sqlite3` |
| **API** | FastAPI, Uvicorn |
| **Frontend** | React 19, Vite 8, Framer Motion, React Router |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).