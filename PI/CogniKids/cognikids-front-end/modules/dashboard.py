"""
Módulo do painel de desempenho (Dashboard) do CogniKids
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import sys
import os

# Configuração do matplotlib para usar fonte Unicode
matplotlib.rc('font', family='DejaVu Sans')

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import carregar_progresso, obter_cor_desempenho, obter_emoji_desempenho, calcular_percentual_acertos
from modules.stats import (
    calcular_desempenho, 
    calcular_percentual_evolucao,
    identificar_areas_fortes_fracas,
    calcular_consistencia
)

def mostrar_dashboard(usuario):
    """
    Mostra o painel de desempenho do aluno
    
    Args:
        usuario (dict): Dados do usuário logado
    """
    st.markdown("## Meu Desempenho")
    st.write("")
    
    # Carrega dados do usuario
    df_progresso = carregar_progresso(usuario['id'])
    
    if df_progresso.empty:
        st.warning("Voce ainda nao realizou nenhuma atividade. Comece agora!")
        return
    
    # Calcula métricas gerais
    metricas_gerais = calcular_desempenho(df_progresso)
    evolucao = calcular_percentual_evolucao(df_progresso)
    areas = identificar_areas_fortes_fracas(df_progresso)
    consistencia = calcular_consistencia(df_progresso)
    
    # Cards com métricas principais
    mostrar_cards_metricas(metricas_gerais, evolucao, consistencia)
    
    st.write("")
    st.write("")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        mostrar_grafico_desempenho_tema(df_progresso)
    
    with col2:
        mostrar_grafico_evolucao_temporal(df_progresso)
    
    st.write("")
    
    # Áreas fortes e fracas
    mostrar_areas_fortes_fracas(areas, df_progresso)
    
    st.write("")
    
    # Últimas atividades
    mostrar_ultimas_atividades(df_progresso)

def mostrar_cards_metricas(metricas, evolucao, consistencia):
    """
    Mostra cards com as principais métricas
    
    Args:
        metricas (dict): Métricas gerais
        evolucao (dict): Percentuais de evolução
        consistencia (dict): Métricas de consistência
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        taxa_acertos = metricas['Taxa de acertos (%)']
        cor = obter_cor_desempenho(taxa_acertos)
        emoji = obter_emoji_desempenho(taxa_acertos)
        
        st.markdown(f"""
            <div style='padding: 1.5rem; background: {cor}; border-radius: 15px; 
            color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; font-size: 2.5rem;'>{emoji}</h3>
                <h2 style='margin: 0.5rem 0;'>{taxa_acertos}%</h2>
                <p style='margin: 0; opacity: 0.9;'>Taxa de Acertos</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total = metricas['Total de atividades']
        st.markdown(f"""
            <div style='padding: 1.5rem; background: #3B82F6; border-radius: 15px; 
            color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; font-size: 2.5rem;'></h3>
                <h2 style='margin: 0.5rem 0;'>{total}</h2>
                <p style='margin: 0; opacity: 0.9;'>Atividades</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tempo = metricas['Tempo médio (s)']
        st.markdown(f"""
            <div style='padding: 1.5rem; background: #FACC15; border-radius: 15px; 
            color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; font-size: 2.5rem;'></h3>
                <h2 style='margin: 0.5rem 0;'>{tempo}s</h2>
                <p style='margin: 0; opacity: 0.9;'>Tempo Médio</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        nivel = consistencia['nivel']
        cor_consistencia = "#10B981" if "Muito" in nivel or nivel == "Consistente" else "#F59E0B"
        st.markdown(f"""
            <div style='padding: 1.5rem; background: {cor_consistencia}; border-radius: 15px; 
            color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; font-size: 2.5rem;'></h3>
                <h2 style='margin: 0.5rem 0; font-size: 1.2rem;'>{nivel}</h2>
                <p style='margin: 0; opacity: 0.9;'>Consistência</p>
            </div>
        """, unsafe_allow_html=True)

def mostrar_grafico_desempenho_tema(df):
    """
    Mostra gráfico de desempenho por tema
    
    Args:
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Desempenho por Tema")
    
    # Calcula desempenho por tema
    desempenho_tema = df.groupby('tema').agg({
        'acertos': 'sum',
        'total_questoes': 'sum'
    })
    
    desempenho_tema['percentual'] = (desempenho_tema['acertos'] / desempenho_tema['total_questoes'] * 100).round(1)
    desempenho_tema = desempenho_tema.sort_values('percentual', ascending=True)
    
    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(8, 5))
    
    cores = [obter_cor_desempenho(p) for p in desempenho_tema['percentual']]
    
    bars = ax.barh(desempenho_tema.index, desempenho_tema['percentual'], color=cores)
    
    # Adiciona valores nas barras
    for i, (bar, valor) in enumerate(zip(bars, desempenho_tema['percentual'])):
        ax.text(valor + 2, i, f'{valor}%', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Percentual de Acertos (%)', fontsize=11, fontweight='bold')
    ax.set_xlim(0, 110)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_facecolor('#F9FAFB')
    fig.patch.set_facecolor('#F9FAFB')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def mostrar_grafico_evolucao_temporal(df):
    """
    Mostra gráfico de evolução temporal
    
    Args:
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Evolução do Desempenho")
    
    # Agrupa por data
    evolucao = df.groupby('data').agg({
        'acertos': 'mean',
        'total_questoes': 'mean'
    })
    
    evolucao['percentual'] = (evolucao['acertos'] / evolucao['total_questoes'] * 100).round(1)
    
    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(evolucao.index, evolucao['percentual'], 
            marker='o', linewidth=3, markersize=8, 
            color='#8B5CF6', markerfacecolor='#EC4899')
    
    ax.fill_between(evolucao.index, evolucao['percentual'], alpha=0.3, color='#8B5CF6')
    
    ax.set_ylabel('Percentual de Acertos (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Data', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#F9FAFB')
    fig.patch.set_facecolor('#F9FAFB')
    
    # Formata datas no eixo x
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def mostrar_areas_fortes_fracas(areas, df):
    """
    Mostra áreas fortes e fracas do aluno
    
    Args:
        areas (dict): Áreas fortes e fracas
        df (DataFrame): Dados de progresso
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Áreas Fortes")
        if areas['fortes']:
            for tema in areas['fortes']:
                desempenho = df[df['tema'] == tema]['acertos'].mean()
                total = df[df['tema'] == tema]['total_questoes'].mean()
                percentual = calcular_percentual_acertos(desempenho, total)
                
                st.markdown(f"""
                    <div style='padding: 1rem; background: #10B981; border-radius: 10px; 
                    color: white; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <strong>{tema}</strong><br>
                        <span style='font-size: 1.2rem;'>{percentual:.1f}% de acertos</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Continue praticando para identificar suas áreas fortes!")
    
    with col2:
        st.markdown("### Áreas para Melhorar")
        if areas['fracas']:
            for tema in areas['fracas']:
                desempenho = df[df['tema'] == tema]['acertos'].mean()
                total = df[df['tema'] == tema]['total_questoes'].mean()
                percentual = calcular_percentual_acertos(desempenho, total)
                
                st.markdown(f"""
                    <div style='padding: 1rem; background: #F59E0B; border-radius: 10px; 
                    color: white; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <strong>{tema}</strong><br>
                        <span style='font-size: 1.2rem;'>{percentual:.1f}% de acertos</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Parabéns! Você está indo bem em todas as áreas!")

def mostrar_ultimas_atividades(df):
    """
    Mostra as últimas atividades realizadas
    
    Args:
        df (DataFrame): Dados de progresso
    """
    st.markdown("### Últimas Atividades")
    
    # Pega as últimas 5 atividades
    ultimas = df.sort_values('data', ascending=False).head(5)
    
    for _, row in ultimas.iterrows():
        percentual = calcular_percentual_acertos(row['acertos'], row['total_questoes'])
        cor = obter_cor_desempenho(percentual)
        emoji = obter_emoji_desempenho(percentual)
        data_formatada = row['data'].strftime('%d/%m/%Y')
        
        st.markdown(f"""
            <div style='padding: 1rem; background: white; border-left: 5px solid {cor}; 
            border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='font-size: 1.1rem;'>{emoji} {row['tema']}</strong><br>
                        <span style='color: #6B7280;'>{data_formatada}</span>
                    </div>
                    <div style='text-align: right;'>
                        <strong style='font-size: 1.3rem; color: {cor};'>{percentual:.0f}%</strong><br>
                        <span style='color: #6B7280;'>{row['acertos']}/{row['total_questoes']} acertos</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


