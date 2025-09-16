from matplotlib.dates import relativedelta
import pandas as pd
import streamlit as st
from data.querys_blueme import *
from data.querys_estaff import *
from data.querys_grupoe import *
from menu.page import Page
from utils.components import *
from utils.functions import *
from datetime import date, datetime

def BuildGeneralResults(billingCompanies, worksByFunctions, generalRevenueEvents, generalRevenueBrigada, averageFreelaValueAndHourlyRate):

    row1 = st.columns(6)
    global day_GeneralResults1, day_GeneralResults2

    with row1[2]:
        day_GeneralResults1 = st.date_input('Data Inicio:', value=date(datetime.today().year, datetime.today().month, 1) - relativedelta(months=1), format='DD/MM/YYYY', key='day_GeneralResults1') 
    with row1[3]:
        day_GeneralResults2 = st.date_input('Data Final:', value=date(datetime.today().year, datetime.today().month, 1) - relativedelta(days=1), format='DD/MM/YYYY', key='day_GeneralResults2')

    num_months = (day_GeneralResults2.year - day_GeneralResults1.year) * 12 + (day_GeneralResults2.month - day_GeneralResults1.month) + 1

    day_GeneralResults3 = day_GeneralResults1 - relativedelta(months=num_months)
    day_GeneralResults4 = day_GeneralResults2 - relativedelta(months=num_months)

    last_day_of_the_month = (day_GeneralResults2.replace(day=1) + relativedelta(months=1, days=-1)).day
    if day_GeneralResults2.day == last_day_of_the_month:
        day_GeneralResults4 = (day_GeneralResults4.replace(day=1) + relativedelta(months=1, days=-1))

    row2 = st.columns([2, 1.5])
    billingCompanies = billing_companies(day_GeneralResults1, day_GeneralResults2)
    worksByFunctions = works_by_functions(day_GeneralResults1, day_GeneralResults2)
    averageFreelaValueAndHourlyRate = average_freela_value_and_hourly_rate(day_GeneralResults1, day_GeneralResults2)
    
    billingCompanies2 = billing_companies(day_GeneralResults3, day_GeneralResults4)
    worksByFunctions2 = works_by_functions(day_GeneralResults3, day_GeneralResults4)
    averageFreelaValueAndHourlyRate2 = average_freela_value_and_hourly_rate(day_GeneralResults3, day_GeneralResults4)

    with row2[0]:
            
        row2_1 = st.columns(5)
        tile = row2_1[0].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'NÚM. DE TRABALHOS', tile, 'Núm. Jobs', type='sum')

        tile = row2_1[1].container(border=True)
        function_callsigns_structure(averageFreelaValueAndHourlyRate, averageFreelaValueAndHourlyRate2, 'FREELAS DISTINTOS', tile, 'Freelas Dist.', type='sum')
        
        tile = row2_1[2].container(border=True)
        function_callsigns_structure(worksByFunctions, worksByFunctions2, 'FUNÇÃO', tile, 'Funções Dist.', type='count')

        tile = row2_1[3].container(border=True)

        function_callsigns_structure(averageFreelaValueAndHourlyRate, averageFreelaValueAndHourlyRate2, 'VALOR MEDIO POR JOB', tile, 'Valor Med./Jobs', num=True, type='average')

        tile = row2_1[4].container(border=True)
        function_callsigns_structure(averageFreelaValueAndHourlyRate, averageFreelaValueAndHourlyRate2, 'VALOR MEDIO POR HORA', tile, 'Valor Med./Hora', num=True, type='average')
        
        row2_2 = st.columns(5)
        tile = row2_2[0].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'VALOR LIQUIDO', tile, 'Valor Propostas', num=True, type='sum')
        
        tile = row2_2[1].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'VALOR EXTRA', tile, 'Valor Extra', num=True, type='sum')
        
        tile = row2_2[2].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'VALOR FREELA', tile, 'Valor Freelas', num=True, type='sum')
        
        tile = row2_2[3].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'VALOR BRUTO', tile, 'Valor Bruto', num=True, type='sum')
        
        tile = row2_2[4].container(border=True)
        function_callsigns_structure(billingCompanies, billingCompanies2, 'TAXA ESTAFF', tile, 'Fat. Estaff', num=True, type='sum')
        
        billingCompanies = billingCompanies.drop(columns=['VALOR LIQUIDO', 'VALOR EXTRA', 'VALOR FREELA', 'VALOR BRUTO'])
        billingCompanies = function_format_numeric_columns(billingCompanies, ['VALOR TRANSACIONADO', 'TAXA ESTAFF'])
        filtered_copy, count = component_plotDataframe(billingCompanies, "Faturamento Por Estabelecimento")
        function_copy_dataframe_as_tsv(filtered_copy)

    with row2[1]:
        worksByFunctions = function_format_numeric_columns(worksByFunctions, ['VALOR MÉDIO POR HORA'])
        worksByFunctions["JORNADA MEDIA (HORAS)"] = worksByFunctions["JORNADA MEDIA (HORAS)"].map(lambda x: f"{x:.2f}".replace(".", ","))
        filtered_copy, count = component_plotDataframe(worksByFunctions, "Trabalhos Por Funções",height=631)
        function_copy_dataframe_as_tsv(filtered_copy)
    
    with st.expander("📊 Abertura por Evento Geral", expanded=False):
        generalRevenueEvents = general_revenue_events(day_GeneralResults1, day_GeneralResults2, filters='')
        generalRevenueEvents = function_format_numeric_columns(generalRevenueEvents, ['VALOR BRUTO', 'VALOR LIQUIDO', 'CUSTO EXTRA', 'TAXA EVENTO'])
        filtered_copy, count = component_plotDataframe(generalRevenueEvents, "Abertura Geral por Evento")
        function_copy_dataframe_as_tsv(filtered_copy)
        #function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Propostas')

    with st.expander("📊 Abertura por Brigada Geral", expanded=False):
        generalRevenueBrigada = general_revenue_brigada(day_GeneralResults1, day_GeneralResults2, filters='')
        generalRevenueBrigada = function_format_numeric_columns(generalRevenueBrigada, ['VALOR CONTRATO', 'PARCELA 1', 'PARCELA 2', 'PARCELA 3', 'PARCELA 4', 'PARCELA 5'])
    
        filtered_copy, count = component_plotDataframe(generalRevenueBrigada, "Abertura Geral por Brigada")
        function_copy_dataframe_as_tsv(filtered_copy)
        #function_box_lenDf(len_df=count, df=filtered_copy, y='-100', x='500', box_id='box1', item='Propostas')


class GeneralResults(Page):
    def render(self):
        self.data = {}
        day_GeneralResults1 = date(datetime.today().year, datetime.today().month, 1) - relativedelta(months=1)
        day_GeneralResults2 = date(datetime.today().year, datetime.today().month, 1) - relativedelta(days=1)
        self.data['billingCompanies'] = billing_companies(day_GeneralResults1, day_GeneralResults2)
        self.data['worksByFunctions'] = works_by_functions(day_GeneralResults1, day_GeneralResults2) 
        self.data['generalRevenueEvents'] = general_revenue_events(day_GeneralResults1, day_GeneralResults2, filters='')
        self.data['generalRevenueBrigada'] = general_revenue_brigada(day_GeneralResults1, day_GeneralResults2, filters='')
        self.data['averageFreelaValueAndHourlyRate'] = average_freela_value_and_hourly_rate(day_GeneralResults1, day_GeneralResults2)
        BuildGeneralResults(self.data['billingCompanies'], 
                            self.data['worksByFunctions'],
                            self.data['generalRevenueEvents'],
                            self.data['generalRevenueBrigada'],
                            self.data['averageFreelaValueAndHourlyRate'])
