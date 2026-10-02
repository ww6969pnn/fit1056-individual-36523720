from app.user import User


class TeacherUser(User):
    """Teacher class, inherits from User"""

    def __init__(self, user_id, name, specialty):
        super().__init__(user_id, name)
        self.specialty = specialty

    def __str__(self):
        return f"{self.name} (Teacher ID: {self.user_id}), Specialty: {self.specialty}"


class Course:
    """Course class"""

    def __init__(self, course_id, name, teacher, instrument, day=None, time=None):
        self.course_id = course_id
        self.name = name
        self.teacher = teacher
        self.instrument = instrument
        self.day = day
        self.time = time
        self.enrolled_student_ids = []
        self.lessons = []

    def __str__(self):
        teacher_name = self.teacher.name if self.teacher else "No teacher"
        return f"{self.name} (Teacher: {teacher_name}, Instrument: {self.instrument})"