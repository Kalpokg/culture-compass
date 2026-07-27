# 🎭 Culture Compass

A modular platform for aggregating, processing, searching, and recommending cultural events.

Culture Compass collects event data from multiple providers, transforms it into a unified data model, stores it in PostgreSQL, and provides search and content-based recommendations through an interactive Streamlit application.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![CI](https://img.shields.io/github/actions/workflow/status/Kalpokg/culture-compass/ci.yml)

---

## Live Demo

https://culture-compass-production.up.railway.app

---

# Overview

Event information is spread across different providers, each with its own API and data format.

Culture Compass collects events from multiple sources, converts them into a common format, stores them in a PostgreSQL database, and allows users to search and discover similar events through a simple web interface.

The project demonstrates:

- API integration
- ETL pipelines
- Database design
- Repository pattern
- Search
- Content-based recommendation
- Docker
- Cloud deployment
- Continuous Integration

---

# Features

## Data Ingestion

- Multi-source event collection
- Ticketmaster integration
- Eventim integration
- Provider-specific fetchers and parsers
- Canonical event model
- Country normalisation
- Reverse geocoding
- Venue normalisation

---

## Data Platform

- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- Repository pattern
- Modular ETL architecture

Current pipeline:

```text
Fetch
   ↓
Parse
   ↓
Load
```

The current pipeline already performs validation and data normalisation during parsing. The architecture is designed so these responsibilities can later be separated into dedicated ETL modules.

---

## Search

- Search by event name
- Filter by city
- Filter by country
- Filter by genre
- Filter by provider
- Filter by date

---

## Recommendation Engine

Culture Compass includes a content-based recommendation engine built with scikit-learn.

The recommender uses TF-IDF vectorisation and cosine similarity to recommend events with similar content.

Current features:

- Similar event recommendations
- Alternative performances of the same event

---

## Application

- Interactive Streamlit interface
- Docker support
- Railway deployment
- GitHub Actions Continuous Integration

---

# Architecture

```text
                  External APIs
             ┌─────────┬─────────┐
             │         │
        Ticketmaster  Eventim
             │         │
             └────┬────┘
                  │
                  ▼
             ETL Pipeline
          Fetch → Parse → Load
                  │
                  ▼
       Canonical Event Model
                  │
                  ▼
             PostgreSQL
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Search Engine     Recommendation Engine
        │                   │
        └─────────┬─────────┘
                  ▼
      Streamlit Web Application
                  │
                  ▼
               Railway
```

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.13 |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Data Processing | Pandas |
| Machine Learning | scikit-learn |
| Deployment | Railway |
| Containerisation | Docker |
| APIs | Ticketmaster, Eventim |
| CI/CD | GitHub Actions |

---

# Project Structure

```text
culture-compass/
│
├── app/                         # Streamlit application
├── tests/                       # Unit tests
├── notebooks/                   # Experiments
├── scripts/                     # Development utilities
├── data/
│
├── culture_compass/
│   ├── api/
│   ├── config/
│   ├── database/
│   ├── dto/
│   ├── etl/
│   │   ├── fetchers/
│   │   └── parsers/
│   ├── recommender/
│   ├── search/
│   ├── services/
│   ├── features/
│   └── utils/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── run_app.py
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Kalpokg/culture-compass.git
cd culture-compass
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

---

# Running the Application

Create a `.env` file containing your database configuration and API credentials.

Run the application

```bash
python run_app.py
```

or

```bash
streamlit run run_app.py
```

---

# Roadmap

Implemented

- [x] Ticketmaster integration
- [x] Eventim integration
- [x] Canonical event model
- [x] PostgreSQL backend
- [x] Search engine
- [x] Content-based recommendation engine
- [x] Docker support
- [x] Railway deployment
- [x] GitHub Actions CI

Planned

- [ ] Refactor validation and normalisation into dedicated ETL modules
- [ ] Advanced cross-provider event deduplication
- [ ] Eventbrite integration
- [ ] Interactive maps
- [ ] User accounts
- [ ] Personalised recommendations
- [ ] Hybrid recommendation models
- [ ] Embedding-based semantic search
- [ ] Additional event providers

---

# License

This project is licensed under the MIT License.