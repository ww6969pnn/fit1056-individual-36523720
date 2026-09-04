import json
import os
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

ALLOWED_INSTRUMENTS={"piano","guitar","violin","drums","flute"}

class ScheduleManager:
    """Core management category, responsible for data management and storage"""
    def __init__(self, data_file="data/msms.json"):
        self.data_file = data_file
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []
        self.next_student_id = 1
        self.next_teacher_id = 1

        #load data
        self._load_data()

    def _load_data(self):
        """Load data from JSON and convert it into an object"""
        if not os.path.exists(self.data_file):
            print(f"The data file {self.data_file} does not exists. New data will be created shortly.")
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # load student data
            for student_data in data.get('students', []):
                student = StudentUser(
                    student_data['id'],
                    student_data['name'],
                    student_data.get('enrolled_in',[])
                )
                #load attendance record
                if 'attendance' in student_data:
                    student.attendance = student_data['attendance']
                self.students.append(student)

            #load teacher data
            for teacher_data in data.get('teachers',[]):
                teacher = TeacherUser(
                    teacher_data['id'],
                    teacher_data['name'],
                    teacher_data.get('speciality', '')
                )
                self.teachers.append(teacher)

            #load sign-in records
            self.attendance = data.get('attendance', [])

            #load the next available ID
            self.next_student_id = data.get('next_student_id', 1)
            self.next_teacher_id = data.get('next_teacher_id', 1)

            print(f"Load successfully: {len(self.students)} students, {len(self.teachers)} teachers")
        except Exception as e:
            print(f"Error occurred while loading data: {e}")

    def _save_data(self):
        """Save the current data to JSON"""
        try:
            #prepare students' data
            students_data = []
            for student in self.students:
                students_data.append({
                    'id': student.user_id,
                    'name': student.name,
                    'enrolled_in': student.enrooled_in,
                    'attendance': student.attendacne
                })

            #prepare teachers' data
            teachers_data = []
            for teacher in self.teachers:
                teachers_data.append({
                    'id': teacher.user_id,
                    'name': teacher.name,
                    'speciality': teacher.speciality
                })

            #Assemble the complete data
            all_data = {
                'students': students_data,
                'teachers': teachers_data,
                'attendance': self.attendace,
                'next_student_id': self.next_student_id,
                'next_teacher_id': self.next_teacher_id
            }

            #write in
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

            print("Data saved successfully")

        except Exception as e:
            print(f"Error occurred while saving the data: {e}")

    def add_student(self, name, courses=None):
        """add students"""
        if courses is None:
            courses=[]

        #check length of name
        if len(name)>15:
            print("Error: Name is too long! Max length is 15 characters.")
            return False

        #check instruments
        for c in courses:
            if c.lower() not in ALLOWED_INSTRUMENTS:
                print(f"Invalid instrument {c}, allowed instruments: {ALLOWED_INSTRUMENTS}.")
                return False

        student_id = self.next_student_id
        student = StudentUser(student_id, name, courses)
        self.students.append(student)
        self.next_student_id += 1

        print(f"Student '{name}' added successfully! ID: {student_id}")
        self._save_data()
        return True

    def list_all_students(self):
        """list all students"""
        if not self.students:
            print("No student records available.")
            return

        print("\n" + "="*50)
        for student in self.students:
            courses = ', '.join(student.enrolled_in) if student.enrolled_in else 'Not taking any courses'
            print(f"ID: {student['id']} | Name: {student['name']} | Course: {courses}")
        print("="*50)

    def update_student(self, student_id, **fields):
        """update students data"""
        for student in self.students:
            if student.user_id == student_id:
                #update name
                if 'name' in fields:
                    if len(fields['name']) > 15:
                        print("Error: Name is too long")
                        return False
                    student.name = fields['name']
                #update course
                if 'enrolled_in' in fields:
                    for c in fields['enrolled_in']:
                        if c.lower() not in ALLOWED_INSTRUMENTS:
                            print(f"Invalid instrument {c}")
                            return False
                    student.enrolled_in = fields['enrolled_in']

                print(f"Student ID {student_id} has been updated.")
                self._save_data()
                return True

            print(f"No student with ID {student_id} was found")
            return False

        def remove_student(self, student_id):
            """delete student"""
            original_count = len(self.students)
            self.students = [s for s in self.students if s.user_id != student_id]
        
            if len(self.students) < original_count:
                print(f"Student ID {student_id} has been deleted")
                self._save_data()
                return True
            else:
                print(f"No student with ID {student_id} was found")
                return False

        def add_teacher(self, name, speciality):
            """add teacher"""
            if len(name)>15:
                print("Error: Name is too long! Max length is 15 characters.")
                return False

            if speciality.lower() not in ALLOWED_INSTRUMENTS:
                print(f"Invalid speciality {speciality}, allowed instruments: {ALLOWED_INSTRUMENTS}.")
                return False

            teacher_id = self.next_teacher_id
            teacher = TeacherUser(teacher_id, name, speciality)
            self.teachers.append(teacher)
            self.next_teacher_id += 1

            print(f"Teacher '{name}' added successfully! ID: {teacher_id}")
            self._save_data()
            return True

        def list_all_teachers(self):
            """list all teachers"""
            if not self.teachers:
                print("No teacher records available.")
                return

            print("\n" + "="*50)
            print("List of all teachers")
            print("="*50)
            for teacher in self.teachers:
                print(f"ID: {teacher['id']} | Name: {teacher['name']} | Speciality: {teacher['speciality']}")
                print("="*50)

        def update_teacher(self, teacher_id, **fields):
            """update teacher data"""
            for teacher in self.teachers:
                if teacher.user_id == teacher_id:
                    if 'name' in fields:
                        if len(fields['name']) > 15:
                            print("Error: Name is too long! Max length is 15 characters.")
                            return False
                        teacher.name = fields['name']

                    if 'speciality' in fields:
                        if fields['speciality'].lower() not in ALLOWED_INSTRUMENTS:
                            print(f"Invalid instrument.")
                            return False
                        teacher.speciality = fields['speciality']

                    print(f"Teacher ID {teacher_id} has been updated.")
                    self._save_data()
                    return True

            print(f"No teacher with {teacher_id} was found")
            return False

        def remove_teacher(self, teacher_id):
            """delete teacher"""
            original_count = len(self.teachers)
            self.teachers = [t for t in self.teachers if t.user_id != teacher_id]

            if len(self.teachers) < original_count:
                print(f"Teacher ID {teacher_id} deleted")
                self._save_data()
                return True
            else:
                print(f"Teacher with ID {teacher_id} not found")
                return False

        def check_in(self, student_id, course_name):
            """student attendance"""
            #Check whether students exist
            student_exists = any(s.user_id == student_id for s in self.students)
            if not student_exists:
                print(f"No student with ID {student_id} was found")
                return False

            #Record check-in
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {
                "student_id": student_id,
                "course_name": course_name,
                "timestamp": timestamp
            }
            self.attendance.append(record)

            #Update the student attendance records
            for student in self.students:
                if student.user_id == student_id:
                    student.attendance.append({"course": course_name, "time": timestamp})
                    break
            print(f"Student {student_id} checked in! Course: {course_id} Time: {timestamp}")
            self._save_data()
            return True

        def view_attendace(self):
            """view attendance"""
            if not self.attendance:
                print("No sign-in record available.")
                return
            print("\n" + "="*50)
            print("Check-in record")
            print("="*50)
            for record in self.attendance:
                print(f"Student ID: {record['student_id']} | Course: {record['course_name']} | Time: record['timestamp']")

        