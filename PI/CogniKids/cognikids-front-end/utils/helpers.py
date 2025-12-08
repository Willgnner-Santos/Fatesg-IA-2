"""
Funções auxiliares para o sistema CogniKids
Inclui funções para trabalhar com API e dados locais (fallback)
"""

import json
import pandas as pd
from datetime import datetime
import os
from typing import Optional, Dict, List, Any

# Importa o cliente da API
try:
    from utils.api_client import api_client
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False
    print("[AVISO] API Client nao disponivel. Usando dados locais.")

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def carregar_usuarios():
    """
    DEPRECATED: Esta função está obsoleta e será removida em versões futuras.
    Use api_client.get_users() para obter usuários via API.
    
    Carrega os dados dos usuários do arquivo JSON
    
    Returns:
        list: Lista de usuários
    """
    import warnings
    warnings.warn(
        "carregar_usuarios() está obsoleto. Use api_client.get_users() para obter usuários via API.",
        DeprecationWarning,
        stacklevel=2
    )
    try:
        with open(os.path.join(DATA_DIR, 'users.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['users']
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        return []

def salvar_usuarios(usuarios):
    """
    DEPRECATED: Esta função está obsoleta e será removida em versões futuras.
    Use api_client.create_user() ou api_client.update_user() para gerenciar usuários via API.
    
    Salva os dados dos usuários no arquivo JSON
    
    Args:
        usuarios (list): Lista de usuários
    """
    import warnings
    warnings.warn(
        "salvar_usuarios() está obsoleto. Use api_client para gerenciar usuários via API.",
        DeprecationWarning,
        stacklevel=2
    )
    try:
        with open(os.path.join(DATA_DIR, 'users.json'), 'w', encoding='utf-8') as f:
            json.dump({'users': usuarios}, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")
        return False

def autenticar_usuario(username, password):
    """
    DEPRECATED: Esta função está obsoleta e será removida em versões futuras.
    Use api_client.login() para autenticação via API.
    
    Autentica um usuário
    
    Args:
        username (str): Nome de usuário
        password (str): Senha
        
    Returns:
        dict: Dados do usuário se autenticado, None caso contrário
    """
    import warnings
    warnings.warn(
        "autenticar_usuario() está obsoleto. Use api_client.login() para autenticação via API.",
        DeprecationWarning,
        stacklevel=2
    )
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            return usuario
    return None

def carregar_progresso(usuario_id=None):
    """
    DEPRECATED: Esta função está obsoleta e será removida em versões futuras.
    Use api_client.get_student_grades() para obter notas via API.
    
    Carrega os dados de progresso do arquivo CSV ou API
    
    Args:
        usuario_id (int|str): ID do usuário (opcional)
        
    Returns:
        DataFrame: Dados de progresso
    """
    import warnings
    warnings.warn(
        "carregar_progresso() está obsoleto. Use api_client.get_student_grades() diretamente.",
        DeprecationWarning,
        stacklevel=2
    )
    # Tenta carregar via API primeiro
    if API_AVAILABLE and usuario_id:
        try:
            result = api_client.get_student_grades(str(usuario_id))
            if result.get('success'):
                # Converte dados da API para DataFrame
                grades_data = result.get('data', {}).get('grades', [])
                if grades_data:
                    df = pd.DataFrame(grades_data)
                    # Ajusta nomes de colunas se necessário
                    if 'created_at' in df.columns:
                        df['data'] = pd.to_datetime(df['created_at'])
                    if 'subject' in df.columns:
                        df['tema'] = df['subject']
                    if 'grade' in df.columns:
                        df['pontuacao'] = df['grade']
                    
                    return df
        except Exception as e:
            print(f"Erro ao carregar via API: {e}")
    
    # Fallback: carrega de arquivo local
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'progress.csv'))
        df['data'] = pd.to_datetime(df['data'])
        
        if usuario_id is not None:
            df = df[df['usuario_id'] == int(usuario_id) if isinstance(usuario_id, (int, str)) and str(usuario_id).isdigit() else usuario_id]
        
        return df
    except Exception as e:
        print(f"Erro ao carregar progresso: {e}")
        return pd.DataFrame()

def salvar_resposta(usuario_id, tema, acertos, total_questoes, tempo_resposta, pontuacao):
    """
    DEPRECATED: Esta função está obsoleta e será removida em versões futuras.
    Use api_client.save_grade() diretamente para salvar notas via API.
    
    Salva uma nova resposta no arquivo de progresso ou via API
    
    Args:
        usuario_id (int|str): ID do usuário
        tema (str): Tema da atividade
        acertos (int): Número de acertos
        total_questoes (int): Total de questões
        tempo_resposta (float): Tempo de resposta em segundos
        pontuacao (int): Pontuação obtida
    """
    import warnings
    warnings.warn(
        "salvar_resposta() está obsoleto. Use api_client.save_grade() diretamente.",
        DeprecationWarning,
        stacklevel=2
    )
    # Tenta salvar via API primeiro
    if API_AVAILABLE:
        try:
            result = api_client.save_grade(
                student_id=str(usuario_id),
                subject=tema,
                grade=pontuacao,
                observation=f"Acertos: {acertos}/{total_questoes} - Tempo: {tempo_resposta}s"
            )
            if result.get('success'):
                return True
        except Exception as e:
            print(f"Erro ao salvar via API: {e}")
    
    # Fallback: salva em arquivo local
    try:
        # Carrega o progresso existente
        df = pd.read_csv(os.path.join(DATA_DIR, 'progress.csv'))
        
        # Cria nova linha
        nova_linha = pd.DataFrame([{
            'usuario_id': usuario_id,
            'data': datetime.now().strftime('%Y-%m-%d'),
            'tema': tema,
            'acertos': acertos,
            'total_questoes': total_questoes,
            'tempo_resposta': tempo_resposta,
            'pontuacao': pontuacao
        }])
        
        # Adiciona ao DataFrame
        df = pd.concat([df, nova_linha], ignore_index=True)
        
        # Salva
        df.to_csv(os.path.join(DATA_DIR, 'progress.csv'), index=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar resposta: {e}")
        return False

def formatar_tempo(segundos):
    """
    Formata tempo em segundos para string legível
    
    Args:
        segundos (float): Tempo em segundos
        
    Returns:
        str: Tempo formatado
    """
    if segundos < 60:
        return f"{segundos:.1f}s"
    else:
        minutos = int(segundos // 60)
        segundos_rest = segundos % 60
        return f"{minutos}m {segundos_rest:.0f}s"

def calcular_percentual_acertos(acertos, total):
    """
    Calcula o percentual de acertos
    
    Args:
        acertos (int): Número de acertos
        total (int): Total de questões
        
    Returns:
        float: Percentual de acertos
    """
    if total == 0:
        return 0
    return (acertos / total) * 100

def obter_cor_desempenho(percentual):
    """
    Retorna uma cor baseada no percentual de desempenho
    
    Args:
        percentual (float): Percentual de acertos
        
    Returns:
        str: Código de cor hexadecimal
    """
    if percentual >= 90:
        return "#10B981"  # Verde
    elif percentual >= 70:
        return "#FACC15"  # Amarelo
    elif percentual >= 50:
        return "#F59E0B"  # Laranja
    else:
        return "#EF4444"  # Vermelho

def obter_emoji_desempenho(percentual):
    """
    Retorna um emoji baseado no percentual de desempenho
    
    Args:
        percentual (float): Percentual de acertos
        
    Returns:
        str: Emoji
    """
    if percentual >= 90:
        return "🌟"
    elif percentual >= 70:
        return "😊"
    elif percentual >= 50:
        return "😐"
    else:
        return "😢"


