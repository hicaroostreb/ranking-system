"""
app.py - Interface Streamlit
Versão final otimizada e atualizada para Streamlit 1.39+
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from database import SupabaseDB
from business import (
    calculate_metrics,
    calculate_growth,
    format_currency,
    format_percentage,
    get_top_performers
)

# Configuração
st.set_page_config(
    page_title="Liga Gambito Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CACHE OTIMIZADO
# ============================================

@st.cache_resource(show_spinner="Conectando ao banco...")
def init_database():
    """Cache do cliente Supabase."""
    return SupabaseDB()

@st.cache_data(ttl=600, show_spinner="Carregando datas...")
def get_all_dates(_db):
    """Cache das datas disponíveis (10min)."""
    return _db.get_all_dates()

@st.cache_data(ttl=600, show_spinner="Carregando ranking...")
def get_ranking_cached(_db, data_ref):
    """Cache do ranking por data (10min)."""
    return _db.get_ranking(data_ref)

@st.cache_data(ttl=600, show_spinner="Carregando histórico...")
def get_assessor_history_cached(_db, assessor, days):
    """Cache do histórico do assessor (10min)."""
    return _db.get_assessor_history(assessor, days)

@st.cache_data(ttl=600, show_spinner="Carregando evolução...")
def get_date_range_cached(_db, start_date, end_date):
    """Cache do range de datas (10min)."""
    return _db.get_date_range(start_date, end_date)

# ============================================
# INICIALIZAÇÃO
# ============================================

db = init_database()

# ============================================
# INTERFACE
# ============================================

st.title("📊 Liga Gambito Pro")
st.markdown("**Performance Intelligence System**")
st.divider()

# Carregar dados iniciais
dates = get_all_dates(db)

if not dates:
    st.error("❌ Nenhum dado disponível no banco")
    st.info("Verifique se a tabela foi criada e os dados importados")
    st.stop()

latest = dates[0]

# ============================================
# SIDEBAR
# ============================================

st.sidebar.header("🎛️ Filtros")
view_mode = st.sidebar.radio(
    "Modo de Visualização",
    ["📊 Ranking", "📈 Evolução", "🔍 Individual"],
    help="Escolha o tipo de análise"
)

# ============================================
# MODO 1: RANKING
# ============================================

if view_mode == "📊 Ranking":
    selected_date = st.sidebar.selectbox(
        "📅 Selecione a data",
        dates,
        format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y")
    )

    # Buscar dados
    ranking_data = get_ranking_cached(db, selected_date)
    metrics = calculate_metrics(ranking_data)

    if not metrics:
        st.warning("⚠️ Sem dados para esta data")
        st.stop()

    # Métricas em cards
    st.subheader("📈 Métricas Gerais")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Score Médio", f"{metrics['score_medio']:.1f}")
    with col2:
        st.metric("Cap. Total", format_currency(metrics['cap_total']))
    with col3:
        st.metric("Cap. PF Total", format_currency(metrics['cap_pf']))
    with col4:
        st.metric("ROA Médio", format_percentage(metrics['roa_medio']))

    st.divider()

    # Tabs
    tab1, tab2 = st.tabs(["📋 Tabela Completa", "📊 Gráfico de Barras"])

    with tab1:
        df = pd.DataFrame(ranking_data)

        # Preparar dados para exibição
        display_df = df[['rank', 'assessor', 'score', 'cap_total', 'cap_pf', 
                        'roa_xp', 'ativ', 'mds', 'fp', 'nps', 'n_client']].copy()

        # Formatação
        display_df['cap_total'] = display_df['cap_total'].apply(format_currency)
        display_df['cap_pf'] = display_df['cap_pf'].apply(format_currency)
        display_df['roa_xp'] = display_df['roa_xp'].apply(lambda x: f"{x:.2f}%")

        display_df.columns = ['#', 'Assessor', 'Score', 'Cap. Total', 'Cap. PF',
                             'ROA XP', 'Ativ', 'MDS', 'FP', 'NPS', 'Clientes']

        st.dataframe(
            display_df, 
            width="stretch",  # Atualizado: use_container_width → width
            hide_index=True,
            height=400
        )

    with tab2:
        df = pd.DataFrame(ranking_data)

        fig = px.bar(
            df.sort_values('score', ascending=False).head(10),  # Top 10 para performance
            x='assessor',
            y='score',
            color='score',
            color_continuous_scale='RdYlGn',
            title='Top 10 Assessores por Score',
            labels={'assessor': 'Assessor', 'score': 'Score'}
        )
        fig.update_layout(
            showlegend=False, 
            height=500,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# MODO 2: EVOLUÇÃO
# ============================================

elif view_mode == "📈 Evolução":
    col1, col2 = st.sidebar.columns(2)

    with col1:
        weeks = st.slider("📅 Semanas", 4, 52, 12)

    with col2:
        metric = st.selectbox(
            "📊 Métrica",
            ["score", "cap_total", "roa_xp", "nps", "n_client"],
            format_func=lambda x: {
                "score": "Score",
                "cap_total": "Captação",
                "roa_xp": "ROA XP",
                "nps": "NPS",
                "n_client": "Clientes"
            }[x]
        )

    end_date = latest
    start_date = (datetime.strptime(latest, "%Y-%m-%d") - timedelta(weeks=weeks)).strftime("%Y-%m-%d")

    # Buscar dados
    evolution_data = get_date_range_cached(db, start_date, end_date)

    if not evolution_data:
        st.warning("⚠️ Sem dados para este período")
        st.stop()

    df = pd.DataFrame(evolution_data)

    st.subheader(f"📈 Evolução: {metric.upper()}")
    st.caption(f"Últimas {weeks} semanas")

    # Gráfico de linha
    fig = px.line(
        df,
        x='data_referencia',
        y=metric,
        color='assessor',
        markers=True,
        title=f'Evolução de {metric.upper()} ao longo do tempo',
        labels={
            'data_referencia': 'Data',
            metric: metric.upper(),
            'assessor': 'Assessor'
        }
    )
    fig.update_layout(
        height=600,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Ranking atual
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🏆 Top 5 Atual")
        current = get_ranking_cached(db, latest)
        top5 = get_top_performers(current, 5)
        df_top = pd.DataFrame(top5)

        display_top = df_top[['rank', 'assessor', 'score', 'cap_total']].copy()
        display_top['cap_total'] = display_top['cap_total'].apply(format_currency)
        display_top.columns = ['#', 'Assessor', 'Score', 'Captação']

        st.dataframe(display_top, width="stretch", hide_index=True)

# ============================================
# MODO 3: INDIVIDUAL
# ============================================

else:
    # Carregar ranking
    ranking_data = get_ranking_cached(db, latest)
    df_latest = pd.DataFrame(ranking_data)

    # Sidebar
    assessor = st.sidebar.selectbox(
        "👤 Selecione o Assessor",
        sorted(df_latest['assessor'].tolist())
    )

    days = st.sidebar.slider(
        "📅 Período de Análise (dias)",
        min_value=30,
        max_value=365,
        value=90,
        step=30
    )

    # Buscar histórico
    history_data = get_assessor_history_cached(db, assessor, days)

    if not history_data:
        st.warning(f"⚠️ Sem dados para {assessor}")
        st.stop()

    current = history_data[-1]
    growth = calculate_growth(history_data)

    # Header
    st.subheader(f"🔍 Análise Individual: {assessor}")
    st.caption(f"Período: últimos {days} dias")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rank Atual", f"#{int(current['rank'])}")

    with col2:
        if growth:
            delta_score = f"{growth['score_growth']:+.1f}%"
            st.metric("Score", f"{current['score']:.1f}", delta=delta_score)
        else:
            st.metric("Score", f"{current['score']:.1f}")

    with col3:
        if growth:
            delta_cap = f"{growth['cap_growth']:+.1f}%"
            st.metric("Captação Total", format_currency(current['cap_total']), delta=delta_cap)
        else:
            st.metric("Captação Total", format_currency(current['cap_total']))

    with col4:
        if growth and growth['rank_change'] != 0:
            delta_rank = f"{growth['rank_change']:+d} posições"
            st.metric("Mudança no Rank", delta_rank)
        else:
            st.metric("Clientes", int(current['n_client']))

    st.divider()

    # Gráficos de evolução
    st.subheader("📊 Evolução Temporal")

    df_history = pd.DataFrame(history_data)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            df_history, 
            x='data_referencia', 
            y='score',
            markers=True,
            title='Evolução do Score',
            labels={'data_referencia': 'Data', 'score': 'Score'}
        )
        fig1.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            df_history,
            x='data_referencia',
            y='cap_total',
            markers=True,
            title='Evolução da Captação Total',
            labels={'data_referencia': 'Data', 'cap_total': 'Captação'}
        )
        fig2.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Histórico detalhado
    st.divider()
    st.subheader("📋 Histórico Detalhado")

    history_display = df_history[['data_referencia', 'rank', 'score', 'cap_total', 'roa_xp', 'n_client']].copy()
    history_display = history_display.sort_values('data_referencia', ascending=False)

    history_display['data_referencia'] = pd.to_datetime(history_display['data_referencia']).dt.strftime('%d/%m/%Y')
    history_display['cap_total'] = history_display['cap_total'].apply(format_currency)
    history_display['roa_xp'] = history_display['roa_xp'].apply(lambda x: f"{x:.2f}%")

    history_display.columns = ['Data', 'Rank', 'Score', 'Captação', 'ROA XP', 'Clientes']

    st.dataframe(history_display, width="stretch", hide_index=True, height=300)

# ============================================
# FOOTER
# ============================================

st.sidebar.divider()
st.sidebar.caption(f"📅 Última atualização: {datetime.strptime(latest, '%Y-%m-%d').strftime('%d/%m/%Y')}")
st.sidebar.caption("⚡ Cache ativo (10 min)")

# Botão para limpar cache
if st.sidebar.button("🔄 Recarregar Dados", help="Limpa o cache e recarrega dados do banco"):
    st.cache_data.clear()
    st.rerun()