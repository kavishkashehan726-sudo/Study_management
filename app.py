import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta

# --- Config and Setup ---
st.set_page_config(page_title="Work-Study-Life OS", layout="wide")

# Scopes for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def init_connection():
    # Load credentials from Streamlit Secrets
    # Streamlit Cloud uses st.secrets; locally it looks in .streamlit/secrets.toml
    if "gcp_service_account" in st.secrets:
        credentials_dict = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
    else:
        # Fallback for local testing without secrets.toml (if credentials.json is present)
        credentials = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )
        
    client = gspread.authorize(credentials)
    return client

try:
    client = init_connection()
    # Ensure this matches the exact name of your Google Sheet
    sheet = client.open("Work-Study-Life-OS")
    academic_ws = sheet.worksheet("Academic")
    professional_ws = sheet.worksheet("Professional")
except Exception as e:
    st.error(f"Error connecting to Google Sheets. Make sure you have `credentials.json` in this folder and you shared the sheet with your Service Account email. Error: {e}")
    st.stop()

# --- Helper Functions ---
def fetch_data(worksheet):
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty and 'Deadline' in df.columns:
        df['Deadline'] = pd.to_datetime(df['Deadline'], format='%Y-%m-%d', errors='coerce')
    return df

def add_task(worksheet, task_data):
    worksheet.append_row(task_data)

# --- Data Fetching ---
academic_df = fetch_data(academic_ws)
professional_df = fetch_data(professional_ws)

# --- UI Components ---
st.title("🚀 Work-Study-Life OS Dashboard")
st.markdown("Balancing OUSL Software Engineering & ICT Management")

# --- Stress Management Check ---
def check_workload(df1, df2):
    today = pd.to_datetime('today').normalize()
    next_week = today + pd.DateOffset(days=7)
    
    high_priority_count = 0
    if not df1.empty and 'Deadline' in df1.columns and 'Priority' in df1.columns:
        high_priority_count += len(df1[
            (df1['Deadline'] >= today) & 
            (df1['Deadline'] <= next_week) & 
            (df1['Priority'].str.lower() == 'high') &
            (df1['Status'].str.lower() != 'completed')
        ])
    if not df2.empty and 'Deadline' in df2.columns and 'Priority' in df2.columns:
        high_priority_count += len(df2[
            (df2['Deadline'] >= today) & 
            (df2['Deadline'] <= next_week) & 
            (df2['Priority'].str.lower() == 'high') &
            (df2['Status'].str.lower() != 'completed')
        ])
        
    return high_priority_count

high_priority_tasks = check_workload(academic_df, professional_df)

if high_priority_tasks > 3:
    st.error(f"🚨 WORKLOAD WARNING: You have {high_priority_tasks} high-priority tasks due within the next 7 days! Prioritize your focus, consider delegating ICT tasks if possible, and manage your stress.")
else:
    st.success(f"✅ Workload is manageable. You have {high_priority_tasks} high-priority task(s) in the next 7 days.")

# --- Master Calendar / Timeline ---
st.subheader("📅 Upcoming Tasks")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Academic Deadlines")
    if not academic_df.empty:
        # Filter future pending tasks
        upcoming_acad = academic_df[
            (academic_df['Deadline'] >= pd.to_datetime('today').normalize()) & 
            (academic_df.get('Status', 'Pending').str.lower() != 'completed')
        ].sort_values(by='Deadline')
        
        # Format the datetime object back to string for clean display
        if not upcoming_acad.empty:
            upcoming_acad['Deadline'] = upcoming_acad['Deadline'].dt.strftime('%Y-%m-%d')
            st.dataframe(upcoming_acad[['Task', 'Module', 'Type', 'Deadline', 'Priority', 'Status']], hide_index=True, use_container_width=True)
        else:
            st.info("No upcoming academic tasks found.")
    else:
        st.info("No academic tasks in the database.")

with col2:
    st.markdown("### 💼 Professional Deliverables")
    if not professional_df.empty:
        upcoming_prof = professional_df[
            (professional_df['Deadline'] >= pd.to_datetime('today').normalize()) &
            (professional_df.get('Status', 'Pending').str.lower() != 'completed')
        ].sort_values(by='Deadline')
        
        if not upcoming_prof.empty:
            upcoming_prof['Deadline'] = upcoming_prof['Deadline'].dt.strftime('%Y-%m-%d')
            st.dataframe(upcoming_prof[['Task', 'Project', 'Deadline', 'Priority', 'Status']], hide_index=True, use_container_width=True)
        else:
             st.info("No upcoming professional tasks found.")
    else:
        st.info("No professional tasks in the database.")

# --- Manual Task Entry Forms ---
st.divider()
st.subheader("➕ Add New Task")

tab1, tab2 = st.tabs(["Academic Task", "Professional Task"])

with tab1:
    with st.form("academic_form", clear_on_submit=True):
        acad_task = st.text_input("Task Name (e.g., Assignment 1)")
        acad_module = st.selectbox("Module", ["EEI3346", "EEI3467", "MHZ2250", "EEI3372", "Other"])
        acad_type = st.selectbox("Assessment Type", ["CAT", "Lab Test", "Assignment", "ILS", "Viva", "Exam"])
        acad_deadline = st.date_input("Deadline")
        acad_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        submitted_acad = st.form_submit_button("Add Academic Task")
        if submitted_acad:
            if acad_task:
                add_task(academic_ws, [acad_task, acad_module, acad_type, str(acad_deadline), acad_priority, "Pending"])
                st.success("Task added successfully! Refresh the app to see updates.")
            else:
                st.warning("Please enter a task name.")

with tab2:
    with st.form("professional_form", clear_on_submit=True):
        prof_task = st.text_input("Task Name (e.g., Deploy Agrian v1.2)")
        prof_project = st.selectbox("Project", ["Agrian.lk", "PLR System", "Team Comms", "General Admin", "Other"])
        prof_deadline = st.date_input("Deadline")
        prof_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        submitted_prof = st.form_submit_button("Add Professional Task")
        if submitted_prof:
            if prof_task:
                add_task(professional_ws, [prof_task, prof_project, str(prof_deadline), prof_priority, "Pending"])
                st.success("Task added successfully! Refresh the app to see updates.")
            else:
                st.warning("Please enter a task name.")
