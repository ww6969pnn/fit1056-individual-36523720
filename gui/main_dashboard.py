import streamlit as st
from app.schedule import ScheduleManager

from gui.student_pages import show_student_management_page
from gui.roster_pages import show_roster_page

def launch():
    st.set_page_config(page_title="MSMS", layout="wide")

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio("Selection Page", ["Student Management", "Daily Schedule"])

    if page == "Student Management":
        show_student_management_page(manager)
    elif page == "Daily Schedule":
        show_roster_page(manager)
        