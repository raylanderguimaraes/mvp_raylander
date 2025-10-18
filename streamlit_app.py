import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Análise de Desempenho Escolar", layout="wide")

st.title("Análise de Desempenho e Demografia de Estudantes do Ensino Médio")

with st.sidebar:
    st.subheader("Painel de controle")
    page = st.radio("Ir para", ["Introdução", "Dados de Português", "Dados de Matemática", "Análises Avançadas", "Evoluções"])
    
colunas_traduzidas = {
    "student_id": "id_estudante",
    "school": "escola",
    "sex": "sexo",
    "age": "idade",
    "address_type": "tipo_endereco",
    "family_size": "tamanho_familia",
    "parent_status": "situacao_pais",
    "mother_education": "escolaridade_mae",
    "father_education": "escolaridade_pai",
    "mother_job": "ocupacao_mae",
    "father_job": "ocupacao_pai",
    "school_choice_reason": "motivo_escolha_escola",
    "guardian": "responsavel",
    "travel_time": "tempo_deslocamento",
    "study_time": "tempo_estudo",
    "class_failures": "repetencias",
    "school_support": "apoio_escolar",
    "family_support": "apoio_familiar",
    "extra_paid_classes": "aulas_extras",
    "activities": "atividades_extracurriculares",
    "nursery_school": "frequentou_creche",
    "higher_ed": "deseja_ensino_superior",
    "internet_access": "acesso_internet",
    "romantic_relationship": "relacionamento_amoroso",
    "family_relationship": "relacionamento_familiar",
    "free_time": "tempo_livre",
    "social": "vida_social",
    "weekday_alcohol": "alcool_dias_uteis",
    "weekend_alcohol": "alcool_fim_semana",
    "health": "saude",
    "absences": "faltas",
    "grade_1": "nota_1",
    "grade_2": "nota_2",
    "final_grade": "nota_final"
}

if page == "Introdução":
    st.markdown("""
    **Autor:** Raylander Guimarães Ramos  
    **Descrição:**  
    Este aplicativo é um **MVP** que demonstra a análise de dados educacionais.  
    Aqui você encontrará visualizações e métricas sobre o desempenho em **Português** e **Matemática**.
    
    O aplicativo apresenta uma base de dados de desempenho escolar, que abrange não apenas as notas dos estudantes, mas também diversos aspectos contextuais e socioeconômicos.
    
    **Sobre o Conjunto de Dados**
    
    Este conjunto de dados contém dados sobre o desempenho dos alunos de duas escolas secundárias portuguesas.
    Os dados foram coletados por meio de relatórios escolares e questionários e incluem notas dos alunos, dados demográficos, sociais, parentais e características relacionadas à escola.

    Dois conjuntos de dados são fornecidos sobre o desempenho em duas disciplinas distintas: Matemática e Língua Portuguesa.
    
    Disponível em: https://www.kaggle.com/datasets/dillonmyrick/high-school-student-performance-and-demographics
    """)


elif page == "Dados de Português":
    @st.cache_data
    def load_data():
        return pd.read_csv('student_portuguese_clean.csv')
    df = load_data()
    df.rename(columns=colunas_traduzidas, inplace=True)

    st.subheader("Desempenho e Demografia de Estudantes - Português")
    st.dataframe(df.head(10))

  
    tab1, tab2, tab3 = st.tabs(["📊 Notas", "👩‍🎓 Perfil dos estudantes", "📈 Hábitos e apoio"])

    with tab1:
        st.markdown("### Distribuição das notas finais em Português")
        notas = df['nota_final']
        fig, ax = plt.subplots()
        ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
        ax.set_xlabel("Nota")
        ax.set_ylabel("Quantidade de estudantes")
        st.pyplot(fig)

        st.markdown("### Média de notas por gênero")
        medias = df.groupby('sexo')['nota_final'].mean()
        fig, ax = plt.subplots()
        medias.plot(kind='bar', color=['#ff9999', '#66b3ff'], ax=ax)
        ax.set_ylabel("Média das notas")
        st.pyplot(fig)

    with tab2:
        st.markdown("### Distribuição por idade")
        fig, ax = plt.subplots()
        df['idade'].hist(bins=10, color='lightgreen', edgecolor='white', ax=ax)
        ax.set_xlabel("Idade")
        ax.set_ylabel("Quantidade")
        st.pyplot(fig)

        st.markdown("### Quantidade de estudantes por escola")
        fig, ax = plt.subplots()
        df['escola'].value_counts().plot(kind='bar', color='orange', ax=ax)
        ax.set_xlabel("Escola")
        ax.set_ylabel("Quantidade de alunos")
        st.pyplot(fig)

    with tab3:
        st.markdown("### Nota média por tempo de estudo semanal")
        medias_estudo = df.groupby('tempo_estudo')['nota_final'].mean()
        fig, ax = plt.subplots()
        medias_estudo.plot(kind='bar', color='lightblue', ax=ax)
        ax.set_xlabel("Tempo de estudo (categoria)")
        ax.set_ylabel("Média da nota final")
        st.pyplot(fig)

        st.markdown("### Efeito do apoio familiar e escolar no desempenho")
        apoio = df.groupby(['apoio_escolar', 'apoio_familiar'])['nota_final'].mean().unstack()
        fig, ax = plt.subplots()
        apoio.plot(kind='bar', ax=ax)
        ax.set_xlabel("Apoio Escolar (Sim/Não)")
        ax.set_ylabel("Média da nota final")
        st.pyplot(fig)


