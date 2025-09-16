from data.dbconnect import get_dataframe_from_query
import streamlit as st

@st.cache_data
def general_costs(day1, day2):
    return get_dataframe_from_query(f"""
#Tabela de Custos da Staff
SELECT
DATE_FORMAT(CES.Primeiro_Dia_Mes_Vencimento, '%m/%Y') as 'Mês/Ano',

SUM(CASE WHEN CES.ID_Categoria = 100 THEN CES.Valor END) AS 'C1 Impostos',
SUM(CASE WHEN CES.ID_Categoria = 104 THEN CES.Valor END) AS 'C2 Custos de Ocupação',
SUM(CASE WHEN CES.ID_Categoria = 101 THEN CES.Valor END) AS 'C3 Despesas com Pessoal Interno',
SUM(CASE WHEN CES.ID_Categoria = 105 THEN CES.Valor END) AS 'C4 Despesas com Pessoal Terceirizado',
SUM(CASE WHEN CES.ID_Categoria = 109 THEN CES.Valor END) AS 'C5 Despesas Operacionais com Freelas',
SUM(CASE WHEN CES.ID_Categoria = 103 THEN CES.Valor END) AS 'C6 Despesas com Clientes',
SUM(CASE WHEN CES.ID_Categoria = 108 THEN CES.Valor END) AS 'C7 Despesas com Softwares e Licenças',
SUM(CASE WHEN CES.ID_Categoria = 107 THEN CES.Valor END) AS 'C8 Despesas com Marketing',
SUM(CASE WHEN CES.ID_Categoria = 106 THEN CES.Valor END) AS 'C9 Despesas Financeiras',
NULL AS 'C10 Investimentos',
SUM(CASE WHEN CES.ID_Categoria IN (100, 104, 101, 105, 109, 103, 108, 107, 106) THEN CES.Valor END) AS 'Custos Totais'

FROM View_Custos_Estaff_Consolidados CES
WHERE CES.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CES.Primeiro_Dia_Mes_Vencimento <= '{day2}'

GROUP BY DATE_FORMAT(CES.Primeiro_Dia_Mes_Vencimento, '%m/%Y')
ORDER BY STR_TO_DATE('Mês/Ano', '%m/%Y') DESC;
""", use_grupoe=True)

@st.cache_data
def cost_details(day1, day2):
    return get_dataframe_from_query(f"""
SELECT
CES.Categoria_de_Custo AS 'CATEGORIA DE CUSTO',
CES.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA',
CES.Valor AS 'VALOR',
DATE_FORMAT(CES.Primeiro_Dia_Mes_Vencimento, '%Y/%m') AS 'DATA'
FROM View_Custos_Estaff_Consolidados CES
WHERE CES.Primeiro_Dia_Mes_Vencimento >= '{day1}'
AND CES.Primeiro_Dia_Mes_Vencimento <= '{day2}'
""", use_grupoe=True)

@st.cache_data
def ratings_rank(data):
    return get_dataframe_from_query(f"""
SELECT
DATE_FORMAT(CES.Data_Vencimento, '%m/%Y') AS 'Mês/Ano',
CES.Classificacao_Primaria AS 'CLASSIFICAÇÃO PRIMÁRIA',
SUM(CES.Valor) AS 'VALOR'

FROM View_Custos_Estaff_Consolidados CES
WHERE CES.Primeiro_Dia_Mes_Vencimento LIKE '{data}%'
AND CES.ID_Classificacao_Primaria NOT IN ('136')

GROUP BY CES.Classificacao_Primaria, CES.Primeiro_Dia_Mes_Vencimento
ORDER BY SUM(CES.Valor) DESC
""", use_grupoe=True)

