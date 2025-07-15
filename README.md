# Security Risk Dashboard

A modern, interactive dashboard for monitoring user risk levels across multiple systems.  
Built with Streamlit, Plotly, Pandas, and SQLite, this project helps organizations visualize, filter, and report on user security risks.

---

## What is this project?

**Security Risk Dashboard** is a tool designed to help security teams and IT administrators:
- **Identify users with weak security profiles** (e.g., weak passwords, risky countries, public email domains).
- **Monitor risk trends over time** across different systems (HR, Cloud Storage, etc.).
- **Export and share risk reports** for compliance or further analysis.
- **Quickly respond to high-risk situations** with alerting and filtering.

---

## Technologies Used

- **Python 3.8+**
- **Streamlit**: For building the interactive dashboard UI.
- **Plotly**: For rich, interactive charts and visualizations.
- **Pandas**: For data manipulation and analysis.
- **SQLite**: For persistent storage of risk logs.
- **Requests**: For fetching user data from external APIs.
- **python-dateutil**: For robust date parsing.

---

## Features

- **User Risk Analysis:**  
  Calculates risk scores for users based on password strength, email domain, registration age, and country.
- **Multi-System Support:**  
  Integrates with HR and Cloud Storage systems (simulated via [randomuser.me](https://randomuser.me)).
- **Interactive Dashboard:**  
  Filter by system, risk level, and user; switch between dark/light themes.
- **Visualizations:**  
  View risk breakdowns, score trends, and detailed logs.
- **Reporting:**  
  Export filtered risk logs as CSV.
- **Alerting:**  
  Console alerts for high-risk user thresholds.
- **Persistent Storage:**  
  All risk logs are stored in a local SQLite database.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the risk analysis and database population

```bash
python src/main.py
```

### 3. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

---

## Project Structure

```
security_risk_dashboard/
│
├── src/
│   ├── fetchers/
│   │   ├── hr_system.py            # Fetches users from HR (randomuser.me)
│   │   └── cloud_storage.py        # Simulated Cloud Storage users
│   │
│   ├── risk_engine.py              # Calculates risk score and reasons
│   ├── report_generator.py         # Exports risk report to JSON/CSV (per system)
│   ├── alert_system.py             # Console-based alerts for high risk
│   ├── database.py                 # SQLite risk log handling
│   └── main.py                     # Main script to orchestrate the pipeline
│
├── dashboard/
│   └── app.py                      # Streamlit web dashboard for visualizing risk logs
│
├── data/
│   └── risk_history.db             # SQLite database (auto-created if missing)
│
├── reports/
│   └── *.csv                       # Risk reports (timestamped + system-specific)
│   └── *.json
│
├── requirements.txt                # All project dependencies
├── README.md                       # Project overview, setup guide, usage
```

---

## How It Works

1. **Data Fetching:**  
   - `fetchers/hr_system.py` and `fetchers/cloud_storage.py` pull user data from randomuser.me.
2. **Risk Analysis:**  
   - `risk_engine.py` scores users based on security criteria.
3. **Reporting & Storage:**  
   - `report_generator.py` saves reports; `database.py` persists logs in SQLite.
4. **Alerting:**  
   - `alert_system.py` prints alerts if high-risk users exceed a threshold.
5. **Dashboard:**  
   - `dashboard/app.py` provides an interactive UI for exploring and exporting risk data.

---

## Customization

- **Add new systems:**  
  Extend the `fetchers/` directory and update `main.py`.
- **Tune risk logic:**  
  Edit scoring rules in `risk_engine.py`.
- **Change alert threshold:**  
  Adjust the `threshold` parameter in `alert_system.py`.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for Python packages.

---

## License

MIT
