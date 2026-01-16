"""
database.py - Camada de acesso aos dados
Todas as queries do Supabase ficam aqui
"""
import os
from datetime import datetime, timedelta
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


class SupabaseDB:
    """Cliente Supabase para consultas."""

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("Configure SUPABASE_URL e SUPABASE_KEY no .env")

        self.client = create_client(url, key)
        self.table = "assessores_performance"

    def get_latest_date(self):
        """Retorna última data disponível."""
        response = self.client.table(self.table)\
            .select("data_referencia")\
            .order("data_referencia", desc=True)\
            .limit(1)\
            .execute()

        return response.data[0]["data_referencia"] if response.data else None

    def get_all_dates(self):
        """Retorna todas as datas disponíveis."""
        response = self.client.table(self.table)\
            .select("data_referencia")\
            .order("data_referencia", desc=True)\
            .execute()

        dates = [item["data_referencia"] for item in response.data]
        return sorted(list(set(dates)), reverse=True)

    def get_ranking(self, data_ref):
        """Retorna ranking de uma data."""
        response = self.client.table(self.table)\
            .select("*")\
            .eq("data_referencia", data_ref)\
            .order("rank")\
            .execute()

        return response.data

    def get_assessor_history(self, assessor, days=90):
        """Retorna histórico de um assessor."""
        date_limit = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        response = self.client.table(self.table)\
            .select("*")\
            .eq("assessor", assessor)\
            .gte("data_referencia", date_limit)\
            .order("data_referencia")\
            .execute()

        return response.data

    def get_date_range(self, start_date, end_date):
        """Retorna dados em um intervalo de datas."""
        response = self.client.table(self.table)\
            .select("*")\
            .gte("data_referencia", start_date)\
            .lte("data_referencia", end_date)\
            .order("data_referencia")\
            .execute()

        return response.data