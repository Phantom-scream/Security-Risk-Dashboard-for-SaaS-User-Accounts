import pandas as pd
from src.validation import validate_dataframe

def test_validate_dataframe_flags_invalid_risk():
    df = pd.DataFrame([{"user_id":"1","name":"n","email":"a@b","score":1,"risk_level":"BAD","system":"HR","timestamp":"2024-01-01"}])
    issues = validate_dataframe(df)
    assert any("Invalid risk levels" in s for s in issues)