"""
Data Loaders - Funções robustas para carregar dados sem erros.
"""
import streamlit as st
from utils.api_client import api_client
from utils.constants import CACHE_TTL
import pandas as pd

# ===== CARREGADORES DE TURMAS =====

@st.cache_data(ttl=300)
def carregar_turmas_professor():
    try:
        result = api_client.get_teacher_classes()
        
        print(f"[DEBUG carregar_turmas] result.get('success'): {result.get('success')}")
        
        if not result.get('success'):
            print("[DEBUG carregar_turmas] success=False, retornando []")
            return []

        # Pega o conteúdo bruto de 'data'
        raw_data = result.get('data', [])
        print(f"[DEBUG carregar_turmas] raw_data: {raw_data}")
        print(f"[DEBUG carregar_turmas] type(raw_data): {type(raw_data)}")

        # BLINDAGEM: Verifica o tipo antes de acessar
        turmas = []
        if isinstance(raw_data, dict):
            # Se for dicionário (Novo formato: {'data': [...]})
            turmas = raw_data.get('data', [])
            print(f"[DEBUG carregar_turmas] raw_data é dict, extraiu turmas: {turmas}")
        elif isinstance(raw_data, list):
            # Se for lista direta (Velho formato: [...])
            turmas = raw_data
            print(f"[DEBUG carregar_turmas] raw_data já é lista: {turmas}")
        
        # Garante que é uma lista de dicionários
        if not isinstance(turmas, list):
            print(f"[DEBUG carregar_turmas] turmas nao e lista! type: {type(turmas)}")
            return []

        print(f"[DEBUG carregar_turmas] Total antes filtro: {len(turmas)}")
        
        # Filtra apenas itens válidos (que são dicts e ativos)
        turmas_filtradas = [t for t in turmas if isinstance(t, dict) and t.get('is_active', True)]
        
        print(f"[DEBUG carregar_turmas] Retornando {len(turmas_filtradas)} turmas filtradas")
        for idx, t in enumerate(turmas_filtradas):
            print(f"[DEBUG carregar_turmas]   Turma {idx}: name={t.get('name')}, student_count={t.get('student_count')}")
        
        return turmas_filtradas

    except Exception as e:
        # Log silencioso para não sujar a tela
        print(f"[DEBUG carregar_turmas] Exception: {e}")
        import traceback
        traceback.print_exc()
        return []

# ===== CARREGADORES DE ALUNOS =====

@st.cache_data(ttl=300)
def carregar_alunos_professor():
    try:
        result = api_client.get_all_students_by_teacher()
        if not result.get('success'): return []
        
        raw_data = result.get('data', [])
        
        if isinstance(raw_data, dict):
            return raw_data.get('data', [])
        elif isinstance(raw_data, list):
            return raw_data
        return []
    except Exception:
        return []

@st.cache_data(ttl=300)
def carregar_alunos_turma(turma_id):
    try:
        todos = carregar_alunos_professor()
        return [a for a in todos if str(a.get('turma_id', '')) == str(turma_id)]
    except: return []

# ===== CARREGADORES DE ALERTAS (ESSENCIAL) =====

@st.cache_data(ttl=10) 
def carregar_alertas_crise():
    try:
        result = api_client.get_crisis_alerts()
        
        print(f"[DEBUG carregar_alertas_crise] result completo: {result}")
        print(f"[DEBUG carregar_alertas_crise] success: {result.get('success')}")
        
        if not result.get('success'): 
            print(f"[DEBUG carregar_alertas_crise] success=False")
            return []
        
        raw_data = result.get('data', [])
        print(f"[DEBUG carregar_alertas_crise] raw_data: {raw_data}")
        print(f"[DEBUG carregar_alertas_crise] type(raw_data): {type(raw_data)}")
        
        # Mesma lógica de blindagem
        dados = []
        if isinstance(raw_data, dict):
            dados = raw_data.get('data', [])
        elif isinstance(raw_data, list):
            dados = raw_data
            
        # Se por acaso vier aninhado extra (data dentro de data)
        if isinstance(dados, dict) and 'data' in dados:
            dados = dados.get('data', [])
        
        print(f"[DEBUG carregar_alertas_crise] Retornando {len(dados) if isinstance(dados, list) else 0} alertas")
        if isinstance(dados, list) and len(dados) > 0:
            print(f"[DEBUG carregar_alertas_crise] Primeiro alerta: {dados[0]}")
            
        return dados if isinstance(dados, list) else []
            
    except Exception as e:
        print(f"Erro alertas: {e}")
        import traceback
        traceback.print_exc()
        return []

# ===== MÉDIA DE NOTAS =====

@st.cache_data(ttl=300, show_spinner=False)
def carregar_media_notas():
    """
    Carrega a média de notas de todos os alunos do professor.
    Retorna None se não houver notas ou ocorrer erro.
    """
    try:
        resultado = api_client.get_students_average_grade()
        
        if resultado.get('success') and resultado.get('data'):
            data = resultado['data']
            # Retorna a média arredondada ou None se não houver notas
            return data.get('average') if data.get('count', 0) > 0 else None
        
        return None
    except Exception as e:
        print(f"Erro ao carregar média de notas: {e}")
        return None

# ===== SENTIMENTOS =====

@st.cache_data(ttl=60)
def carregar_sentimentos_alunos(turma_id=None):
    """
    Carrega sentimentos dos alunos.
    Se turma_id for informado, filtra apenas os alunos dessa turma.
    """
    try:
        # Se der erro, retorna DataFrame vazio para não quebrar gráficos
        alunos = carregar_alunos_professor()
        
        # Filtra por turma se especificado
        if turma_id and turma_id != 'todas':
            alunos = [a for a in alunos if str(a.get('turma_id', '')) == str(turma_id)]
        
        todos = []
        for aluno in alunos:
            # (Lógica simplificada para evitar erros)
            try:
                res = api_client.get_student_feelings(str(aluno.get('_id')))
                sents = res.get('data', [])
                if isinstance(sents, dict): sents = sents.get('data', [])
                
                if isinstance(sents, list):
                    for s in sents:
                        s['nome_aluno'] = aluno.get('nome', 'Desconhecido')
                        s['turma_id'] = aluno.get('turma_id', '')
                        todos.append(s)
            except: pass
            
        return pd.DataFrame(todos) if todos else pd.DataFrame()
    except: return pd.DataFrame()

def limpar_todos_caches():
    st.cache_data.clear()