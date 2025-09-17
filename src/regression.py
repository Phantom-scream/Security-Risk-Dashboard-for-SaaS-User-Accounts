import pandas as pd

def compare_latest_runs(df: pd.DataFrame):
    if "run_id" not in df.columns or df["run_id"].dropna().nunique() < 2:
        return pd.DataFrame(), (None, None)

    latest_runs = sorted(df["run_id"].dropna().unique())[-2:]
    prev_run, curr_run = latest_runs[0], latest_runs[1]

    def summarize(d):
        return (
            d.groupby(["system","risk_level"])
             .size()
             .rename("count")
             .reset_index()
        )

    prev = summarize(df[df["run_id"] == prev_run])
    curr = summarize(df[df["run_id"] == curr_run])

    merged = prev.merge(curr, on=["system","risk_level"], how="outer", suffixes=("_prev","_curr")).fillna(0)
    merged["delta"] = merged["count_curr"] - merged["count_prev"]
    return merged.sort_values(["system","risk_level"]), (prev_run, curr_run)