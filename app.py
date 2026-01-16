"""
app.py - Liga Gambito Pro
Dashboard de Performance - Versão Final CORRIGIDA
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

# ============================================
# CONFIGURAÇÃO
# ============================================

st.set_page_config(
    page_title="Liga Gambito Pro",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado - Dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
    }

    .header-container {
        background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }

    .header-title {
        color: #fff;
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }

    .header-subtitle {
        color: #ffd700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }

    .metric-label {
        color: #888;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: #ffd700;
        font-size: 28px;
        font-weight: bold;
    }

    .metric-value-green {
        color: #00ff88;
        font-size: 24px;
        font-weight: bold;
    }

    .stButton button {
        background-color: #2d2d2d;
        color: #fff;
        border: 1px solid #444;
        border-radius: 5px;
        padding: 8px 20px;
        font-weight: 500;
    }

    .stButton button:hover {
        background-color: #ffd700;
        color: #000;
        border-color: #ffd700;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    hr {
        border-color: #333;
        margin: 20px 0;
    }

    [data-testid="stDataFrame"] {
        background-color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CACHE
# ============================================

@st.cache_resource(show_spinner=False)
def init_database():
    return SupabaseDB()

@st.cache_data(ttl=600, show_spinner=False)
def get_all_dates(_db):
    return _db.get_all_dates()

@st.cache_data(ttl=600, show_spinner=False)
def get_ranking_cached(_db, data_ref):
    return _db.get_ranking(data_ref)

@st.cache_data(ttl=600, show_spinner=False)
def get_assessor_history_cached(_db, assessor, days):
    return _db.get_assessor_history(assessor, days)

@st.cache_data(ttl=600, show_spinner=False)
def get_date_range_cached(_db, start_date, end_date):
    return _db.get_date_range(start_date, end_date)

# ============================================
# INICIALIZAÇÃO
# ============================================

db = init_database()

with st.spinner("🔄 Carregando..."):
    dates = get_all_dates(db)

if not dates:
    st.error("❌ Sem dados")
    st.stop()

latest = dates[0]

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="header-container">
    <p class="header-subtitle">JFK | LIGA GAMBITO PRO</p>
    <h1 class="header-title">PERFORMANCE INTELLIGENCE SYSTEM</h1>
</div>
""", unsafe_allow_html=True)

# ============================================
# FILTROS NO TOPO
# ============================================

st.markdown("### 📊 Filtros")

col_f1, col_f2, col_f3, col_f4 = st.columns([2, 2, 3, 1])

with col_f1:
    periodo = st.selectbox(
        "📅 Período",
        ["SEMANAL", "MENSAL", "TRIMESTRAL", "TOTAL"],
        index=1
    )

with col_f2:
    selected_date = st.selectbox(
        "📆 Data",
        dates,
        format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y")
    )

with col_f3:
    view_mode = st.selectbox(
        "👁️ Visualização",
        ["Ranking", "Evolução", "Individual"]
    )

