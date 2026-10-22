import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Risk Register", layout="wide")

st.title("Enterprise Risk Register")
st.caption("Identify, score, filter and review cybersecurity risks.")

DATA_DIR = Path(__file__).parent.parent / "data"
risks = pd.read_csv(DATA_DIR / "risk_register.csv")

risks["risk_score"] = risks["likelihood"] * risks["impact"]

def classify_risk(score):
    if score >= 20:
        return "Critical"
    elif score >= 12:
        return "High"
    elif score >= 6:
        return "Medium"
    return "Low"

risks["risk_level"] = risks["risk_score"].apply(classify_risk)

col1, col2, col3 = st.columns(3)
col1.metric("Total Risks", len(risks))
col2.metric("Critical Risks", int((risks["risk_level"] == "Critical").sum()))
col3.metric("High Risks", int((risks["risk_level"] == "High").sum()))

st.divider()

selected_levels = st.multiselect(
    "Filter by risk level",
    options=["Critical", "High", "Medium", "Low"],
    default=["Critical", "High", "Medium", "Low"]
)

filtered_risks = risks[risks["risk_level"].isin(selected_levels)]

st.subheader("Risk Details")
st.dataframe(filtered_risks, use_container_width=True, hide_index=True)

csv_data = filtered_risks.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered risk register (CSV)",
    data=csv_data,
    file_name="risk_register_export.csv",
    mime="text/csv"
)

st.info(
    "Risk scoring uses likelihood × impact on a 1–5 scale. "
    "Thresholds are illustrative project rules, not a universal standard."
)
