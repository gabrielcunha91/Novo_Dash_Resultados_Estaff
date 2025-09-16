import streamlit as st
    
def logout():
    st.session_state.clear()
    st.session_state['page'] = 'login'
    st.cache_data.clear()