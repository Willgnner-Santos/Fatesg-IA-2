"""
Módulo de gerenciamento de turmas (conectado ao Backend)
"""

import streamlit as st
from utils.api_client import api_client
from utils.data_loaders import carregar_turmas_professor, carregar_alunos_professor

def mostrar_gerenciador_turmas(usuario):
    """
    Mostra a interface de gerenciamento de turmas
    
    Args:
        usuario (dict): Dados do usuário logado (professor)
    """
    st.title("Minhas Turmas")
    
    # Token temporário para funções que ainda não foram refatoradas
    token = st.session_state.get('token')

    if 'selected_class_id' not in st.session_state:
        st.session_state['selected_class_id'] = None

    if st.session_state['selected_class_id']:
        mostrar_detalhes_da_turma(st.session_state['selected_class_id'], usuario, token)
    else:
        mostrar_lista_e_form_turmas(usuario, token)


def mostrar_lista_e_form_turmas(usuario, token):
    """Mostra a lista de turmas e o formulário de criação."""
    
    st.write("Aqui você verá a lista de turmas que você gerencia.")
    
    with st.spinner("Carregando turmas..."):
        turmas_professor = carregar_turmas_professor()

    tab1, tab2 = st.tabs(["Minhas Turmas", "Criar Turma"])
    
    with tab1:
        st.subheader("Lista de Turmas")

        if not turmas_professor:
            st.info("Você ainda não criou nenhuma turma.")
        else:
            cols = st.columns(2)
            for i, turma in enumerate(turmas_professor):
                col = cols[i % 2]
                with col:
                    with st.container(border=True):
                        turma_id = str(turma.get('_id'))
                        st.markdown(f"### {turma.get('name')}")
                        st.markdown(f"**Ano:** {turma.get('school_year')} | **Período:** {turma.get('section')}")
                        st.markdown(f"**Alunos:** {turma.get('student_count', 0)}")
                        
                        if st.button("Ver Detalhes", key=f"details_{turma_id}", width="stretch"):
                            st.session_state['selected_class_id'] = turma_id
                            st.rerun()
                        
                        # --- INÍCIO DA ALTERAÇÃO (Editar e Excluir) ---
                        
                        # Botão de Edição
                        with st.expander("Editar Turma"):
                            with st.form(key=f"edit_form_{turma_id}"):
                                st.write("Ajuste os dados da turma:")
                                
                                new_name = st.text_input("Nome da Turma", value=turma.get('name'))
                                new_grade = st.text_input("Série/Ano", value=turma.get('grade'))
                                
                                # Corrige o problema do section "N/A"
                                periodos_validos = ["Manhã", "Tarde", "Noite"]
                                section_atual = turma.get('section', 'Manhã')
                                # Se o valor não está na lista, usa "Manhã" como padrão
                                if section_atual not in periodos_validos:
                                    section_atual = "Manhã"
                                section_index = periodos_validos.index(section_atual)
                                
                                new_section = st.selectbox("Período (Section)", 
                                                           options=periodos_validos, 
                                                           index=section_index)
                                
                                # Converte school_year para int, tratando "N/A"
                                try:
                                    year_value = int(str(turma.get('school_year', 2025)).split('/')[0])
                                except (ValueError, AttributeError):
                                    year_value = 2025
                                    
                                new_year = st.number_input("Ano Letivo", 
                                                           min_value=2024, max_value=2030, 
                                                           value=year_value)
                                
                                if st.form_submit_button("Salvar Alterações"):
                                    payload = {
                                        "name": new_name,
                                        "grade": new_grade,
                                        "section": new_section,
                                        "school_year": new_year
                                    }
                                    with st.spinner("Atualizando turma..."):
                                        result = api_client.update_class(turma_id, payload)
                                    
                                    if result.get("success"):
                                        st.success("Turma atualizada com sucesso!")
                                        carregar_turmas_professor.clear()
                                        st.rerun()
                                    else:
                                        st.error(f"Erro ao atualizar: {result.get('error')}")

                        # Botão de Exclusão
                        with st.expander("Excluir Turma"):
                            st.warning(f"Atenção: Isso irá desativar a turma '{turma.get('name')}' (soft delete).")
                            
                            if st.button("Confirmar Exclusão", key=f"delete_{turma_id}", width="stretch", type="primary"):
                                with st.spinner("Desativando turma..."):
                                    result = api_client.delete_class(turma_id)
                                
                                if result.get("success"):
                                    st.success("Turma desativada com sucesso!")
                                    carregar_turmas_professor.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao excluir: {result.get('error')}")
                        
                        # --- FIM DA ALTERAÇÃO ---

        # ... (O restante da tab1 - Estatísticas - continua igual)
        st.write("")
        st.subheader("Estatísticas Gerais")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Turmas", len(turmas_professor))
        with col2:
            total_alunos = sum([turma.get('student_count', 0) for turma in turmas_professor])
            st.metric("Total de Alunos", total_alunos)
        with col3:
            st.metric("Média Geral", "N/A", help="Cálculo da média geral em desenvolvimento.")
    
    with tab2:
        # ... (O formulário da tab2 - Criar Turma - continua exatamente o mesmo)
        st.subheader("Criar Nova Turma")
        with st.form("form_nova_turma"):
            st.warning("O campo 'Grade' (Série/Ano) é obrigatório pelo backend.", icon="ℹ️")
            nome_turma = st.text_input("Nome da Turma", placeholder="Ex: Turma 303")
            grade = st.text_input("Série/Ano", placeholder="Ex: 3º Ano")
            section = st.selectbox("Período (Section)", ["Manhã", "Tarde", "Noite"])
            ano_letivo = st.number_input("Ano Letivo", min_value=2024, max_value=2030, value=2025)
            
            submitted = st.form_submit_button("Criar Turma", width="stretch")
            if submitted:
                if not nome_turma or not grade or not section or not ano_letivo:
                    st.error("Por favor, preencha todos os campos obrigatórios.")
                else:
                    payload = {"nome": nome_turma, "grade": grade, "section": section, "school_year": ano_letivo}
                    with st.spinner("Criando turma..."):
                        result = api_client.create_class(payload)
                    if result.get("success"):
                        st.success(f"Turma '{nome_turma}' criada com sucesso!")
                        carregar_turmas_professor.clear()
                    else:
                        st.error(f"Erro ao criar turma: {result.get('error')}")

