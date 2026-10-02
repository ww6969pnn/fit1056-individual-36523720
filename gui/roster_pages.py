import streamlit as st


def show_roster_page(manager):
    st.header("Daily Roster and Check-in")

    st.subheader("Daily Roster")
    day = st.selectbox(
        "Select Day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    roster = manager.get_daily_roster(day)
    if roster:
        st.dataframe(roster, use_container_width=True)
    else:
        st.info(f"No courses scheduled on {day}.")

    st.divider()
    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        student_id = st.text_input("Student ID")
        course_name = st.text_input("Course Name")
        submitted = st.form_submit_button("Check In")

        if submitted:
            try:
                sid = int(student_id)
            except ValueError:
                st.error("Student ID must be a number.")
            else:
                ok = manager.check_in(sid, course_name)
                if ok:
                    st.success("Check-in successful.")
                    st.rerun()
                else:
                    st.error("Check-in failed: student not found / course not found / student not enrolled.")

    st.divider()
    st.subheader("Attendance Records")
    records = manager.get_attendance_records()
    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.info("No attendance records.")