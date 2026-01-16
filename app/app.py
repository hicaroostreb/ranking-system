"""Dashboard Liga Gambito Pro"""
import reflex as rx


class State(rx.State):
    dates: list[str] = ["2026-01-16", "2026-01-15", "2026-01-14"]
    selected_date: str = "2026-01-16"
    view_mode: str = "Ranking"
    is_loading: bool = False
    
    metrics: dict = {
        "score_medio": 85.5,
        "cap_total": "R$ 50.2M",
        "cap_pf": "R$ 30.1M",
        "roa_medio": 8.5
    }
    
    ranking_data: list[dict] = [
        {"rank": 1, "assessor": "João Silva", "score": 95.5, "cap_total": "R$ 10.5M", "cap_pf": "R$ 6.2M", "roa_xp": 9.2, "nps": 92},
        {"rank": 2, "assessor": "Maria Santos", "score": 92.3, "cap_total": "R$ 8.2M", "cap_pf": "R$ 5.1M", "roa_xp": 8.8, "nps": 89},
        {"rank": 3, "assessor": "Pedro Costa", "score": 88.1, "cap_total": "R$ 6.5M", "cap_pf": "R$ 4.3M", "roa_xp": 8.1, "nps": 85},
    ]
    
    def change_date(self, date: str):
        self.selected_date = date
        
    def change_view(self, mode: str):
        self.view_mode = mode
        
    def refresh(self):
        self.is_loading = True
        yield
        self.is_loading = False


def metric_card(label: str, value, color: str = "blue"):
    """Card de métrica sem ícone."""
    return rx.card(
        rx.vstack(
            rx.text(label, size="2", weight="medium", color=rx.color("gray", 11)),
            value,
            spacing="3",
            align="start",
        ),
        size="3",
        style={
            "transition": "all 0.2s",
            "_hover": {
                "transform": "translateY(-2px)",
            },
        },
    )


def index():
    return rx.box(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.icon("trophy", size=32, color="gold"),
                    rx.vstack(
                        rx.heading("Liga Gambito Pro", size="6"),
                        rx.text("Performance Intelligence", size="1", color="gray"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                ),
                rx.spacer(),
                rx.badge("JFK", color_scheme="yellow", size="3"),
                width="100%",
                align="center",
            ),
            bg=rx.color("gray", 2),
            padding="1rem",
            position="sticky",
            top="0",
            z_index="999",
        ),
        rx.container(
            rx.vstack(
                rx.card(
                    rx.vstack(
                        rx.heading(" Filtros", size="4"),
                        rx.grid(
                            rx.vstack(
                                rx.text("Data", size="2", weight="medium"),
                                rx.select(
                                    State.dates, 
                                    value=State.selected_date, 
                                    on_change=State.change_date, 
                                    size="3"
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Visualização", size="2", weight="medium"),
                                rx.select(
                                    ["Ranking", "Evolução"], 
                                    value=State.view_mode, 
                                    on_change=State.change_view, 
                                    size="3"
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.vstack(
                                rx.text("Ações", size="2", weight="medium"),
                                rx.button(
                                    " Atualizar", 
                                    on_click=State.refresh, 
                                    loading=State.is_loading, 
                                    size="3"
                                ),
                                align="start",
                                spacing="2",
                            ),
                            columns="3",
                            spacing="4",
                        ),
                        spacing="4",
                    ),
                    size="3",
                ),
                rx.grid(
                    metric_card(" Score Médio", rx.text("85.5", size="7", weight="bold"), "yellow"),
                    metric_card(" Captação Total", rx.text("R$ 50.2M", size="7", weight="bold"), "green"),
                    metric_card(" Cap. PF", rx.text("R$ 30.1M", size="7", weight="bold"), "green"),
                    metric_card(" ROA Médio", rx.text("8.5%", size="7", weight="bold"), "blue"),
                    columns="4",
                    spacing="4",
                ),
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.heading(" Ranking de Assessores", size="5"),
                            rx.badge(State.selected_date, color_scheme="gray"),
                            justify="between",
                            width="100%",
                        ),
                        rx.data_table(
                            data=State.ranking_data,
                            columns=["rank", "assessor", "score", "cap_total", "cap_pf", "roa_xp", "nps"],
                            pagination=True,
                            search=True,
                            sort=True,
                        ),
                        spacing="4",
                    ),
                    size="3",
                ),
                spacing="5",
                padding_y="2rem",
            ),
            size="4",
        ),
        rx.box(
            rx.hstack(
                rx.text(" 2026 Liga Gambito Pro", size="2", color="gray"),
                rx.spacer(),
                rx.text(" Cache: 10min   JFK", size="2", color="gray"),
                width="100%",
                align="center",
            ),
            bg=rx.color("gray", 2),
            padding="1rem",
            margin_top="2rem",
        ),
        min_height="100vh",
        bg=rx.color("gray", 1),
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="yellow",
        gray_color="slate",
        radius="large",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
)

app.add_page(index, route="/", title="Liga Gambito Pro | Dashboard")
