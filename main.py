import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.schedule import ScheduleManager


def display_menu():
    """Display the main menu options"""
    print("\n" + "="*45)
    print("Music School Management System v3.0 (OOP)")
    print("="*45)
    print("[Student Management]")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("[Teacher Management]")
    print("5. Add Teacher")
    print("6. View All Teachers")
    print("7. Update Teacher")
    print("8. Delete Teacher")
    print("[Check-in]")
    print("9. Student Check-in")
    print("10. View Attendance")
    print("q. Quit and Save")
    print("="*45)


def main():
    """Main program entry point"""
    manager = ScheduleManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == '1':
            name = input("Student name: ").strip()
            if not name:
                print("Name cannot be empty")
                continue
            
            courses_input = input("Enrolled courses (comma-separated, e.g., piano,guitar): ").strip()
            courses = [c.strip() for c in courses_input.split(',')] if courses_input else []
            manager.add_student(name, courses)
        
        elif choice == '2':
            manager.list_all_students()
        
        elif choice == '3':
            try:
                student_id = int(input("Enter student ID: "))
                print("Enter fields to update (leave blank to skip):")
                name = input("New name: ").strip()
                courses_input = input("New courses (comma-separated): ").strip()
                
                fields = {}
                if name:
                    fields['name'] = name
                if courses_input:
                    new_courses = [c.strip() for c in courses_input.split(',')]
                    fields['enrolled_in'] = new_courses
                
                if fields:
                    manager.update_student(student_id, **fields)
                else:
                    print("No fields to update")
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '4':
            try:
                student_id = int(input("Enter student ID to delete: "))
                manager.remove_student(student_id)
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '5':
            name = input("Teacher name: ").strip()
            if not name:
                print("Name cannot be empty")
                continue
            speciality = input("Teaching speciality: ").strip()
            manager.add_teacher(name, speciality)
        
        elif choice == '6':
            manager.list_all_teachers()
        
        elif choice == '7':
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
                    manager.update_teacher(teacher_id, **fields)
                else:
                    print("No fields to update")
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '8':
            try:
                teacher_id = int(input("Enter teacher ID to delete: "))
                manager.remove_teacher(teacher_id)
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '9':
            try:
                student_id = int(input("Enter student ID: "))
                course_name = input("Enter course name: ").strip()
                manager.check_in(student_id, course_name)
            except ValueError:
                print("Please enter a valid numeric ID")
        
        elif choice == '10':
            manager.view_attendance()
        
        elif choice == 'q':
            print("Saving and exiting...")
            manager._save_data()
            break
        
        else:
            print("Invalid option, please try again")


if __name__ == "__main__":
    main()