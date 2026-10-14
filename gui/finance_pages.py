import streamlit as st
import pandas as pd

def show_finance_page(manager):
    """Renders the UI for all financial operations."""
    st.header("Finance & Payments")

    # Build a mapping from display label -> student_id
    students = manager.get_all_students()
    if not students:
        st.warning("There are no students yet. Please add a student first.")
        return

    student_list = {f"{s['ID']} - {s['Name']}": s['ID'] for s in students}

    # Record a Payment
    st.subheader("Record New Payment")
    with st.form("payment_form"):
        selected_student_label = st.selectbox("Select Student", list(student_list.keys()))
        amount = st.number_input("Payment Amount", min_value=0.01, step=1.0, format="%.2f")
        method = st.text_input("Payment Method (e.g., Credit Card, Cash)")

        submitted = st.form_submit_button("Record Payment")
        if submitted:
            if not method.strip():
                st.error("Payment method cannot be empty.")
            else:
                student_id = student_list[selected_student_label]
                ok = manager.record_payment(student_id, amount, method)
                if ok:
                    st.success(f"Payment of {amount} for {selected_student_label} recorded.")
                    st.rerun()
                else:
                    st.error("Fail to record payment.")

    st.divider()

    # view payment history
    st.subheader("View Student Payment History")
    history_student_label = st.selectbox(
        "Select Student to View History",
        list(student_list.keys()),
        key="history_student"
    )
    if history_student_label:
        history_student_id = student_list[history_student_label]
        history = manager.get_payment_history(history_student_id)
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("This student has no payment history.")

    st.divider()

    # export report
    st.subheader("Export Report")
    with st.form("export_report_form"):
        kind = st.selectbox("Report Type", ["finance", "attendance"])
        out_path = st.text_input("Output File Path", value="report.csv")
        export_submitted = st.form_submit_button("Export")
        if export_submitted:
            if not out_path.strip():
                st.error("Output path cannot be empty.")
            else:
                ok = manager.export_report(kind, out_path)
                if ok:
                    st.success(f"Report exported to {out_path}")
                else:
                    st.error("Fail to export report.")