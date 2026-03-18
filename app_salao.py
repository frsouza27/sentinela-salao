import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection
from datetime import datetime, timedelta
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Espaço da Mulher | Sentinela", page_icon="✨", layout="wide")

# --- DESIGN PREMIUM: ROSA, GLITTER E FONTES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #fff5f8 0%, #ffe4ed 100%); }
    .main-title {
        font-family: 'Great Vibes', cursive;
        background: linear-gradient(to right, #d63384, #d4af37, #d63384);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 4.5rem !important; text-align: center; font-weight: bold;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .sub-title {
        font-family: 'Cinzel', serif; color: #b8860b; text-align: center;
        letter-spacing: 5px; font-size: 1.1rem; margin-top: -20px; margin-bottom: 40px; font-weight: 700;
    }
    .price-card {
        background: white; border-left: 5px solid #d4af37; padding: 12px;
        margin-bottom: 10px; border-radius: 8px; display: flex;
        justify-content: space-between; align-items: center;
        box-shadow: 2px 2px 10px rgba(214, 51, 132, 0.1);
    }
    .price-name { font-family: 'Montserrat', sans-serif; font-weight: 600; color: #444; }
    .price-value { font-family: 'Cinzel', serif; color: #d63384; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(45deg, #d63384, #d4af37) !important;
        color: white !important; border-radius: 50px !important; font-weight: bold !important;
        width: 100%; transition: 0.3s;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO SEGURA ---
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except:
    st.error("Erro na ligação ao Banco de Dados.")

# --- SEGURANÇA SENTINELA (IP) ---
def get_user_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        return _get_websocket_headers().get("X-Forwarded-For", "127.0.0.1").split(",")[0]
    except: return "127.0.0.1"

def possui_reserva_ativa(ip):
    res = conn.table("agendamentos").select("id").eq("ip_cliente", ip).in_("status", ["pendente", "aguardando"]).execute()
    return len(res.data) > 0

# --- INTERFACE ---
st.markdown('<h1 class="main-title">Espaço da Mulher</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">SENTINELA OMNI | PREMIUM SERVICE</p>', unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state.pagina = 'home'

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# --- HOME: ESCOLHA DA PROFISSIONAL ---
if st.session_state.pagina == 'home':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align:center; font-family:Great Vibes;'>Bianca Teles (Unhas)</h3>", unsafe_allow_html=True)
        if st.button("VER SERVIÇOS DE UNHAS ✨"): 
            st.session_state.profissional = "BIANCA"
            navegar('servicos')
    with col2:
        st.markdown("<h3 style='text-align:center; font-family:Great Vibes;'>Ghi Oliveira (Cabelo & Estética)</h3>", unsafe_allow_html=True)
        if st.button("VER SERVIÇOS DE CABELO/DEPILAÇÃO ✨"): 
            st.session_state.profissional = "GHI"
            navegar('servicos')

# --- PÁGINA DE SERVIÇOS SEPARADOS ---
elif st.session_state.pagina == 'servicos':
    if st.button("← VOLTAR"): navegar('home')
    
    # DEFINIÇÃO DOS SERVIÇOS POR PROFISSIONAL
    if st.session_state.profissional == "BIANCA":
        st.markdown("### ✨ Serviços de Unhas - Bianca")
        lista = {
            "Manicure (Simples)": "25,00",
            "Manicure (c/ Decoração)": "30,00",
            "Pé (c/ Decoração)": "35,00",
            "Mão e Pé (Simples)": "50,00",
            "Mão e Pé (c/ Decoração)": "60,00",
            "Unha Postiça": "55,00",
            "Unha em Gel na Tips": "150,00",
            "Manutenção Gel": "80,00",
            "Spa dos Pés": "60,00",
            "Blindagem": "70,00",
            "Banho de Gel": "80,00",
            "Esmaltação Simples": "20,00",
            "Esmaltação (c/ Decoração)": "25,00"
        }
    else:
        st.markdown("### 💇‍♀️ Cabelo & Estética - Ghi")
        lista = {
            "Alisamento (A partir de)": "150,00",
            "Botox Capilar": "100,00",
            "Escova": "45,00",
            "Penteados": "100,00",
            "Tratamento Personalizado": "60,00",
            "Corte Simples": "50,00",
            "Aplicação de Coloração": "50,00",
            "Depilação Meia Perna": "35,00",
            "Depilação Perna Inteira": "70,00",
            "Depilação Buço": "20,00",
            "Depilação Queixo e Buço": "35,00",
            "Depilação Axila": "35,00",
            "Designer de Sobrancelha": "35,00",
            "Designer c/ Henna": "50,00"
        }

    for s, v in lista.items():
        st.markdown(f'<div class="price-card"><span class="price-name">{s}</span><span class="price-value">R$ {v}</span></div>', unsafe_allow_html=True)
        if st.button(f"ESCOLHER {s.upper()}", key=s):
            st.session_state.servico = s
            navegar('form')

# --- FORMULÁRIO FINAL ---
elif st.session_state.pagina == 'form':
    if st.button("← VOLTAR"): navegar('servicos')
    st.markdown(f"#### Confirmando: {st.session_state.servico} com {st.session_state.profissional}")
    
    with st.form("final"):
        nome = st.text_input("Seu Nome")
        tel = st.text_input("WhatsApp (Ex: 11999999999)")
        data = st.date_input("Escolha a Data")
        hora = st.selectbox("Escolha a Hora", [f"{h:02d}:00" for h in range(8, 20)])
        
        if st.form_submit_button("FINALIZAR ✨"):
            ip = get_user_ip()
            if possui_reserva_ativa(ip):
                st.error("⚠️ Segurança: Você já possui um agendamento ativo!")
            elif not nome or not tel:
                st.warning("Preencha todos os campos.")
            else:
                conn.table("agendamentos").insert([{
                    "cliente": nome, "telefone": tel, "servico": st.session_state.servico,
                    "categoria": st.session_state.profissional, "data": data.isoformat(),
                    "hora": hora, "ip_cliente": ip, "status": "pendente"
                }]).execute()
                st.balloons()
                st.success("✨ Agendamento enviado! Aguarde o contato do Sentinela.")
                time.sleep(2); navegar('home')
