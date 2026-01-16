"""
config.py - Configurações da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações centralizadas."""

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # App
    APP_NAME = "Liga Gambito Pro"
    VERSION = "1.0.0"

    # Cache
    CACHE_TTL = 600  # 10 minutos

    @classmethod
    def validate(cls):
        """Valida configurações obrigatórias."""
        if not cls.SUPABASE_URL:
            raise ValueError("SUPABASE_URL não configurada")
        if not cls.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY não configurada")
        return True