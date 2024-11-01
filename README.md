## 📊 Análise de Churn de Clientes

### 🎯 Objetivo do Projeto
Neste projeto, meu objetivo foi entender os fatores que contribuem para o churn (cancelamento) de clientes em uma empresa de telecomunicações. Ao identificar esses fatores, a empresa poderá tomar medidas para melhorar a retenção de clientes e otimizar suas estratégias de marketing.

### 🔍 Abordagem
Utilizei um conjunto de dados que contém informações sobre clientes, incluindo dados demográficos, serviços contratados e informações financeiras. As etapas principais do projeto foram:

1. **Pré-processamento de Dados**: 
   - Limpeza dos dados para remover entradas duplicadas e valores ausentes.
   - Transformação de variáveis categóricas em variáveis numéricas para análise.

### 🧹 Limpeza e Preparação dos Dados
O código começa com a importação das bibliotecas necessárias, incluindo Streamlit para a criação do dashboard, pandas para manipulação de dados e Plotly para visualizações interativas.
```
import streamlit as st
import pandas as pd
import plotly.express as px
```

Em seguida, o arquivo CSV que contém os dados dos clientes é carregado e a coluna id_cliente é removida, pois não é relevante para a análise.
```
ARQUIVO_DADOS = r"churn_clientes.csv"
df_churn = pd.read_csv(ARQUIVO_DADOS)
df_churn = df_churn.drop(columns='id_cliente', axis=1)
```
A coluna churn é convertida de texto para valores numéricos, onde "Sim" se torna 1 e "Não" se torna 0. Isso facilita a análise estatística posterior.
```
df_churn['churn'] = df_churn['churn'].map({'Sim': 1, 'Não': 0})
```

### 📊 Dashboard Interativo

A configuração da página do Streamlit é realizada para criar um layout amplo e centralizar o título do dashboard.

```python
st.set_page_config(page_title="Dashboard de Churn", layout="wide")
st.markdown(
    "<h2 style='text-align: center;'>Análise de Churn</h2>", 
    unsafe_allow_html=True
)
```
Carregando os dados

```
data = df_churn
data['churn'] = data['churn'].map({1: 'Sim', 0: 'Não'})
```


### 🔍 Filtragem de Dados
Os dados são carregados e preparados para filtragem. A barra lateral permite que os usuários filtrem os dados por tipo de contrato e se são idosos. Isso é realizado com o uso de multiselect e selectbox.
```
contratos_unicos = data['contrato'].unique()

contratos_selecionados = st.sidebar.multiselect(
    'Selecione o(s) tipo(s) de contrato:',
    options=contratos_unicos,
    default=contratos_unicos
)

idoso_selecionado = st.sidebar.selectbox(
    'Idoso?',
    options=['Todos', 'Sim', 'Não'],
    index=0
)
```

### 📈 Exibição de Métricas
As principais métricas, como a quantidade total de clientes e as porcentagens de churn, são calculadas e exibidas em cartões personalizados com ícones.
```
qtd_clientes = len(data_filtrada)
churn_sim_count = data_filtrada['churn'].value_counts().get(1, 0)
churn_sim_pct = (churn_sim_count / len(data_filtrada)) * 100
```
A função criar_card é utilizada para formatar e exibir essas métricas de forma atraente, com um cartão e icones além dos textos e números 
```
def criar_card(icone, numero, texto, coluna_card):
    container = coluna_card.container(border =True)
    coluna_esquerda, coluna_direita = container.columns([1, 2.5])
    coluna_esquerda.markdown(f" # {icone}", unsafe_allow_html=True)  # Emoji como texto
    coluna_direita.markdown(f"# {numero}")
    coluna_direita.markdown(f"## {texto}")
```

Criando os Cartões:
```
# Ícones para os cartões
icone_churn_sim = "⚠️"  # Alerta para Churn Sim
icone_churn_nao = "✅"  # Check para Churn Não
icone_clientes = "👥"  # Ícone de grupo/pessoas

# Criando as colunas para os cartões
col1, col2, col3  = st.columns(3)

# Exibindo os cartões com a função personalizada
criar_card(icone_clientes, qtd_clientes, "Qtd.Clientes", col1)
criar_card(icone_churn_sim, f"{churn_sim_pct:.2f}%", "Churn: Sim ", col2)
criar_card(icone_churn_nao, f"{churn_nao_pct:.2f}%", "Churn: Não", col3)

```

