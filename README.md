# Resultados Estaff

## Índice
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Funcionalidades](#funcionalidades)
   - [Resultados Gerais](#1-resultados-gerais)
   - [Faturamento Estaff Gerencial](#2-faturamento-estaff-gerencial)
   - [Gerenciamento de Custos](#3-gerenciamento-de-custos)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Como Executar](#como-executar)
5. [Contato](#contato)

## Sobre o Projeto
O Dash **Resultados Estaff** é um dashboard desenvolvido em Streamlit para visualizar o faturamento e os custos da Estaff de forma gerencial e detalhada. O sistema permite a filtragem e análise de dados financeiros, proporcionando uma visão estratégica do desempenho financeiro da empresa.

## Funcionalidades

### 1. Resultados Gerais
- Exibe indicadores para mostrar se houve aumento ou queda nos resultados.
- O cálculo funciona comparando o período selecionado com o período anterior.
- Permite análises diárias, mensais, trimestrais, etc.
- **Seções principais:**
  - **Faturamento por estabelecimento:** Mostra o faturamento no período selecionado.
  - **Quantidade de trabalhos por função:** Apresenta a distribuição dos trabalhos por função.
  - **Abertura por evento geral:** Lista os eventos ocorridos no período selecionado.
  - **Abertura por brigada geral:** Mostra as brigadas gerais do período.

### 2. Faturamento Estaff Gerencial
- Apresenta uma tabela com o faturamento geral da Estaff.
- Permite a seleção de um grupo de casas para análise específica.
- Após selecionar um grupo, libera a opção de selecionar casas individuais para detalhar ainda mais o faturamento.
- Exibe os dados segmentados por grupo e por casa.
- Libera também Três novas visualizações **Abertura Por Oportunidade, Evento e Brigada**, onde irá exibir as Oportunidades, Eventos e Brigadas referente aos filtros selecionados.

### 3. Gerenciamento de Custos
- Exibe uma tabela com todos os custos por categoria, incluindo:
  - Diferença entre faturamento e custo.
  - Total de custos e representações percentuais.
- Apresenta uma segunda tabela com detalhes específicos das classificações de cada categoria de custo.
  - **Exemplo: `c2_Custos_de_Ocupacao` inclui:**  
    - Aluguel  
    - Manutenção  
    - Utilidades  
    - Equipamentos de Escritório  
    - Telefone e Internet 
    - Entre outros...
  - Exibe o total Geral e por classificação.
- #### As próximas tabelas são construídas lado a lado para uma comparação de meses:
- Permite a seleção de dois meses específicos para visualizar custos detalhados e compará-los.
- Inclui dois gráficos de pizza comparativos para melhor visualização dos custos selecionados.
- Exibe tabelas comparativas com o ranking dos maiores custos conforme o mês selecionado.
- Apresenta tabelas detalhadas com informações adicionais, como ID do custo, nível, fornecedor, pagamento, entre outros.

## Tecnologias Utilizadas
As principais tecnologias utilizadas no projeto são:
- **Python** - Linguagem principal do desenvolvimento.
- **Streamlit** - Framework para construção de dashboards interativos.
- **Pandas** - Manipulação e análise de dados.
- **Streamlit ECharts** - Visualizações interativas avançadas.

## Como Executar

```sh
# Clone este repositório:
git clone https://github.com/Eshows-Tech/streamlit-resultados-staff.git

# Acesse a pasta do projeto:
cd streamlit-resultados-estaff

# Instale as dependências:
pip install -r requirements.txt

# Execute o dashboard:
streamlit run main.py
```

## Contato
Caso tenha dúvidas ou sugestões, sinta-se à vontade para entrar em contato via [GitHub Issues](https://github.com/Eshows-Tech/streamlit-resultados-staff/issues).