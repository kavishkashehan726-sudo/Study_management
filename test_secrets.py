import streamlit as st
print("App loaded")

st.write("Checking secrets...")
try:
    has_secrets = "gcp_service_account" in st.secrets
    st.write(f"Has secrets: {has_secrets}")
except Exception as e:
    st.write(f"Exception: {e}")
