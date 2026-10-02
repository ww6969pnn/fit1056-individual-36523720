import streamlit as st

def show_roster_page(manager):
    st.header("Daily schedule and attendance registration")

    st.subheader("Student attendance registration")
    with st.form("check_in_form"):
        student_id = st.text_input("Student ID")
        course_name = st.text_input("Course Name")
        submitted = st.form_submit_button("Check In")

        if submitted:
            try:
                sid = int(student_id)
            except ValueError:
                st.error("The student ID must be a series of numbers.")
            else:
                ok = manager.check_in(sid, course_name)
                if ok:
                    st.success("Sign-in successful")
                else:
                    st.error("Sign-in failed: The student does not exist, or the student has not registered for this course.")

    st.divider()
    st.subheader("Attendance Record")
    records = manager.get_attendance_records()
    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.info("No attendance record available.")
        