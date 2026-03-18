import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA (BACK-END) ---
st.set_page_config(page_title="Espaço da Mulher | Bia e Ghi", page_icon="✨", layout="centered")

# --- 2. FRONT-END: CSS PREMIUM (INTERFACE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=Montserrat:wght@400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #fff5f8 0%, #ffe4ed 100%); }
    .main-title {
        font-family: 'Great Vibes', cursive;
        background: linear-gradient(to right, #b83280, #8a6d1a, #b83280);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 4rem !important; text-align: center; font-weight: bold;
    }
    .sub-title {
        font-family: 'Cinzel', serif; color: #7a5d0a !important; text-align: center;
        letter-spacing: 4px; font-size: 1rem; margin-bottom: 40px;
    }
    .price-card {
        background: white; border-left: 6px solid #d4af37; padding: 15px;
        margin-bottom: 15px; border-radius: 10px; display: flex;
        justify-content: space-between; align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .price-name { font-family: 'Montserrat', sans-serif; color: #333 !important; font-weight: 600; }
    .price-value { font-family: 'Cinzel', serif; color: #b83280 !important; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(45deg, #d63384, #d4af37) !important;
        color: white !important; border-radius: 12px !important; font-weight: bold !important;
        width: 100%; border: none !important; height: 3em; transition: 0.3s;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXÃO E SEGURANÇA (BACK-END) ---
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except:
    st.error("Erro de conexão com o Banco de Dados.")

def get_user_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        return _get_websocket_headers().get("X-Forwarded-For", "127.0.0.1").split(",")[0]
    except: return "127.0.0.1"

def possui_reserva_ativa(ip):
    try:
        res = conn.table("agendamentos").select("id").eq("ip_cliente", ip).in_("status", ["pendente", "aguardando"]).execute()
        return len(res.data) > 0
    except: return False

# --- 4. LÓGICA DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'home'

def navegar(destino):
    st.session_state.pagina = destino
    st.rerun()

# --- 5. ROTEAMENTO DE PÁGINAS ---
st.markdown('<h1 class="main-title">Espaço da Mulher</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">SENTINELA OMNI | PREMIUM SERVICE</p>', unsafe_allow_html=True)

# PÁGINA HOME
if st.session_state.pagina == 'home':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align:center; font-family:Great Vibes; color:#b83280;'>Bianca Teles</h3>", unsafe_allow_html=True)
        if st.button("VER UNHAS ✨"): 
            st.session_state.profissional = "BIANCA"
            navegar('servicos')
    with col2:
        st.markdown("<h3 style='text-align:center; font-family:Great Vibes; color:#b83280;'>Ghi Oliveira</h3>", unsafe_allow_html=True)
        if st.button("VER ESTÉTICA ✨"): 
            st.session_state.profissional = "GHI"
            navegar('servicos')

# PÁGINA SERVIÇOS
elif st.session_state.pagina == 'servicos':
    st.button("← VOLTAR", on_click=lambda: navegar('home'))
    prof = st.session_state.profissional
    st.markdown(f"<h2 style='text-align:center; color:#8a6d1a; font-family:Cinzel;'>{prof}</h2>", unsafe_allow_html=True)
    
    lista = {
        "BIANCA": {"Manicure": "25,00", "Pé e Mão": "50,00", "Gel na Tips": "150,00"},
        "GHI": {"Escova": "45,00", "Botox": "100,00", "Sobrancelha": "35,00"}
    }[prof]

    for s, v in lista.items():
        st.markdown(f'<div class="price-card"><span class="price-name">{s}</span><span class="price-value">R$ {v}</span></div>', unsafe_allow_html=True)
        if st.button(f"ESCOLHER {s.upper()}", key=s):
            st.session_state.servico = s
            navegar('form')

# PÁGINA FORMULÁRIO
elif st.session_state.pagina == 'form':
    st.button("← VOLTAR", on_click=lambda: navegar('servicos'))
    with st.form("final"):
        nome = st.text_input("Nome")
        tel = st.text_input("WhatsApp")
        data = st.date_input("Data")
        hora = st.selectbox("Hora", [f"{h:02d}:00" for h in range(8, 20)])
        
        if st.form_submit_button("FINALIZAR ✨"):
            ip = get_user_ip()
            if possui_reserva_ativa(ip):
                st.error("🚨 Você já tem um agendamento!")
            else:
                conn.table("agendamentos").insert([{
                    "cliente": nome, "telefone": tel, "servico": st.session_state.servico,
                    "categoria": st.session_state.profissional, "data": str(data),
                    "hora": hora, "ip_cliente": ip, "status": "pendente"
                }]).execute()
                st.balloons()
                st.success("Agendamento Enviado!")
                time.sleep(2); navegar('home')
