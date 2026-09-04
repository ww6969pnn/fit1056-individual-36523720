import json
import os
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

ALLOWED_INSTRUMENTS = {"piano", "guitar", "violin", "drums", "flute"}

class ScheduleManager:
    """Main manager class - handles all data operations"""
    
    def __init__(self, data_file=None):
        """Initialize manager and load data from JSON file"""
        if data_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(current_dir)
            data_file = os.path.join(project_dir, 'data', 'msms.json')
        
        self.data_file = data_file
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        
        self._load_data()
        
        try:
            self.next_student_id = int(self.next_student_id)
            self.next_teacher_id = int(self.next_teacher_id)
        except:
            self.next_student_id = 1
            self.next_teacher_id = 1
    
    def _load_data(self):
        """Load data from JSON file and convert to objects"""
        if not os.path.exists(self.data_file):
            print(f"Data file not found. Creating new data...")
            self._save_data()
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for student_data in data.get('students', []):
                student = StudentUser(
                    student_data['id'],
                    student_data['name'],
                    student_data.get('enrolled_in', [])
                )
                student.attendance = student_data.get('attendance', [])
                self.students.append(student)
            
            for teacher_data in data.get('teachers', []):
                teacher = TeacherUser(
                    teacher_data['id'],
                    teacher_data['name'],
                    teacher_data.get('speciality', '')
                )
                self.teachers.append(teacher)
            
            self.attendance = data.get('attendance', [])
            self.next_student_id = int(data.get('next_student_id', 1))
            self.next_teacher_id = int(data.get('next_teacher_id', 1))
            
            print(f"Successfully loaded: {len(self.students)} students, {len(self.teachers)} teachers")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
    
    def _save_data(self):
        """Save all data to JSON file"""
        try:
            students_data = []
            for student in self.students:
                students_data.append({
                    'id': student.user_id,
                    'name': student.name,
                    'enrolled_in': student.enrolled_in,
                    'attendance': student.attendance
                })
            
            teachers_data = []
            for teacher in self.teachers:
                teachers_data.append({
                    'id': teacher.user_id,
                    'name': teacher.name,
                    'speciality': teacher.speciality
                })
            
            all_data = {
                'students': students_data,
                'teachers': teachers_data,
                'attendance': self.attendance,
                'next_student_id': self.next_student_id,
                'next_teacher_id': self.next_teacher_id
            }
            
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
            
            print("Data saved successfully")
            
        except Exception as e:
            print(f"Error saving data: {e}")
    
    # ----- Student Management -----
    
    def add_student(self, name, courses=None):
        """Add a new student to the system"""
        if courses is None:
            courses = []
        
        if len(name) > 15:
            print("Error: Name is too long! Maximum 15 characters.")
            return False
        
        for c in courses:
            if c.lower() not in ALLOWED_INSTRUMENTS:
                print(f"Invalid instrument '{c}'. Allowed instruments: {ALLOWED_INSTRUMENTS}")
                return False
        
        student_id = self.next_student_id
        student = StudentUser(student_id, name, courses)
        self.students.append(student)
        self.next_student_id += 1
        
        print(f"Student '{name}' added successfully! ID: {student_id}")
        self._save_data()
        return True
    
    def list_all_students(self):
        """Display all students"""
        if not self.students:
            print("No student records found.")
            return
        
        print("\n" + "="*50)
        for student in self.students:
            courses = ', '.join(student.enrolled_in) if student.enrolled_in else 'No courses'
            print(f"ID: {student.user_id} | Name: {student.name} | Courses: {courses}")
        print("="*50)
    
    def update_student(self, student_id, **fields):
        """Update a student's information"""
        for student in self.students:
            if student.user_id == student_id:
                if 'name' in fields:
                    if len(fields['name']) > 15:
                        print("Error: Name is too long!")
                        return False
                    student.name = fields['name']
                
                if 'enrolled_in' in fields:
                    for c in fields['enrolled_in']:
                        if c.lower() not in ALLOWED_INSTRUMENTS:
                            print(f"Invalid instrument '{c}'")
                            return False
                    student.enrolled_in = fields['enrolled_in']
                
                print(f"Student ID {student_id} has been updated.")
                self._save_data()
                return True
        
        print(f"No student found with ID {student_id}")
        return False
    
    def remove_student(self, student_id):
        """Delete a student from the system"""
        original_count = len(self.students)
        self.students = [s for s in self.students if s.user_id != student_id]
        
        if len(self.students) < original_count:
            print(f"Student ID {student_id} has been deleted.")
            self._save_data()
            return True
        else:
            print(f"No student found with ID {student_id}")
            return False
    
    # ----- Teacher Management -----
    
    def add_teacher(self, name, speciality):
        """Add a new teacher to the system"""
        if len(name) > 15:
            print("Error: Name is too long! Maximum 15 characters.")
            return False
        
        if speciality.lower() not in ALLOWED_INSTRUMENTS:
            print(f"Invalid speciality '{speciality}'. Allowed: {ALLOWED_INSTRUMENTS}")
            return False
        
        teacher_id = self.next_teacher_id
        teacher = TeacherUser(teacher_id, name, speciality)
        self.teachers.append(teacher)
        self.next_teacher_id += 1
        
        print(f"Teacher '{name}' added successfully! ID: {teacher_id}")
        self._save_data()
        return True
    
    def list_all_teachers(self):
        """Display all teachers"""
        if not self.teachers:
            print("No teacher records found.")
            return
        
        print("\n" + "="*50)
        print("List of all teachers")
        print("="*50)
        for teacher in self.teachers:
            print(f"ID: {teacher.user_id} | Name: {teacher.name} | Speciality: {teacher.speciality}")
        print("="*50)
    
    def update_teacher(self, teacher_id, **fields):
        """Update a teacher's information"""
        for teacher in self.teachers:
            if teacher.user_id == teacher_id:
                if 'name' in fields:
                    if len(fields['name']) > 15:
                        print("Error: Name is too long!")
                        return False
                    teacher.name = fields['name']
                
                if 'speciality' in fields:
                    if fields['speciality'].lower() not in ALLOWED_INSTRUMENTS:
                        print(f"Invalid speciality")
                        return False
                    teacher.speciality = fields['speciality']
                
                print(f"Teacher ID {teacher_id} has been updated.")
                self._save_data()
                return True
        
        print(f"No teacher found with ID {teacher_id}")
        return False
    
    def remove_teacher(self, teacher_id):
        """Delete a teacher from the system"""
        original_count = len(self.teachers)
        self.teachers = [t for t in self.teachers if t.user_id != teacher_id]
        
        if len(self.teachers) < original_count:
            print(f"Teacher ID {teacher_id} has been deleted.")
            self._save_data()
            return True
        else:
            print(f"No teacher found with ID {teacher_id}")
            return False
    
    # ----- Check-in -----
    
    def check_in(self, student_id, course_name):
        """Record a student's check-in for a course"""
        student_exists = any(s.user_id == student_id for s in self.students)
        if not student_exists:
            print(f"No student found with ID {student_id}")
            return False
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "student_id": student_id,
            "course_name": course_name,
            "timestamp": timestamp
        }
        self.attendance.append(record)
        
        for student in self.students:
            if student.user_id == student_id:
                student.attendance.append({"course": course_name, "time": timestamp})
                break
        
        print(f"Student {student_id} checked in! Course: {course_name} Time: {timestamp}")
        self._save_data()
        return True
    
    def view_attendance(self):
        """Display all attendance records"""
        if not self.attendance:
            print("No attendance records found.")
            return
        
        print("\n" + "="*50)
        print("Attendance Records")
        print("="*50)
        for record in self.attendance:
            print(f"Student ID: {record['student_id']} | Course: {record['course_name']} | Time: {record['timestamp']}")
        print("="*50)