import streamlit as st
import numpy as np


st.title("Raylander Guimarães Ramos")

intro = ''' **Projeto de análise de dados de desempenho escolar de estudantes da rede estadual de ensino**

'''

st.markdown(intro)

with st.sidebar:
    st.write('Menu')

with st.container():
    st.write("Gráfico de barras ilustrativo")
    st.bar_chart(np.random.randn(50,3))


col1, col2, col3 = st.columns([ 4, 4, 4])

with st.container():
    with col1:
        st.header("Coluna 1 de informação")

    with col2:
        st.header("Coluna 2 de gráfico de gauge")

    with col3:
        st.header("Coluna 3 gráfico de pizza")

