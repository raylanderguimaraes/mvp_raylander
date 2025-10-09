import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.title("Raylander Guimarães Ramos")

intro = ''' **Projeto de análise de dados de desempenho escolar de estudantes da rede estadual de ensino**

'''
@st.cache_data
def load_data(name):
    return pd.read_csv(name)


df = load_data('student_math_clean.csv')

st.subheader("Desempenho e Demografia de Estudantes do Ensino Médio: Matemática")
st.subheader("Dez primeiros registros da base de dados")
st.dataframe(df.head(10), )

st.subheader("Tabela de Descrição dos dados")
st.dataframe(df.describe())

st.markdown(intro)





with st.container():
    st.subheader("Distribuição das notas de Matemática")
    notas = df['final_grade']
    fig, ax = plt.subplots()
    ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
    ax.set_xlabel("Nota")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)


# col1, col2, col3 = st.columns([ 4, 4, 4])

# with st.container():
#     with col1:
#         st.header("Coluna 1 de informação")

#     with col2:
#         st.header("Coluna 2 de gráfico de gauge")

#     with col3:
#         st.header("Coluna 3 gráfico de pizza")

