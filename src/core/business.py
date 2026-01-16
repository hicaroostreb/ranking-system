"""
business.py - Lógica de negócio pura
"""


def calculate_metrics(ranking_data: list[dict]) -> dict:
    """Calcula métricas agregadas do ranking."""
    if not ranking_data:
        return {}

    cap_total = sum(item.get("cap_total", 0) for item in ranking_data)
    cap_pf = sum(item.get("cap_pf", 0) for item in ranking_data)
    roa_medio = sum(item.get("roa_xp", 0) for item in ranking_data) / len(ranking_data)
    score_medio = sum(item.get("score", 0) for item in ranking_data) / len(ranking_data)

    return {
        "score_medio": score_medio,
        "cap_total": cap_total,
        "cap_pf": cap_pf,
        "roa_medio": roa_medio,
        "num_assessores": len(ranking_data)
    }


def calculate_growth(history_data: list[dict]) -> dict:
    """Calcula crescimento baseado no histórico."""
    if not history_data or len(history_data) < 2:
        return {}

    latest = history_data[-1]
    oldest = history_data[0]

    score_growth = 0
    if oldest.get("score"):
        score_growth = ((latest["score"] - oldest["score"]) / oldest["score"]) * 100

    cap_growth = 0
    if oldest.get("cap_total"):
        cap_growth = ((latest["cap_total"] - oldest["cap_total"]) / oldest["cap_total"]) * 100

    return {
        "score_growth": score_growth,
        "cap_growth": cap_growth,
        "rank_change": oldest["rank"] - latest["rank"]
    }


def format_currency(value: float) -> str:
    """Formata valor em reais."""
    if value >= 1_000_000_000:
        return f"R$ {value/1_000_000_000:.1f}bi"
    elif value >= 1_000_000:
        return f"R$ {value/1_000_000:.1f}mi"
    elif value >= 1_000:
        return f"R$ {value/1_000:.0f}k"
    return f"R$ {value:.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Formata percentual."""
    return f"{value:.{decimals}f}%"


def get_top_performers(ranking_data: list[dict], limit: int = 5) -> list[dict]:
    """Retorna top N performers."""
    return ranking_data[:limit]