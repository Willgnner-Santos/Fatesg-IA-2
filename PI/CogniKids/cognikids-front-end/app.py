"""
CogniKids - Sistema Educacional Infantil Inteligente
Arquivo principal do aplicativo Streamlit (com roteamento por papel)
"""

import streamlit as st
from pathlib import Path

# Importa os módulos
from modules.login import (
    mostrar_tela_login, 
    verificar_login, 
    obter_usuario_logado, 
    mostrar_perfil_header,
    fazer_logout
)
from utils.api_client import api_client
from config import APP_CONFIG

# --- MÓDULOS DE ALUNO ---
from modules.dashboard import mostrar_dashboard
from modules.activities import mostrar_atividades
from modules.reports import mostrar_relatorios

# --- MÓDULOS DE PROFESSOR (Serão criados) ---
try:
    from modules.teacher_dashboard import mostrar_painel_professor
    from modules.manage_students import mostrar_gerenciador_alunos
    from modules.manage_classes import mostrar_gerenciador_turmas
except ImportError:
    pass

# --- MÓDULOS DE PAIS (Serão criados) ---
try:
    from modules.parent_dashboard import mostrar_painel_responsavel
except ImportError:
    pass


# Configuração da página
st.set_page_config(
    page_title="CogniKids - Aprendendo com Diversão",
    page_icon="CK",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
def aplicar_estilos():
    """
    Aplica estilos CSS customizados
    """
    st.markdown("""
        <style>
        /* Importa fonte Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        /* Estilos globais */
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Esconde elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Estiliza botões */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Estiliza inputs */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #E5E7EB;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #8B5CF6;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        }
        
        /* Estiliza sidebar */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #8B5CF6 0%, #EC4899 100%);
            padding: 2rem 1rem;
        }
        
        .css-1d391kg p, [data-testid="stSidebar"] p,
        .css-1d391kg span, [data-testid="stSidebar"] span,
        .css-1d391kg label, [data-testid="stSidebar"] label {
            color: white !important;
        }
        
        /* Estiliza expanders */
        .streamlit-expanderHeader {
            border-radius: 10px;
            background-color: #F9FAFB;
            font-weight: 600;
        }
        
        /* Estiliza métricas */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        /* Animações */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .element-container {
            animation: slideIn 0.5s ease-out;
        }
        
        /* Estiliza tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 1rem 2rem;
            font-weight: 600;
        }
        
        /* Cores do tema */
        :root {
            --primary-color: #8B5CF6;
            --secondary-color: #EC4899;
            --accent-color: #FACC15;
            --success-color: #10B981;
            --info-color: #3B82F6;
        }
        </style>
    """, unsafe_allow_html=True)

def inicializar_sessao():
    """
    Inicializa variáveis de sessão
    """
    if 'pagina_atual' not in st.session_state:
        st.session_state['pagina_atual'] = 'login'
    if 'usuario_logado' not in st.session_state:
        st.session_state['usuario_logado'] = None

def mostrar_sidebar():
    """
    Mostra a sidebar com navegação baseada no tipo de usuário.
    """
    with st.sidebar:
        # Logo
        logo_relative_path = APP_CONFIG.get("LOGO_PATH", "")
        # Constrói o caminho absoluto baseado no diretório do app
        base_dir = Path(__file__).parent  # Diretório cognikids/
        logo_path = base_dir / logo_relative_path
        
        if logo_path.exists():
            st.image(str(logo_path), width=250)
        else:
            # Fallback para texto se logo nao existir
            st.markdown("""
                <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
                    <h2 style='color: white; margin: 0.5rem 0 0 0;'>CogniKids</h2>
                    <p style='color: white; opacity: 0.9; margin: 0;'>Aprendendo com diversão!</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # --- LÓGICA DE MENU DINÂMICO ---
        
        usuario = obter_usuario_logado()
        menu_items = {}
        default_page = 'login'

        if not usuario:
            st.warning("Usuário não logado.")
            return

        user_type = usuario.get('tipo')

        if user_type == 'aluno' or user_type == 'estudante':
            st.markdown("### Menu do Aluno")
            menu_items = {
                'dashboard': {'label': 'Meu Desempenho', 'icon': ''},
                'activities': {'label': 'Atividades', 'icon': ''},
                'reports': {'label': 'Relatórios', 'icon': ''}
            }
            default_page = 'dashboard'
        
        elif user_type == 'professor':
            st.markdown("### Menu do Professor")
            menu_items = {
                'teacher_dashboard': {'label': 'Painel Professor', 'icon': ''},
                'manage_students': {'label': 'Gerenciar Alunos', 'icon': ''},
                'manage_classes': {'label': 'Minhas Turmas', 'icon': ''}
            }
            default_page = 'teacher_dashboard'
            
        elif user_type == 'pai':
            st.markdown("### Menu do Responsável")
            menu_items = {
                'parent_dashboard': {'label': 'Painel Família', 'icon': ''},
            }
            default_page = 'parent_dashboard'
        
        else:
            st.error(f"Tipo de usuário '{user_type}' não reconhecido.")
            fazer_logout()
            st.rerun()

        # Define a página padrão se a atual não pertencer ao menu
        if st.session_state['pagina_atual'] not in menu_items:
             st.session_state['pagina_atual'] = default_page
             
        # Renderiza os botões do menu
        for key, item in menu_items.items():
            if st.button(
                item['label'],
                key=f"menu_{key}",
                width="stretch",
                type="primary" if st.session_state['pagina_atual'] == key else "secondary"
            ):
                st.session_state['pagina_atual'] = key
                st.rerun()
        
        st.divider()
        
        # Informacoes do usuario (Restante da sidebar)
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; 
            border-radius: 10px; text-align: center;'>
                <p style='margin: 0.5rem 0; color: white; font-weight: 600;'>{usuario['nome']}</p>
                <p style='margin: 0; color: white; opacity: 0.8; font-size: 0.9rem;'>
                    ({usuario['tipo'].capitalize()})
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        if st.button("Sair", width="stretch", type="secondary"):
            fazer_logout()
    
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: white; opacity: 0.7; font-size: 0.8rem;'>
                <p style='margin: 0;'>Versão 1.0</p>
                <p style='margin: 0;'>© 2025 CogniKids</p>
            </div>
        """, unsafe_allow_html=True)

def main():
    """
    Função principal do aplicativo com roteamento
    """
    inicializar_sessao()
    aplicar_estilos()
    
    if not verificar_login():
        mostrar_tela_login()
    else:
        # Usuário está logado, mostrar UI principal
        mostrar_sidebar()
        usuario = obter_usuario_logado()
        mostrar_perfil_header()
        
        st.write("")
        st.write("")
        
        pagina = st.session_state['pagina_atual']
        user_type = usuario.get('tipo')

        # --- LÓGICA DE ROTEAMENTO DE PÁGINA ---
        try:
            if user_type == 'aluno' or user_type == 'estudante':
                if pagina == 'dashboard':
                    mostrar_dashboard(usuario)
                elif pagina == 'activities':
                    mostrar_atividades(usuario)
                elif pagina == 'reports':
                    mostrar_relatorios(usuario)
                else:
                    st.session_state['pagina_atual'] = 'dashboard'
                    st.rerun()
            
            elif user_type == 'professor':
                if pagina == 'teacher_dashboard':
                    mostrar_painel_professor(usuario)
                elif pagina == 'manage_students':
                    mostrar_gerenciador_alunos(usuario)
                elif pagina == 'manage_classes':
                    mostrar_gerenciador_turmas(usuario)
                else:
                    st.session_state['pagina_atual'] = 'teacher_dashboard'
                    st.rerun()
                    
            elif user_type == 'pai':
                if pagina == 'parent_dashboard':
                    mostrar_painel_responsavel(usuario)
                else:
                    st.session_state['pagina_atual'] = 'parent_dashboard'
                    st.rerun()
            
            else:
                st.error(f"Tipo de usuário '{user_type}' desconhecido. Fazendo logout.")
                fazer_logout()

        except Exception as e:
            st.error(f"Ocorreu um erro ao carregar a página '{pagina}': {e}")
            st.exception(e)

if __name__ == "__main__":
    main()


