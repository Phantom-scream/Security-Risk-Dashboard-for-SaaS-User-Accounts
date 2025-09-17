from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import sqlite3
import pandas as pd

DB_PATH = "data/risk_history.db"
app = FastAPI(title="Security Risk Dashboard API")

def get_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM risk_log", conn)
    conn.close()
    return df

@app.get("/health")
def health():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/risks")
def list_risks(
    system: Optional[str] = None,
    risk_level: Optional[str] = Query(None, pattern="^(LOW|MEDIUM|HIGH)$"),
    name: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
):
    df = get_df()
    if system:
        df = df[df["system"] == system]
    if risk_level:
        df = df[df["risk_level"] == risk_level]
    if name:
        df = df[df["name"].str.contains(name, case=False, na=False)]
    out = df.sort_values("timestamp", ascending=False).head(limit)
    return out.to_dict(orient="records")

@app.get("/risks/{user_id}")
def get_risk(user_id: str):
    df = get_df()
    rows = df[df["user_id"] == user_id]
    if rows.empty:
        raise HTTPException(status_code=404, detail="User not found")
    return rows.sort_values("timestamp").to_dict(orient="records")

@app.get("/stats/summary")
def stats_summary():
    df = get_df()
    summary = (
        df.groupby(["system","risk_level"])
          .size()
          .rename("count")
          .reset_index()
          .to_dict(orient="records")
    )
    return {"summary": summary, "total": int(len(df))}