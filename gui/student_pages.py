import streamlit as st

def show_student_management_page(manager):
    st.header("Student Management")

    st.subheader("Add Students")
    st.caption("Name should not exceed 15 characters; Instruments supported only: piano, guitar, violin, drums, flute")
    
    all_courses = manager.get_all_courses() 

    if not all_courses:
        st.warning("There are no courses yet. Please create a course first.")
    else:
        course_options = {f"{c['ID']} - {c['Name']}": c['ID'] for c in all_courses}

        with st.form("add_student_form"):
            name = st.text_input("Student Name").strip()
            selected = st.multiselect("Choose courses", list(course_options.keys()))
            submitted = st.form_submit_button("Submit")

            if submitted:
                if not name:
                    st.error("Name cannot be empty")
                else:
                    course_ids = [course_options[s] for s in selected]
                    ok = manager.add_student(name, course_ids)
                    if ok:
                        st.success(f"Student added: {name}")
                        st.rerun()
                    else:
                        st.error("Fail to add.")

    st.divider()
    st.subheader("Student List")
    students = manager.get_all_students()
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No student records available.")

    #remove student
    st.divider()
    st.subheader("Remove Student")
    if students:
        student_options = {f"{s['ID']} - {s['Name']}": s['ID'] for s in students}
        with st.form("remove_student_form"):
            key = st.selectbox("Select a student to remove", list(student_options.keys()))
            del_submitted = st.form_submit_button("Remove")
            if del_submitted:
                sid = student_options[key]
                ok = manager.remove_student(sid)
                if ok:
                    st.success("Student removed.")
                    st.rerun()
                else:
                    st.error(manager.last_error or "Failed to remove student.")
    else:
        st.info("No student records to remove.")
