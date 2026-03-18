import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection
from datetime import datetime, timedelta
import time

# --- CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="Espaço da Mulher | Sentinela", page_icon="✨", layout="wide")

# --- DESIGN LUXO: ROSA, GLITTER DOURADO E FONTE CHIQUE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');
    
    .stApp { background: linear-gradient(135deg, #fff5f8 0%, #ffe4ed 100%); }

    .main-title {
        font-family: 'Great Vibes', cursive;
        background: linear-gradient(to right, #d63384 20%, #d4af37 40%, #d4af37 60%, #d63384 80%);
        background-size: 200% auto;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-size: 4.5rem !important;
        text-align: center;
        margin-bottom: 0px;
        font-weight: bold;
    }

    @keyframes shine { to { background-position: 200% center; } }

    .sub-title {
        font-family: 'Cinzel', serif;
        color: #b8860b;
        text-align: center;
        letter-spacing: 5px;
        font-size: 1rem;
        margin-top: -20px;
        margin-bottom: 50px;
        font-weight: 700;
    }

    .profile-img {
        border-radius: 50%;
        border: 5px solid #d4af37;
        padding: 5px;
        background: radial-gradient(circle, #fff3e0, #d4af37);
        width: 260px; height: 260px;
        object-fit: cover;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }

    .service-item {
        background: white;
        border: 2px solid #fce4ec;
        border-image: linear-gradient(45deg, #ff85a2, #d4af37) 1;
        padding: 15px; margin-bottom: 10px;
        display: flex; justify-content: space-between;
        box-shadow: 3px 3px 10px rgba(214, 51, 132, 0.05);
    }

    .stButton>button {
        background: linear-gradient(45deg, #d63384, #ff85a2, #d4af37) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        animation: glitter-btn 4s ease infinite;
    }

    @keyframes glitter-btn { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO SUPABASE ---
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except:
    st.error("Erro na ligação ao Banco de Dados.")

# --- SEGURANÇA: CAPTURA DE IP E TRAVA ---
def get_user_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", "Localhost").split(",")[0]
    except:
        return "Localhost"

def verificar_agendamento_ativo(ip):
    # Procura agendamentos que NÃO estejam cancelados para este IP
    res = conn.table("agendamentos").select("id").eq("ip_cliente", ip).neq("status", "cancelado").execute()
    return len(res.data) > 0

def db_salvar_reserva(nome, tel, serv, cat, data, hora):
    ip = get_user_ip()
    if verificar_agendamento_ativo(ip):
        return False, "⚠️ Já tens uma reserva ativa! Aguarda o cancelamento ou contacta-nos."
    
    data_str = data.isoformat()
    lembrete = (data - timedelta(days=2)).isoformat()
    
    conn.table("agendamentos").insert([{
        "cliente": nome, "telefone": tel, "servico": serv, "categoria": cat,
        "data": data_str, "hora": hora, "data_lembrete": lembrete,
        "status": "pendente", "ip_cliente": ip, "criado_em": datetime.now().isoformat()
    }]).execute()
    return True, "✅ Reserva confirmada com sucesso! ✨"

# --- NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'home'
def navegar(dest): 
    st.session_state.pagina = dest
    st.rerun()

st.markdown('<h1 class="main-title">Espaço da Mulher</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">BY BIANCA TELES & GHI OLIVEIRA</p>', unsafe_allow_html=True)

if st.session_state.pagina == 'home':
    col_b, col_g = st.columns(2)
    with col_b:
        st.markdown('<div style="text-align:center;"><img src="https://via.placeholder.com/400?text=Bianca" class="profile-img"></div>', unsafe_allow_html=True)
        if st.button("AGENDAR COM BIANCA ✨"): navegar('bianca')
    with col_g:
        st.markdown('<div style="text-align:center;"><img src="https://via.placeholder.com/400?text=Ghi" class="profile-img"></div>', unsafe_allow_html=True)
        if st.button("AGENDAR COM GHI ✨"): navegar('ghi')

elif st.session_state.pagina in ['bianca', 'ghi']:
    if st.button("← VOLTAR"): navegar('home')
    prof = st.session_state.pagina.capitalize()
    st.markdown(f"<h2 style='font-family:Great Vibes; color:#d63384;'>Serviços de {prof}</h2>", unsafe_allow_html=True)
    
    lista = {"Manicure": "25,00", "Pé e Mão": "50,00", "Cabelo": "100,00"} # Exemplos
    for s, p in lista.items():
        st.markdown(f"<div class='service-item'><b>{s}</b><span style='color:#b8860b;'>R$ {p}</span></div>", unsafe_allow_html=True)
        if st.button(f"Escolher {s}", key=s):
            st.session_state.serv_escolhido = s
            st.session_state.cat_escolhida = prof.upper()
            navegar('form')

elif st.session_state.pagina == 'form':
    with st.form("final"):
        nome = st.text_input("Nome Completo")
        tel = st.text_input("WhatsApp (Ex: 11999999999)")
        data = st.date_input("Data")
        hora = st.selectbox("Hora", [f"{h:02d}:00" for h in range(8, 20)])
        if st.form_submit_button("CONFIRMAR ✨"):
            ok, msg = db_salvar_reserva(nome, tel, st.session_state.serv_escolhido, st.session_state.cat_escolhida, data, hora)
            if ok:
                st.balloons()
                st.success(msg)
                time.sleep(2); navegar('home')
            else: st.error(msg)
    if st.button("Cancelar"): navegar('home')
