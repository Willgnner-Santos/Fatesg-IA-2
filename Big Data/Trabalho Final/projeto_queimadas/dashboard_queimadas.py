import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# Configuração
# ============================================================
st.set_page_config(
    page_title="Dashboard de Queimadas - Goiás", 
    layout="wide",
    page_icon="🔥"
)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "queimadas_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_TABLE = "fact_queimadas"

# ============================================================
# Função para conectar e carregar dados
# ============================================================
@st.cache_data(ttl=600)
def load_data():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        query = f"SELECT * FROM {POSTGRES_TABLE}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        return None

# ============================================================
# Header
# ============================================================
st.title("🔥 Dashboard de Queimadas em Goiás")
st.markdown("**Análise de focos de incêndio por município (2017-2019)**")

# Carrega dados
with st.spinner("Carregando dados..."):
    df = load_data()

if df is None or df.empty:
    st.error("Nenhum dado disponível no banco de dados.")
    st.stop()

# ============================================================
# Sidebar - Filtros
# ============================================================
st.sidebar.header("⚙️ Filtros")
anos = ["2017", "2018", "2019"]
ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos, index=2)

# Filtro por município
municipios = sorted(df["localidade"].unique())
municipio_filtro = st.sidebar.multiselect(
    "Filtrar municípios (opcional)", 
    municipios,
    default=[]
)

# Aplica filtro
if municipio_filtro:
    df_filtrado = df[df["localidade"].isin(municipio_filtro)]
else:
    df_filtrado = df

# ============================================================
# Métricas principais
# ============================================================
col1, col2, col3, col4 = st.columns(4)

total_municipios = len(df_filtrado)
total_focos = df_filtrado[anos].sum().sum()
total_ano = df_filtrado[ano_selecionado].sum()
media_ano = df_filtrado[ano_selecionado].mean()

col1.metric("📍 Municípios", f"{total_municipios:,}")
col2.metric("🔥 Total de Focos (2017-2019)", f"{int(total_focos):,}")
col3.metric(f"🔥 Focos em {ano_selecionado}", f"{int(total_ano):,}")
col4.metric(f"📊 Média por Município", f"{int(media_ano):,}")

st.divider()

# ============================================================
# Gráfico 1: Evolução temporal
# ============================================================
st.subheader("📈 Evolução de Focos de Queimadas por Ano")
evolucao = df_filtrado[anos].sum()
fig_evolucao = px.line(
    x=anos, 
    y=evolucao.values,
    labels={"x": "Ano", "y": "Total de Focos"},
    markers=True,
    title="Evolução Anual"
)
fig_evolucao.update_traces(line_color='#FF6B6B', marker=dict(size=12))
st.plotly_chart(fig_evolucao, use_container_width=True)

st.divider()

# ============================================================
# Gráfico 2: Top 10 municípios
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"🏆 Top 10 Municípios - {ano_selecionado}")
    top10 = df_filtrado.nlargest(10, ano_selecionado)[["localidade", ano_selecionado]]
    fig_top10 = px.bar(
        top10, 
        x=ano_selecionado, 
        y="localidade",
        orientation='h',
        color=ano_selecionado,
        color_continuous_scale='Reds',
        labels={ano_selecionado: "Focos", "localidade": "Município"}
    )
    fig_top10.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_top10, use_container_width=True)

# ============================================================
# Gráfico 3: Distribuição por faixas
# ============================================================
with col_right:
    st.subheader(f"📊 Distribuição de Focos - {ano_selecionado}")
    bins = [0, 10, 50, 100, 500]
    labels = ['0-10', '11-50', '51-100', '100+']
    df_filtrado['faixa'] = pd.cut(df_filtrado[ano_selecionado], bins=bins, labels=labels, include_lowest=True)
    dist = df_filtrado['faixa'].value_counts().sort_index()
    
    fig_dist = px.pie(
        values=dist.values,
        names=dist.index,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig_dist.update_layout(height=400)
    st.plotly_chart(fig_dist, use_container_width=True)

st.divider()

# ============================================================
# Tabela de dados
# ============================================================
st.subheader("📋 Dados Detalhados")
st.dataframe(
    df_filtrado[["localidade"] + anos].sort_values(by=ano_selecionado, ascending=False),
    use_container_width=True,
    height=400
)

# ============================================================
# Comparativo entre anos
# ============================================================
st.subheader("📊 Comparativo entre Anos")
comparativo = df_filtrado.nlargest(15, ano_selecionado)[["localidade"] + anos]
fig_comparativo = px.bar(
    comparativo.melt(id_vars="localidade", var_name="Ano", value_name="Focos"),
    x="localidade",
    y="Focos",
    color="Ano",
    barmode="group",
    color_discrete_map={"2017": "#FFCDD2", "2018": "#EF5350", "2019": "#B71C1C"}
)
fig_comparativo.update_layout(xaxis_tickangle=-45, height=500)
st.plotly_chart(fig_comparativo, use_container_width=True)

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption("🔥 Dashboard de Queimadas | Dados: 2017-2019 | Desenvolvido com Streamlit")