@st.cache_data
def ratings_rank_details(data):
    return get_dataframe_from_query(f"""
WITH CUSTOS AS (
    # Primeira parte: Custos Internos
    SELECT
        CC2.DESCRICAO AS GRUPO_GERAL,
        ECI.ID AS ID_CUSTO,
        CP.ID AS ID_NIVEL1,
        CP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        ECI.DESCRICAO AS DESCRICAO,
        ECI.VALOR AS VALOR,
        SP.DESCRICAO AS STATUS_PAGAMENTO,
        CC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(ECI.DATA_VENCIMENTO), '-', MONTH(ECI.DATA_VENCIMENTO), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        ECI.DATA_LANCAMENTO AS DATA_LANCAMENTO,
        ECI.DATA_PAGAMENTO AS DATA_COMPETENCIA,
        ECI.DATA_VENCIMENTO AS DATA_VENCIMENTO
    FROM
        T_ESTAFF_CUSTOS_INTERNOS ECI
        LEFT JOIN T_CENTROS_DE_CUSTOS CC ON ECI.CENTRO_DE_CUSTO = CC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA CP ON ECI.CLASSIFICACAO_PRIMARIA = CP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CC2 ON CP.FK_CATEGORIA_CUSTO = CC2.ID
  			LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = ECI.STATUS_PAGAMENTO
    WHERE
        ECI.DATA_VENCIMENTO > '2022-12-31 23:59:59'
        AND ECI.TAG_INVESTIMENTO <> 1
        AND ECI.TAG_ESTORNO <> 1

    UNION ALL

    # Segunda parte: Custos Colaboradores
    SELECT
        CC2.DESCRICAO AS GRUPO_GERAL,
        CCE.ID AS ID_CUSTO, 
        CP.ID AS ID_NIVEL1,
        CP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        CONCAT(CE.NOME_COMPLETO, ' - ', CP.DESCRICAO) AS DESCRICAO,
        CCE.VALOR AS VALOR,
        SP.DESCRICAO AS STATUS_PAGAMENTO,
        CC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(CCE.DATA_VENCIMENTO), '-', MONTH(CCE.DATA_VENCIMENTO), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        CCE.DATA_LANCAMENTO AS DATA_LANCAMENTO, 
        CCE.DATA_PAGAMENTO AS DATA_COMPETENCIA,
        CCE.DATA_VENCIMENTO AS DATA_VENCIMENTO
    FROM
        T_CUSTOS_COLABORADORES_ESTAFF CCE
        JOIN T_COLABORADORES_ESTAFF CE ON CCE.FK_NOME_COLABORADOR = CE.ID
        LEFT JOIN T_CENTROS_DE_CUSTOS CC ON CCE.FK_CENTRO_DE_CUSTO = CC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA CP ON CCE.FK_CLASSIFICACAO_PRIMARIA = CP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CC2 ON CP.FK_CATEGORIA_CUSTO = CC2.ID
  			LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = CCE.FK_STATUS_PAGAMENTO
                                    
    UNION ALL

    # Terceira parte: Custos Pessoal
    SELECT
        CC2.DESCRICAO AS GRUPO_GERAL,
        ECP.ID AS ID_CUSTO, 
        CP.ID AS ID_NIVEL1,
        CP.DESCRICAO AS CLASSIFICACAO_NIVEL1,
        CONCAT(ECP.NOME, ' - ', CP.DESCRICAO) AS DESCRICAO,
        ECP.VALOR AS VALOR,
        SP.DESCRICAO AS STATUS_PAGAMENTO,
        CC2.ID AS ID_NIVEL2,
        CAST(CONCAT(YEAR(ECP.DATA_VENCIMENTO), '-', MONTH(ECP.DATA_VENCIMENTO), '-01') AS DATE) AS PRIMEIRO_DIA_MES_VENCIMENTO,
        ECP.DATA_LANCAMENTO AS DATA_LANCAMENTO, 
        ECP.DATA_PAGAMENTO AS DATA_COMPETENCIA,
        ECP.DATA_VENCIMENTO AS DATA_VENCIMENTO
    FROM
        T_ESTAFF_CUSTOS_PESSOAL ECP
        LEFT JOIN T_CENTROS_DE_CUSTOS CC ON ECP.CENTRO_DE_CUSTO = CC.ID
        LEFT JOIN T_CLASSIFICACAO_PRIMARIA CP ON ECP.CLASSIFICACAO_PRIMARIA = CP.ID
        LEFT JOIN T_CATEGORIAS_DE_CUSTO CC2 ON CP.FK_CATEGORIA_CUSTO = CC2.ID
  			LEFT JOIN T_STATUS_PAGAMENTO SP ON SP.ID = ECP.STATUS_PAGAMENTO
)

# Consulta final
SELECT 
    C.ID_CUSTO AS 'ID CUSTO',
    C.GRUPO_GERAL AS 'GRUPO GERAL',
    C.CLASSIFICACAO_NIVEL1 AS 'NIVEL 1',
    C.VALOR AS 'VALOR',
    C.STATUS_PAGAMENTO AS 'PAGAMENTO',
    DATE_FORMAT(C.DATA_COMPETENCIA, '%d/%m/%Y') AS 'DATA COMPETÊNCIA',
    DATE_FORMAT(C.DATA_VENCIMENTO, '%d/%m/%Y') AS 'DATA VENCIMENTO',
    C.DESCRICAO AS 'DESCRIÇÃO'
FROM CUSTOS C

JOIN 
    (SELECT CLASSIFICACAO_NIVEL1, SUM(VALOR) AS TOTAL_VALOR
     FROM CUSTOS
     WHERE PRIMEIRO_DIA_MES_VENCIMENTO LIKE '{data}%'
     GROUP BY CLASSIFICACAO_NIVEL1
    ) AS TOTAL_CUSTOS
ON C.CLASSIFICACAO_NIVEL1 = TOTAL_CUSTOS.CLASSIFICACAO_NIVEL1

WHERE C.PRIMEIRO_DIA_MES_VENCIMENTO LIKE '{data}%'
AND ID_NIVEL1 NOT IN ('136')

ORDER BY TOTAL_CUSTOS.TOTAL_VALOR DESC, C.VALOR DESC;
""", use_grupoe=True)







