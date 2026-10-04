# 🚀 Work-Study-Life OS

### A Unified Productivity & Study Management Dashboard

> **Work smarter. Study better. Stay in control.**

**Work-Study-Life OS** is a productivity and study-management platform built with **Python and Streamlit**, designed to help students and professionals manage academic deadlines, professional responsibilities, workload risks, and daily priorities from a single dashboard.

The system uses **Google Sheets as a lightweight cloud backend**, with optional LMS calendar synchronization for automatically importing upcoming academic events.

---

## ✨ Features

### 📚 Academic & Professional Task Management

- Create and manage academic tasks
- Track professional/work responsibilities
- Assign priorities and deadlines
- Monitor task status
- Organize tasks by module, project, or type
- Persistent storage using Google Sheets

### 📅 Upcoming Deadline Monitoring

- View upcoming academic deadlines
- Track pending professional tasks
- Identify approaching due dates
- Quickly understand what needs attention

### 🚨 Workload Risk Detection

The dashboard automatically identifies potentially overloaded periods.

> ⚠️ **High-priority workload alerts** are triggered when multiple high-priority tasks are approaching within the next 7 days.

This helps prevent deadline congestion and encourages better workload planning.

### 📊 Enterprise Dashboard

The advanced dashboard provides an enterprise-style productivity experience:

- 🔐 Password-protected access
- 📈 Executive analytics
- 📊 Productivity metrics
- 🗂️ Kanban workflow board
- 🎓 Academic task filtering
- 💼 Professional task filtering
- ✏️ Administrative task management
- 🔄 Task insert/update operations

### 🗓️ LMS Calendar Synchronization

The optional calendar synchronization utility can:

- Fetch academic events from the OUSL LMS calendar feed
- Parse upcoming events
- Identify modules
- Determine task types
- Assign priorities
- Automatically add new tasks to Google Sheets
- Avoid inserting duplicate events

---

# 🖥️ Application Components

| Component | Description |
|---|---|
| `app.py` | Main productivity dashboard |
| `enterprise_os.py` | Advanced enterprise-style dashboard |
| `calendar_sync.py` | LMS calendar synchronization |
| `notifier.py` | Future notification system |
| `scraper.py` | Future scraping utilities |
| `test_app.py` | Streamlit smoke tests |
| `test_secrets.py` | Secrets/configuration validation |

---

# 🏗️ Project Architecture

```text
                    ┌─────────────────────────┐
                    │     Work-Study-Life OS   │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
       ┌──────▼───────┐                     ┌───────▼────────┐
       │ Main Dashboard│                     │ Enterprise OS  │
       │    app.py     │                     │enterprise_os.py│
       └──────┬────────┘                     └───────┬────────┘
              │                                      │
              └──────────────────┬───────────────────┘
                                 │
                        ┌────────▼────────┐
                        │  Google Sheets  │
                        │   Data Store    │
                        └────────┬────────┘
                                 │
                       ┌─────────▼─────────┐
                       │  Calendar Sync    │
                       │  calendar_sync.py │
                       └─────────┬─────────┘
                                 │
                        ┌────────▼────────┐
                        │   OUSL LMS       │
                        │ Calendar Feed     │
                        └──────────────────┘
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python 3** | Core application logic |
| 🎈 **Streamlit** | Interactive web dashboard |
| 📊 **Pandas** | Data processing and analysis |
| 📈 **Plotly** | Interactive analytics and charts |
| 📑 **Google Sheets** | Cloud-based data storage |
| 🔑 **gspread** | Google Sheets API integration |
| 🔐 **Google Auth** | Service-account authentication |
| 🌐 **Requests** | HTTP/API requests |
| 📅 **icalendar** | Calendar feed parsing |

---

# 📁 Repository Structure

```text
Study_management/
│
├── app.py                    # Main productivity dashboard
├── enterprise_os.py          # Secure enterprise dashboard
├── calendar_sync.py          # LMS calendar synchronization
├── notifier.py               # Notification module placeholder
├── scraper.py                # Scraping utility placeholder
│
├── requirements.txt          # Python dependencies
├── test_app.py               # Streamlit smoke tests
├── test_secrets.py           # Secrets validation
│
├── credentials.json          # Local service account credentials
│
├── .streamlit/
│   └── secrets.toml          # Streamlit secrets
│
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/kavishkashehan726-sudo/Study_management.git
```

```bash
cd Study_management
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ☁️ Google Sheets Configuration

