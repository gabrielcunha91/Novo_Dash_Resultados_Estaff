from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def general_costs_blueme(day1, day2):
    return get_dataframe_from_query(f"""
SELECT 
    DATE_FORMAT(DR.COMPETENCIA, '%m/%Y') AS 'Mês/Ano',
    
    SUM(CASE WHEN G1.ID IN ('216') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C1 Impostos',
    SUM(CASE WHEN G1.ID IN ('220','221','222','225','232', '218', '226') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C2 Custos de Ocupação',
    SUM(CASE WHEN G1.ID IN ('223','231') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C3 Despesas com Pessoal Interno',
    SUM(CASE WHEN G1.ID IN ('230', '210') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C4 Despesas com Pessoal Terceirizado',
    SUM(CASE WHEN G1.ID IN ('234', '215') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C5 Despesas Operacionais com Freelas',
    SUM(CASE WHEN G1.ID IN ('233') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C6 Despesas com Clientes',
    SUM(CASE WHEN G1.ID IN ('217') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C7 Despesas com Softwares e Licenças',
    SUM(CASE WHEN G1.ID IN ('211', '224', '227') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C8 Despesas com Marketing',
    SUM(CASE WHEN G1.ID IN ('213', '229', '228', '212', '214') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C9 Despesas Financeiras',
    SUM(CASE WHEN G1.ID IN ('219') THEN DR.VALOR_LIQUIDO ELSE 0 END) AS 'C10 Investimentos',
    SUM(DR.VALOR_LIQUIDO) AS 'Custos Totais'
FROM T_DESPESA_RAPIDA DR
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1 ON DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_1 = G1.ID
WHERE DR.FK_LOJA = '134'
AND DR.COMPETENCIA >= '2025-01-01'
AND (DR.TAG_ESTORNO IS NULL OR DR.TAG_ESTORNO = 0)
AND DR.COMPETENCIA >= '{day1}'
AND DR.COMPETENCIA <= '{day2}'
GROUP BY YEAR(DR.COMPETENCIA), MONTH(DR.COMPETENCIA)
ORDER BY STR_TO_DATE(DATE_FORMAT(DR.COMPETENCIA, '%m/%Y'), '%m/%Y');
""", use_blueme=True)

@st.cache_data
def costs_blueme_details(day1, day2):
    return get_dataframe_from_query(f"""
SELECT
    CASE 
        WHEN G1.ID IN ('216') THEN 'c1_Impostos'
        WHEN G1.ID IN ('220','221','222','225','232', '218', '226') THEN 'c2_Custos_de_Ocupacao'
        WHEN G1.ID IN ('223','231') THEN 'c3_Despesas_com_Pessoal_Interno'
        WHEN G1.ID IN ('230', '210') THEN 'c4_Despesas_com_Pessoal_Terceirizado'
        WHEN G1.ID IN ('234', '215') THEN 'c5_Despesas_Operacionais_com_Freelas'
        WHEN G1.ID IN ('233') THEN 'c6_Despesas_com_Clientes'
        WHEN G1.ID IN ('217') THEN 'c7_Despesas_com_Softwares_e_Licencas'
        WHEN G1.ID IN ('211', '224', '227') THEN 'c8_Despesas_com_Marketing'
        WHEN G1.ID IN ('213', '229', '228', '212', '214') THEN 'c9_Despesas_Financeiras'
        WHEN G1.ID IN ('219') THEN 'c10_Investimentos'
    END AS `CATEGORIA DE CUSTO`,
    G1.DESCRICAO AS 'CLASSIFICAÇÃO PRIMÁRIA',
    SUM(DR.VALOR_LIQUIDO) AS 'VALOR',
    DATE_FORMAT(DR.COMPETENCIA, '%Y/%m') AS 'DATA'
FROM T_DESPESA_RAPIDA DR
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.ID = DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1 ON G2.FK_GRUPO_1 = G1.ID
LEFT JOIN T_VERSOES_PLANO_CONTABIL VPC ON VPC.ID = G1.FK_VERSAO_PLANO_CONTABIL
WHERE DR.FK_LOJA = '134'
AND DR.COMPETENCIA >= '2025-01-01'
AND (DR.TAG_ESTORNO IS NULL OR DR.TAG_ESTORNO = 0)
AND DR.COMPETENCIA >= '{day1}'
AND DR.COMPETENCIA <= '{day2}'
GROUP BY YEAR(DR.COMPETENCIA), MONTH(DR.COMPETENCIA), `CATEGORIA DE CUSTO`, G1.DESCRICAO
ORDER BY `CATEGORIA DE CUSTO`
""", use_blueme=True)

