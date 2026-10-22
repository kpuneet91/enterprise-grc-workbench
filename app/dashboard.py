import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "app"))

from risk_engine import load_risks


st.set_page_config(
    page_title="Enterprise GRC Workbench",
    page_icon="🛡️",
    layout="wide",
)

st.title("Enterprise GRC & IT Risk Workbench")
st.caption("Independent portfolio project | Fictional company data")

risks = load_risks()
df = pd.DataFrame(risks)

st.header("Cybersecurity Risk Overview")

critical_count = int((df["risk_level"] == "Critical").sum())
high_count = int((df["risk_level"] == "High").sum())
open_count = int((df["status"] == "Open").sum())

col1, col2, col3 = st.columns(3)
col1.metric("Total Risks", len(df))
col2.metric("Critical Risks", critical_count)
col3.metric("Open Risks", open_count)

st.subheader("Risk Severity Distribution")

severity_order = ["Critical", "High", "Medium", "Low"]
severity_counts = (
    df["risk_level"]
    .value_counts()
    .reindex(severity_order, fill_value=0)
    .rename_axis("Severity")
    .reset_index(name="Count")
)

fig = px.bar(
    severity_counts,
    x="Severity",
    y="Count",
    title="Number of Risks by Severity",
    category_orders={"Severity": severity_order},
    text="Count",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Risk Register")

selected_levels = st.multiselect(
    "Filter by severity",
    options=severity_order,
    default=severity_order,
)

filtered_df = df[df["risk_level"].isin(selected_levels)]

display_columns = [
    "risk_id",
    "risk_title",
    "category",
    "risk_score",
    "risk_level",
    "risk_owner",
    "treatment",
    "status",
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered risk register (CSV)",
    data=csv_data,
    file_name="filtered_risk_register.csv",
    mime="text/csv",
)

st.info(
    "Risk thresholds are illustrative portfolio assumptions. "
    "This dashboard uses synthetic data and is not a production GRC system."
)

st.divider()
st.header("Security Control Library")

CONTROL_FILE = PROJECT_ROOT / "data" / "control_library.csv"

controls_df = pd.read_csv(CONTROL_FILE)

st.metric("Documented Controls", len(controls_df))

selected_domain = st.selectbox(
    "Filter by control domain",
    ["All"] + sorted(controls_df["control_domain"].unique().tolist()),
)

if selected_domain != "All":
    controls_view = controls_df[
        controls_df["control_domain"] == selected_domain
    ]
else:
    controls_view = controls_df

st.dataframe(
    controls_view,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "These are illustrative controls linked to synthetic portfolio risks. "
    "Documenting a control does not establish its operating effectiveness."
)

st.divider()
st.header("Control Testing & Audit Results")

TEST_FILE = PROJECT_ROOT / "data" / "control_tests.csv"
tests_df = pd.read_csv(TEST_FILE)

st.subheader("Testing Summary")

total_tests = len(tests_df)
passed_tests = int((tests_df["result"] == "Pass").sum())
failed_tests = int((tests_df["result"] == "Fail").sum())

col1, col2, col3 = st.columns(3)
col1.metric("Tests Recorded", total_tests)
col2.metric("Passed Tests", passed_tests)
col3.metric("Failed Tests", failed_tests)

tests_df["exception_rate"] = (
    tests_df["exceptions_found"] / tests_df["sample_size"] * 100
).round(2)

st.subheader("Observed Exception Rates")

st.dataframe(
    tests_df[
        [
            "test_id",
            "control_id",
            "test_period",
            "sample_size",
            "exceptions_found",
            "exception_rate",
            "result",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Illustrative test results using synthetic data. "
    "Exception rates describe the recorded samples and do not, "
    "by themselves, establish population-wide control effectiveness."
)
