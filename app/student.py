from app.user import User

class StudentUser(User):
    """Student class, from User"""
    def __init__(self, user_id, name, enrolled_course_ids=None):
        super().__init__(user_id, name)
        self.enrolled_course_ids = enrolled_course_ids or []
        self.attendance = []

    def __str__(self):
        if self.enrolled_course_ids:
            courses = ', '.join(str(cid) for cid in self.enrolled_course_ids)
        else:
            courses = 'Not taking any courses'
        return f"{self.name} (student: ID: {self.user_id}, Courses: {courses})"
    