import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from icalendar import Calendar
from datetime import datetime, date

# --- Configuration ---
CALENDAR_URL = "https://oulms.ou.ac.lk/calendar/export_execute.php?userid=67500&authtoken=2ada3093248fba7e3ef2a4e8f2071d5a1dd71347&preset_what=all&preset_time=custom"
CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "Work-Study-Life-OS"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def connect_sheets():
    print("Connecting to Google Sheets...")
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    return client.open(SHEET_NAME).worksheet("Academic")

def fetch_and_parse_calendar():
    print("Downloading calendar data from OUSL LMS...")
    response = requests.get(CALENDAR_URL)
    response.raise_for_status()
    
    cal = Calendar.from_ical(response.text)
    tasks = []
    
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('summary'))
            
            # Extract deadline
            dtstart = component.get('dtstart').dt
            if hasattr(dtstart, 'date'):
                dt_date = dtstart.date()
                deadline = dtstart.strftime("%Y-%m-%d")
            else:
                dt_date = dtstart
                deadline = dtstart.strftime("%Y-%m-%d")
            
            # Extract Module from Categories (e.g., EEI3347_2025 -> EEI3347)
            categories = component.get('categories')
            module = "General"
            if categories:
                cat_str = str(categories.to_ical().decode('utf-8')) if hasattr(categories, 'to_ical') else str(categories)
                module = cat_str.split('_')[0] if '_' in cat_str else cat_str
            
            # Infer Type and Priority based on Task Name
            type_val = "Assignment"
            task_upper = summary.upper()
            if "QUIZ" in task_upper or "CAT" in task_upper: 
                type_val = "CAT"
            elif "LAB" in task_upper: 
                type_val = "Lab Test"
            elif "ILS" in task_upper: 
                type_val = "ILS"
            
            priority = "High" if "CAT" in type_val or "QUIZ" in task_upper or "EXAM" in task_upper else "Medium"
            
            # Only add future or ongoing events
            if dt_date >= datetime.today().date():
                tasks.append([summary, module, type_val, deadline, priority, "Pending"])
                print(f"Found Upcoming Task: {summary} | {module} | {deadline}")
                
    return tasks

def append_to_sheets(tasks, worksheet):
    print("Fetching existing records to prevent duplicates...")
    existing_records = worksheet.get_all_records()
    existing_task_names = [record.get("Task") for record in existing_records]
    
    new_tasks = []
    for task in tasks:
        # Prevent exact duplicate names
        if task[0] not in existing_task_names:
            new_tasks.append(task)
            
    if new_tasks:
        print(f"Appending {len(new_tasks)} new tasks to Google Sheets...")
        worksheet.append_rows(new_tasks)
        print("Done!")
    else:
        print("No new tasks to append. Everything is already up to date!")

if __name__ == "__main__":
    tasks = fetch_and_parse_calendar()
    if tasks:
        ws = connect_sheets()
        append_to_sheets(tasks, ws)
        print("---------------------------------")
        print("Calendar sync completed successfully!")
    else:
        print("No upcoming tasks found in calendar.")
