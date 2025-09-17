import os
import sqlite3
import pandas as pd
from fastapi.testclient import TestClient
from src.api import app, DB_PATH

def setup_module():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS risk_log")
    conn.execute("""
        CREATE TABLE risk_log (
            user_id TEXT, name TEXT, email TEXT, score INTEGER,
            risk_level TEXT, system TEXT, run_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    df = pd.DataFrame([
        {"user_id":"u1","name":"Alice","email":"a@ex.com","score":7,"risk_level":"MEDIUM","system":"HRSystem","run_id":"1"},
        {"user_id":"u2","name":"Bob","email":"b@ex.com","score":10,"risk_level":"HIGH","system":"CloudStorage","run_id":"1"},
    ])
    df.to_sql("risk_log", conn, if_exists="append", index=False)
    conn.close()

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_list_risks():
    r = client.get("/risks?risk_level=HIGH")
    assert r.status_code == 200
    data = r.json()
    assert any(x["risk_level"] == "HIGH" for x in data)

def test_get_risk_not_found():
    r = client.get("/risks/missing")
    assert r.status_code == 404