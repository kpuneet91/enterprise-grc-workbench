import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Control Library", layout="wide")

st.title("Security Control Library")
st.caption("A central inventory of controls mapped to identified enterprise risks.")

DATA_DIR = Path(__file__).parent.parent / "data"
controls = pd.read_csv(DATA_DIR / "control_library.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Total Controls", len(controls))
col2.metric("Control Domains", controls["control_domain"].nunique())
col3.metric("Control Owners", controls["control_owner"].nunique())

st.divider()

domains = sorted(controls["control_domain"].dropna().unique().tolist())
selected_domains = st.multiselect(
    "Filter by control domain",
    options=domains,
    default=domains
)

filtered_controls = controls[
    controls["control_domain"].isin(selected_domains)
]

st.subheader("Control Inventory")
st.dataframe(filtered_controls, use_container_width=True, hide_index=True)

csv_data = filtered_controls.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered control library (CSV)",
    data=csv_data,
    file_name="control_library_export.csv",
    mime="text/csv"
)

st.info(
    "Control records are illustrative. In a real GRC environment, "
    "validate control design, ownership, frequency and evidence requirements "
    "against approved policies and risk appetite."
)
