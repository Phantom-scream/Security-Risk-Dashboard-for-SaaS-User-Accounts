import sqlite3
import os

DB_PATH = "data/risk_history.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_log (
            user_id TEXT,
            name TEXT,
            email TEXT,
            score INTEGER,
            risk_level TEXT,
            system TEXT,
            run_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        cursor.execute("ALTER TABLE risk_log ADD COLUMN run_id TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def save_risks_to_db(risks, system_name, run_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for r in risks:
        cursor.execute("""
            INSERT INTO risk_log (user_id, name, email, score, risk_level, system, run_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"],
            r["name"],
            r["email"],
            r["score"],
            r["risk_level"],
            system_name,
            run_id
        ))
    conn.commit()
    conn.close()