The application uses a Google Spreadsheet named:

```text
Work-Study-Life-OS
```

Create the following worksheets:

```text
Academic
Professional
```

### Recommended Columns

```text
Task
Module or Project
Type
Deadline
Priority
Status
```

Example:

| Task | Module or Project | Type | Deadline | Priority | Status |
|---|---|---|---|---|---|
| Complete Assignment | Software Engineering | Assignment | 2026-10-10 | High | Pending |
| Client Website | Hotel Project | Development | 2026-10-15 | Medium | In Progress |
| Study Chapter 5 | Mathematics | Study | 2026-10-08 | High | Pending |

---

# 🔐 Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

Then configure your Google service account:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

For the enterprise dashboard, optionally add:

```toml
APP_PASSWORD = "your-master-password"
```

> 🔒 **Never commit real credentials, private keys, passwords, or service-account files to GitHub.**

Make sure sensitive files are included in `.gitignore`.

---

# ▶️ Running the Application

## Main Dashboard

```bash
streamlit run app.py
```

The main dashboard provides:

- Academic task tracking
- Professional task tracking
- Deadline monitoring
- Priority alerts
- Task creation forms
- Google Sheets persistence

---

## Enterprise Dashboard

```bash
streamlit run enterprise_os.py
```

The enterprise dashboard provides:

- 🔐 Secure login
- 📊 Executive analytics
- 🗂️ Kanban workflow
- 🎓 Academic filtering
- 💼 Professional filtering
- ✏️ Administrative task controls

---

## Calendar Synchronization

Run:

```bash
python calendar_sync.py
```

The synchronization utility retrieves upcoming events from the configured OUSL LMS calendar feed and adds newly discovered academic tasks to Google Sheets.

---

# 🧠 How It Works

```text
                 User
                   │
                   ▼
        ┌─────────────────────┐
        │  Streamlit Dashboard │
        └──────────┬──────────┘
                   │
          ┌────────▼────────┐
          │ Task Management │
          └────────┬────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │    Google Sheets    │
        │      Backend        │
        └──────────┬──────────┘
                   │
          ┌────────▼─────────┐
          │ Analytics & Risk │
          │    Detection     │
          └────────┬─────────┘
                   │
                   ▼
          📊 Dashboard Insights
```

The optional calendar workflow adds another source:

```text
OUSL LMS Calendar
        │
        ▼
Calendar Parser
        │
        ▼
Event Classification
        │
        ├── Module
        ├── Task Type
        └── Priority
        │
        ▼
Google Sheets
        │
        ▼
Work-Study-Life OS
```

---

# 🎯 Workload Risk Management

One of the core concepts of the system is identifying periods where workload may become difficult to manage.

The dashboard monitors:

```text
Upcoming Tasks
      +
Priority
      +
Deadline
      ↓
Workload Analysis
      ↓
Potential Risk
      ↓
⚠️ Early Warning
```

For example, if several **high-priority tasks** are due within the next seven days, the dashboard can highlight the workload as a potential risk.

This allows the user to prioritize work before deadlines become critical.

---

# 🔮 Future Roadmap

The project is designed to grow beyond a simple task tracker.

### Planned Improvements

- [ ] 🔔 Smart notifications
- [ ] 📱 Mobile-friendly interface
- [ ] 📧 Email reminders
- [ ] 🤖 AI-powered task prioritization
- [ ] 🧠 Intelligent workload forecasting
- [ ] 📆 Advanced calendar integration
- [ ] 🔄 Two-way calendar synchronization
- [ ] 👥 Multi-user support
- [ ] 📊 Productivity history
- [ ] 📈 Weekly/monthly productivity reports
- [ ] 🌙 Dark/light theme customization
- [ ] 🔐 Improved
