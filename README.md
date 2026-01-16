# Ranking System

Sistema de ranking desenvolvido com Reflex.

## 🚀 Deploy

Deploy automático no Render: https://ranking-system-y7h1.onrender.com

## 💻 Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Inicializar app
reflex init

# Rodar em dev
reflex run
🔧 Variáveis de Ambiente
DATABASE_URL: URL do banco de dados (opcional)

PORT: Porta do backend (auto no Render)

text

## 📦 Como Aplicar o Patch

```bash
# 1. Atualizar rxconfig.py
# Copie o código acima

# 2. Commit e push
git add rxconfig.py .gitignore
git commit -m "fix: configure production URLs and WebSocket connection"
git push origin main

# 3. O Render vai redesenhar automaticamente