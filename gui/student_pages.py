import streamlit as st

def show_student_management_page(manager):
    st.header("Student Management")

    st.subheader("Add Students")
    st.caption("Name should not exceed 15 characters; Instruments supported only: piano, guitar, violin, drums, flute")
    
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        courses_input = st.text_input("Couse (Comma-separated, e.g. piano, guitar)")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name:
                st.error("The name cannot be empty.")
            else:
                courses = [c.strip() for c in courses_input.split(",")] if courses_input else []

                ok = manager.add_student(name, courses)
                if ok:
                    st.success(f"Student added: {name}")
                else:
                    st.error("Addition failed. Please check the length of the name and whether the instrument is valid.")

    st.divider()

    #students list + delete students
    st.subheader("All Students")
    students = manager.get_all_students()
    if students:
        st.dataframe(students, use_container_width=True)

        st.subheader("Delete Students")
        with st.form("delete_student_form"):
            sid = st.text_input("The student ID to be deleted")
            delete_submitted = st.form_submit_button("Delete")
            if delete_submitted:
                try:
                    sid_int = int(sid)
                    ok = manager.remove_student(sid_int)
                    if ok:
                        st.success("Student deleted: {sid_int}")
                        st.rerun()
                    else:
                        st.error("No student with this ID was found.")
                except ValueError:
                    st.error("Invalid student ID")
    else:
        st.info("No student records available.")
