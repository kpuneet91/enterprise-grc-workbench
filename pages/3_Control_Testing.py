import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Control Testing", layout="wide")

st.title("IT Control Testing")
st.caption("Review test execution, sample sizes, exceptions and control effectiveness.")

DATA_DIR = Path(__file__).parent.parent / "data"
tests = pd.read_csv(DATA_DIR / "control_tests.csv")

tests["result"] = tests["result"].astype(str).str.strip().str.title()
tests["exceptions_found"] = pd.to_numeric(tests["exceptions_found"], errors="coerce").fillna(0)
tests["sample_size"] = pd.to_numeric(tests["sample_size"], errors="coerce").fillna(0)

tests["exception_rate_pct"] = (
    tests["exceptions_found"].div(tests["sample_size"].replace(0, pd.NA)) * 100
).fillna(0).round(1)

total_tests = len(tests)
passed_tests = int((tests["result"] == "Pass").sum())
failed_tests = int((tests["result"] == "Fail").sum())
total_exceptions = int(tests["exceptions_found"].sum())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tests Executed", total_tests)
col2.metric("Passed", passed_tests)
col3.metric("Failed", failed_tests)
col4.metric("Exceptions Found", total_exceptions)

st.divider()

results = sorted(tests["result"].dropna().unique().tolist())
selected_results = st.multiselect(
    "Filter by test result",
    options=results,
    default=results
)

filtered_tests = tests[tests["result"].isin(selected_results)]

st.subheader("Test Results")
st.dataframe(filtered_tests, use_container_width=True, hide_index=True)

st.subheader("Exceptions by Control")
exceptions_summary = (
    tests.groupby("control_id", as_index=False)["exceptions_found"].sum()
)
st.bar_chart(exceptions_summary.set_index("control_id"))

csv_data = filtered_tests.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered test results (CSV)",
    data=csv_data,
    file_name="control_testing_export.csv",
    mime="text/csv"
)

st.warning(
    "These are fictional test results for demonstration. A failed test or "
    "exception does not, by itself, establish a final audit finding; assess "
    "the evidence, control criteria, root cause and risk before concluding."
)