### 📊 Gráficos de Análise
1. Churn por Tempo na Empresa: Um histograma que mostra a relação entre o tempo que os clientes estão na empresa e o churn é criado com a biblioteca Plotly. Isso é importante para identificar se há uma tendência de churn ao longo do tempo.
```
# Histograma para Meses na Empresa
fig_meses = px.histogram(
    data_filtrada, x='meses_na_empresa', color='churn',
    barmode='overlay', title='Churn por Tempo na Empresa',
    color_discrete_map={'Sim': '#EF553B', 'Não': '#636EFA'}
)
fig_meses.update_layout(
    title={'text': 'Churn por Tempo na Empresa', 'x': 0.5, 'xanchor': 'center'},  # Centralizando o título do gráfico
    title_font_size=36,  # Aumentando o tamanho do título
    xaxis_title='Meses na Empresa',
    yaxis_title='Quantidade'  # Aqui você define o título do eixo Y
)
with st.container():
    st.plotly_chart(fig_meses, use_container_width=True)
```
2. Churn por Valor Mensal: Outro histograma que analisa como o valor mensal que os clientes pagam está relacionado ao churn.
```
# Churn por Valor Mensal
fig_valor_mensal = px.histogram(
    data_filtrada, x='valor_mensal', color='churn',
    barmode='overlay', title='Churn por Valor Mensal',
    color_discrete_map={'Sim': '#EF553B', 'Não': '#636EFA'}
)
fig_valor_mensal.update_layout(
    title={'text': 'Churn por Valor Mensal', 'x': 0.5, 'xanchor': 'center'},  # Centralizando o título do gráfico
    title_font_size=36,  # Aumentando o tamanho do título
    xaxis_title='Valor Mensal (R$)',
    yaxis_title='Quantidade'  # Aqui você define o título do eixo Y
)
st.plotly_chart(fig_valor_mensal, use_container_width=True)
```
### 📉 Análise de Correlação
Por fim, a análise de correlação entre as variáveis é feita usando a função corr() do pandas, também são mapeados e trocados os nomes das colunas para melhor visualização, os resultados são apresentados em um gráfico de barras, mostrando quais fatores mais influenciam o churn.
```
# Substituindo 'Sim' e 'Não' por 1 e 0
df_churn['churn'] = df_churn['churn'].replace({'Sim': 1, 'Não': 0})

# Criando dummies para variáveis categóricas
df_dummies = pd.get_dummies(df_churn, drop_first=True)

# Calculando a correlação
churn_c = df_dummies.corr()['churn'].sort_values(ascending=False)

# Dicionário para mapear os nomes das colunas
coluna_nomes = {
    'valor_mensal': 'Valor Mensal',
    'total_gasto': 'Total Gasto',
    'meses_na_empresa': 'Meses na Empresa',
    'fatura_digital_Sim': 'Fatura Digital (Sim)',
    'idoso_Sim': 'Idoso (Sim)',
    'streaming_tv_Sim': 'Streaming de TV (Sim)',
    'streaming_filmes_Sim': 'Streaming de Filmes (Sim)',
    'multiplas_linhas_Sim': 'Múltiplas Linhas (Sim)',
    'servico_telefone_Sim': 'Serviço de Telefone (Sim)',
    'genero_Masculino': 'Gênero (Masculino)',
    'servico_protecao_equipamento_Sim': 'Proteção de Equipamentos (Sim)',
    'servico_backup_Sim': 'Serviço de Backup (Sim)',
    'forma_pagamento_Cheque': 'Forma de Pagamento (Cheque)',
    'forma_pagamento_Transferencia': 'Forma de Pagamento (Transferência)',
    'forma_pagamento_Cartao de credito': 'Forma de Pagamento (Cartão de Crédito)',
    'tem_parceiro_Sim': 'Tem Parceiro (Sim)',
    'tem_dependentes_Sim': 'Tem Dependentes (Sim)',
    'servico_suporte_tecnico_Sim': 'Suporte Técnico (Sim)',
    'servico_seguranca_Sim': 'Serviço de Segurança (Sim)',
    'servico_internet_Fibra optica': 'Serviço de Internet (Fibra Óptica)',
    'contrato_Mensal': 'Contrato (Mensal)',
    'contrato_Bianual': 'Contrato (Bianual)',
    'servico_internet_Não': 'Serviço de Internet (Não)',
}

# Aplicando a renomeação
churn_c_renomeado = churn_c.rename(coluna_nomes)

# Criando o gráfico de barras com Plotly
fig_correlation = px.bar(
    x=churn_c_renomeado.index[1:],  # Excluindo a primeira linha (churn)
    y=churn_c_renomeado.values[1:],  # Excluindo a primeira correlação (churn com churn)
    labels={'x': 'Variáveis', 'y': 'Correlação com Churn'},
    title='Correlação com Churn',
    color=churn_c_renomeado.values[1:],  # Cor de acordo com os valores de correlação
    color_continuous_scale='RdBu'
)

# Atualizando o layout do gráfico
fig_correlation.update_layout(
    title={'text': 'Correlação com Churn', 'x': 0.5, 'xanchor': 'center'},  # Centralizando o título do gráfico
    title_font_size=36,  # Aumentando o tamanho do título
    xaxis_title='Variáveis',
    yaxis_title='Correlação com Churn',
    xaxis_tickangle=-45,  # Rotaciona os rótulos do eixo x
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_correlation, use_container_width=True)
```
### 🚀 Conclusão
Este projeto fornece uma ferramenta interativa para análise de churn, caso queria acessar: https://churnapp-nb9hgxhh8xavfqurkmqe4i.streamlit.app/ , permitindo que a empresa visualize e compreenda os fatores que influenciam o cancelamento de clientes. Com essas informações, é possível desenvolver estratégias mais eficazes de retenção e melhorar o relacionamento com os clientes, caso queria ver minha analise com esse dashboard pode ir ao meu artigo no linkedin: https://www.linkedin.com/pulse/an%C3%A1lise-de-churn-streamlit-alexandre-eur%C3%ADcio-trqwf/?trackingId=3I5yfrRKSceg5mQmvpaoMg%3D%3D



