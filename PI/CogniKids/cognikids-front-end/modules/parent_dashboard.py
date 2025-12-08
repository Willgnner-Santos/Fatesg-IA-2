"""
Módulo do painel do responsável (pais)
"""

import streamlit as st
# from utils.api_client import api_client  # Será usado quando implementado

def mostrar_painel_responsavel(usuario):
    """
    Mostra o painel principal do responsável
    
    Args:
        usuario (dict): Dados do usuário logado (responsável)
    """
    st.title(f"Painel do Responsável: {usuario['nome']}")
    
    # Mensagem de funcionalidade em desenvolvimento
    st.info("""
        ### Funcionalidade em Desenvolvimento
        
        O painel do responsável está sendo desenvolvido e estará disponível em breve.
        
        **Funcionalidades planejadas:**
        - Visualização dos filhos cadastrados
        - Acompanhamento de desempenho acadêmico
        - Monitoramento de sentimentos e bem-estar
        - Comunicação direta com professores
        - Visualização de frequência e presença
        - Alertas de crise e situações críticas
        
        Para mais informações, entre em contato com a administração da escola.
    """)
    
    st.markdown("---")
    
    # Mostra informacoes do responsavel
    with st.expander("Minhas Informações", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Nome:** {usuario.get('nome', 'N/A')}")
            st.write(f"**Email:** {usuario.get('email', 'N/A')}")
        with col2:
            st.write(f"**Tipo:** {usuario.get('tipo', 'N/A')}")
            st.write(f"**Status:** {'Ativo' if usuario.get('ativo', False) else 'Inativo'}")
    
    # Documentacao para desenvolvimento futuro disponivel em docs/


