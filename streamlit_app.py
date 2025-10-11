import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Desempenho Escolar", layout="wide")

st.title("Análise de Desempenho e Demografia de Estudantes do Ensino Médio")



with st.sidebar:
    st.subheader("Painel de controle")
    page = st.radio("Ir para", ["Introdução", "Dados de Português", "Dados de Matemática", "Evoluções"])



if page == "Introdução":
    st.markdown("""
    **Autor:** Raylander Guimarães Ramos  
    **Descrição:**  
    Este aplicativo é um **MVP** que demonstra a análise de dados educacionais.  
    Aqui você encontrará visualizações e métricas sobre o desempenho em **Português** e **Matemática**.
    
    O aplicativo apresenta uma base de dados de desempenho escolar, que abrange não apenas as notas dos estudantes, mas também diversos aspectos contextuais e socioeconômicos.
    Entre as variáveis analisadas estão:

    👨‍👩‍👧‍👦 Composição familiar: número de integrantes da família e situação conjugal dos pais.

    🏫 Características da escola: localização e motivo da escolha da instituição.

    💑 Aspectos pessoais: se o estudante está em um relacionamento amoroso.

    ⚧️ Informações demográficas: gênero e idade do estudante.

    🎓 Nível educacional dos responsáveis: grau de escolaridade do pai e da mãe.

    💼 Situação profissional dos responsáveis: ocupação da mãe e do pai.

    🕒 Hábitos de estudo: horas de estudo por semana e tempo de deslocamento até a escola.

    📉 Histórico acadêmico: quantidade de reprovações anteriores.

    💚 Aspectos estruturais e de saúde: variáveis que refletem o ambiente escolar e o bem-estar do estudante.
    """)

elif page == "Dados de Português":
    @st.cache_data
    def load_data():
        return pd.read_csv('student_portuguese_clean.csv')
    df = load_data()
    
    st.subheader("Desempenho e Demografia de Estudantes do Ensino Médio")
    st.subheader("Dez primeiros registros da base de dados")
    st.dataframe(df.head(10), )
    
    st.subheader("Tabela de Descrição dos dados")
    st.dataframe(df.describe())

    st.subheader("Distribuição de notas finais Português")
    notas = df['final_grade']
    fig, ax = plt.subplots()
    ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
    ax.set_xlabel("Nota")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

elif page == "Dados de Matemática":
    @st.cache_data
    def load_data():
        return pd.read_csv('student_math_clean.csv')
    df = load_data()
    
    st.subheader("Desempenho e Demografia de Estudantes do Ensino Médio")
    st.subheader("Dez primeiros registros da base de dados")
    st.dataframe(df.head(10), )
    
    st.subheader("Tabela de Descrição dos dados")
    st.dataframe(df.describe())

    st.subheader("Distribuição de notas finais Matemática")
    notas = df['final_grade']
    fig, ax = plt.subplots()
    ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
    ax.set_xlabel("Nota")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

elif page == "Evoluções":
    st.subheader("Evoluções")
    st.markdown("""
    🚀 Objetivo do MVP
    Inicialmente foi feito apenas a exploração dos dados, e a plotagem das métricas de todas as 
    features, futuramente o aplicativo pode evoluir para atender os seguintes objetivos:
    - Identificar correlações entre fatores socioeconômicos e desempenho escolar.
    - Gerar métricas e insights estatísticos sobre o comportamento dos estudantes.
    - Realizar predições com base em modelos de aprendizado de máquina,
    a fim de estimar o desempenho escolar ou identificar fatores de risco.
    """)

