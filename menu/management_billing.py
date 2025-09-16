import streamlit as st
from data.querys_estaff import *
from menu.page import Page
from utils.components import *
from utils.functions import *
from datetime import date, datetime

def BuildManegementBilling(generalRevenue, groupsCompanies, generalRevenueOportunity, generalRevenueEvents, generalRevenueBrigada): #estabelecimentoTransaction

    row1 = st.columns(6)
    global day_ManegementBilling1, day_ManegementBilling2
    
    with row1[2]:
        day_ManegementBilling1 = st.date_input('Data Inicio:', value=datetime(2024, 1, 1).date(), format='DD/MM/YYYY', key='day_ManegementBilling1') 
    with row1[3]:
        day_ManegementBilling2 = st.date_input('Data Final:', value=datetime.today().date(), format='DD/MM/YYYY', key='day_ManegementBilling2')

    
    row2 = st.columns([1])#st.columns([2,0.8])

    with row2[0]:
        generalRevenue = general_revenue(day_ManegementBilling1, day_ManegementBilling2, filters='')
        generalRevenue = function_format_numeric_columns(generalRevenue, ['Valor Bruto B2B', 'Taxa B2B', 'Total Oportunidade', 'Total Extra', 'Valor Freela','Valor Transac. Eventos', 'Taxa Eventos', 'Taxa Brigada Fixa','Faturamento Total'])
        generalRevenue = generalRevenue.drop(['Total Oportunidade', 'Total Extra', 'Valor Freela'], axis=1)
        filtered_copy, count = component_plotDataframe(generalRevenue, "Faturamento Estaff Gerencial")
        function_copy_dataframe_as_tsv(filtered_copy)

    # with row2[1]:
    #     estabelecimentoTransaction = estabelecimento_transaction(day_ManegementBilling1, day_ManegementBilling2)
    #     estabelecimentoTransaction = function_format_numeric_columns(estabelecimentoTransaction, ['Valor Transac.'])
    #     filtered_copy, count = component_plotDataframe(estabelecimentoTransaction, "Transações Por Estabelecimento")
    #     function_copy_dataframe_as_tsv(filtered_copy)

    col1, col2 = st.columns(2)
    with col1:
        groupsCompanies = groups_companies(day_ManegementBilling1, day_ManegementBilling2)
        selected_groups = st.multiselect("Selecione um grupo:", ['Outros'] + sorted(filter(None, groupsCompanies['GRUPO'].unique())), default=[], placeholder='Grupos')

    filters = ''
    select_companies = []

    if selected_groups:
        selected_groups.append(None)
        groupsCompanies_filtered = groupsCompanies[groupsCompanies['GRUPO'].isin(selected_groups)]

        selected_groups_str = ", ".join(f"'{group}'" for group in selected_groups)

        if "Outros" in selected_groups:
            filters = f"AND (TCG.NOME IN ({selected_groups_str}) OR (TCG.NOME IS NULL))"
        else:
            filters = f"AND TCG.NOME IN ({selected_groups_str})"

        with col2:
            if "Outros" not in selected_groups:
                groupsCompanies_filtered = groupsCompanies_filtered.dropna(subset=['GRUPO'])

            select_companies = st.multiselect("Selecione as casas:", groupsCompanies_filtered['ESTABELECIMENTO'].unique(), placeholder='Casas')
        
        if select_companies:
            groupsCompanies_filtered = groupsCompanies_filtered[groupsCompanies_filtered['ESTABELECIMENTO'].isin(select_companies)]

        if select_companies:
            select_companies_str = ", ".join(f"'{company}'" for company in select_companies)
            if "Outros" in selected_groups:
                filters += f" AND (TC.NAME IN ({select_companies_str}) OR TCG.NOME IS NULL)"
            else:
                filters += f" AND TC.NAME IN ({select_companies_str})"
        
        generalRevenue = general_revenue(day_ManegementBilling1, day_ManegementBilling2, filters)
        generalRevenue = function_format_numeric_columns(generalRevenue, ['Valor Bruto B2B', 'Taxa B2B', 'Total Oportunidade', 'Total Extra', 'Valor Freela','Valor Transac. Eventos', 'Taxa Eventos', 'Taxa Brigada Fixa','Faturamento Total'])
        filtered_copy, count = component_plotDataframe(generalRevenue, "Faturamento Detalhado")
        function_copy_dataframe_as_tsv(filtered_copy)


        with st.expander("📊 Abertura por Oportunidade", expanded=False):
            generalRevenueOportunity = general_revenue_oportunity(day_ManegementBilling1, day_ManegementBilling2, filters)
            generalRevenueOportunity = function_format_numeric_columns(generalRevenueOportunity, ['VALOR BRUTO P', 'VALOR OPORTUNIDADE', 'VALOR EXTRA', 'VALOR FREELA', 'VALOR STAFF'])
            filtered_copy, count = component_plotDataframe(generalRevenueOportunity, "Abertura por Oportunidade")
            function_copy_dataframe_as_tsv(filtered_copy)

        with st.expander("📊 Abertura por Evento", expanded=False):
            generalRevenueEvents = general_revenue_events(day_ManegementBilling1, day_ManegementBilling2, filters)
            generalRevenueEvents = function_format_numeric_columns(generalRevenueEvents, ['VALOR BRUTO', 'VALOR LIQUIDO', 'CUSTO EXTRA', 'TAXA EVENTO'])
            filtered_copy, count = component_plotDataframe(generalRevenueEvents, "Abertura por Evento")
            function_copy_dataframe_as_tsv(filtered_copy)

        with st.expander("📊 Abertura por Brigada", expanded=False):
            generalRevenueBrigada = general_revenue_brigada(day_ManegementBilling1, day_ManegementBilling2, filters)
            generalRevenueBrigada = function_format_numeric_columns(generalRevenueBrigada, ['VALOR CONTRATO', 'PARCELA 1', 'PARCELA 2', 'PARCELA 3', 'PARCELA 4', 'PARCELA 5'])
            filtered_copy, count = component_plotDataframe(generalRevenueBrigada, "Abertura por Brigada")
            function_copy_dataframe_as_tsv(filtered_copy)

class ManegementBilling(Page):
    def render(self):
        self.data = {}
        day_ManegementBilling1 = datetime.today().date()
        day_ManegementBilling2 = datetime.today().date()
        self.data['generalRevenue'] = general_revenue(day_ManegementBilling1, day_ManegementBilling2, filters='')
        #self.data['estabelecimentoTransaction'] = estabelecimento_transaction(day_ManegementBilling1, day_ManegementBilling2)
        self.data['groupsCompanies'] = groups_companies(day_ManegementBilling1, day_ManegementBilling2)
        self.data['generalRevenueOportunity'] = general_revenue_oportunity(day_ManegementBilling1, day_ManegementBilling2, filters='')
        self.data['generalRevenueEvents'] = general_revenue_events(day_ManegementBilling1, day_ManegementBilling2, filters='')
        self.data['generalRevenueBrigada'] = general_revenue_brigada(day_ManegementBilling1, day_ManegementBilling2, filters='')


        BuildManegementBilling(self.data['generalRevenue'],
                               #self.data['estabelecimentoTransaction'],
                               self.data['groupsCompanies'],
                               self.data['generalRevenueOportunity'],
                               self.data['generalRevenueEvents'],
                               self.data['generalRevenueBrigada'])