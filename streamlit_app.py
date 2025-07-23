# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
# st.set_page_config define as configurações iniciais da sua página.
# page_title: O título que aparece na aba do navegador.
# page_icon: O ícone que aparece na aba do navegador (pode ser um emoji).
# layout: "wide" faz com que o conteúdo ocupe toda a largura da tela.
st.set_page_config(page_title="Dashboard de Gráficos", page_icon="📊", layout="wide")

# --- DADOS DE EXEMPLO ---
# Para demonstrar os gráficos, vamos criar um DataFrame (tabela de dados) de exemplo.
# Usaremos a biblioteca pandas para isso.
# np.random.rand(20, 3) cria uma matriz 20x3 com números aleatórios.
# columns=['A', 'B', 'C'] nomeia as colunas.
@st.cache_data # O decorador @st.cache_data armazena o resultado da função em cache.
               # Isso evita que os dados sejam recarregados toda vez que o usuário interage com o app,
               # tornando-o mais rápido.
def carregar_dados():
    df = pd.DataFrame(
        np.random.rand(50, 4),
        columns=['Preço', 'Vendas', 'Meta', 'Dia']
    )
    # Ajustando os dados para ficarem mais realistas para o exemplo
    df['Preço'] = df['Preço'] * 100
    df['Vendas'] = df['Vendas'] * 500
    df['Meta'] = df['Meta'] * 1000
    df['Dia'] = np.arange(1, 51) # Cria uma sequência de 1 a 50
    df['Categoria'] = np.random.choice(['Eletrônicos', 'Roupas', 'Alimentos', 'Livros'], 50) # Adiciona uma coluna de categoria
    return df

df = carregar_dados()


# --- BARRA LATERAL (SIDEBAR) ---
# Tudo o que for adicionado ao objeto st.sidebar aparecerá na barra lateral esquerda.
st.sidebar.header("Filtros e Opções")

# Caixa de Seleção (Selectbox)
# st.sidebar.selectbox cria uma caixa de seleção na barra lateral.
# O primeiro argumento é o rótulo que aparece acima da caixa de seleção.
# O segundo argumento é uma lista de opções para o usuário escolher.
# A escolha do usuário é armazenada na variável 'tipo_de_grafico'.
tipo_de_grafico = st.sidebar.selectbox(
    "Selecione o tipo de gráfico:",
    ["Gráfico de Linha", "Gráfico de Barras", "Gráfico de Dispersão (Scatter)", "Gráfico de Pizza (Pie)", "Histograma"]
)


# --- PÁGINA PRINCIPAL ---
# st.title() cria um título principal para a sua aplicação.
st.title("📊 Dashboard Interativo de Gráficos")
st.markdown("---") # Cria uma linha horizontal para separar o conteúdo

# st.markdown() permite escrever texto formatado usando a sintaxe Markdown.
st.markdown("Use a **caixa de seleção** na barra lateral à esquerda para escolher o gráfico que deseja visualizar.")


# --- LÓGICA PARA EXIBIR O GRÁFICO SELECIONADO ---
# Usamos uma estrutura if/elif/else para verificar qual opção foi escolhida
# na variável 'tipo_de_grafico' e então exibir o gráfico correspondente.

# Se o usuário escolher "Gráfico de Linha"
if tipo_de_grafico == "Gráfico de Linha":
    st.subheader("Gráfico de Linha: Vendas ao longo dos Dias")
    # px.line cria um gráfico de linha.
    # df: o DataFrame com os dados.
    # x: a coluna para o eixo X.
    # y: a coluna (ou colunas) para o eixo Y.
    fig = px.line(df, x="Dia", y=["Vendas", "Meta"], title="Evolução de Vendas vs. Meta")
    # st.plotly_chart() exibe o gráfico criado com Plotly na página.
    st.plotly_chart(fig, use_container_width=True)

# Se o usuário escolher "Gráfico de Barras"
elif tipo_de_grafico == "Gráfico de Barras":
    st.subheader("Gráfico de Barras: Total de Vendas por Categoria")
    # Agrupamos os dados por categoria e somamos as vendas
    vendas_por_categoria = df.groupby('Categoria')['Vendas'].sum().reset_index()
    # px.bar cria um gráfico de barras.
    fig = px.bar(vendas_por_categoria, x="Categoria", y="Vendas", title="Total de Vendas por Categoria", color="Categoria")
    st.plotly_chart(fig, use_container_width=True)

# Se o usuário escolher "Gráfico de Dispersão (Scatter)"
elif tipo_de_grafico == "Gráfico de Dispersão (Scatter)":
    st.subheader("Gráfico de Dispersão: Relação entre Preço e Vendas")
    # px.scatter cria um gráfico de dispersão, ideal para ver a correlação entre duas variáveis.
    fig = px.scatter(df, x="Preço", y="Vendas", color="Categoria", title="Relação Preço vs. Vendas")
    st.plotly_chart(fig, use_container_width=True)

# Se o usuário escolher "Gráfico de Pizza (Pie)"
elif tipo_de_grafico == "Gráfico de Pizza (Pie)":
    st.subheader("Gráfico de Pizza: Proporção de Vendas por Categoria")
    # px.pie cria um gráfico de pizza, bom para mostrar proporções.
    fig = px.pie(df, names="Categoria", values="Vendas", title="Proporção de Vendas por Categoria")
    st.plotly_chart(fig, use_container_width=True)

# Se o usuário escolher "Histograma"
elif tipo_de_grafico == "Histograma":
    st.subheader("Histograma: Distribuição de Preços dos Produtos")
    # px.histogram cria um histograma, que mostra a distribuição de uma variável numérica.
    fig = px.histogram(df, x="Preço", nbins=20, title="Distribuição de Preços")
    st.plotly_chart(fig, use_container_width=True)

# --- EXIBINDO OS DADOS BRUTOS (OPCIONAL) ---
# Adiciona uma seção para mostrar a tabela de dados se o usuário quiser ver.
st.markdown("---")
st.subheader("Dados Brutos")
st.dataframe(df)
