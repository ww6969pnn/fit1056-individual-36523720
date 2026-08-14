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
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
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
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    
    if len(app_data['teachers']) < original_count:
        print(f"Teacher ID {teacher_id} deleted")
    else:
        print(f"Teacher with ID {teacher_id} not found")


# Check-in and statistics
def check_in(student_id, course_id):
    student_exists = any(s['id'] == student_id for s in app_data['students'])
    if not student_exists:
        print(f"No student with ID {student_id} was found")
        return False
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    app_data['attendance'].append(record)
    print(f"Student {student_id} checked in! Course: {course_id} Time: {timestamp}")
    return True

def view_attendance_records():
    records = app_data['attendance']
    if not records:
        print("No attendance records found")
        return
    print("\n" + "="*60)
    print("Attendance Records")
    print("="*60)
    for record in records:
        student_name = "Unknown"
        for s in app_data['students']:
            if s['id'] == record['student_id']:
                student_name = s['name']
                break
        print(f"Student: {student_name} (ID: {record['student_id']}) | "
              f"Course: {record['course_id']} | "
              f"Time: {record['timestamp']}")
    print("="*60)

def show_statistics():
    print("\n" + "="*50)
    print("📊 System Statistics")
    print("="*50)
    print(f"Total Students: {len(app_data['students'])}")
    print(f"Total Teachers: {len(app_data['teachers'])}")
    print(f"Total Check-ins: {len(app_data['attendance'])}")
    course_count = {}
    for student in app_data['students']:
        for course in student.get('enrolled_in', []):
            course_count[course] = course_count.get(course, 0) + 1
    if course_count:
        most_popular = max(course_count, key=course_count.get)
        print(f"Most Popular Course: {most_popular} ({course_count[most_popular]} students)")
    print("="*50)


#main menu
def print_student_card(student_id):
    student = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student = s
            break
    if not student:
        print(f"Student with ID {student_id} not found")
        return
    filename = f"student_card_{student_id}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*35 + "\n")
        f.write("     Music School Student ID\n")
        f.write("="*35 + "\n")
        f.write(f"Student ID: {student['id']}\n")
        f.write(f"Name: {student['name']}\n")
        f.write(f"Enrolled Courses: {', '.join(student.get('enrolled_in', [])) or 'None'}\n")
        f.write("="*35 + "\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Student card generated: {filename}")

#MAIN program
def main():
    load_data()
    while True:
        print("\n" + "="*45)
        print("Music School Management System v2.0")
        print("="*45)
        print("[Student Management]")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Filter Students by Course")
        print("4. Update Student")
        print("5. Delete Student")
        print("[Teacher Management]")
        print("6. Add Teacher")
        print("7. View All Teachers")
        print("  8. Update Teacher")
        print("  9. Delete Teacher")
        print("【Check-in】")
        print(" 10. Student Check-in")
        print(" 11. View Attendance Records")
        print("【Other】")
        print(" 12. Print Student Card")
        print(" 13. View Statistics")
        print("  q. Quit and Save")
        print("="*45)
        choice = input("Enter your choice: ").strip().lower()
        made_change = False

        if choice == '1':
            name = input("Student name: ").strip()
            if not name:
                print("Name cannot be empty")
                continue
            courses_input = input("Enrolled courses (comma-separated, e.g., Piano,Vocal): ").strip()
            courses = [c.strip() for c in courses_input.split(',')] if courses_input else []
            add_student(name, courses)
            made_change = True
            
        elif choice == '2':
            list_all_students()

        elif choice == '3':
            course = input("Enter course name: ").strip()
            list_students_by_course(course)
            
        elif choice == '4':
            try:
                student_id = int(input("Enter student ID: "))
                print("Enter fields to update (leave blank to skip):")
                name = input("New name: ").strip()
                courses_input = input("New courses (comma-separated): ").strip()
                fields = {}
                if name:
                    fields['name'] = name
                if courses_input:
                    fields['enrolled_in'] = [c.strip() for c in courses_input.split(',')]
                
                if fields:
                    update_student(student_id, **fields)
                    made_change = True
                else:
                    print("No fields to update")
            except ValueError:
                print("Please enter a valid numeric ID")

        elif choice == '5':
            try:
                student_id = int(input("Enter student ID to delete: "))
                remove_student(student_id)
                made_change = True
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '6':
            name = input("Teacher name: ").strip()
            if not name:
                print("Name cannot be empty")
                continue
            speciality = input("Teaching speciality: ").strip()
            add_teacher(name, speciality)
            made_change = True 

        elif choice == '7':
            list_all_teachers()
            
        elif choice == '8':
            try:
                teacher_id = int(input("Enter teacher ID: "))
                name = input("New name (leave blank to skip): ").strip()
                speciality = input("New speciality (leave blank to skip): ").strip()
                
                fields = {}
                if name:
                    fields['name'] = name
                if speciality:
                    fields['speciality'] = speciality
                    if fields:
                        update_teacher(teacher_id, **fields)
                        made_change = True
                else:
                    print("No fields to update")
            except ValueError:
                print("Please enter a valid numeric ID")
                
        elif choice == '9':
            try:
                teacher_id = int(input("Enter teacher ID to delete: "))
                remove_teacher(teacher_id)
                made_change = True
            except ValueError:
                print("Please enter a valid numeric ID")

        elif choice == '10':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course name: ").strip()
                if check_in(student_id, course_id):
                    made_change = True
            except ValueError:
                print("Please enter a valid numeric ID")
                
        elif choice == '11':
            view_attendance_records()

        elif choice == '12':
            try:
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            except ValueError:
                print("Please enter a valid numeric ID")
                
        elif choice == '13':
            show_statistics()
            
        elif choice == 'q':
            print("Saving and exiting...")
            save_data()
            break

        else:
            print("Invalid option, please try again")
        
        if made_change:
            save_data()


if __name__ == "__main__":
    main()