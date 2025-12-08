"""
Módulo de estatísticas e análises do CogniKids
"""

import pandas as pd
from datetime import datetime, timedelta

def calcular_desempenho(df):
    """
    Calcula métricas de desempenho geral
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        dict: Dicionário com métricas calculadas
    """
    if df.empty:
        return {
            "Média de acertos": 0,
            "Tempo médio (s)": 0,
            "Variação de desempenho": 0,
            "Total de atividades": 0,
            "Taxa de acertos (%)": 0
        }
    
    acertos_medio = df['acertos'].mean()
    tempo_medio = df['tempo_resposta'].mean()
    desvio = df['acertos'].std()
    total_atividades = len(df)
    
    # Calcula taxa de acertos percentual
    taxa_acertos = (df['acertos'].sum() / df['total_questoes'].sum()) * 100 if df['total_questoes'].sum() > 0 else 0
    
    return {
        "Média de acertos": round(acertos_medio, 2),
        "Tempo médio (s)": round(tempo_medio, 1),
        "Variação de desempenho": round(desvio, 2),
        "Total de atividades": total_atividades,
        "Taxa de acertos (%)": round(taxa_acertos, 1)
    }

def calcular_desempenho_por_tema(df):
    """
    Calcula desempenho agrupado por tema
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        DataFrame: Desempenho por tema
    """
    if df.empty:
        return pd.DataFrame()
    
    resultado = df.groupby('tema').agg({
        'acertos': ['mean', 'sum'],
        'total_questoes': 'sum',
        'pontuacao': 'mean',
        'tempo_resposta': 'mean'
    }).round(2)
    
    # Calcula taxa de acertos por tema
    resultado['taxa_acertos'] = ((resultado[('acertos', 'sum')] / resultado[('total_questoes', 'sum')]) * 100).round(1)
    
    return resultado

def calcular_evolucao_temporal(df, dias=7):
    """
    Calcula a evolução do desempenho ao longo do tempo
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        dias (int): Número de dias para análise
        
    Returns:
        DataFrame: Evolução temporal do desempenho
    """
    if df.empty:
        return pd.DataFrame()
    
    # Filtra últimos N dias
    data_limite = datetime.now() - timedelta(days=dias)
    df_recente = df[df['data'] >= data_limite].copy()
    
    if df_recente.empty:
        return df.copy()
    
    # Agrupa por data
    evolucao = df_recente.groupby('data').agg({
        'acertos': 'mean',
        'pontuacao': 'mean',
        'tempo_resposta': 'mean'
    }).round(2)
    
    return evolucao

def calcular_percentual_evolucao(df):
    """
    Calcula o percentual de evolução comparando primeira e última semana
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        dict: Percentuais de evolução
    """
    if df.empty or len(df) < 2:
        return {
            "acertos": 0,
            "pontuacao": 0,
            "tempo": 0
        }
    
    # Ordena por data
    df_sorted = df.sort_values('data')
    
    # Divide em primeira e segunda metade
    meio = len(df_sorted) // 2
    primeira_metade = df_sorted.iloc[:meio]
    segunda_metade = df_sorted.iloc[meio:]
    
    # Calcula médias
    media_acertos_inicio = primeira_metade['acertos'].mean()
    media_acertos_fim = segunda_metade['acertos'].mean()
    
    media_pontuacao_inicio = primeira_metade['pontuacao'].mean()
    media_pontuacao_fim = segunda_metade['pontuacao'].mean()
    
    media_tempo_inicio = primeira_metade['tempo_resposta'].mean()
    media_tempo_fim = segunda_metade['tempo_resposta'].mean()
    
    # Calcula percentuais de evolução
    evol_acertos = ((media_acertos_fim - media_acertos_inicio) / media_acertos_inicio * 100) if media_acertos_inicio > 0 else 0
    evol_pontuacao = ((media_pontuacao_fim - media_pontuacao_inicio) / media_pontuacao_inicio * 100) if media_pontuacao_inicio > 0 else 0
    evol_tempo = ((media_tempo_inicio - media_tempo_fim) / media_tempo_inicio * 100) if media_tempo_inicio > 0 else 0  # Redução é positiva
    
    return {
        "acertos": round(evol_acertos, 1),
        "pontuacao": round(evol_pontuacao, 1),
        "tempo": round(evol_tempo, 1)
    }

def identificar_areas_fortes_fracas(df):
    """
    Identifica áreas fortes e fracas do aluno
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        dict: Áreas fortes e fracas
    """
    if df.empty:
        return {
            "fortes": [],
            "fracas": []
        }
    
    # Calcula média de acertos por tema
    desempenho_tema = df.groupby('tema')['acertos'].mean()
    
    # Calcula mediana geral
    mediana_geral = df['acertos'].median()
    
    # Identifica fortes (acima da mediana) e fracas (abaixo da mediana)
    areas_fortes = desempenho_tema[desempenho_tema > mediana_geral].sort_values(ascending=False).index.tolist()
    areas_fracas = desempenho_tema[desempenho_tema <= mediana_geral].sort_values().index.tolist()
    
    return {
        "fortes": areas_fortes,
        "fracas": areas_fracas
    }

def calcular_consistencia(df):
    """
    Calcula a consistência do desempenho (menor desvio padrão = mais consistente)
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        dict: Métricas de consistência
    """
    if df.empty:
        return {
            "consistencia": 0,
            "nivel": "Sem dados"
        }
    
    desvio = df['acertos'].std()
    media = df['acertos'].mean()
    
    # Calcula coeficiente de variação (CV)
    cv = (desvio / media * 100) if media > 0 else 0
    
    # Classifica consistência
    if cv < 15:
        nivel = "Muito Consistente"
    elif cv < 30:
        nivel = "Consistente"
    elif cv < 45:
        nivel = "Moderado"
    else:
        nivel = "Inconsistente"
    
    return {
        "consistencia": round(100 - cv, 1),  # Inverte para que maior = melhor
        "nivel": nivel,
        "coeficiente_variacao": round(cv, 1)
    }

def calcular_media_movel(df, janela=3):
    """
    Calcula média móvel do desempenho
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        janela (int): Tamanho da janela para média móvel
        
    Returns:
        Series: Série com média móvel
    """
    if df.empty:
        return pd.Series()
    
    df_sorted = df.sort_values('data')
    return df_sorted['acertos'].rolling(window=janela).mean()

def gerar_resumo_estatistico(df):
    """
    Gera um resumo estatístico completo
    
    Args:
        df (DataFrame): DataFrame com dados de progresso
        
    Returns:
        dict: Resumo estatístico completo
    """
    if df.empty:
        return {}
    
    return {
        "desempenho_geral": calcular_desempenho(df),
        "evolucao": calcular_percentual_evolucao(df),
        "areas": identificar_areas_fortes_fracas(df),
        "consistencia": calcular_consistencia(df),
        "ultima_atividade": df['data'].max().strftime('%d/%m/%Y') if not df.empty else "N/A"
    }


