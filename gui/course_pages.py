import streamlit as st


def show_course_management_page(manager):
    st.header("Course Management")

    st.subheader("Add Course")

    teachers = manager.get_all_teachers()
    if not teachers:
        st.warning("No teachers available yet. Please add a teacher first.")
    else:
        teacher_options = {f"{t['ID']} - {t['Name']}": t['ID'] for t in teachers}

        with st.form("add_course_form"):
            name = st.text_input("Course Name")
            teacher_key = st.selectbox("Teacher", list(teacher_options.keys()))
            instrument = st.selectbox(
                "Instrument",
                ["piano", "guitar", "violin", "drums", "flute"]
            )
            day = st.selectbox(
                "Day",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            )
            time = st.text_input("Time (e.g. 15:00)")
            submitted = st.form_submit_button("Add")

            if submitted:
                if not name:
                    st.error("Course name cannot be empty.")
                else:
                    teacher_id = teacher_options[teacher_key]
                    ok = manager.add_course(name, teacher_id, instrument, day, time)
                    if ok:
                        st.success(f"Course added: {name}")
                        st.rerun()
                    else:
                        st.error("Failed to add course. Check the terminal output.")

    st.divider()
    st.subheader("Course List")
    courses = manager.get_all_courses()
    if courses:
        st.dataframe(courses, use_container_width=True)
    else:
        st.info("No course records.")

    st.divider()
    st.subheader("Remove Course")
    if courses:
        course_options = {f"{c['ID']} - {c['Name']}": c['ID'] for c in courses}
        with st.form("remove_course_form"):
            key = st.selectbox("Select a course to remove", list(course_options.keys()))
            del_submitted = st.form_submit_button("Remove")
            if del_submitted:
                cid = course_options[key]
                ok = manager.remove_course(cid)
                if ok:
                    st.success("Course removed.")
                    st.rerun()
                else:
                    st.error("Failed to remove course.")