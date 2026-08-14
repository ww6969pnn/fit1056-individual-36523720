import json
import datetime

DATA_FILE = "msms.json"
app_data = {}

#Data persistence engine
def load_data(path=DATA_FILE):
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }
        save_data()

def save_data(path=DATA_FILE):
    with open(path,'w') as f:
        json.dump(app_data, f, indent=4, ensure_ascii=False)
    print("Data saved successfully.")

#student management
def add_student(name, courses=None):
    if courses is None:
        courses=[]
    student_id = app_data['next_student_id']

    new_student = {
        "id": student_id,
        "name": name,
        "enrolled_in": courses
    }
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    print(f"Student '{name}' added successfully! ID: {student_id}")

def list_all_students():
    students = app_data['students']
    if not students:
        print("No student records available.")
        return
    print("\n" + "="*50)
    for student in students:
        courses = ','.join(student.get('enrolled_in', [])) or 'Not taking any courses'
        print(f"ID: {student['id']} | Name: {student['name']} | Course: {courses}")
    print("="*50)

def list_students_by_course(course_name):
    if not course_name:
        print("Please enter the course name.")
        return
    found=[]
    for student in app_data['students']:
        if course_name in student.get('enrolled_in', []):
            found.append(student)
    if found:
        print(f"\n Students who choose to take '{course_name}'")
        for s in found:
            print(f" -{s['name']}(ID: {s['id']})")
    else:
        print(f"No students have chosen to take '{course_name}'")

def updata_student(student_id, **fields):
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student ID {student_id} has been updated.")
            return
    print(f"No student with ID {student_id} was found")

def remove_student(student_id):
    original_count = len(app_data['students'])
    app_data['student'] = [s for s in app_data['students'] if s['id'] ! = students_id]
    if len(app_data['students']) < original_count:
        print(f"Student ID {student_id} has been deleted")
    else:
        print(f"No student with ID {student_id} was found")

#teacher management
def add_teacher(name, speciality):
    teacher_id = app_data['next_teacher_id']
    new_teacher={
        "id": teacher_id,
        "name":name,
        "speciality": speciality
    }
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id']+=1
    print(f"Teacher '{name}' added successfully! ID: {teacher_id}")

def list_all_teachers():
    teachers=app_data['teachers']
    if not teachers:
        print("No teacher records available.")
        return
    print("\n"+"="*50)
    print("List of all teachers")
    print("="*50)
    for teacher in teachers:
        print(f"ID: {teacher['id']} | Name: {teacher['name']} | Speciality: {teacher['specielity']}")
        print("="*50)

def update_teacher(teacher_id, **fields):
    for teacher in app_data['teachers']:
        if teacher['id']==teacher_id:
            teacher.update(fields)
            print(f"Teacher ID {teacher_id} has been updated.")
            return
    print(f"No teacher with {teacher_id} was found")

def remove_teacher(teacher_id):
    original_count = len(app_data['teachers'])
    app_data['teachers'] = [t ofr t in app_data['teachers'] if t['id'] != teacher_id]
    if len(app_data['teachers']) < original_count:
        print(f"Teacher ID {teacher_id} has been deleted.")
    else:
        print(f"No teacher with ID {teacher_id} has been found")


# 