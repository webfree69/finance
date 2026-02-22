import streamlit as st
import pandas as pd
from alpaca_trade_api.rest import REST
import os

# 1. CONFIGURATION DE LA PAGE (DOIT ÊTRE LA PREMIÈRE LIGNE)
st.set_page_config(page_title="Alpha-5 Dashboard", layout="wide", page_icon="📈")

st.title("🚀 Alpha-5 : Monitoring en Temps Réel")

# ==========================================
# 2. SIMULATION VISUELLE (Pour valider l'alerte 🔥)
# ==========================================
st.subheader("🎯 Test de l'Alerte Objectif (+5%)")

# On simule AAPL à 4.65% de profit
mock_profit_pc = 4.65
progress_val = min(max(mock_profit_pc / 5.0, 0.0), 1.0)

col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.write(f"**AAPL (TEST)** | Profit actuel : `{mock_profit_pc}%` / Objectif : `5.00%`")
    st.progress(progress_val)
with col_t2:
    if mock_profit_pc >= 4.5:
        st.warning("🔥 VENTE IMMINENTE")

st.divider()

# ==========================================
# 3. VRAIES DONNÉES DU COMPTE ALPACA
# ==========================================
st.subheader("🏦 Données Réelles du Compte")

try:
    # Récupération sécurisée des clés (Streamlit ou Local)
    try:
        ALPACA_KEY = st.secrets["ALPACA_API_KEY"]
        ALPACA_SECRET = st.secrets["ALPACA_SECRET_KEY"]
        ALPACA_URL = st.secrets["ALPACA_BASE_URL"]
    except Exception:
        ALPACA_KEY = os.getenv('ALPACA_API_KEY')
        ALPACA_SECRET = os.getenv('ALPACA_SECRET_KEY')
        ALPACA_URL = os.getenv('ALPACA_BASE_URL')

    # Connexion à l'API
    api = REST(ALPACA_KEY, ALPACA_SECRET, ALPACA_URL)
    account = api.get_account()

    # Affichage des Soldes
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Solde Cash", f"{float(account.cash):,.2f} $")
    col2.metric("📊 Valeur Portefeuille", f"{float(account.portfolio_value):,.2f} $")
    profit_today = float(account.equity) - float(account.last_equity)
    col3.metric("📅 Profit Jour", f"{profit_today:,.2f} $")
