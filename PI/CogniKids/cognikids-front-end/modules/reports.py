"""
Módulo de relatórios e recomendações do CogniKids
"""

import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import carregar_progresso, obter_cor_desempenho
from modules.stats import gerar_resumo_estatistico

def mostrar_relatorios(usuario):
    """
    Mostra relatórios e recomendações personalizadas
    
    Args:
        usuario (dict): Dados do usuário logado
    """
    st.markdown("## Relatórios e Recomendações")
    st.write("")
    
    # Carrega dados do usuário
    df_progresso = carregar_progresso(usuario['id'])
    
    if df_progresso.empty:
        st.warning("Você ainda não realizou nenhuma atividade. Comece agora para ver seus relatórios!")
        return
    
    # Gera resumo estatístico
    resumo = gerar_resumo_estatistico(df_progresso)
    
    # Seção de resumo geral
    mostrar_resumo_geral(resumo)
    
    st.write("")
    st.divider()
    st.write("")
    
    # Análise detalhada por tema
    mostrar_analise_temas(df_progresso)
    
    st.write("")
    st.divider()
    st.write("")
    
    # Recomendações personalizadas
    mostrar_recomendacoes(resumo, df_progresso)
    
    st.write("")
    st.divider()
    st.write("")
    
    # Gráfico de radar (habilidades)
    mostrar_grafico_radar(df_progresso)

