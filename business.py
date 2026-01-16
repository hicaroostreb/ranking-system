"""
business.py - Lógica de negócio
Cálculos, agregações e regras ficam aqui
"""


def calculate_metrics(ranking_data):
    """Calcula métricas agregadas do ranking."""
    if not ranking_data:
        return None

    cap_total = sum(item["cap_total"] for item in ranking_data)
    cap_pf = sum(item["cap_pf"] for item in ranking_data)
    roa_medio = sum(item["roa_xp"] for item in ranking_data) / len(ranking_data)
    score_medio = sum(item["score"] for item in ranking_data) / len(ranking_data)

    return {
        "score_medio": score_medio,
        "cap_total": cap_total,
        "cap_pf": cap_pf,
        "roa_medio": roa_medio,
        "num_assessores": len(ranking_data)
    }


def calculate_growth(history_data):
    """Calcula crescimento baseado no histórico."""
    if not history_data or len(history_data) < 2:
        return None

    latest = history_data[-1]
    oldest = history_data[0]

    score_growth = ((latest["score"] - oldest["score"]) / oldest["score"]) * 100 if oldest["score"] else 0
    cap_growth = ((latest["cap_total"] - oldest["cap_total"]) / oldest["cap_total"]) * 100 if oldest["cap_total"] else 0

    return {
        "score_growth": score_growth,
        "cap_growth": cap_growth,
        "rank_change": oldest["rank"] - latest["rank"]  # positivo = subiu no ranking
    }


def format_currency(value):
    """Formata valor em reais."""
    if value >= 1_000_000_000:
        return f"R$ {value/1_000_000_000:.1f} bi"
    elif value >= 1_000_000:
        return f"R$ {value/1_000_000:.1f} mi"
    return f"R$ {value/1000:.0f} mil"


def format_percentage(value, decimals=2):
    """Formata percentual."""
    return f"{value:.{decimals}f}%"


def get_top_performers(ranking_data, limit=5):
    """Retorna top N performers."""
    return ranking_data[:limit]


def filter_by_score(ranking_data, min_score):
    """Filtra assessores por score mínimo."""
    return [item for item in ranking_data if item["score"] >= min_score]