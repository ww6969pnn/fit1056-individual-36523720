# Music School Management System (MSMS) - PST4

A Python-based music school management system with a Streamlit GUI.

## Features

- Add, view, update, and delete students
- Add, view, and delete teachers
- Add, view, and remove courses (linked to a teacher, instrument, day, and time)
- Student check-in with course existence and enrollment validation
- Daily roster by day of week
- Attendance records
- Data persistence via JSON (`data/msms.json`)

## GUI Pages

- **Student Management** – register students, view student list
- **Course Management** – create and remove courses, view course list
- **Daily Roster** – view roster by day, check in students, view attendance

## Project Structure
msms.project/
├── app/
│ ├── schedule.py # ScheduleManager (business logic)
│ ├── student.py # StudentUser
│ ├── teacher.py # TeacherUser, Course
│ └── user.py # User base class
├── data/
│ └── msms.json # Persisted data
├── gui/
│ ├── main_dashboard.py
│ ├── student_pages.py
│ ├── course_pages.py
│ └── roster_pages.py
└── main.py


## Installation

```bash
git clone <your-repo-url>
cd msms.project
pip install streamlit

# How to Run
streamlit run main.py