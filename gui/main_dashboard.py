import streamlit as st
from app.schedule import ScheduleManager

from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page
from gui.course_pages import show_course_management_page


def launch():
    st.set_page_config(page_title="MSMS", layout="wide")

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Student Management", "Course Management", "Daily Roster"]
    )

    if page == "Student Management":
        show_student_management_page(manager)
    elif page == "Course Management":
        show_course_management_page(manager)
    elif page == "Daily Roster":
        show_roster_page(manager)