"""
Funções Streamlit reutilizáveis para:
- mostrar um formulário de edição de aluno
- confirmar e executar a exclusão de um aluno
"""
from typing import Callable
import streamlit as st
from utils.api_client import api_client  # CORRIGIDO: Importa o api_client do frontend

def show_edit_student_form(student: dict, token: str):
    """Exibe um formulário de edição para o aluno fornecido."""
    if token is None or token == '':
        st.error('Token de autenticação ausente.')
        return

    student_id = str(student.get('_id'))
    nome_default = student.get('nome', '')
    email_default = student.get('email', '')
    turma_default = str(student.get('turma_id') or student.get('class_id') or '')

    # Usar expander para não ocupar muito espaço
    with st.expander("Editar"):
        with st.form(key=f'edit_student_{student_id}'):
            nome = st.text_input('Nome', value=nome_default, key=f'nome_{student_id}')
            email = st.text_input('Email', value=email_default, key=f'email_{student_id}')
            turma_id = st.text_input('Turma ID', value=turma_default, help='ID da turma (ObjectId)', key=f'turma_{student_id}')

            submit = st.form_submit_button('Salvar alterações')
            if submit:
                payload = {
                    'nome': nome,
                    'email': email,
                }
                if turma_id:
                    payload['turma_id'] = turma_id

                with st.spinner('Salvando alterações...'):
                    # CORRIGIDO: Chama o api_client do frontend
                    resp = api_client.update_student(student_id, payload)

                if resp.get("success"):
                    st.success('Aluno atualizado com sucesso.')
                    st.rerun() # Adicionado para recarregar a lista
                else:
                    st.error(f"Erro: {resp.get('error', 'Erro desconhecido')}")


def confirm_delete_student(student_id: str, token: str, on_success: Callable[[], None] = None):
    """Mostra botão/expander para confirmar e executar a exclusão de um aluno."""
    if token is None or token == '':
        st.error('Token de autenticação ausente.')
        return

    # Usar session_state para controlar o estado da confirmação
    confirm_key = f'confirm_delete_state_{student_id}'
    
    if confirm_key not in st.session_state:
        st.session_state[confirm_key] = False
    
    if not st.session_state[confirm_key]:
        # Mostrar botão para iniciar confirmação
        if st.button('Deletar', key=f'delete_btn_{student_id}', width="stretch", type="secondary"):
            st.session_state[confirm_key] = True
            st.rerun()
    else:
        # Mostrar confirmação
        st.warning('Confirmar exclusao?')
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button('Sim', key=f'confirm_yes_{student_id}', width="stretch", type="primary"):
                with st.spinner('Removendo aluno...'):
                    resp = api_client.delete_student(student_id)

                if resp.get("success"):
                    st.success('Aluno removido com sucesso.')
                    st.session_state[confirm_key] = False
                    if on_success:
                        try:
                            on_success()
                        except Exception as e:
                            st.error(f'Erro no callback on_success: {e}')
                else:
                    st.error(f"Erro: {resp.get('error', 'Erro desconhecido')}")
                    st.session_state[confirm_key] = False
        
        with col_b:
            if st.button('Cancelar', key=f'confirm_no_{student_id}', width="stretch"):
                st.session_state[confirm_key] = False
                st.rerun()


