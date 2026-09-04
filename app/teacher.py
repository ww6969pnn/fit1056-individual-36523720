from app.user import User

class TeacherUser(User):
    """Teacher class, from User"""
    def __init__(self, user_id, name, speciality):
        super().__init__(user_id, name)
        self.speciality = speciality

    def __str__(self):
        return f"{self.name} (Teacher: ID: {self.user_id}, Speciality: {self.speciality})"

class Course:
    """course class"""
    def __init__(self, course_id, name, teacher, instrument):
        self.course_id = course_id
        self.name = name
        self.teacher = teacher
        self.instrument = instrument
        self.students = []

    def __str__(self):
        return f"{self.name} (Teacher: {self.teacher.name}, Instrument: {self.instrument})"