with col_f4:
    if st.button("🔄", use_container_width=True, help="Atualizar dados"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# ============================================
# MODO: RANKING
# ============================================

if view_mode == "Ranking":

    with st.spinner("Carregando..."):
        ranking_data = get_ranking_cached(db, selected_date)
        metrics = calculate_metrics(ranking_data)

    if not metrics:
        st.warning("⚠️ Sem dados")
        st.stop()

    # MÉTRICAS
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SCORE MÉDIO EQUIPE</div>
            <div class="metric-value">{metrics['score_medio']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CAP. TOTAL</div>
            <div class="metric-value-green">{format_currency(metrics['cap_total'])}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CAP. PF TOTAL</div>
            <div class="metric-value-green">{format_currency(metrics['cap_pf'])}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MÉDIA ROA XP</div>
            <div class="metric-value">{metrics['roa_medio']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        custodia = metrics['cap_total'] + metrics['cap_pf']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CUSTÓDIA TOTAL</div>
            <div class="metric-value-green">{format_currency(custodia)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # TABELA
    df = pd.DataFrame(ranking_data)

    available_cols = ['rank', 'assessor', 'score', 'cap_total', 'cap_pf', 
                      'roa_xp', 'ativ', 'mds', 'fp', 'nps', 'n_client']

    display_cols = [col for col in available_cols if col in df.columns]
    display_df = df[display_cols].copy()

    # Formatação
    if 'cap_total' in display_df.columns:
        display_df['cap_total'] = display_df['cap_total'].apply(format_currency)
    if 'cap_pf' in display_df.columns:
        display_df['cap_pf'] = display_df['cap_pf'].apply(format_currency)
    if 'roa_xp' in display_df.columns:
        display_df['roa_xp'] = display_df['roa_xp'].apply(lambda x: f"{x:.2f}%")

    # Renomear
    col_names = {
        'rank': 'RANK',
        'assessor': 'ASSESSOR',
        'score': 'SCORE',
        'cap_total': 'CAP. TOTAL',
        'cap_pf': 'CAP. PF',
        'roa_xp': 'ROA XP',
        'ativ': 'ATIV',
        'mds': 'MDS',
        'fp': 'FP',
        'nps': 'NPS',
        'n_client': 'N CLIENT.'
    }

    display_df.columns = [col_names.get(col, col.upper()) for col in display_df.columns]

    st.markdown("### 📋 Ranking de Assessores")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=600
    )

# ============================================
# MODO: EVOLUÇÃO
# ============================================

elif view_mode == "Evolução":

    col1, col2 = st.columns([1, 3])

    with col1:
        weeks = st.slider("Semanas", 4, 52, 12)
        metric = st.selectbox(
            "Métrica",
            ["score", "cap_total", "roa_xp", "nps"],
            format_func=lambda x: {
                "score": "Score",
                "cap_total": "Captação",
                "roa_xp": "ROA XP",
                "nps": "NPS"
            }[x]
        )

    end_date = latest
    start_date = (datetime.strptime(latest, "%Y-%m-%d") - timedelta(weeks=weeks)).strftime("%Y-%m-%d")

    with st.spinner("Carregando..."):
        evolution_data = get_date_range_cached(db, start_date, end_date)

    if not evolution_data:
        st.warning("⚠️ Sem dados")
        st.stop()

    df = pd.DataFrame(evolution_data)

    with col2:
        fig = px.line(
            df,
            x='data_referencia',
            y=metric,
            color='assessor',
            markers=True,
            title=f'Evolução - {metric.upper()}',
            template='plotly_dark'
        )
        fig.update_layout(
            height=600,
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#0a0a0a',
            font_color='#fff'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# MODO: INDIVIDUAL
# ============================================

else:
    ranking_data = get_ranking_cached(db, latest)
    df_latest = pd.DataFrame(ranking_data)

    col1, col2 = st.columns([2, 1])

    with col1:
        assessor = st.selectbox(
            "👤 Assessor",
            sorted(df_latest['assessor'].tolist())
        )

    with col2:
        days = st.slider("Dias", 30, 365, 90, step=30)

    with st.spinner("Carregando..."):
        history_data = get_assessor_history_cached(db, assessor, days)

    if not history_data:
        st.warning(f"⚠️ Sem dados para {assessor}")
        st.stop()

    current = history_data[-1]
    growth = calculate_growth(history_data)

    st.markdown(f"### 🔍 {assessor}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rank", f"#{int(current['rank'])}")

    with col2:
        delta = f"{growth['score_growth']:+.1f}%" if growth else None
        st.metric("Score", f"{current['score']:.1f}", delta=delta)

    with col3:
        delta = f"{growth['cap_growth']:+.1f}%" if growth else None
        st.metric("Captação", format_currency(current['cap_total']), delta=delta)

    with col4:
        st.metric("Clientes", int(current['n_client']))

    st.divider()

    df_history = pd.DataFrame(history_data)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            df_history, 
            x='data_referencia', 
            y='score',
            markers=True, 
            title='Score', 
            template='plotly_dark'
        )
        fig1.update_layout(
            height=350, 
            plot_bgcolor='#1a1a1a', 
            paper_bgcolor='#0a0a0a'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            df_history, 
            x='data_referencia', 
            y='cap_total',
            markers=True, 
            title='Captação', 
            template='plotly_dark'
        )
        fig2.update_layout(
            height=350, 
            plot_bgcolor='#1a1a1a', 
            paper_bgcolor='#0a0a0a'
        )
        st.plotly_chart(fig2, use_container_width=True)

# FOOTER
st.divider()
st.caption(f"📅 {datetime.strptime(latest, '%Y-%m-%d').strftime('%d/%m/%Y')} | ⚡ Cache: 10min | 🏆 Liga Gambito Pro")