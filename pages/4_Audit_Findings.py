import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Audit Findings", layout="wide")

st.title("Audit Findings & Remediation Tracker")
st.caption("Track audit exceptions, corrective actions, owners and remediation deadlines.")

DATA_DIR = Path(__file__).parent.parent / "data"
findings = pd.read_csv(DATA_DIR / "audit_findings.csv")

findings["identified_date"] = pd.to_datetime(findings["identified_date"], errors="coerce")
findings["target_date"] = pd.to_datetime(findings["target_date"], errors="coerce")
findings["status"] = findings["status"].astype(str).str.strip().str.title()
findings["severity"] = findings["severity"].astype(str).str.strip().str.title()

today = pd.Timestamp.now().normalize()

findings["overdue"] = (
    findings["status"].ne("Closed")
    & findings["target_date"].notna()
    & findings["target_date"].lt(today)
)

total = len(findings)
open_count = int((findings["status"] == "Open").sum())
in_progress = int((findings["status"] == "In Progress").sum())
overdue_count = int(findings["overdue"].sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Findings", total)
col2.metric("Open", open_count)
col3.metric("In Progress", in_progress)
col4.metric("Overdue", overdue_count)

st.divider()

col1, col2 = st.columns(2)
with col1:
    severity_options = sorted(findings["severity"].dropna().unique().tolist())
    selected_severities = st.multiselect(
        "Filter by severity",
        options=severity_options,
        default=severity_options
    )

with col2:
    status_options = sorted(findings["status"].dropna().unique().tolist())
    selected_statuses = st.multiselect(
        "Filter by status",
        options=status_options,
        default=status_options
    )

filtered = findings[
    findings["severity"].isin(selected_severities)
    & findings["status"].isin(selected_statuses)
].copy()

filtered["identified_date"] = filtered["identified_date"].dt.strftime("%Y-%m-%d")
filtered["target_date"] = filtered["target_date"].dt.strftime("%Y-%m-%d")

st.subheader("Findings Register")
st.dataframe(
    filtered.drop(columns=["overdue"]),
    use_container_width=True,
    hide_index=True
)

st.subheader("Remediation Status")
status_summary = (
    findings["status"]
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Findings")
)
st.bar_chart(status_summary.set_index("Status"))

csv_data = filtered.drop(columns=["overdue"]).to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered findings (CSV)",
    data=csv_data,
    file_name="audit_findings_export.csv",
    mime="text/csv"
)

st.info(
    "Overdue status is calculated using today's date and the target date. "
    "Closed findings are excluded from overdue counts. Sample records are fictional."
)
