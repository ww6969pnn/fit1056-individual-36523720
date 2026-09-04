class User:
    """Basic user class, the parent class of students and teachers"""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f"{self.name}(ID: {self.user_id})"