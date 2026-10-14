import streamlit as st
from app.schedule import ALLOWED_INSTRUMENTS


def show_teacher_management_page(manager):
    st.header("Teacher Management")

    # ---------- Add Teacher ----------
    st.subheader("Add Teacher")

    with st.form("add_teacher_form"):
        name = st.text_input("Teacher Name").strip()
        specialty = st.selectbox("Specialty", sorted(ALLOWED_INSTRUMENTS))
        submitted = st.form_submit_button("Add")

        if submitted:
            if not name:
                st.error("Teacher name cannot be empty.")
            else:
                ok = manager.add_teacher(name, specialty)
                if ok:
                    st.success(f"Teacher added: {name}")
                    st.rerun()
                else:
                    st.error("Failed to add teacher. Check the terminal output.")

    st.divider()

    # ---------- Teacher List ----------
    st.subheader("Teacher List")
    teachers = manager.get_all_teachers()
    if teachers:
        st.dataframe(teachers, use_container_width=True)
    else:
        st.info("No teacher records.")

    st.divider()

    # ---------- Remove Teacher ----------
    st.subheader("Remove Teacher")
    if teachers:
        teacher_options = {f"{t['ID']} - {t['Name']}": t['ID'] for t in teachers}
        with st.form("remove_teacher_form"):
            key = st.selectbox("Select a teacher to remove", list(teacher_options.keys()))
            del_submitted = st.form_submit_button("Remove")
            if del_submitted:
                tid = teacher_options[key]
                ok = manager.remove_teacher(tid)
                if ok:
                    st.success("Teacher removed.")
                    st.rerun()
                else:
                    st.error(manager.last_error or "Failed to remove teacher.")