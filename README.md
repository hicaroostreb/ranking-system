📊 Liga Gambito Pro - Dashboard
Dashboard de performance de assessores com Streamlit + Supabase.

🚀 Instalação Local
bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar
source venv/bin/activate      # Linux/Mac
source venv/Scripts/activate  # Windows Git Bash

# 3. Instalar
pip install streamlit supabase pandas plotly python-dotenv

# 4. Configurar .env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sb_publishable_sua_chave

# 5. Executar
streamlit run app.py
📁 Estrutura
text
ranking-system/
├── app.py           # Interface Streamlit
├── database.py      # Conexão Supabase
├── business.py      # Lógica de negócio
├── requirements.txt
└── .env            # Credenciais (não commitar)
🌐 Deploy (Streamlit Community Cloud)
Push para GitHub

bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/seu-usuario/ranking-system.git
git push -u origin main
Deploy

Acesse: https://share.streamlit.io

New app → Connect GitHub

Main file path: app.py

Deploy

Adicionar Secrets (Settings → Secrets)

text
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_KEY = "sb_publishable_sua_chave"
🔧 Configuração do Banco
Criar tabela no Supabase
Execute no SQL Editor:

sql
-- Ver arquivo: create_table_assessores.sql
Importar dados
Table Editor → assessores_performance

Insert → Import from CSV

Selecione: assessores_historico_12meses.csv

🎯 Features
✅ Ranking de assessores por data

✅ Evolução temporal (4-52 semanas)

✅ Análise individual com gráficos

✅ 3 modos de visualização

📋 Credenciais Supabase
Pegue em: Settings → API

Project URL → SUPABASE_URL

Publishable key → SUPABASE_KEY

⚠️ Importante
❌ NÃO commite o arquivo .env

✅ Use secrets no Streamlit Cloud

✅ O .gitignore já ignora .env