def mostrar_resumo_geral(resumo):
    """
    Mostra resumo geral do desempenho
    
    Args:
        resumo (dict): Resumo estatístico
    """
    st.markdown("### Resumo Geral")
    st.write("")
    
    desempenho = resumo['desempenho_geral']
    evolucao = resumo['evolucao']
    consistencia = resumo['consistencia']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #8B5CF6, #EC4899); 
            border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; opacity: 0.9;'>Total de Atividades</h4>
                <h1 style='margin: 0.5rem 0;'>""" + str(desempenho['Total de atividades']) + """</h1>
                <p style='margin: 0; opacity: 0.8;'>Completas</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        taxa = desempenho['Taxa de acertos (%)']
        cor = obter_cor_desempenho(taxa)
        st.markdown(f"""
            <div style='padding: 1.5rem; background: {cor}; 
            border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; opacity: 0.9;'>Taxa de Acertos</h4>
                <h1 style='margin: 0.5rem 0;'>{taxa}%</h1>
                <p style='margin: 0; opacity: 0.8;'>Desempenho</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='padding: 1.5rem; background: #3B82F6; 
            border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0; opacity: 0.9;'>Consistência</h4>
                <h1 style='margin: 0.5rem 0; font-size: 1.5rem;'>{consistencia['nivel']}</h1>
                <p style='margin: 0; opacity: 0.8;'>Estabilidade</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Mostra evolução
    st.markdown("#### Evolução do Desempenho")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        evol_acertos = evolucao['acertos']
        cor_evol = "#10B981" if evol_acertos >= 0 else "#EF4444"
        sinal = "+" if evol_acertos >= 0 else ""
        st.markdown(f"""
            <div style='padding: 1rem; background: white; border-left: 4px solid {cor_evol}; 
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='margin: 0; color: #6B7280; font-size: 0.9rem;'>Acertos</p>
                <h3 style='margin: 0.25rem 0; color: {cor_evol};'>{sinal}{evol_acertos}%</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        evol_pontuacao = evolucao['pontuacao']
        cor_evol = "#10B981" if evol_pontuacao >= 0 else "#EF4444"
        sinal = "+" if evol_pontuacao >= 0 else ""
        st.markdown(f"""
            <div style='padding: 1rem; background: white; border-left: 4px solid {cor_evol}; 
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='margin: 0; color: #6B7280; font-size: 0.9rem;'>Pontuação</p>
                <h3 style='margin: 0.25rem 0; color: {cor_evol};'>{sinal}{evol_pontuacao}%</h3>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        evol_tempo = evolucao['tempo']
        cor_evol = "#10B981" if evol_tempo >= 0 else "#EF4444"
        sinal = "+" if evol_tempo >= 0 else ""
        mensagem = "Mais rápido" if evol_tempo >= 0 else "Mais lento"
        st.markdown(f"""
            <div style='padding: 1rem; background: white; border-left: 4px solid {cor_evol}; 
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='margin: 0; color: #6B7280; font-size: 0.9rem;'>Velocidade</p>
                <h3 style='margin: 0.25rem 0; color: {cor_evol};'>{sinal}{evol_tempo}%</h3>
                <p style='margin: 0; color: #6B7280; font-size: 0.8rem;'>{mensagem}</p>
            </div>
        """, unsafe_allow_html=True)

def mostrar_analise_temas(df):
    """
    Mostra análise detalhada por tema
    
    Args:
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Análise por Tema")
    st.write("")
    
    # Calcula desempenho por tema
    desempenho_tema = df.groupby('tema').agg({
        'acertos': ['sum', 'mean'],
        'total_questoes': 'sum',
        'tempo_resposta': 'mean',
        'pontuacao': 'mean'
    }).round(2)
    
    desempenho_tema['taxa_acertos'] = (
        (desempenho_tema[('acertos', 'sum')] / desempenho_tema[('total_questoes', 'sum')]) * 100
    ).round(1)
    
    # Ordena por taxa de acertos
    desempenho_tema = desempenho_tema.sort_values('taxa_acertos', ascending=False)
    
    # Mostra cards para cada tema
    for tema in desempenho_tema.index:
        taxa = desempenho_tema.loc[tema, 'taxa_acertos']
        cor = obter_cor_desempenho(taxa)
        media_tempo = desempenho_tema.loc[tema, ('tempo_resposta', 'mean')]
        pontuacao = desempenho_tema.loc[tema, ('pontuacao', 'mean')]
        total_acertos = int(desempenho_tema.loc[tema, ('acertos', 'sum')])
        total_questoes = int(desempenho_tema.loc[tema, ('total_questoes', 'sum')])
        
        st.markdown(f"""
            <div style='padding: 1.5rem; background: white; border-left: 6px solid {cor}; 
            border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h3 style='margin: 0; color: #1F2937;'>{tema}</h3>
                        <p style='margin: 0.5rem 0 0 0; color: #6B7280;'>
                            {total_acertos} de {total_questoes} questões corretas
                        </p>
                    </div>
                    <div style='text-align: right;'>
                        <h2 style='margin: 0; color: {cor};'>{taxa}%</h2>
                        <p style='margin: 0.25rem 0 0 0; color: #6B7280; font-size: 0.9rem;'>
                            {media_tempo:.1f}s | {pontuacao:.0f} pts
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def mostrar_recomendacoes(resumo, df):
    """
    Mostra recomendações personalizadas
    
    Args:
        resumo (dict): Resumo estatístico
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Recomendações Personalizadas")
    st.write("")
    
    areas = resumo['areas']
    desempenho = resumo['desempenho_geral']
    consistencia = resumo['consistencia']
    
    recomendacoes = []
    
    # Recomendacoes baseadas em areas fracas
    if areas['fracas']:
        for tema in areas['fracas'][:2]:
            recomendacoes.append({
                "tipo": "area_fraca",
                "titulo": f"Reforce seus estudos em {tema}",
                "descricao": f"Voce pode melhorar em {tema}. Pratique mais atividades desse tema para fortalecer suas habilidades!",
                "icone": "",
                "cor": "#F59E0B"
            })
    
    # Recomendacoes baseadas na consistencia
    if consistencia['nivel'] in ['Inconsistente', 'Moderado']:
        recomendacoes.append({
            "tipo": "consistencia",
            "titulo": "Mantenha uma rotina de estudos",
            "descricao": "Tente praticar um pouco todos os dias para melhorar sua consistência e fixar melhor o aprendizado!",
            "icone": "",
            "cor": "#3B82F6"
        })
    
    # Recomendacoes baseadas no tempo
    tempo_medio = desempenho['Tempo médio (s)']
    if tempo_medio > 50:
        recomendacoes.append({
            "tipo": "tempo",
            "titulo": "Pratique para ganhar mais agilidade",
            "descricao": "Você está indo bem, mas pode tentar resolver as questões um pouco mais rápido. A prática ajuda!",
            "icone": "",
            "cor": "#FACC15"
        })
    
    # Recomendacoes positivas
    if areas['fortes']:
        tema_forte = areas['fortes'][0]
        recomendacoes.append({
            "tipo": "area_forte",
            "titulo": f"Você é ótimo em {tema_forte}!",
            "descricao": f"Continue assim! Suas habilidades em {tema_forte} estão excelentes. Você pode ajudar seus colegas!",
            "icone": "",
            "cor": "#10B981"
        })
    
    # Mostra as recomendacoes
    for rec in recomendacoes:
        st.markdown(f"""
            <div style='padding: 1.5rem; background: white; border-left: 6px solid {rec['cor']}; 
            border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; color: #1F2937;'>
                    {rec['titulo']}
                </h3>
                <p style='margin: 0.75rem 0 0 0; color: #6B7280; line-height: 1.6;'>
                    {rec['descricao']}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    if not recomendacoes:
        st.success("Parabéns! Você está indo muito bem em todas as áreas. Continue assim!")

def mostrar_grafico_radar(df):
    """
    Mostra gráfico de radar com habilidades por tema
    
    Args:
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Mapa de Habilidades")
    st.write("")
    
    # Calcula percentual por tema
    desempenho = df.groupby('tema').agg({
        'acertos': 'sum',
        'total_questoes': 'sum'
    })
    
    desempenho['percentual'] = (desempenho['acertos'] / desempenho['total_questoes'] * 100).round(1)
    desempenho = desempenho.sort_index()
    
    # Cria gráfico de barras horizontal colorido
    fig, ax = plt.subplots(figsize=(10, 6))
    
    temas = desempenho.index
    percentuais = desempenho['percentual']
    
    cores = [obter_cor_desempenho(p) for p in percentuais]
    
    bars = ax.barh(range(len(temas)), percentuais, color=cores, height=0.6)
    
    # Adiciona labels e valores
    ax.set_yticks(range(len(temas)))
    ax.set_yticklabels(temas, fontsize=11, fontweight='bold')
    ax.set_xlabel('Percentual de Acertos (%)', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 105)
    
    # Adiciona valores nas barras
    for i, (bar, valor) in enumerate(zip(bars, percentuais)):
        ax.text(valor + 2, i, f'{valor}%', va='center', fontweight='bold', fontsize=11, color='#1F2937')
    
    # Estilização
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
    ax.set_facecolor('#F9FAFB')
    fig.patch.set_facecolor('#F9FAFB')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Legenda explicativa
    st.info("""
        **Como interpretar:**
        - Verde: Excelente (90-100%)
        - Amarelo: Bom (70-89%)
        - Laranja: Regular (50-69%)
        - Vermelho: Precisa melhorar (0-49%)
    """)


