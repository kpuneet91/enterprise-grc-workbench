
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise GRC Workbench",
    page_icon="🛡️",
    layout="wide",
)

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.title("Enterprise GRC & IT Risk Workbench")
st.caption(
    "Executive Overview | Cybersecurity Governance, Risk and Compliance"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"

risks = pd.read_csv(DATA_DIR / "risk_register.csv")
controls = pd.read_csv(DATA_DIR / "control_library.csv")
tests = pd.read_csv(DATA_DIR / "control_tests.csv")

# --------------------------------------------------
# RISK SCORING
# --------------------------------------------------
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

# --------------------------------------------------
# EXECUTIVE METRICS
# --------------------------------------------------
total_risks = len(risks)
critical_risks = int((risks["risk_level"] == "Critical").sum())
high_risks = int((risks["risk_level"] == "High").sum())
total_controls = len(controls)

test_results = tests["result"].astype(str).str.strip().str.lower()
failed_tests = int((test_results == "fail").sum())
passed_tests = int((test_results == "pass").sum())
total_tests = passed_tests + failed_tests

pass_rate = (
    passed_tests / total_tests * 100
    if total_tests > 0
    else 0
)

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------
st.subheader("Executive Summary")
st.caption(
    "A consolidated view of enterprise risk exposure and control assurance."
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Risks", total_risks)
col2.metric("Critical Risks", critical_risks)
col3.metric("High Risks", high_risks)
col4.metric("Controls in Library", total_controls)
col5.metric("Control Pass Rate", f"{pass_rate:.1f}%")

st.divider()

# --------------------------------------------------
# RISK AND CONTROL CHARTS
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Risk Profile")

    risk_summary = (
        risks["risk_level"]
        .value_counts()
        .reindex(
            ["Critical", "High", "Medium", "Low"],
            fill_value=0,
        )
        .rename_axis("Risk Level")
        .reset_index(name="Count")
    )

    st.bar_chart(
        risk_summary.set_index("Risk Level"),
        x_label="Risk Level",
        y_label="Number of Risks",
        color="#0F766E",
    )

with right:
    st.subheader("Control Testing Snapshot")

    test_summary = (
        tests["result"]
        .astype(str)
        .str.strip()
        .str.title()
        .value_counts()
        .reindex(["Pass", "Fail"], fill_value=0)
        .rename_axis("Test Result")
        .reset_index(name="Count")
    )

    st.bar_chart(
        test_summary.set_index("Test Result"),
        x_label="Test Result",
        y_label="Number of Tests",
        color="#0F766E",
    )

# --------------------------------------------------
# WORKBENCH NAVIGATION
# --------------------------------------------------
st.divider()
st.subheader("Explore the Workbench")

st.write(
    "Use the page navigation in the sidebar to explore the detailed "
    "risk register, control library, control testing results, "
    "and audit findings."
)

# --------------------------------------------------
# PORTFOLIO DISCLAIMER
# --------------------------------------------------
st.info(
    "Portfolio note: This workbench uses fictional sample data for "
    "demonstration and learning. It does not contain real company or "
    "military information."
)