elif page == "Dados de Matemática":
    @st.cache_data
    def load_data():
        return pd.read_csv('student_math_clean.csv')
    df = load_data()
    df.rename(columns=colunas_traduzidas, inplace=True)

    st.subheader("Desempenho e Demografia de Estudantes - Matemática")
    st.dataframe(df.head(10))

    with st.container():
        st.markdown("### Filtros")
        col1, col2 = st.columns(2)
        sexo_filtro = col1.selectbox("Filtrar por sexo:", ["Todos"] + sorted(df['sexo'].unique().tolist()))
        escola_filtro = col2.selectbox("Filtrar por escola:", ["Todas"] + sorted(df['escola'].unique().tolist()))

        df_filtrado = df.copy()
        if sexo_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo_filtro]
        if escola_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['escola'] == escola_filtro]

    tab1, tab2, tab3 = st.tabs(["📊 Notas", "📈 Comparações", "🏫 Fatores externos"])

    with tab1:
        st.markdown("### Distribuição das notas finais em Matemática")
        notas = df_filtrado['nota_final']
        fig, ax = plt.subplots()
        ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
        ax.set_xlabel("Nota")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

        st.markdown("### Média de notas por gênero")
        medias = df_filtrado.groupby('sexo')['nota_final'].mean()
        fig, ax = plt.subplots()
        medias.plot(kind='bar', color=['#ff9999', '#66b3ff'], ax=ax)
        ax.set_ylabel("Média das notas")
        st.pyplot(fig)

    with tab2:
        st.markdown("### Média das notas por tempo de estudo")
        medias_estudo = df_filtrado.groupby('tempo_estudo')['nota_final'].mean()
        fig, ax = plt.subplots()
        medias_estudo.plot(kind='bar', color='lightblue', ax=ax)
        ax.set_xlabel("Tempo de estudo (categoria)")
        ax.set_ylabel("Média da nota final")
        st.pyplot(fig)

        st.markdown("### Relação entre número de faltas e nota final")
        fig, ax = plt.subplots()
        ax.scatter(df_filtrado['faltas'], df_filtrado['nota_final'], alpha=0.6, color='green')
        ax.set_xlabel("Faltas")
        ax.set_ylabel("Nota final")
        st.pyplot(fig)

    with tab3:
        st.markdown("### Nota média por nível de escolaridade dos pais")
        fig, ax = plt.subplots()
        df_filtrado.groupby('escolaridade_pai')['nota_final'].mean().plot(kind='bar', ax=ax, color='salmon', label='Pai')
        df_filtrado.groupby('escolaridade_mae')['nota_final'].mean().plot(kind='bar', ax=ax, color='lightgreen', label='Mãe')
        ax.set_xlabel("Nível educacional")
        ax.set_ylabel("Média da nota final")
        ax.legend()
        st.pyplot(fig)

elif page == "Análises Avançadas":
    st.subheader("🔍 Análises Avançadas de Correlação")
    
    st.markdown("### 📈 Mapa de Correlação entre Variáveis Numéricas")
    tipo_dado = st.radio("Escolha o conjunto de dados", ["Português", "Matemática"])

    @st.cache_data
    def load_data(tipo):
        if tipo == "Português":
            return pd.read_csv('student_portuguese_clean.csv')
        else:
            return pd.read_csv('student_math_clean.csv')

    df = load_data(tipo_dado)
    df = df.drop(columns=["id_estudante"], errors="ignore")
   
    df.rename(columns=colunas_traduzidas, inplace=True)

    variaveis_numericas = [col for col in df.select_dtypes(include=['int64', 'float64']).columns 
                       if col != "id_estudante"]
    
    variaveis_selecionadas = st.multiselect(
        "Selecione as variáveis para incluir no mapa de calor:",
        variaveis_numericas,
        default=["idade", "repetencias", "faltas", "nota_final", "nota_1", "nota_2"]
    )

    if len(variaveis_selecionadas) >= 2:
        corr = df[variaveis_selecionadas].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Selecione pelo menos duas variáveis para gerar o mapa de correlação.")
        
    

    

    st.markdown("### 🏘️ Comparações entre Grupos")

    var_categ = st.selectbox(
        "Escolha uma variável categórica para comparar:",
        ["sexo", "tipo_endereco", "apoio_familiar", "acesso_internet", "relacionamento_amoroso"]
    )

    # Calcula a média da nota final por grupo
    media_notas_df = df.groupby(var_categ)["nota_final"].mean().reset_index()

    # Gráfico de barras horizontal interativo com Altair
    grafico = alt.Chart(media_notas_df).mark_bar().encode(
        y=alt.Y(var_categ, sort='-x'),   # eixo Y com os grupos, ordenado pela média
        x="nota_final",
        tooltip=[var_categ, "nota_final"]  # mostra tooltip ao passar o mouse
    ).properties(
        height=300,
        width=600,
        title=f"Média da nota final por {var_categ}"
    )

    st.altair_chart(grafico, use_container_width=True)
    
elif page == "Evoluções":
    st.subheader("Evoluções")
    st.markdown("""
    🚀 Objetivo do MVP
    - Identificar correlações entre fatores socioeconômicos e desempenho escolar.
    - Gerar métricas e insights estatísticos sobre o comportamento dos estudantes.
    - Realizar predições com base em modelos de aprendizado de máquina,
      a fim de estimar o desempenho escolar ou identificar fatores de risco.
    """)
