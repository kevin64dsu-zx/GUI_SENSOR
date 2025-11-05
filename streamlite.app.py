# ==========================================================
# 🌡️ PROJETO IoT – MONITOR DE GASES
# Autor: Grupo 3 Kevin (Fatec)
# Objetivo: Monitorar níveis de CO e CH₄ em tempo real com alertas visuais e sonoros
# ==========================================================

import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="Monitor de Gases IoT", layout="wide")

st.title("💨 Monitor de Gases – IoT")
st.write("""
Sistema de monitoramento de gases perigosos.  
As leituras abaixo vêm do **endpoint Flask online**.
""")

# ==========================================================
# 🛰️ Leitura via endpoint Flask no Render
# ==========================================================
FLASK_URL = "https://end-point-c138.onrender.com/dados"  # <-- Teu endpoint no Render

def ler_dados_sensor():
    try:
        resposta = requests.get(FLASK_URL)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            st.error("Falha ao obter dados do endpoint Flask.")
            return {"CO": 0, "CH4": 0}
    except Exception as e:
        st.error(f"Erro de conexão com o servidor Flask: {e}")
        return {"CO": 0, "CH4": 0}

def emitir_som_alerta():
    sound_html = """
    <audio autoplay>
      <source src="data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAAA////AP///wAAAP///wD///8A//8AAP8AAAAAAP///wD///8A//8AAP8AAAAAAP///wAA//8A//8AAP8AAP8AAAAA//8AAP///wAA//8A//8AAP8AAP8AAAAA//8AAAAAAP///wD///8A//8AAP8AAP8AAAAA" type="audio/wav">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# ==========================================================
# 🎨 Estrutura visual
# ==========================================================
col1, col2 = st.columns(2)
placeholder = st.empty()
historico = []

st.write("📡 Iniciando monitoramento em tempo real...")

for ciclo in range(100):
    dados = ler_dados_sensor()
    historico.append(dados)
    df = pd.DataFrame(historico)

    with placeholder.container():
        col1.metric("CO (ppm)", dados["CO"])
        col2.metric("CH₄ (ppm)", dados["CH4"])

        st.line_chart(df)

        if dados["CO"] > 80 or dados["CH4"] > 150:
            st.error("🔴 PERIGO: Concentração crítica detectada!")
            emitir_som_alerta()
        elif dados["CO"] > 50 or dados["CH4"] > 100:
            st.warning("🟠 Atenção: níveis elevados, verifique o ambiente.")
            emitir_som_alerta()
        else:
            st.success("🟢 Ambiente seguro.")

    time.sleep(1)

st.info("✅ Monitoramento finalizado.")
