import streamlit as st
from menu.cost_management import CostManagement
from menu.general_results import GeneralResults
from menu.management_billing import ManegementBilling
from menu.page import Page
from utils.components import *
from utils.user import logout
from data.get_data import *
from streamlit_theme import st_theme

def render():
    # pegando dados da sessão como ID e NOME
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']
    theme = st_theme(key=f"theme_")
    base_theme = theme.get("base") if theme else "default"
    st.session_state["base_theme"] = base_theme
    col1, col2, col3 = st.columns([3,0.6,0.3])
    
    col1.write(f"## Olá, "+user_name)
    col2.image("./assets/imgs/staff.png")
    col3.markdown("<p style='padding-top:0.0em'></p>", unsafe_allow_html=True)
    col3.button(label="Logout", on_click=logout)
    
    component_effect_underline()
    st.write('## Resultados')
    st.markdown('<div class="full-width-line-white"></div>', unsafe_allow_html=True)
    st.markdown('<div class="full-width-line-black"></div>', unsafe_allow_html=True)

    col6, col7, col8, = st.columns([3.4,0.2,0.4])
    col8.button(label="Atualizar", on_click = st.cache_data.clear)
    
    data = initialize_data(user_id)
    # data = get_data(data) 
    tab1, tab2, tab3 = st.tabs(["Resultados Gerais","Faturamento Estaff Gerencial", "Gerenciamento de Custos"])
    
    with tab1:
        page = GeneralResults()

    with tab2:
        page = ManegementBilling()
    
    with tab3:
        page = CostManagement()

if __name__ == "__main__":
    if 'jwt_token' not in st.session_state:
        st.switch_page("main.py")
    
    st.set_page_config(page_title="Home | Resultados Estaff",page_icon="./assets/imgs/staff-logo.png", layout="wide")

    component_hide_sidebar()
    component_fix_tab_echarts()

    if 'user_data' in st.session_state:
        render()
    else:
        st.switch_page("main.py")