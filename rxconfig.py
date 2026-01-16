import reflex as rx
import os

# Detecta ambiente automaticamente
is_production = os.getenv("RENDER") == "true" or os.getenv("RENDER_EXTERNAL_URL") is not None

# URLs dinâmicas
if is_production:
    # Usa a URL externa do Render
    external_url = os.getenv("RENDER_EXTERNAL_URL", "https://ranking-system-y7h1.onrender.com")
    api_url = external_url  # WebSocket usa mesma URL base
    deploy_url = external_url
else:
    # Desenvolvimento local
    api_url = "http://localhost:8000"
    deploy_url = "http://localhost:3000"

config = rx.Config(
    app_name="ranking_system",
    
    # URLs
    api_url=api_url,
    deploy_url=deploy_url,
    
    # Portas (Render usa PORT env var)
    backend_port=int(os.getenv("PORT", 8000)),
    frontend_port=3000,
    
    # Host
    backend_host="0.0.0.0",
    
    # CORS (importante para produção)
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://ranking-system-y7h1.onrender.com",
    ],
    
    # Desabilita warnings
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    
    # Banco de dados (se usar)
    db_url=os.getenv("DATABASE_URL", "sqlite:///reflex.db"),
    
    # Performance
    telemetry_enabled=False,
    loglevel="info" if is_production else "debug",
)
