import reflex as rx
import os
from reflex.constants import LogLevel

# Detecta a URL do Render automaticamente
render_url = os.getenv("RENDER_EXTERNAL_URL")
is_production = render_url is not None

config = rx.Config(
    app_name="app",
    
    # URLs para produção
    api_url=render_url if is_production else "http://localhost:8000",
    deploy_url=render_url if is_production else "http://localhost:3000",
    
    # Porta do Render
    backend_port=int(os.getenv("PORT", 8000)),
    backend_host="0.0.0.0",
    
    # CORS
    cors_allowed_origins=["*"],
    
    # Simplificado
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    telemetry_enabled=False,
    loglevel=LogLevel.INFO,
)
