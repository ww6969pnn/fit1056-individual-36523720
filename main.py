import sys
import os
from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data

# Endure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    import streamlit as st
    if "app_initialised" not in st.session_state:
        log_path    = os.path.join(BASE_DIR, "msms.log")
        data_path   = os.path.join(BASE_DIR, "data", "msms.json")
        backup_dir  = os.path.join(BASE_DIR, "data", "backups")

        # Set up logging first
        init_logger(log_path)

        # Bach up the data file before the session starts
        backup_data(data_path, backup_dir)

        st.session_state.app_initialised = True

    launch()
