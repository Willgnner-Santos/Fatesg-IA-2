"""
Módulo de login e autenticação do CogniKids
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import api_client
from config import APP_CONFIG

def mostrar_tela_login():
    """
    Mostra a tela de login do sistema
    """
    # Estilo customizado para a página de login
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .login-title {
            text-align: center;
            color: white;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .login-subtitle {
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Centralizando o conteúdo
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo
        logo_relative_path = APP_CONFIG.get("LOGO_PATH", "")
        # Constrói o caminho absoluto baseado no diretório do módulo
        base_dir = Path(__file__).parent.parent  # Volta para cognikids/
        logo_path = base_dir / logo_relative_path
        
        if logo_path.exists():
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image(str(logo_path), width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Fallback caso logo nao seja encontrado
            st.markdown("""
                <div class="login-container">
                    <h1 class="login-title">CogniKids</h1>
                    <p class="login-subtitle">Aprendendo com diversão!</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Formulario de login
        with st.form("login_form"):
            st.markdown("### Entre na sua conta")
            
            email = st.text_input(
                "Email",
                placeholder="Digite seu email",
                help="Ex: ana.sofia@aluno.dev"
            )
            
            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                help="Senha padrão para todos: senha123"
            )
            
            st.write("")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submit = st.form_submit_button(
                    "Entrar",
                    width="stretch",
                    type="primary"
                )
            
            if submit:
                if email and password:
                    # Tenta autenticar via API
                    result = api_client.login(email, password)
                    
                    if result.get('success'):
                        # Salva dados do usuário na sessão
                        # O backend retorna o token e o usuário dentro de 'data'
                        st.session_state['token'] = result['data'].get('token')
                        usuario = result.get('data', {}).get('user', {})

                        if not usuario:  # Fallback se 'user' não estiver em 'data'
                            usuario = result.get('user', {})
                        
                        if not st.session_state.get('token'):  # Fallback se 'token' não estiver em 'data'
                            st.session_state['token'] = result.get('token')

                        tipo_usuario = usuario.get('tipo', usuario.get('role'))
                        
                        # Define avatar e idade com base no tipo
                        if tipo_usuario == 'aluno' or tipo_usuario == 'estudante':
                            avatar = 'A'
                            idade = usuario.get('data_nascimento', {}).get('idade', 8) if isinstance(usuario.get('data_nascimento'), dict) else 8
                        elif tipo_usuario == 'professor':
                            avatar = 'P'
                            idade = None
                        elif tipo_usuario == 'pai':
                            avatar = 'R'
                            idade = None
                        else:
                            avatar = 'U'
                            idade = None

                        st.session_state['usuario_logado'] = {
                            'id': usuario.get('_id', usuario.get('id')),
                            'nome': usuario.get('nome', usuario.get('name')),
                            'email': usuario.get('email'),
                            'tipo': tipo_usuario,
                            'avatar': avatar,
                            'idade': idade # <-- Agora será None para professor
                        }
                        
                        st.session_state['pagina_atual'] = 'dashboard'
                        st.success(f"Bem-vindo(a), {usuario.get('nome', usuario.get('name'))}!")
                        st.rerun()
                    else:
                        error_msg = result.get('error', 'Email ou senha incorretos!')
                        st.error(error_msg)
                else:
                    st.warning("Por favor, preencha todos os campos!")
        
        # Informações de ajuda
        st.write("")
        st.write("")
        
        with st.expander("Ajuda - Contas de teste"):
            st.markdown("""
                **Contas disponíveis para teste (Backend):**
                
                **Professores:**
                - Email: `carlos.antunes@escola.dev`
                - Email: `beatriz.moreira@escola.dev`
                
                **Pais/Responsáveis:**
                - Email: `ricardo.alves@pais.dev`
                - Email: `mariana.costa@pais.dev`
                - Email: `helena.mendes@pais.dev`
                
                **Alunos:**
                - Email: `ana.sofia@aluno.dev`
                - Email: `bruno.costa@aluno.dev`
                - Email: `clara.lima@aluno.dev`
                - Email: `diogo.mendes@aluno.dev`
                
                **Senha padrão para todos:** `senha123`
                
                ---
                
                **Importante:** O backend deve estar rodando em `http://localhost:5001`
            """)

def verificar_login():
    """
    Verifica se o usuário está logado
    
    Returns:
        bool: True se logado, False caso contrário
    """
    return 'usuario_logado' in st.session_state and st.session_state['usuario_logado'] is not None

def obter_usuario_logado():
    """
    Retorna o usuário logado
    
    Returns:
        dict: Dados do usuário logado ou None
    """
    if verificar_login():
        return st.session_state['usuario_logado']
    return None

def fazer_logout():
    """
    Realiza o logout do usuário
    """
    if 'usuario_logado' in st.session_state:
        del st.session_state['usuario_logado']
    if 'pagina_atual' in st.session_state:
        st.session_state['pagina_atual'] = 'login'
    st.rerun()

def mostrar_perfil_header():
    """
    Mostra o cabeçalho com o perfil do usuário logado
    """
    if verificar_login():
        usuario = obter_usuario_logado()
        
        # --- INÍCIO DA ALTERAÇÃO ---
        # Define a linha de informação com base no tipo de usuário
        user_type = usuario.get('tipo')
        info_line = ""
        
        if user_type == 'aluno' or user_type == 'estudante':
            info_line = f"<p style='margin: 0; opacity: 0.9;'>{usuario.get('idade', 'N/A')} anos</p>"
        elif user_type == 'professor':
            info_line = f"<p style='margin: 0; opacity: 0.9;'>{usuario.get('email')}</p>"
        elif user_type == 'pai':
            info_line = "<p style='margin: 0; opacity: 0.9;'>Responsável</p>"
        # --- FIM DA ALTERAÇÃO ---

        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div style='padding: 1rem; background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%); 
                border-radius: 15px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <h2 style='margin: 0;'>Olá, {usuario['nome']}!</h2>
                    {info_line}
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("Sair", width="stretch"):
                fazer_logout()