def mostrar_detalhes_da_turma(turma_id, usuario, token):
    """Mostra os detalhes de uma turma específica e seus alunos."""
    
    st.info("Carregando detalhes da turma...")

    if st.button("Voltar para Todas as Turmas"):
        st.session_state['selected_class_id'] = None
        st.rerun()

    result_class = api_client.get_class_details(turma_id)
    master_student_list = carregar_alunos_professor()
    
    if not result_class.get("success"):
        st.error(f"Erro ao carregar detalhes da turma: {result_class.get('error')}")
        return

    # O backend retorna {'status': 'sucesso', 'dados': class_data}
    # E o _handle_response envolve em {"success": True, "data": {...}}
    detalhes_turma = result_class.get("data", {}).get("dados", {})
    
    # Se 'dados' não existir, tenta acessar diretamente 'data'
    if not detalhes_turma:
        detalhes_turma = result_class.get("data", {})

    st.subheader(f"Detalhes da Turma: {detalhes_turma.get('name')}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ano Letivo", detalhes_turma.get("school_year", "N/A"))
    col2.metric("Período", detalhes_turma.get("section", "N/A"))
    col3.metric("Série/Ano", detalhes_turma.get("grade", "N/A"))
    
    st.divider()
    
    st.subheader("Alunos Matriculados")
    
    # Filtra a lista mestre de alunos
    student_ids_na_turma = detalhes_turma.get('students', [])
    if not student_ids_na_turma:
        student_ids_na_turma = detalhes_turma.get('alunos_ids', [])
        
    # Converte todos os IDs para string para comparação
    student_ids_na_turma_str = [str(sid) for sid in student_ids_na_turma]
    
    # Filtra a lista mestre
    alunos_na_turma = [
        aluno for aluno in master_student_list 
        if str(aluno.get("_id")) in student_ids_na_turma_str
    ]

    if not alunos_na_turma:
        st.info("Nenhum aluno matriculado nesta turma ainda.")
    else:
        for aluno in alunos_na_turma:
            col_name, col_btn = st.columns([3, 1])
            with col_name:
                with st.container(border=True):
                    st.markdown(f"**{aluno.get('nome')}**")
                    st.caption(f"Email: {aluno.get('email')}")
            with col_btn:
                if st.button("Remover", key=f"remove_{aluno.get('_id')}"):
                    result_remove = api_client.remove_student_from_class(turma_id, str(aluno.get('_id')))
                    if result_remove.get("success"):
                        st.success(f"{aluno.get('nome')} removido da turma!")
                        carregar_alunos_professor.clear()
                        carregar_turmas_professor.clear()
                        st.rerun()
                    else:
                        st.error(f"Erro ao remover aluno: {result_remove.get('error')}")
    
    st.divider()
    st.subheader("Adicionar Aluno")
    
    # Filtra alunos que NÃO estão na turma
    alunos_disponiveis = [
        aluno for aluno in master_student_list 
        if str(aluno.get("_id")) not in student_ids_na_turma_str
    ]
    
    if not alunos_disponiveis:
        st.info("Todos os seus alunos já estão matriculados nesta turma.")
    else:
        aluno_selecionado = st.selectbox(
            "Selecione o aluno para adicionar",
            options=alunos_disponiveis,
            format_func=lambda x: f"{x.get('nome')} ({x.get('email')})",
            key="add_student_select"
        )
        
        if st.button("Adicionar Aluno", key="add_student_btn"):
            if aluno_selecionado:
                result_enroll = api_client.enroll_student_in_class(turma_id, str(aluno_selecionado.get('_id')))
                if result_enroll.get("success"):
                    st.success(f"{aluno_selecionado.get('nome')} adicionado à turma!")
                    carregar_alunos_professor.clear()
                    carregar_turmas_professor.clear()
                    st.rerun()
                else:
                    st.error(f"Erro ao adicionar aluno: {result_enroll.get('error')}")



