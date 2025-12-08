"""
Modulo do painel do professor.

Este modulo implementa a interface do dashboard do professor,
incluindo o sistema de alertas de crise e visualizacao de dados biometricos.

Author: Equipe CogniKids
Version: 2.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.constants import SENTIMENT_COLORS
from utils.data_loaders import (
    carregar_turmas_professor, 
    carregar_sentimentos_alunos,
    carregar_alertas_crise,
    carregar_media_notas
)
from utils.api_client import APIClient


def mostrar_grafico_historico_alertas(student_id: str, student_name: str):
    """
    Exibe o grafico temporal de historico de alertas de um aluno.
    
    Busca os alertas dos ultimos 30 dias e renderiza um grafico
    interativo com informacoes detalhadas no hover.
    
    Args:
        student_id: Identificador unico do aluno.
        student_name: Nome do aluno para exibicao.
    """
    api = APIClient()
    
    with st.spinner(f"Carregando histórico de {student_name}..."):
        response = api.get_student_alert_history(student_id)
    
    if not response.get("success"):
        st.error(f"Erro ao carregar histórico: {response.get('error', 'Erro desconhecido')}")
        return
    
    # Os dados vêm aninhados em response.data.alerts
    data = response.get("data", {})
    alerts = data.get("alerts", [])
    
    if not alerts:
        st.info(f"Nenhum alerta registrado para {student_name} nos últimos 30 dias.")
        return
    
# Prepara dados para o grafico
    dates = []
    bpms = []
    gsrs = []
    movements = []
    severities = []
    resolvidos = []
    colors = []
    
    # Mapeamento de severidade para português
    SEVERIDADE_PT = {
        'high': 'Alta',
        'medium': 'Média', 
        'low': 'Baixa'
    }
    
    for alert in alerts:
        # Parse da data
        data_hora = alert.get('data_hora')
        if isinstance(data_hora, str):
            try:
                dt = datetime.fromisoformat(data_hora.replace('Z', '+00:00'))
            except:
                dt = datetime.now()
        else:
            dt = data_hora if data_hora else datetime.now()
        
        dates.append(dt)
        bpms.append(alert.get('bpm', 0))
        gsrs.append(alert.get('gsr', 0))
        movements.append(alert.get('movement_score', 0))
        severity = alert.get('severity', 'medium')
        severities.append(SEVERIDADE_PT.get(severity, severity))
        resolvidos.append("Sim" if alert.get('resolvido', False) else "Não")
        
        # Cor baseada na severidade
        if severity == 'high':
            colors.append('#ff4b4b')  # Vermelho
        elif severity == 'medium':
            colors.append('#ffa500')  # Laranja
        else:
            colors.append('#ffcc00')  # Amarelo
    
# Cria texto do hover com todas as informacoes
    hover_texts = []
    for i in range(len(dates)):
        hover_text = (
            f"<b>{dates[i].strftime('%d/%m/%Y %H:%M')}</b><br>"
            f"<b>BPM:</b> {bpms[i]:.1f}<br>"
            f"<b>GSR:</b> {gsrs[i]:.2f}<br>"
            f"<b>Movimento:</b> {movements[i]:.2f}<br>"
            f"<b>Severidade:</b> {severities[i]}<br>"
            f"<b>Resolvido:</b> {resolvidos[i]}"
        )
        hover_texts.append(hover_text)
    
    # Cria o gráfico Plotly
    fig = go.Figure()
    
    # Linha de BPM
    fig.add_trace(go.Scatter(
        x=dates,
        y=bpms,
        mode='lines+markers',
        name='BPM',
        line=dict(color='#ff6b6b', width=2),
        marker=dict(
            size=12,
            color=colors,
            line=dict(color='white', width=2),
            symbol='circle'
        ),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_texts
    ))
    
    # Linha de referência para BPM crítico
    fig.add_hline(
        y=130, 
        line_dash="dash", 
        line_color="orange",
        annotation_text="Limite de Alerta (130 BPM)",
        annotation_position="top right"
    )
    
    fig.add_hline(
        y=150, 
        line_dash="dash", 
        line_color="red",
        annotation_text="Zona Crítica (150 BPM)",
        annotation_position="bottom right"
    )
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f"Histórico de Alertas de Crise - {student_name}",
            font=dict(size=18)
        ),
        xaxis=dict(
            title="Data/Hora",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title="Batimento Cardíaco (BPM)",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            range=[min(bpms) - 20 if bpms else 60, max(bpms) + 20 if bpms else 200]
        ),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Renderiza o gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    # Estatísticas resumidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Alertas", len(alerts))
    with col2:
        high_count = sum(1 for s in severities if 'Alta' in s)
        st.metric("Severidade Alta", high_count)
    with col3:
        avg_bpm = sum(bpms) / len(bpms) if bpms else 0
        st.metric("BPM Médio", f"{avg_bpm:.1f}")
    with col4:
        resolved_count = sum(1 for r in resolvidos if r == "Sim")
        st.metric("Resolvidos", f"{resolved_count}/{len(alerts)}")

def mostrar_painel_professor(usuario):
    """
    Renderiza o painel principal do professor.
    
    Exibe o sistema de alertas de crise, estatisticas gerais,
    graficos de sentimentos e informacoes das turmas.
    
    Args:
        usuario: Dicionario com dados do usuario autenticado.
    """
    st.title(f"Painel do Professor: {usuario['nome']}")

    # Secao de Alertas de Crise
    
    st.subheader("Sistema de Alerta de Crise")
    
    # Controles de atualizacao
    col_refresh, col_info = st.columns([1, 4])
    with col_refresh:
        if st.button("Atualizar", width="stretch", type="primary"):
            st.cache_data.clear()
            st.rerun()
    with col_info:
        st.caption("O sistema monitora dados biometricos dos ultimos 5 minutos. Crise: BPM > 130 ou GSR > 1.5")
    
    alert_placeholder = st.empty()

    try:
        # Carrega alertas de crise
        alunos_em_crise = carregar_alertas_crise()
        
        if alunos_em_crise:
            # Exibe alertas individuais para cada aluno
            with alert_placeholder.container():
                # Cabecalho do alerta
                st.markdown("""
                    <div style='background-color: #ff4b4b; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                        <h3 style='color: white; margin: 0;'>ALERTA DE CRISE DETECTADO</h3>
                        <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>
                            {0} aluno(s) com sinais biometricos criticos
                        </p>
                    </div>
                """.format(len(alunos_em_crise)), unsafe_allow_html=True)
                
                # Cards individuais para cada aluno
                for aluno in alunos_em_crise:
                    nome = aluno.get('nome', 'Aluno Desconhecido')
                    hr = aluno.get('heart_rate', 0)
                    gsr = aluno.get('gsr', 0)
                    timestamp = aluno.get('timestamp', '')
                    
                    # Determina o nivel de crise
                    nivel_hr = "CRITICO" if hr > 150 else "ELEVADO" if hr > 130 else "NORMAL"
                    nivel_gsr = "CRITICO" if gsr > 2.0 else "ELEVADO" if gsr > 1.5 else "NORMAL"
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {nome}")
                        if timestamp:
                            from datetime import datetime
                            try:
                                if isinstance(timestamp, str):
                                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                else:
                                    dt = timestamp
                                tempo_decorrido = datetime.now(dt.tzinfo) - dt
                                minutos = int(tempo_decorrido.total_seconds() / 60)
                                st.caption(f"Detectado ha {minutos} minuto(s)")
                            except:
                                pass
                    
                    with col2:
                        st.metric(
                            label="Batimento Cardiaco",
                            value=f"{hr:.1f} BPM",
                            delta=f"{hr - 130:.1f}" if hr > 130 else None,
                            delta_color="inverse"
                        )
                        st.caption(nivel_hr)
                    
                    with col3:
                        st.metric(
                            label="Nivel de Stress (GSR)",
                            value=f"{gsr:.2f}",
                            delta=f"{gsr - 1.5:.2f}" if gsr > 1.5 else None,
                            delta_color="inverse"
                        )
                        st.caption(nivel_gsr)
                    
                    # Acoes disponiveis
                    col_action1, col_action2, col_action3 = st.columns(3)
                    with col_action1:
                        if st.button(f"Contatar Responsavel", key=f"contact_{aluno.get('aluno_id')}", width="stretch"):
                            st.info("Funcionalidade em desenvolvimento")
                    with col_action2:
                        # Controle de exibicao do historico
                        history_key = f"show_history_{aluno.get('aluno_id')}"
                        if history_key not in st.session_state:
                            st.session_state[history_key] = False
                        
                        if st.button(f"Ver Historico", key=f"history_{aluno.get('aluno_id')}", width="stretch"):
                            st.session_state[history_key] = not st.session_state[history_key]
                            st.rerun()
                    with col_action3:
                        if st.button(f"Marcar Resolvido", key=f"resolve_{aluno.get('aluno_id')}", width="stretch"):
                            st.success("Alerta marcado como resolvido")
                    
                    # Exibe grafico de historico se solicitado
                    if st.session_state.get(f"show_history_{aluno.get('aluno_id')}", False):
                        with st.container():
                            st.markdown("---")
                            mostrar_grafico_historico_alertas(
                                student_id=aluno.get('aluno_id'),
                                student_name=nome
                            )
                            if st.button("Fechar Historico", key=f"close_history_{aluno.get('aluno_id')}"):
                                st.session_state[f"show_history_{aluno.get('aluno_id')}"] = False
                                st.rerun()
                    
                    st.divider()
        else:
            # Estado normal - sem alertas
            with alert_placeholder.container():
                st.markdown("""
                    <div style='background-color: #00cc44; padding: 20px; border-radius: 10px; text-align: center;'>
                        <h3 style='color: white; margin: 0;'>Tudo Calmo</h3>
                        <p style='color: white; margin: 10px 0 0 0;'>
                            Nenhum alerta de crise detectado. Todos os alunos estao com sinais biometricos normais.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        with alert_placeholder.container():
            st.error(f"Erro de conexao com o sistema de alertas: {e}")
            with st.expander("Detalhes do erro"):
                st.code(str(e))
    
    st.divider()

    # Carregamento de dados do painel
    with st.spinner("Carregando dados do painel..."):
        turmas_professor = carregar_turmas_professor()
        df_sentimentos = carregar_sentimentos_alunos()

    total_turmas = len(turmas_professor)
    total_alunos = sum([turma.get('student_count', 0) for turma in turmas_professor])
    
    alertas_sentimento = 0
    if not df_sentimentos.empty:
        sentimentos_alerta = ['triste', 'ansioso', 'cansado', 'com raiva']
        alertas_df = df_sentimentos[df_sentimentos['sentimento'].str.lower().isin(sentimentos_alerta)]
        alertas_sentimento = alertas_df['aluno_id'].nunique()

    st.subheader("Atalhos Rapidos")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Gerenciar Alunos", width="stretch"):
            st.session_state['pagina_atual'] = 'manage_students'
            st.rerun()
    with col2:
        if st.button("Minhas Turmas", width="stretch"):
            st.session_state['pagina_atual'] = 'manage_classes'
            st.rerun()
    with col3:
        st.button("Mensagens", width="stretch", disabled=True, help="Em desenvolvimento")
    
    st.write("")
    st.write("")
    
    st.subheader("Visao Geral")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Alunos", total_alunos)
    with col2:
        st.metric("Turmas Ativas", total_turmas)
    with col3:
        st.metric("Alunos com Alerta", f"{alertas_sentimento}", 
                   help="Numero de alunos que reportaram sentimentos de alerta recentemente.")
    with col4:
        media_notas = carregar_media_notas()
        if media_notas is not None:
            st.metric("Media de Notas", f"{media_notas:.1f}")
        else:
            st.metric("Media de Notas", "N/A", help="Sem notas registradas")
    
    st.write("")
    st.write("")
    
    st.subheader("Alunos por Turma")
    
    if not turmas_professor:
        st.info("Nenhuma turma encontrada para exibir estatisticas.")
    else:
        try:
            # Usa Plotly para garantir renderizacao correta
            import plotly.express as px
            
            dados_grafico = {
                "Turma": [turma.get("name", "Sem Nome") for turma in turmas_professor],
                "Quantidade": [turma.get("student_count", 0) for turma in turmas_professor]
            }
            df_grafico = pd.DataFrame(dados_grafico)
            
            fig = px.bar(
                df_grafico, 
                x="Turma", 
                y="Quantidade",
                color_discrete_sequence=["#8B5CF6"],
                text="Quantidade"
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Num. de Alunos",
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar grafico: {e}")

    st.subheader("Sentimentos Recentes da Turma")
    
    # Seletor de turma para filtrar sentimentos
    opcoes_turmas = {"todas": "Todas as Turmas"}
    for turma in turmas_professor:
        turma_id = turma.get('_id', '')
        turma_nome = turma.get('name', 'Sem Nome')
        opcoes_turmas[turma_id] = turma_nome
    
    col_select, col_info = st.columns([2, 3])
    with col_select:
        turma_selecionada = st.selectbox(
            "Filtrar por turma:",
            options=list(opcoes_turmas.keys()),
            format_func=lambda x: opcoes_turmas[x],
            key="filtro_turma_sentimentos"
        )
    with col_info:
        if turma_selecionada != "todas":
            st.caption("Mostrando sentimentos apenas da turma selecionada")
        else:
            st.caption("Mostrando sentimentos de todas as turmas")
    
    # Recarrega sentimentos filtrados por turma
    df_sentimentos_filtrado = carregar_sentimentos_alunos(turma_selecionada)
    
    # Grafico de Sentimentos com Plotly
    if df_sentimentos_filtrado.empty:
        st.info("Nenhum sentimento reportado pelos alunos desta turma ainda.")
    else:
        try:
            contagem_sentimentos = df_sentimentos_filtrado['sentimento'].value_counts()
            
            # Mapeia as cores para cada sentimento
            cores_barras = [SENTIMENT_COLORS.get(sentimento.lower(), '#CCCCCC') 
                           for sentimento in contagem_sentimentos.index]
            
            # Cria o grafico Plotly
            fig = go.Figure(data=[
                go.Bar(
                    x=contagem_sentimentos.index,
                    y=contagem_sentimentos.values,
                    marker=dict(
                        color=cores_barras,
                        line=dict(color='rgba(0,0,0,0.3)', width=1)
                    ),
                    text=contagem_sentimentos.values,
                    textposition='auto',
                )
            ])
            
            # Configuracoes do layout
            fig.update_layout(
                xaxis_title="Sentimento",
                yaxis_title="Quantidade",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=400,
                margin=dict(l=40, r=40, t=40, b=40),
                xaxis=dict(
                    showgrid=False,
                    tickangle=-45
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)'
                )
            )
            
            # Renderiza o grafico
            st.plotly_chart(fig, width="stretch")
            
        except Exception as e:
            st.error(f"Erro ao gerar grafico de sentimentos: {e}")
            
    with st.expander("Informacoes Tecnicas"):
        st.code("""
# Endpoints utilizados neste painel:
# 1. GET /api/teachers/crisis_alerts - Alertas de crise em tempo real
# 2. GET /api/classes - Lista de turmas do professor
# 3. GET /api/teachers/{id}/students - Alunos do professor
# 4. GET /api/teachers/students/{id}/feelings - Sentimentos dos alunos
        """, language="python")


