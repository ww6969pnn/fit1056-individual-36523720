# Music School Management System (MSMS)

A Python-based music school management system for managing students, teachers, courses, and attendance.

## Features

- Add, view, update, and delete students
- Add, view, update, and delete teachers
- Student check-in for courses
- View attendance records
- Data persistence using JSON file storage

msms-project/
├── app/
│   ├── user.py          # Base User class
│   ├── student.py       # StudentUser class
│   ├── teacher.py       # TeacherUser and Course classes
│   └── schedule.py      # ScheduleManager (core logic)
├── data/
│   └── msms.json        # Data storage file
├── main.py              # Program entry point
└── README.md

All data is automatically saved to data/msms.json. The program loads existing data on startup.

## Installation

```bash
git clone <your-repo-url>
cd msms-project