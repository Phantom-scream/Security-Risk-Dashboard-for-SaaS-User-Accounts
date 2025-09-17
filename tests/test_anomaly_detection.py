import pandas as pd
from src.anomaly_detection import detect_anomalies

def test_detect_anomalies_flags_outlier():
    df = pd.DataFrame([
        {"user_id":"u","timestamp":"2024-01-01","score":10,"risk_level":"LOW","name":"A","system":"HR"},
        {"user_id":"u","timestamp":"2024-02-01","score":12,"risk_level":"LOW","name":"A","system":"HR"},
        {"user_id":"u","timestamp":"2024-03-01","score":40,"risk_level":"HIGH","name":"A","system":"HR"},
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    out = detect_anomalies(df)
    assert not out.empty