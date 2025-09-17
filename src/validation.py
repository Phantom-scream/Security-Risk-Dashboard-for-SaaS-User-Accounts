import sqlite3
import pandas as pd

DB_PATH = "data/risk_history.db"
ALLOWED_RISK = {"LOW", "MEDIUM", "HIGH"}

def validate_dataframe(df: pd.DataFrame):
    issues = []
    required_cols = {"user_id","name","email","score","risk_level","system","timestamp"}
    missing = required_cols - set(df.columns)
    if missing:
        issues.append(f"Missing columns: {sorted(missing)}")
    if "risk_level" in df.columns:
        bad_levels = sorted(set(df["risk_level"].dropna()) - ALLOWED_RISK)
        if bad_levels:
            issues.append(f"Invalid risk levels: {bad_levels}")
    if "score" in df.columns:
        bad_scores = df[~df["score"].between(0, 1000)]
        if not bad_scores.empty:
            issues.append(f"Out-of-range scores rows: {len(bad_scores)}")
    if "email" in df.columns:
        bad_email = df[~df["email"].astype(str).str.contains("@")]
        if not bad_email.empty:
            issues.append(f"Invalid emails rows: {len(bad_email)}")
    return issues

def validate_db(db_path: str = DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM risk_log", conn)
        conn.close()
    except Exception as e:
        return ["DB read failed: " + str(e)], pd.DataFrame()
    return validate_dataframe(df), df