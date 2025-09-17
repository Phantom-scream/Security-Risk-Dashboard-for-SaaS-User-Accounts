# Security Risk Dashboard

A modern, interactive dashboard and API for monitoring user risk levels across multiple systems.  
Built with Streamlit, FastAPI, Plotly, Pandas, and SQLite. Includes automated ingestion, validation checks, regression comparisons, tests, and Docker.

---

## What is this project?

Security Risk Dashboard helps security/IT teams:
- Identify users with weak security profiles (e.g., weak passwords, risky countries, public email domains).
- Monitor risk trends over time across systems (HR, Cloud Storage).
- Export and share risk reports for compliance or further analysis.
- Validate data quality and detect anomalous score changes.
- Compare latest runs to prior runs (regression-style analysis).
- Access data via a lightweight REST API.

---

## Technologies Used

- Python 3.8+
- Streamlit (dashboard)
- FastAPI + Uvicorn (REST API)
- Plotly (charts)
- Pandas (analysis)
- SQLite (storage)
- Requests + retry logic (ingestion)
- Pytest (tests)
- Docker + docker-compose (portability)
- GitHub Actions (CI + scheduled ingestion)

---

## Features

- User Risk Analysis:
  - Rule-based scoring (password length/common, email domain, registration age, country).
- Multi-System Support:
  - HR and Cloud Storage (via randomuser.me).
- Interactive Dashboard:
  - Filters, risk breakdown, trend charts, CSV export, Light/Dark themes.
- Anomaly Detection:
  - Flags strong outliers in latest user risk scores.
- Data Validation:
  - Column checks, enums, score ranges, email format.
- Regression Comparison:
  - Compare the last two run_ids and show deltas per system/risk level.
- Reporting:
  - Timestamped CSV/JSON per system (reports/).
- Alerting:
  - Console alerts for high-risk thresholds.
- REST API:
  - /health, /risks, /risks/{user_id}, /stats/summary (+ Swagger at /docs).
- CI + Scheduled Ingestion:
  - Tests on PR/push; nightly ingestion via GitHub Actions.
- Docker/Compose:
  - Run API and dashboard on Linux/macOS/Windows.

---

## Project Structure

```
security_risk_dashboard/
│
├── src/
│   ├── fetchers/
│   │   ├── http.py                # Session with retries/backoff
│   │   ├── hr_system.py           # Fetch users from HR (randomuser.me)
│   │   └── cloud_storage.py       # Simulated Cloud Storage users
│   │
│   ├── api.py                     # FastAPI service (health, risks, summary)
│   ├── anomaly_detection.py       # Z-score-based anomaly detection
│   ├── database.py                # SQLite schema + insert (with run_id)
│   ├── regression.py              # Compare last two runs
│   ├── report_generator.py        # Export CSV/JSON reports
│   ├── risk_engine.py             # Risk scoring rules
│   ├── validation.py              # Data validation helpers
│   └── main.py                    # Orchestrates ingestion → scoring → DB/reporting
│
├── dashboard/
│   └── app.py                     # Streamlit dashboard
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_anomaly_detection.py
│   └── test_risk_engine.py
│
├── postman/
│   └── SecurityRiskDashboard.postman_collection.json
│
├── .github/workflows/ci.yml       # CI + nightly ingestion
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── data/                          # risk_history.db (auto-created)
├── reports/                       # timestamped CSV/JSON (auto-created)
└── README.md
```

---

## Quick Start (Local)

1) Create venv and install deps
```bash
cd security_risk_dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Ingest data (run twice to enable regression comparison)
```bash
FETCH_COUNT=120 python src/main.py
sleep 2
FETCH_COUNT=120 python src/main.py
```

3) Launch the dashboard
```bash
streamlit run dashboard/app.py
# open http://localhost:8501
```

4) Run the API
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
# open http://localhost:8000/docs
```

---

## API Endpoints

- GET /health
- GET /risks
  - Query params: system, risk_level in {LOW, MEDIUM, HIGH}, name (substring), limit
  - Example: http://localhost:8000/risks?risk_level=HIGH&limit=50
- GET /risks/{user_id}
- GET /stats/summary
- Swagger UI: http://localhost:8000/docs

Curl examples:
```bash
curl http://localhost:8000/health
curl "http://localhost:8000/risks?risk_level=HIGH&limit=5"
curl http://localhost:8000/stats/summary
```

---

## Dashboard Highlights

- Filters by system, risk level, and user.
- Risk level breakdown bar chart.
- Score trend line chart.
- Anomaly table when outliers are detected.
- Data validation panel (issues or all-pass).
- Regression panel comparing last two run_ids.

Tip: If you see no data, run `python src/main.py` first.

---

## Testing

```bash
pytest -q
```

Tests cover:
- Risk engine classification
- Anomaly detection outliers
- Validation rules
- API endpoints (with an in-memory seeded DB)

---

## Docker

Build and run (single container: dashboard default CMD):
```bash
docker build -t srd .
docker run --rm -p 8501:8501 -p 8000:8000 srd
# Dashboard: http://localhost:8501
# API docs: http://localhost:8000/docs
```

docker-compose (API + dashboard services):
```bash
docker-compose up --build
# Dashboard: http://localhost:8501
# API docs: http://localhost:8000/docs
```

If a port is busy:
```bash
docker run --rm -p 8502:8501 srd
# then open http://localhost:8502
```

---

## CI and Scheduled Ingestion

GitHub Actions workflow:
- Runs pytest on push/PR (ubuntu-latest).
- Nightly ingestion job at 02:00 UTC:
  - Executes `python src/main.py` with `FETCH_COUNT=120`
  - Uploads CSV reports as artifacts.

Workflow file: `.github/workflows/ci.yml`

---

## Postman Collection

Import `postman/SecurityRiskDashboard.postman_collection.json` and run:
- Health
- List Risks
- User Risks
- Summary

Target base URL: `http://localhost:8000`

---

## Configuration

- FETCH_COUNT (env): number of users to fetch per system.
  - Example: `FETCH_COUNT=120 python src/main.py`

---

## Troubleshooting

- Opening 0.0.0.0 shows blank:
  - Use http://localhost:8501 (dashboard) and http://localhost:8000 (API).
- No data in dashboard/API:
  - Run `python src/main.py` at least once (twice for regression).
- macOS quick open:
  - `open http://localhost:8501` or `open http://localhost:8000/docs`
- Tests can’t import src:
  - Ensure `tests/conftest.py` adds project root to `sys.path`.

---

## License

MIT
