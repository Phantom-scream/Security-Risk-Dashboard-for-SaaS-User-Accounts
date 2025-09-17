import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from anomaly_detection import detect_anomalies
from validation import validate_dataframe
from regression import compare_latest_runs

DB_PATH = "data/risk_history.db"

st.set_page_config(page_title="🔐 Security Risk Dashboard", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f4f4f8;
        }
        h1, h2, h3 {
            color: #1f3c88;
        }
        .stDataFrame {
            background-color: white;
            border-radius: 8px;
            padding: 1em;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/fluency/96/lock.png", width=64)
st.sidebar.markdown("""
**Security Risk Dashboard**
""")

def inject_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
                body, .block-container, .stApp {
                    background-color: #181a20 !important;
                    color: #f8f8ff !important;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #f8f8ff !important;
                }
                .stDataFrame, .stTable, .stMarkdown, .stTextInput, .stSelectbox, .stMultiSelect, .stButton, .stDownloadButton, .stExpander, .stSubheader {
                    background-color: #23272f !important;
                    color: #f8f8ff !important;
                    border-radius: 8px;
                }
                .stSidebar, .stSidebarContent {
                    background-color: #23272f !important;
                    color: #f8f8ff !important;
                }
                .stSidebar .stTextInput, .stSidebar .stSelectbox, .stSidebar .stMultiSelect, .stSidebar .stButton, .stSidebar .stDownloadButton, .stSidebar .stRadio {
                    background-color: #23272f !important;
                    color: #f8f8ff !important;
                }
                .stSidebar label, .stSidebar .stRadio label, .stSidebar .stSelectbox label, .stSidebar .stMultiSelect label, .stSidebar .stTextInput label {
                    color: #f8f8ff !important;
                }
                .stRadio label, .stRadio div[role="radiogroup"] > div {
                    color: #f8f8ff !important;
                }
                /* Bright Download Button */
                .stDownloadButton button {
                    background-color: #00e0ff !important;
                    color: #23272f !important;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #00e0ff !important;
                }
                .stDownloadButton button:hover {
                    background-color: #00bfff !important;
                    color: #fff !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body, .block-container, .stApp {
                    background-color: #f4f4f8 !important;
                    color: #23272f !important;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #1f3c88 !important;
                }
                .stDataFrame, .stTable, .stMarkdown, .stTextInput, .stSelectbox, .stMultiSelect, .stButton, .stDownloadButton, .stExpander, .stSubheader {
                    background-color: #fff !important;
                    color: #23272f !important;
                    border-radius: 8px;
                }
                .stSidebar, .stSidebarContent {
                    background-color: #e9ecf5 !important;
                    color: #23272f !important;
                }
                .stSidebar .stTextInput, .stSidebar .stSelectbox, .stSidebar .stMultiSelect, .stSidebar .stButton, .stSidebar .stDownloadButton, .stSidebar .stRadio {
                    background-color: #e9ecf5 !important;
                    color: #23272f !important;
                }
                .stSidebar label, .stSidebar .stRadio label, .stSidebar .stSelectbox label, .stSidebar .stMultiSelect label, .stSidebar .stTextInput label {
                    color: #23272f !important;
                }
                .stRadio label, .stRadio div[role="radiogroup"] > div {
                    color: #23272f !important;
                }
                /* Bright Download Button */
                .stDownloadButton button {
                    background-color: #00bfff !important;
                    color: #fff !important;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 2px solid #00bfff !important;
                }
                .stDownloadButton button:hover {
                    background-color: #0099cc !important;
                    color: #fff !important;
                }
            </style>
        """, unsafe_allow_html=True)

theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
inject_theme(theme)

st.title(" Security Risk Dashboard")

@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM risk_log ORDER BY timestamp DESC", conn)
        conn.close()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.info("No data available. Run `python src/main.py` to populate the database.")
    st.stop()

st.sidebar.header("📂 Filters")

system_filter = st.sidebar.selectbox("System", ["All"] + sorted(df["system"].unique().tolist()))

risk_filter = st.sidebar.multiselect("Risk Level", options=["LOW", "MEDIUM", "HIGH"], default=["LOW", "MEDIUM", "HIGH"])

user_filter = st.sidebar.selectbox("🔍 Focus on User (optional)", ["None"] + sorted(df["name"].unique()))

filtered_df = df.copy()

if system_filter != "All":
    filtered_df = filtered_df[filtered_df["system"] == system_filter]

if risk_filter:
    filtered_df = filtered_df[filtered_df["risk_level"].isin(risk_filter)]

if user_filter != "None":
    filtered_df = filtered_df[filtered_df["name"] == user_filter]

st.subheader(" Filtered Risk Logs")


def highlight_risk(row):

    color = ""
    text = ""
    if row["risk_level"] == "HIGH":
        color = "background-color: #d90429; color: #fff;"  
    elif row["risk_level"] == "MEDIUM":
        color = "background-color: #ffb400; color: #23272f;" 
    elif row["risk_level"] == "LOW":
        color = "background-color: #43aa8b; color: #fff;" 
    return [color if col == "risk_level" else "" for col in row.index]



styled_df = filtered_df.style.apply(highlight_risk, axis=1)
st.dataframe(styled_df, use_container_width=True)

with st.expander("Download filtered risks as CSV"):
    st.download_button("⬇ Download CSV", filtered_df.to_csv(index=False), "filtered_risks.csv", "text/csv", help="Download the filtered risk logs for further analysis.")

with st.expander("See risk level breakdown"):
    st.subheader(" Risk Level Breakdown")
    filtered_df["risk_level"] = filtered_df["risk_level"].str.upper().str.strip()
    risk_counts = filtered_df["risk_level"].value_counts().reindex(["HIGH", "MEDIUM", "LOW"]).fillna(0)
    st.bar_chart(risk_counts)

with st.expander("View risk score trends over time"):
    st.subheader(" Risk Score Trend Over Time")
    if not filtered_df.empty:
        fig = px.line(
            filtered_df.sort_values("timestamp"),
            x="timestamp",
            y="score",
            color="risk_level",
            title=f"Risk Score Trend ({user_filter if user_filter != 'None' else 'All Users'})",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

if user_filter != "None":
    with st.expander(f"Full Risk History for {user_filter}"):
        st.dataframe(filtered_df.sort_values("timestamp"), use_container_width=True)

anomalies_df = detect_anomalies(filtered_df)
if not anomalies_df.empty:
    st.subheader(" Anomalous Risk Changes Detected")
    st.dataframe(anomalies_df, use_container_width=True)
else:
    st.info("No anomalies detected in the selected data.")

with st.expander("Data validation checks"):
    issues = validate_dataframe(filtered_df)
    if not issues:
        st.success("All validation checks passed.")
    else:
        for i in issues:
            st.warning(i)

with st.expander("Regression comparison (last two runs)"):
    summary, runs = compare_latest_runs(df)
    prev_run, curr_run = runs
    if summary.empty:
        st.info("Not enough runs to compare. Execute main.py twice to generate at least two run_ids.")
    else:
        st.write(f"Comparing runs: previous={prev_run}, current={curr_run}")
        st.dataframe(summary, use_container_width=True)