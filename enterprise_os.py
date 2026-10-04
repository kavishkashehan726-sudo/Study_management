import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# --- System Configuration ---
st.set_page_config(page_title="Enterprise OS | Workspace", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

# --- Security Authentication ---
def check_password():
    def password_entered():
        # Fallback to "admin123" if APP_PASSWORD is not set in secrets
        if st.session_state["password"] == st.secrets.get("APP_PASSWORD", "admin123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<br><br><h1 style='text-align: center;'>🔒 Secure Enterprise OS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Please enter your master password to access the system.</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.text_input("Master Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<br><br><h1 style='text-align: center;'>🔒 Secure Enterprise OS</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.text_input("Master Password", type="password", on_change=password_entered, key="password")
            st.error("😕 Incorrect password. Access denied.")
        return False
    return True

if not check_password():
    st.stop()

# --- Custom CSS for Enterprise Look ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #FAFAFA; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { background-color: #1E2127; padding: 15px; border-radius: 10px; border-left: 5px solid #4B90FA; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stDataFrame { border: 1px solid #333; border-radius: 5px; }
    .kanban-card { background-color: #262730; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    </style>
""", unsafe_allow_html=True)

# --- Authentication & Connection ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def init_connection():
    try:
        if getattr(st, "secrets", None) is not None and len(st.secrets) > 0:
            if "gcp_service_account" in st.secrets:
                return gspread.authorize(Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES))
    except Exception: pass 
    return gspread.authorize(Credentials.from_service_account_file("credentials.json", scopes=SCOPES))

try:
    client = init_connection()
    sheet = client.open("Work-Study-Life-OS")
    academic_ws = sheet.worksheet("Academic")
    professional_ws = sheet.worksheet("Professional")
except Exception as e:
    st.error(f"System Offline: Database connection failed. Error: {e}")
    st.stop()

# --- Database Operations ---
def fetch_data(worksheet):
    df = pd.DataFrame(worksheet.get_all_records())
    if not df.empty and 'Deadline' in df.columns:
        df['Deadline'] = pd.to_datetime(df['Deadline'], format='%Y-%m-%d', errors='coerce')
    return df

academic_df = fetch_data(academic_ws)
professional_df = fetch_data(professional_ws)

# --- Sidebar Navigation (Enterprise Menu) ---
st.sidebar.markdown("## 🏢 Enterprise OS")
st.sidebar.markdown("---")
menu_selection = st.sidebar.radio("Navigation Menu", [
    "📊 Executive Dashboard", 
    "📋 Agile Kanban Board",
    "📚 Academic Hub", 
    "💼 Corporate Hub", 
    "⚙️ System Operations"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Global Filters")
sys_status = st.sidebar.selectbox("System Status", ["Active (Pending)", "Archived (Completed)", "All Records"])
sys_priority = st.sidebar.multiselect("Priority Matrix", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])

def apply_filters(df):
    if df.empty: return df
    d = df.copy()
    if sys_status == "Active (Pending)": d = d[d['Status'].str.lower() != 'completed']
    elif sys_status == "Archived (Completed)": d = d[d['Status'].str.lower() == 'completed']
    return d[d['Priority'].isin(sys_priority)]

acad_f = apply_filters(academic_df)
prof_f = apply_filters(professional_df)

# --- Pages Logic ---

if menu_selection == "📊 Executive Dashboard":
    st.title("Executive Dashboard")
    st.markdown("Real-time telemetry and resource management overview.")
    
    total_tasks = len(academic_df) + len(professional_df)
    comp_acad = len(academic_df[academic_df.get('Status', '').str.lower() == 'completed']) if not academic_df.empty else 0
    comp_prof = len(professional_df[professional_df.get('Status', '').str.lower() == 'completed']) if not professional_df.empty else 0
    total_comp = comp_acad + comp_prof
    completion_rate = (total_comp / total_tasks * 100) if total_tasks > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total System Records", total_tasks)
    m2.metric("Overall Completion", f"{completion_rate:.1f}%")
    m3.metric("Active Academic", len(acad_f))
    m4.metric("Active Corporate", len(prof_f))
    
    st.divider()
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Velocity & Deadlines")
        dates = []
        if not acad_f.empty: dates.append(acad_f[['Deadline', 'Task']])
        if not prof_f.empty: dates.append(prof_f[['Deadline', 'Task']])
        if dates:
            t_df = pd.concat(dates).groupby('Deadline').count().reset_index()
            fig = px.area(t_df, x='Deadline', y='Task', title="Upcoming Deliverables Timeline", color_discrete_sequence=['#00D2D3'])
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("No timeline data.")
            
    with c2:
        st.subheader("Resource Allocation")
        fig2 = go.Figure(data=[go.Pie(labels=['Academic', 'Corporate'], values=[len(acad_f), len(prof_f)], hole=.6)])
        fig2.update_layout(title_text="Workload Distribution", annotations=[dict(text='Load', x=0.5, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

elif menu_selection == "📋 Agile Kanban Board":
    st.title("Agile Workflow (Kanban)")
    st.markdown("Visual task management across all sectors.")
    
    kb_data = []
    if not academic_df.empty:
        temp = academic_df.copy()
        temp['Sector'] = 'Academic'
        kb_data.append(temp)
    if not professional_df.empty:
        temp = professional_df.copy()
        temp['Sector'] = 'Corporate'
        kb_data.append(temp)
        
    if kb_data:
        kb_df = pd.concat(kb_data)
        col_todo, col_prog, col_done = st.columns(3)
        
        with col_todo:
            st.markdown("### 🔴 To Do (High Priority)")
            high_tasks = kb_df[(kb_df['Priority'] == 'High') & (kb_df['Status'].str.lower() != 'completed')]
            for _, row in high_tasks.iterrows():
                st.markdown(f"<div class='kanban-card'><h4>{row['Task']}</h4><p><b>{row['Sector']}</b> | 📅 {str(row['Deadline'])[:10]}</p></div>", unsafe_allow_html=True)
                
        with col_prog:
            st.markdown("### 🟡 In Progress (Med/Low)")
            med_tasks = kb_df[(kb_df['Priority'] != 'High') & (kb_df['Status'].str.lower() != 'completed')]
            for _, row in med_tasks.iterrows():
                st.markdown(f"<div class='kanban-card'><h4>{row['Task']}</h4><p><b>{row['Sector']}</b> | 📅 {str(row['Deadline'])[:10]}</p></div>", unsafe_allow_html=True)
                
        with col_done:
            st.markdown("### 🟢 Completed (Recent)")
            done_tasks = kb_df[kb_df['Status'].str.lower() == 'completed'].tail(10)
            for _, row in done_tasks.iterrows():
                st.markdown(f"<div class='kanban-card' style='opacity: 0.6;'><h4><s>{row['Task']}</s></h4><p><b>{row['Sector']}</b></p></div>", unsafe_allow_html=True)
    else:
        st.info("System Database is empty.")

elif menu_selection == "📚 Academic Hub":
    st.title("Academic Hub")
    if not acad_f.empty:
        df_show = acad_f.copy()
        df_show['Deadline'] = df_show['Deadline'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else: st.warning("No records found.")

elif menu_selection == "💼 Corporate Hub":
    st.title("Corporate Hub")
    if not prof_f.empty:
        df_show = prof_f.copy()
        df_show['Deadline'] = df_show['Deadline'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else: st.warning("No records found.")

elif menu_selection == "⚙️ System Operations":
    st.title("System Operations Center")
    st.markdown("Database Write Access & Record Modifications")
    
    op1, op2 = st.columns(2)
    
    with op1:
        st.subheader("Insert New Record")
        form_type = st.radio("Target Database", ["Academic", "Professional"], horizontal=True)
        with st.form("add_form"):
            t_name = st.text_input("Task/Deliverable Name")
            if form_type == "Academic":
                t_module = st.selectbox("Module Identifier", ["EEI3346", "EEI3467", "MHZ2250", "EEI3372", "Other"])
                t_type = st.selectbox("Assessment Type", ["CAT", "Lab Test", "Assignment", "ILS", "Viva", "Exam"])
            else:
                t_module = st.selectbox("Project Portfolio", ["Agrian.lk", "PLR System", "Team Comms", "General Admin", "Other"])
            t_date = st.date_input("Target Date")
            t_pri = st.selectbox("Priority Level", ["High", "Medium", "Low"])
            
            if st.form_submit_button("Execute Insert"):
                if t_name:
                    if form_type == "Academic": academic_ws.append_row([t_name, t_module, t_type, str(t_date), t_pri, "Pending"])
                    else: professional_ws.append_row([t_name, t_module, str(t_date), t_pri, "Pending"])
                    st.cache_data.clear()
                    st.success("Record inserted successfully. Reloading system...")
                    st.rerun()

    with op2:
        st.subheader("Update Record Status")
        upd_type = st.radio("Target Database ", ["Academic", "Professional"], horizontal=True)
        
        with st.form("upd_form"):
            pend_acad = academic_df[academic_df.get('Status', '').str.lower() != 'completed']['Task'].tolist() if not academic_df.empty else []
            pend_prof = professional_df[professional_df.get('Status', '').str.lower() != 'completed']['Task'].tolist() if not professional_df.empty else []
            
            if upd_type == "Academic": sel_task = st.selectbox("Select Pending Academic Record", pend_acad if pend_acad else ["No records"])
            else: sel_task = st.selectbox("Select Pending Corporate Record", pend_prof if pend_prof else ["No records"])
            
            if st.form_submit_button("Mark Status: COMPLETED"):
                if sel_task != "No records":
                    try:
                        df_target = academic_df if upd_type == "Academic" else professional_df
                        ws_target = academic_ws if upd_type == "Academic" else professional_ws
                        r_idx = df_target.index[df_target['Task'] == sel_task].tolist()[0] + 2
                        c_idx = df_target.columns.get_loc('Status') + 1 
                        ws_target.update_cell(r_idx, c_idx, "Completed")
                        st.cache_data.clear()
                        st.success(f"Record '{sel_task}' updated. Reloading system...")
                        st.rerun()
                    except Exception as e:
                        st.error("Operation failed.")
