import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, time, timedelta

# --- CONFIGURAÇÃO DE TELA E ESTILO LUXO ---
st.set_page_config(page_title="Espaço da Mulher", page_icon="🌹", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Montserrat:wght@300;400&family=Cinzel&display=swap');
    
    .stApp { background: #fffcfd; }
    
    /* Títulos */
    .main-title { font-family: 'Great Vibes', cursive; color: #d63384; font-size: 4rem; text-align: center; margin-top: -30px; }
    .sub-title { font-family: 'Cinzel', serif; color: #d4af37; text-align: center; letter-spacing: 3px; font-size: 1rem; margin-bottom: 30px; }
    
    /* Fotos das Meninas */
    .profile-container { text-align: center; padding: 20px; transition: 0.3s; cursor: pointer; border-radius: 20px; }
    .profile-container:hover { background: #fff0f3; transform: translateY(-10px); }
    .profile-img { border-radius: 50%; border: 4px solid #d4af37; width: 220px; height: 220px; object-fit: cover; margin-bottom: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    
    /* Cards de Serviço */
    .service-card { background: white; border: 1px solid #ffdeeb; padding: 15px; border-radius: 15px; margin-bottom: 10px; 
                    display: flex; justify-content: space-between; font-family: 'Montserrat'; box-shadow: 2px 2px 10px rgba(0,0,0,0.02); }
    .price-tag { color: #d4af37; font-weight: bold; }
    
    /* Botões */
    .stButton>button { background: linear-gradient(45deg, #d63384, #ff85a2); color: white; border-radius: 30px; border:none; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 5px 15px rgba(214, 51, 132, 0.3); }
    
    /* Esconder elementos do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND INVISÍVEL ---
def salvar_reserva(nome, tel, serv, cat, data, hora):
    conn = sqlite3.connect('salao_sentinela.db')
    lembrete = (data - timedelta(days=2)).strftime('%Y-%m-%d')
    conn.execute("INSERT INTO agendamentos (cliente, telefone, servico, categoria, data, hora, data_lembrete) VALUES (?,?,?,?,?,?,?)",
                 (nome, tel, serv, cat, str(data), hora, lembrete))
    conn.commit()
    conn.close()

# --- LÓGICA DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

def mudar_pagina(nome_pagina):
    st.session_state.pagina = nome_pagina

# --- CONTEÚDO ---
st.markdown('<h1 class="main-title">Espaço da Mulher</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Bianca Teles & Ghi Oliveira</p>', unsafe_allow_html=True)

# --- TELA 1: HOME (ESCOLHA A PROFISSIONAL) ---
if st.session_state.pagina == 'home':
    st.markdown("<h3 style='text-align:center; font-family:Montserrat; color:#666;'>Agendar serviços com:</h3>", unsafe_allow_html=True)
    col_b, col_g = st.columns(2)
    
    with col_b:
        # COLOQUE O LINK DA FOTO DA BIANCA ABAIXO
        st.markdown(f'<div class="profile-container"><img src="https://via.placeholder.com/400x400/FFC0CB/FFFFFF?text=Bianca+Teles" class="profile-img"></div>', unsafe_allow_html=True)
        if st.button("Ver Serviços da Bianca"):
            mudar_pagina('bianca')
            
    with col_g:
        # COLOQUE O LINK DA FOTO DA GHI ABAIXO
        st.markdown(f'<div class="profile-container"><img src="https://via.placeholder.com/400x400/D4AF37/FFFFFF?text=Ghi+Oliveira" class="profile-img"></div>', unsafe_allow_html=True)
        if st.button("Ver Serviços da Ghi"):
            mudar_pagina('ghi')

# --- TELA 2: SERVIÇOS DA BIANCA ---
elif st.session_state.pagina == 'bianca':
    if st.button("← Voltar"): mudar_pagina('home')
    st.markdown("## 💅 Serviços de Unhas | Bianca Teles")
    
    servicos = {"Manicure": "25,00", "Manicure (dec.)": "30,00", "Mão e Pé": "50,00", "Unha em Gel": "150,00", "Manutenção": "80,00", "Spa dos Pés": "60,00", "Blindagem": "70,00"}
    
    for s, p in servicos.items():
        st.markdown(f"<div class='service-card'><span>{s}</span><span class='price-tag'>R$ {p}</span></div>", unsafe_allow_html=True)
        if st.button(f"Agendar {s}", key=s):
            st.session_state.serv_escolhido = s
            st.session_state.cat_escolhida = "BIANCA"
            mudar_pagina('agenda')

# --- TELA 3: SERVIÇOS DA GHI ---
elif st.session_state.pagina == 'ghi':
    if st.button("← Voltar"): mudar_pagina('home')
    st.markdown("## 💇‍♀️ Cabelo & Estética | Ghi Oliveira")
    
    servicos = {"Alisamento": "150,00", "Botox": "100,00", "Escova": "45,00", "Corte": "50,00", "Design Sobrancelha": "35,00", "Design Henna": "50,00", "Depilação Perna": "70,00"}
    
    for s, p in servicos.items():
        st.markdown(f"<div class='service-card'><span>{s}</span><span class='price-tag'>R$ {p}</span></div>", unsafe_allow_html=True)
        if st.button(f"Agendar {s}", key=s):
            st.session_state.serv_escolhido = s
            st.session_state.cat_escolhida = "GHI"
            mudar_pagina('agenda')

# --- TELA 4: AGENDA E DADOS ---
elif st.session_state.pagina == 'agenda':
    if st.button("← Cancelar"): mudar_pagina('home')
    st.markdown(f"### Reservando: {st.session_state.serv_escolhido}")
    
    with st.form("final"):
        nome = st.text_input("Seu Nome Completo")
        tel = st.text_input("Seu WhatsApp (DDD + Número)")
        data = st.date_input("Escolha o dia")
        hora = st.selectbox("Escolha o horário", [f"{h:02d}:00" for h in range(8, 19)])
        
        if st.form_submit_button("CONFIRMAR AGENDAMENTO"):
            if nome and len(tel) >= 10:
                salvar_reserva(nome, tel, st.session_state.serv_escolhido, st.session_state.cat_escolhida, data, hora)
                st.balloons()
                st.success("✅ Sucesso! Agendamento realizado. Voltando ao início...")
                time.sleep(3)
                mudar_pagina('home')
            else:
                st.error("Por favor, preencha nome e telefone corretamente!")