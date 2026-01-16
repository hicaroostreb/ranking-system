"""
main.py - App principal Reflex
"""
import reflex as rx
from .state import DashboardState
from .components.metric_card import metric_card
from ..infrastructure.config import Config


def index() -> rx.Component:
    """Página principal do dashboard."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    f"🏆 {Config.APP_NAME}",
                    size="8",
                ),
                rx.badge("JFK", color_scheme="yellow", size="3"),
                justify="between",
                width="100%",
            ),

            rx.divider(),

            # Filtros
            rx.hstack(
                rx.select(
                    DashboardState.dates,
                    value=DashboardState.selected_date,
                    on_change=DashboardState.change_date,
                    placeholder="📅 Selecione a data",
                    size="3",
                ),
                rx.select(
                    ["Ranking", "Evolução", "Individual"],
                    value=DashboardState.view_mode,
                    on_change=DashboardState.change_view,
                    placeholder="👁️ Visualização",
                    size="3",
                ),
                rx.button(
                    rx.icon("refresh-cw", size=18),
                    "Atualizar",
                    on_click=DashboardState.refresh,
                    loading=DashboardState.is_loading,
                    size="3",
                ),
                spacing="3",
                width="100%",
            ),

            rx.divider(),

            # Métricas
            rx.cond(
                DashboardState.view_mode == "Ranking",
                rx.grid(
                    metric_card(
                        "Score Médio",
                        rx.text(DashboardState.metrics.get("score_medio", 0)),
                        "yellow",
                        "award"
                    ),
                    metric_card(
                        "Cap. Total",
                        rx.text(DashboardState.metrics.get("cap_total", 0)),
                        "green",
                        "trending-up"
                    ),
                    metric_card(
                        "Cap. PF",
                        rx.text(DashboardState.metrics.get("cap_pf", 0)),
                        "green",
                        "dollar-sign"
                    ),
                    metric_card(
                        "ROA Médio",
                        rx.text(DashboardState.metrics.get("roa_medio", 0)),
                        "blue",
                        "percent"
                    ),
                    columns="4",
                    spacing="4",
                    width="100%",
                ),
            ),

            rx.divider(),

            # Tabela
            rx.cond(
                DashboardState.view_mode == "Ranking",
                rx.card(
                    rx.heading("📋 Ranking de Assessores", size="5"),
                    rx.data_table(
                        data=DashboardState.ranking_data,
                        columns=["rank", "assessor", "score", "cap_total", "roa_xp"],
                        pagination=True,
                        search=True,
                        sort=True,
                    ),
                    size="3",
                ),
            ),

            # Footer
            rx.divider(),
            rx.hstack(
                rx.text(f"v{Config.VERSION}", size="1", color="gray"),
                rx.text("⚡ Cache: 10min", size="1", color="gray"),
                rx.text("🏆 Liga Gambito Pro", size="1", color="gray"),
                justify="center",
                spacing="4",
            ),

            spacing="5",
            width="100%",
        ),
        size="4",
        on_mount=DashboardState.on_load,
    )


# App config
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="yellow",
    )
)

app.add_page(index, route="/", title=Config.APP_NAME)