@st.cache_data
def ratings_rank_blueme(data):
    return get_dataframe_from_query(f"""
SELECT 
    DATE_FORMAT(DR.COMPETENCIA, '%m/%Y') AS 'Mês/Ano',
    G1.DESCRICAO AS 'CLASSIFICAÇÃO PRIMÁRIA',
    SUM(DR.VALOR_LIQUIDO) AS 'VALOR'
FROM T_DESPESA_RAPIDA DR
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.ID = DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1 ON G2.FK_GRUPO_1 = G1.ID
LEFT JOIN T_VERSOES_PLANO_CONTABIL VPC ON VPC.ID = G1.FK_VERSAO_PLANO_CONTABIL
WHERE DR.FK_LOJA = '134'
AND (DR.TAG_ESTORNO IS NULL OR DR.TAG_ESTORNO = 0)
AND DR.COMPETENCIA >= '2025-01-01'
AND DR.COMPETENCIA LIKE '{data}%'
GROUP BY G1.DESCRICAO, YEAR(DR.COMPETENCIA), MONTH(DR.COMPETENCIA)
""", use_blueme=True)

@st.cache_data
def ratings_rank_details_blueme(data):
    return get_dataframe_from_query(f"""
SELECT 
		DR.ID AS 'ID CUSTO',
    CASE 
        WHEN G1.ID IN ('216') THEN 'c1_Impostos'
        WHEN G1.ID IN ('220','221','222','225','232', '218', '226') THEN 'c2_Custos_de_Ocupacao'
        WHEN G1.ID IN ('223','231') THEN 'c3_Despesas_com_Pessoal_Interno'
        WHEN G1.ID IN ('230', '210') THEN 'c4_Despesas_com_Pessoal_Terceirizado'
        WHEN G1.ID IN ('234', '215') THEN 'c5_Despesas_Operacionais_com_Freelas'
        WHEN G1.ID IN ('233') THEN 'c6_Despesas_com_Clientes'
        WHEN G1.ID IN ('217') THEN 'c7_Despesas_com_Softwares_e_Licencas'
        WHEN G1.ID IN ('211', '224', '227') THEN 'c8_Despesas_com_Marketing'
        WHEN G1.ID IN ('213', '229', '228', '212', '214') THEN 'c9_Despesas_Financeiras'
        WHEN G1.ID IN ('219') THEN 'c10_Investimentos'
    END AS `GRUPO GERAL`,
    G1.DESCRICAO AS 'NIVEL 1',
    G2.DESCRICAO AS 'NIVEL 2',
    F.FANTASY_NAME AS 'FORNECEDOR',
    DR.VALOR_LIQUIDO AS 'VALOR',
    SP.DESCRICAO AS 'PAGAMENTO',
    DATE_FORMAT(DR.COMPETENCIA, '%d/%m/%Y') AS 'DATA COMPETÊNCIA',
    DATE_FORMAT(DR.VENCIMENTO, '%d/%m/%Y') AS 'DATA VENCIMENTO',
    DR.OBSERVACAO AS 'DESCRIÇÃO'
FROM T_DESPESA_RAPIDA DR 
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.ID = DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2
LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1 ON G1.ID = G2.FK_GRUPO_1
LEFT JOIN T_FORNECEDOR F ON F.ID = DR.FK_FORNECEDOR
LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = DR.FK_STATUS_PGTO
LEFT JOIN (
    -- Subquery para calcular o total de valor por CLASSIFICAÇÃO PRIMÁRIA
    SELECT 
        G1.ID AS Grupo1_ID,
        SUM(DR.VALOR_LIQUIDO) AS Total_Valor
    FROM T_DESPESA_RAPIDA DR 
  	LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 G2 ON G2.ID = DR.FK_CLASSIFICACAO_CONTABIL_GRUPO_2
  	LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_1 G1 ON G1.ID = G2.FK_GRUPO_1
    
    WHERE DR.FK_LOJA = '134'
    AND (DR.TAG_ESTORNO IS NULL OR DR.TAG_ESTORNO = 0)
    AND DR.COMPETENCIA >= '2025-01-01'
    AND DR.COMPETENCIA LIKE '{data}%'
    GROUP BY G1.ID
) AS Total_Custos ON G1.ID = Total_Custos.Grupo1_ID
WHERE DR.FK_LOJA = '134'
AND (DR.TAG_ESTORNO IS NULL OR DR.TAG_ESTORNO = 0)
AND DR.COMPETENCIA >= '2025-01-01'
AND DR.COMPETENCIA LIKE '{data}%'
ORDER BY Total_Custos.Total_Valor DESC, DR.VALOR_LIQUIDO DESC;
""", use_blueme=True)