import reflex as rx
import os
from reflex.constants import LogLevel

is_production = os.getenv("RENDER") == "true" or os.getenv("RENDER_EXTERNAL_URL") is not None

if is_production:
    external_url = os.getenv("RENDER_EXTERNAL_URL", "https://ranking-system-y7h1.onrender.com")
    api_url = external_url
    deploy_url = external_url
else:
    api_url = "http://localhost:8000"
    deploy_url = "http://localhost:3000"

config = rx.Config(
    app_name="app",  # ← MUDOU DE "ranking_system" PARA "app"
    
    api_url=api_url,
    deploy_url=deploy_url,
    backend_port=int(os.getenv("PORT", 8000)),
    frontend_port=3000,
    backend_host="0.0.0.0",
    
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://ranking-system-y7h1.onrender.com",
    ],
    
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    db_url=os.getenv("DATABASE_URL", "sqlite:///reflex.db"),
    telemetry_enabled=False,
    loglevel=LogLevel.INFO if is_production else LogLevel.DEBUG,
)
