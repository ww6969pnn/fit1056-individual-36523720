# Music School Management System (MSMS) - PST5

A Python-based music school management system with a Streamlit GUI.

## Features

### Core (PST1–PST4)
- Add, view, update, and delete students
- Add, view, and delete teachers
- Add, view, and remove courses (linked to a teacher, instrument, day, and time)
- Student check-in with course existence and enrollment validation
- Daily roster by day of week
- Attendance records
- Data persistence via JSON (`data/msms.json`)

### New in PST5
- **Finance & Payments** – record payments and view payment history per student
- **Report Export** – export finance or attendance logs to CSV
- **Logging** – all key business operations are logged to `msms.log`
- **Data Backup** – the data file is automatically backed up on application startup
- **Automated Tests** – unit tests using pytest covering core logic

## GUI Pages

- **Student Management** – register students, view student list
- **Teacher Management** – add and remove teachers, view teacher list
- **Course Management** – create and remove courses, view course list
- **Daily Roster** – view roster by day, check in students, view attendance
- **Payments** – record a payment, view a student's payment history, export reports

## Project Structure
``` text
msms-project/
├── app/
│ ├── init.py
│ ├── schedule.py  # ScheduleManager (business logic)
│ ├── student.py  # StudentUser
│ ├── teacher.py  # TeacherUser, Course
│ ├── user.py  # User base class
│ └── admin_utils.py  # Logging + data backup utilities 
│ ├── msms.json  # Persisted data
│ └── backups/  # Timestamped data backups (gitignored)
├── gui/
│ ├── main_dashboard.py
│ ├── student_pages.py
│ ├── teacher_pages.py 
│ ├── course_pages.py
│ ├── roster_pages.py
│ └── finance_pages.py 
├── tests/
│ ├── init.py
│ └── test_schedule_manager.py # Unit tests
├── conftest.py # pytest path setup
├── .gitignore
├── main.py
└── README.md
```

## Installation

```bash
git clone https://github.com/ww6969pnn/fit1056-individual-36523720.git
cd msms-project
pip install streamlit pytest
```

## How to Run
streamlit run main.py

## How to Test
```
pytest
```

## Design Notes
- All business logic lives in ScheduleManager; GUI pages only render and call manager methods.
- Validation (allowed payment methods, name length, teacher-course dependencies) is enforced in the manager, not just the GUI.
- The data file is backed up once per session on startup, using st.session_state to avoid duplicate backups on Streamlit reruns.
- Removing a student only removes them from the active list. Payment and attendance records are preserved for audit purposes.

---