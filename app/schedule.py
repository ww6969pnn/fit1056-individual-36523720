import json
import os
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

ALLOWED_INSTRUMENTS = {"piano", "guitar", "violin", "drums", "flute"}
ALLOWED_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}


class ScheduleManager:
    """Main manager class - handles all data operations"""

    def __init__(self, data_file=None):
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
        self.next_course_id = 1

        self._load_data()

    # ---------- Persistence ----------

    def _load_data(self):
        """Load data from JSON file and reconstruct objects"""
        if not os.path.exists(self.data_file):
            print("Data file not found. Creating new data...")
            self._save_data()
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Students
            for student_data in data.get('students', []):
                student = StudentUser(
                    student_data['id'],
                    student_data['name'],
                    student_data.get('enrolled_course_ids', [])
                )
                student.attendance = student_data.get('attendance', [])
                self.students.append(student)

            # Teachers
            for teacher_data in data.get('teachers', []):
                teacher = TeacherUser(
                    teacher_data['id'],
                    teacher_data['name'],
                    teacher_data.get('specialty', '')
                )
                self.teachers.append(teacher)

            # Courses (must be after teachers so we can link teacher objects)
            teacher_by_id = {t.user_id: t for t in self.teachers}
            for course_data in data.get('courses', []):
                teacher = teacher_by_id.get(course_data.get('teacher_id'))
                course = Course(
                    course_data['course_id'],
                    course_data['name'],
                    teacher,
                    course_data.get('instrument', ''),
                    course_data.get('day'),
                    course_data.get('time')
                )
                course.enrolled_student_ids = course_data.get('enrolled_student_ids', [])
                course.lessons = course_data.get('lessons', [])
                self.courses.append(course)

            self.attendance = data.get('attendance', [])
            self.next_student_id = int(data.get('next_student_id', 1))
            self.next_teacher_id = int(data.get('next_teacher_id', 1))
            self.next_course_id = int(data.get('next_course_id', 1))

            print(f"Successfully loaded: {len(self.students)} students, "
                  f"{len(self.teachers)} teachers, {len(self.courses)} courses")

        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def _save_data(self):
        """Save all data to JSON file"""
        try:
            students_data = []
            for s in self.students:
                students_data.append({
                    'id': s.user_id,
                    'name': s.name,
                    'enrolled_course_ids': s.enrolled_course_ids,
                    'attendance': s.attendance
                })

            teachers_data = []
            for t in self.teachers:
                teachers_data.append({
                    'id': t.user_id,
                    'name': t.name,
                    'specialty': t.specialty
                })

            courses_data = []
            for c in self.courses:
                courses_data.append({
                    'course_id': c.course_id,
                    'name': c.name,
                    'teacher_id': c.teacher.user_id if c.teacher else None,
                    'instrument': c.instrument,
                    'day': c.day,
                    'time': c.time,
                    'enrolled_student_ids': c.enrolled_student_ids,
                    'lessons': c.lessons
                })

            all_data = {
                'students': students_data,
                'teachers': teachers_data,
                'courses': courses_data,
                'attendance': self.attendance,
                'next_student_id': self.next_student_id,
                'next_teacher_id': self.next_teacher_id,
                'next_course_id': self.next_course_id
            }

            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

            print("Data saved successfully")

        except Exception as e:
            print(f"Error saving data: {e}")

    # ---------- Student Management ----------

    def add_student(self, name, course_ids=None):
        """Add a new student. course_ids is a list of ints."""
        if course_ids is None:
            course_ids = []

        if not name:
            print("Error: Name cannot be empty.")
            return False

        if name.isdigit():
            print("Error: Name cannot be a series of numbers.")
            return False

        if len(name) > 15:
            print("Error: Name is too long! Maximum 15 characters.")
            return False

        # Validate that all course IDs exist
        for cid in course_ids:
            if not any(c.course_id == cid for c in self.courses):
                print(f"Course ID {cid} does not exist.")
                return False

        student_id = self.next_student_id
        student = StudentUser(student_id, name, list(course_ids))
        self.students.append(student)
        self.next_student_id += 1

        # Update each course's enrolled_student_ids
        for cid in course_ids:
            course = next((c for c in self.courses if c.course_id == cid), None)
            if course and student_id not in course.enrolled_student_ids:
                course.enrolled_student_ids.append(student_id)

        print(f"Student '{name}' added successfully! ID: {student_id}")
        self._save_data()
        return True

    def list_all_students(self):
        """Display all students"""
        if not self.students:
            print("No student records found.")
            return

        print("\n" + "=" * 50)
        for student in self.students:
            courses = ', '.join(str(cid) for cid in student.enrolled_course_ids) \
                if student.enrolled_course_ids else 'No courses'
            print(f"ID: {student.user_id} | Name: {student.name} | Courses: {courses}")
        print("=" * 50)

    def update_student(self, student_id, **fields):
        """Update a student's information. Supports 'name' and 'enrolled_course_ids'."""
        for student in self.students:
            if student.user_id == student_id:
                if 'name' in fields:
                    if len(fields['name']) > 15:
                        print("Error: Name is too long!")
                        return False
                    student.name = fields['name']

                if 'enrolled_course_ids' in fields:
                    new_ids = fields['enrolled_course_ids']
                    for cid in new_ids:
                        if not any(c.course_id == cid for c in self.courses):
                            print(f"Course ID {cid} does not exist.")
                            return False

                    # Keep course.enrolled_student_ids in sync
                    old_ids = set(student.enrolled_course_ids)
                    new_ids_set = set(new_ids)

                    for cid in old_ids - new_ids_set:
                        course = next((c for c in self.courses if c.course_id == cid), None)
                        if course and student_id in course.enrolled_student_ids:
                            course.enrolled_student_ids.remove(student_id)

                    for cid in new_ids_set - old_ids:
                        course = next((c for c in self.courses if c.course_id == cid), None)
                        if course and student_id not in course.enrolled_student_ids:
                            course.enrolled_student_ids.append(student_id)

                    student.enrolled_course_ids = list(new_ids)

                print(f"Student ID {student_id} has been updated.")
                self._save_data()
                return True

        print(f"No student found with ID {student_id}")
        return False

    def remove_student(self, student_id):
        """Delete a student from the system"""
        student = next((s for s in self.students if s.user_id == student_id), None)
        if not student:
            print(f"No student found with ID {student_id}")
            return False

        # Remove the student from every course's enrolled_student_ids
        for course in self.courses:
            if student_id in course.enrolled_student_ids:
                course.enrolled_student_ids.remove(student_id)

        self.students = [s for s in self.students if s.user_id != student_id]
        print(f"Student ID {student_id} has been deleted.")
        self._save_data()
        return True

    # ---------- Teacher Management ----------

    def add_teacher(self, name, specialty):
        """Add a new teacher to the system"""
        if not name:
            print("Error: Name cannot be empty.")
            return False

        if name.isdigit():
            print("Error: Name cannot be a series of numbers.")
            return False

        if len(name) > 15:
            print("Error: Name is too long! Maximum 15 characters.")
            return False

        if specialty.lower() not in ALLOWED_INSTRUMENTS:
            print(f"Invalid specialty '{specialty}'. Allowed: {ALLOWED_INSTRUMENTS}")
            return False

        teacher_id = self.next_teacher_id
        teacher = TeacherUser(teacher_id, name, specialty)
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

        print("\n" + "=" * 50)
        print("List of all teachers")
        print("=" * 50)
        for teacher in self.teachers:
            print(f"ID: {teacher.user_id} | Name: {teacher.name} | Specialty: {teacher.specialty}")
        print("=" * 50)

    def update_teacher(self, teacher_id, **fields):
        """Update a teacher's information"""
        for teacher in self.teachers:
            if teacher.user_id == teacher_id:
                if 'name' in fields:
                    if len(fields['name']) > 15:
                        print("Error: Name is too long!")
                        return False
                    teacher.name = fields['name']

                if 'specialty' in fields:
                    if fields['specialty'].lower() not in ALLOWED_INSTRUMENTS:
                        print("Invalid specialty")
                        return False
                    teacher.specialty = fields['specialty']

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

    # ---------- Course Management ----------

    def add_course(self, name, teacher_id, instrument, day=None, time=None):
        """Add a new course"""
        if not name:
            print("Error: Course name cannot be empty.")
            return False

        teacher = next((t for t in self.teachers if t.user_id == teacher_id), None)
        if not teacher:
            print(f"Teacher ID {teacher_id} does not exist.")
            return False

        if instrument.lower() not in ALLOWED_INSTRUMENTS:
            print(f"Invalid instrument '{instrument}'. Allowed: {ALLOWED_INSTRUMENTS}")
            return False

        if day and day not in ALLOWED_DAYS:
            print(f"Invalid day '{day}'. Allowed: {ALLOWED_DAYS}")
            return False

        course_id = self.next_course_id
        course = Course(course_id, name, teacher, instrument, day, time)
        if day and time:
            course.lessons.append({"day": day, "time": time})

        self.courses.append(course)
        self.next_course_id += 1

        print(f"Course '{name}' added successfully! ID: {course_id}")
        self._save_data()
        return True

    def list_all_courses(self):
        """Display all courses"""
        if not self.courses:
            print("No course records found.")
            return
        print("\n" + "=" * 50)
        for c in self.courses:
            teacher_name = c.teacher.name if c.teacher else "None"
            print(f"ID: {c.course_id} | Name: {c.name} | Teacher: {teacher_name} "
                  f"| Instrument: {c.instrument} | Day: {c.day} | Time: {c.time}")
        print("=" * 50)

    def remove_course(self, course_id):
        """Delete a course"""
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if not course:
            print(f"No course found with ID {course_id}")
            return False

        # Remove this course from every student's enrolled_course_ids
        for student in self.students:
            if course_id in student.enrolled_course_ids:
                student.enrolled_course_ids.remove(course_id)

        self.courses = [c for c in self.courses if c.course_id != course_id]
        print(f"Course ID {course_id} has been deleted.")
        self._save_data()
        return True

    def get_course_by_name(self, name):
        """Return a Course object or None"""
        return next((c for c in self.courses if c.name.lower() == name.lower()), None)

    def get_course_by_id(self, course_id):
        """Return a Course object or None"""
        return next((c for c in self.courses if c.course_id == course_id), None)

    def get_daily_roster(self, day):
        """Return the list of courses for a given day, with check-in info"""
        roster = []
        for c in self.courses:
            if c.day and c.day.lower() == day.lower():
                roster.append({
                    "Course ID": c.course_id,
                    "Course Name": c.name,
                    "Teacher": c.teacher.name if c.teacher else "None",
                    "Instrument": c.instrument,
                    "Time": c.time or "TBA",
                    "Enrolled": len(c.enrolled_student_ids)
                })
        return roster

    def switch_course(self, student_id, source_course_name, dest_course_name):
        """Move a student from one course to another"""
        student = next((s for s in self.students if s.user_id == student_id), None)
        if not student:
            print(f"No student found with ID {student_id}")
            return False

        source = self.get_course_by_name(source_course_name)
        dest = self.get_course_by_name(dest_course_name)
        if not source or not dest:
            print("Source or destination course does not exist.")
            return False

        if source.course_id not in student.enrolled_course_ids:
            print(f"{student.name} is not enrolled in '{source_course_name}'")
            return False

        if dest.course_id in student.enrolled_course_ids:
            print(f"{student.name} is already enrolled in '{dest_course_name}'")
            return False

        student.enrolled_course_ids.remove(source.course_id)
        if student_id in source.enrolled_student_ids:
            source.enrolled_student_ids.remove(student_id)

        student.enrolled_course_ids.append(dest.course_id)
        if student_id not in dest.enrolled_student_ids:
            dest.enrolled_student_ids.append(student_id)

        print(f"{student.name} switched from '{source_course_name}' to '{dest_course_name}'")
        self._save_data()
        return True

    # ---------- Check-in ----------

    def check_in(self, student_id, course_name):
        """Record a student's check-in for a course"""
        student = next((s for s in self.students if s.user_id == student_id), None)
        if not student:
            print(f"No student found with ID {student_id}")
            return False

        course = self.get_course_by_name(course_name)
        if not course:
            print(f"Course '{course_name}' does not exist.")
            return False

        if course.course_id not in student.enrolled_course_ids:
            print(f"Error: {student.name} is not enrolled in '{course_name}'")
            enrolled_names = [
                c.name for c in self.courses
                if c.course_id in student.enrolled_course_ids
            ]
            print(f"Enrolled courses: {', '.join(enrolled_names)}")
            return False

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.attendance.append({
            "student_id": student_id,
            "course_name": course_name,
            "timestamp": timestamp
        })
        student.attendance.append({"course": course_name, "time": timestamp})

        print(f"Student {student_id} checked in! Course: {course_name} Time: {timestamp}")
        self._save_data()
        return True

    def view_attendance(self):
        """Display all attendance records"""
        if not self.attendance:
            print("No attendance records found.")
            return

        print("\n" + "=" * 50)
        print("Attendance Records")
        print("=" * 50)
        for record in self.attendance:
            print(f"Student ID: {record['student_id']} | "
                  f"Course: {record['course_name']} | Time: {record['timestamp']}")
        print("=" * 50)

    # ---------- GUI data reading ----------

    def get_all_students(self):
        """Return the student list (dict form) for the GUI"""
        def course_names(student):
            names = [
                c.name for c in self.courses
                if c.course_id in student.enrolled_course_ids
            ]
            return ", ".join(names) if names else "No courses"

        return [
            {
                "ID": s.user_id,
                "Name": s.name,
                "Courses": course_names(s)
            }
            for s in self.students
        ]

    def get_all_teachers(self):
        """Return the teacher list (dict form) for the GUI"""
        return [
            {"ID": t.user_id, "Name": t.name, "Specialty": t.specialty}
            for t in self.teachers
        ]

    def get_all_courses(self):
        """Return the course list (dict form) for the GUI"""
        return [
            {
                "ID": c.course_id,
                "Name": c.name,
                "Teacher": c.teacher.name if c.teacher else "None",
                "Instrument": c.instrument,
                "Day": c.day or "TBA",
                "Time": c.time or "TBA",
                "Enrolled": len(c.enrolled_student_ids)
            }
            for c in self.courses
        ]

    def get_attendance_records(self):
        """Return the attendance record list (dict form) for the GUI"""
        return [
            {
                "Student ID": r["student_id"],
                "Course": r["course_name"],
                "Time": r["timestamp"]
            }
            for r in self.attendance
        ]