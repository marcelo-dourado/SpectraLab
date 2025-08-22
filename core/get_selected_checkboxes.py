import streamlit as st

def get_selected_checkboxes():
    checkbox_on = {}
    for key in st.session_state:
        if key.startswith("checkbox_"):
            if st.session_state[key]:
                checkbox_on.update({key[-2:]: st.session_state[key]})
    return checkbox_on