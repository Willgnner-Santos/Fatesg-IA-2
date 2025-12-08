"""
Módulo de gerenciamento de alunos (conectado ao Backend)
"""

import streamlit as st
from utils.api_client import api_client
from utils.management_helpers import show_edit_student_form, confirm_delete_student
from utils.data_loaders import carregar_turmas_professor, carregar_alunos_professor

def mostrar_gerenciador_alunos(usuario):
    """
    Mostra a interface de gerenciamento de alunos
    
    Args:
        usuario (dict): Dados do usuário logado (professor)
    """
    st.title("Gerenciador de Alunos")
    st.write("Aqui você poderá ver, adicionar, editar e remover alunos das suas turmas.")

    # Token temporário para helpers que ainda não foram refatorados
    token = st.session_state.get('token')

    # Carrega as turmas do professor
    turmas_professor = carregar_turmas_professor()

    # Tabs para organizar funcionalidades
    tab1, tab2 = st.tabs(["Lista de Alunos", "Adicionar Aluno"])
    
    with tab1:
        st.subheader("Meus Alunos")
        
        with st.spinner("Buscando lista de alunos no backend..."):
            # --- ALTERAÇÃO AQUI ---
            alunos_list = carregar_alunos_professor() 
            
            if not alunos_list:
                st.info("Você ainda não tem alunos cadastrados nas suas turmas.")
            else:
                # Guarda a lista de alunos na sessão para referência
                st.session_state['lista_alunos_professor'] = alunos_list
                
                # Mapeia ID da turma para Nome da turma para exibição
                mapa_turmas = {str(turma.get("_id")): turma.get("name", "N/A") for turma in turmas_professor}
                
                # Cria um card para cada aluno
                for aluno in alunos_list:
                    aluno_id = str(aluno.get("_id"))
                    
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.markdown(f"**{aluno.get('nome')}**")
                            st.caption(f"Email: {aluno.get('email')}")
                            # Mostra o nome da turma ao invés do ID
                            turma_nome = mapa_turmas.get(str(aluno.get("turma_id")), "Sem turma")
                            st.caption(f"Turma: {turma_nome}")
                        
                        with col2:
                            # O helper 'show_edit_student_form' cria um expander
                            # com um formulário de edição dentro dele.
                            show_edit_student_form(aluno, token)
                            
                        with col3:
                            # O helper 'confirm_delete_student' cria o botão
                            # e o pop-up de confirmação para exclusão.
                            # Passamos 'st.rerun' para que a página recarregue
                            # automaticamente após a exclusão.
                            confirm_delete_student(aluno_id, token, on_success=st.rerun)

    with tab2:
        st.subheader("Adicionar Novo Aluno")
        
        if not turmas_professor:
            st.warning("Você precisa criar uma turma antes de adicionar alunos.")
            if st.button("Ir para 'Minhas Turmas'"):
                st.session_state['pagina_atual'] = 'manage_classes'
                st.rerun()
            return

        # Prepara o selectbox de turmas
        # Formato: "Nome da Turma (ID: ...)"
        opcoes_turma = {f"{turma.get('name')} (ID: {turma.get('_id')})": str(turma.get('_id')) for turma in turmas_professor}

        with st.form("form_novo_aluno", clear_on_submit=True):
            nome = st.text_input("Nome completo do aluno")
            email = st.text_input("Email do aluno")
            # O backend (student_controller) espera uma senha
            senha = st.text_input("Senha inicial do aluno", type="password", help="O aluno poderá trocar depois.")
            
            # Selectbox dinâmico
            turma_selecionada_label = st.selectbox(
                "Selecione a turma",
                options=list(opcoes_turma.keys())
            )
            
            submitted = st.form_submit_button("Adicionar Aluno", width="stretch")
            
            if submitted:
                if not nome or not email or not senha or not turma_selecionada_label:
                    st.error("Por favor, preencha todos os campos.")
                else:
                    # Pega o ID real da turma a partir do label selecionado
                    turma_id_real = opcoes_turma[turma_selecionada_label]
                    
                    with st.spinner("Criando novo aluno..."):
                        result = api_client.create_student(nome, email, senha, turma_id_real)
                    
                    if result.get("success"):
                        st.success(f"Aluno {nome} criado com sucesso!")
                        # Limpa o cache das turmas para forçar a atualização da lista
                        carregar_turmas_professor.clear()
                        st.rerun() # Recarrega para mostrar o novo aluno na lista
                    else:
                        st.error(f"Erro ao criar aluno: {result.get('error')}")


