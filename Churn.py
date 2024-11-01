import streamlit as st
import pandas as pd
import plotly.express as px


# Caminho para o arquivo CSV
ARQUIVO_DADOS = "https://raw.githubusercontent.com/AEAA17/ChurnStreamlit/main/churn_clientes.csv"


# Carregando o dataset e removendo a coluna de ID
df_churn = pd.read_csv(ARQUIVO_DADOS)
df_churn = df_churn.drop(columns='id_cliente', axis=1)

# Convertendo a coluna 'churn' em valores numéricos
df_churn['churn'] = df_churn['churn'].map({'Sim': 1, 'Não': 0})

# Configuração da página e título
st.set_page_config(page_title="Dashboard de Churn", layout="wide")
st.markdown(
    "<h1 style='text-align: center; font-size: 96px;'>Análise de Churn</h1>", 
    unsafe_allow_html=True
)


# Carregar os dados
data = df_churn

# Converter os valores 1 e 0 na coluna 'churn' para "Sim" e "Não"
data['churn'] = data['churn'].map({1: 'Sim', 0: 'Não'})

# Sidebar: Filtro de Contratos (com validação)
contratos_unicos = data['contrato'].unique()
contratos_selecionados = st.sidebar.multiselect(
    'Selecione o(s) tipo(s) de contrato:',
    options=contratos_unicos,
    default=contratos_unicos  # Garantir que sempre haverá pelo menos uma opção selecionada
)

# Garantir que sempre haverá pelo menos um contrato selecionado
if not contratos_selecionados:
    st.sidebar.warning("Selecione pelo menos um tipo de contrato.")
    st.stop()  # Interromper a execução do script até que haja uma seleção válida

# Sidebar: Filtro de Idoso
idoso_selecionado = st.sidebar.selectbox(
    'Idoso?',
    options=['Todos', 'Sim', 'Não'],
    index=0
)

# Aplicando o filtro de contrato
data_filtrada = data[data['contrato'].isin(contratos_selecionados)]

# Aplicando o filtro de idoso, se necessário
if idoso_selecionado != 'Todos':
    data_filtrada = data_filtrada[data_filtrada['idoso'] == idoso_selecionado]

# Cálculo das métricas principais
qtd_clientes = len(data_filtrada)
churn_sim_count = data_filtrada['churn'].value_counts().get(1, 0)  # Contagem de churn = 1
churn_sim_pct = (churn_sim_count / len(data_filtrada)) * 100
churn_nao_count = data_filtrada['churn'].value_counts().get(0, 0)  # Contagem de churn = 0
churn_nao_pct = (churn_nao_count / len(data_filtrada)) * 100


# Função para criar cartões personalizados
def criar_card(icone, numero, texto, coluna_card):
    container = coluna_card.container(border =True)
    coluna_esquerda, coluna_direita = container.columns([1, 2.5])
    coluna_esquerda.markdown(f" # {icone}", unsafe_allow_html=True)  # Emoji como texto
    coluna_direita.markdown(f"# {numero}")
    coluna_direita.markdown(f"## {texto}")
    


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


