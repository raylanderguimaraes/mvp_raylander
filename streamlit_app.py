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

# Função genérica para carregar e renomear os dados
@st.cache_data
def load_data(tipo):
    if tipo == "Português":
        df = pd.read_csv('student_portuguese_clean.csv')
    else:
        df = pd.read_csv('student_math_clean.csv')
    df.rename(columns=colunas_traduzidas, inplace=True)
    return df

# Função genérica para criar a aba de notas
def aba_notas(df, disciplina):
    st.subheader(f"Desempenho e Demografia de Estudantes - {disciplina}")
    st.dataframe(df.head(10))

    # Filtros
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

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Notas", "📈 Comparações", "🏫 Fatores externos"])

    with tab1:
        st.markdown(f"### Distribuição das notas finais em {disciplina}")
        notas = df_filtrado['nota_final']
        fig, ax = plt.subplots()
        ax.hist(notas, bins=20, color='skyblue', edgecolor='white')
        ax.set_xlabel("Nota")
        ax.set_ylabel("Quantidade de estudantes")
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

        # st.markdown("### Relação entre número de faltas e nota final")
        # fig, ax = plt.subplots()
        # ax.scatter(df_filtrado['faltas'], df_filtrado['nota_final'], alpha=0.6, color='green')
        # ax.set_xlabel("Faltas")
        # ax.set_ylabel("Nota final")
        # st.pyplot(fig)

    with tab3:
        st.markdown("### Nota média por nível de escolaridade dos pais")
        fig, ax = plt.subplots()
        df_filtrado.groupby('escolaridade_pai')['nota_final'].mean().plot(kind='bar', ax=ax, color='salmon', label='Pai')
        df_filtrado.groupby('escolaridade_mae')['nota_final'].mean().plot(kind='bar', ax=ax, color='lightgreen', label='Mãe')
        ax.set_xlabel("Nível educacional")
        ax.set_ylabel("Média da nota final")
        ax.legend()
        st.pyplot(fig)


# Página Introdução
if page == "Introdução":
    st.markdown("""
    **Autor:** Raylander Guimarães Ramos  
    **Descrição:**  
    Este aplicativo é um **MVP** que demonstra a análise de dados educacionais.  
    Aqui você encontrará visualizações e métricas sobre o desempenho em **Português** e **Matemática**.
    
    **Sobre o Conjunto de Dados**
    
    Este conjunto de dados contém informações sobre o desempenho dos alunos de duas escolas secundárias portuguesas, incluindo notas, dados demográficos, sociais e parentais.
    
    Dois conjuntos de dados são fornecidos: Matemática e Língua Portuguesa.
    
    Disponível em: https://www.kaggle.com/datasets/dillonmyrick/high-school-student-performance-and-demographics
    """)

# Página Dados de Português
elif page == "Dados de Português":
    df = load_data("Português")
    aba_notas(df, "Português")

# Página Dados de Matemática
elif page == "Dados de Matemática":
    df = load_data("Matemática")
    aba_notas(df, "Matemática")

# Página Análises Avançadas
elif page == "Análises Avançadas":
    st.subheader("🔍 Análises Avançadas de Correlação")
    
    tipo_dado = st.radio("Escolha o conjunto de dados", ["Português", "Matemática"])
    df = load_data(tipo_dado)
    df = df.drop(columns=["id_estudante"], errors="ignore")

    # Seleção de variáveis numéricas
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
    media_notas_df = df.groupby(var_categ)["nota_final"].mean().reset_index()

    grafico = alt.Chart(media_notas_df).mark_bar().encode(
        y=alt.Y(var_categ, sort='-x'),
        x="nota_final",
        tooltip=[var_categ, "nota_final"]
    ).properties(
        height=300,
        width=600,
        title=f"Média da nota final por {var_categ}"
    )
    st.altair_chart(grafico, use_container_width=True)

# Página Evoluções
elif page == "Evoluções":
    st.subheader("Evoluções")
    st.markdown("""
    🚀 Objetivo do MVP
    - Identificar correlações entre fatores socioeconômicos e desempenho escolar.
    - Gerar métricas e insights estatísticos sobre o comportamento dos estudantes.
    - Realizar predições com base em modelos de aprendizado de máquina,
      a fim de estimar o desempenho escolar ou identificar fatores de risco.
    """)
