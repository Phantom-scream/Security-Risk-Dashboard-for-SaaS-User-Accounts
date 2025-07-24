import pandas as pd

def detect_anomalies(df, z_thresh=2.0):
    """
    Flags users whose latest risk score is a strong outlier compared to their own history.
    Returns a DataFrame of anomalies.
    """
    anomalies = []
    for user_id, group in df.groupby("user_id"):
        if len(group) < 3:
            continue  # Not enough history
        scores = group.sort_values("timestamp")["score"]
        mean = scores[:-1].mean()
        std = scores[:-1].std()
        latest = scores.iloc[-1]
        if std > 0 and abs(latest - mean) > z_thresh * std:
            anomalies.append(group.iloc[-1])
    return pd.DataFrame(anomalies)