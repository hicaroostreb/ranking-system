import reflex as rx
import os
from reflex.constants import LogLevel

config = rx.Config(
    app_name="app",
    
    # Simplificado para Render
    backend_port=int(os.getenv("PORT", 8000)),
    backend_host="0.0.0.0",
    
    # Remove CORS temporariamente
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    telemetry_enabled=False,
    loglevel=LogLevel.INFO,
)
