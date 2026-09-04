from app.user import User

class StudentUser(User):
    """Student class, from User"""
    def __init__(self, user_id, name, enrolled_in=None):
        super().__init__(user_id, name)
        self.enrolled_in = enrolled_in if enrolled_in else []
        self.attendance = []

    def __str__(self):
        courses = ', '.join(self.enrolled_In) if self.enrolled_in else 'Not taking ant courses'
        return f"{self.name} (student: ID: {self.user_id}, Courses: {courses})"
    