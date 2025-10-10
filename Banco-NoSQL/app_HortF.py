import streamlit as st
import time
import pandas as pd

SEGUNDOS_POR_MINUTO = 60
SEGUNDOS_POR_HORA = 3600
SEGUNDOS_POR_DIA = 86400

# --- RELÓGIO FALSO (Mocking Time) ---
if 'time_offset' not in st.session_state:
    st.session_state.time_offset = 0.0

def get_current_time():
    """ Retorna o tempo real + o offset simulado. """
    return time.time() + st.session_state.time_offset

# --- CLASSE DE SIMULAÇÃO DO CACHE (BACKEND DO MEMCACHED) ---

class CacheSimulador:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, ttl_seconds):
        try:
            ttl_seconds = int(ttl_seconds)
        except ValueError:
            return "Erro: TTL deve ser um número inteiro."
        
        # USA O RELÓGIO FALSO AQUI
        expiry_time = get_current_time() + ttl_seconds
        self.cache[key] = (value, expiry_time)
        return f"✅ SET: '{key}' (Valor: {value}) armazenada. Expira em {ttl_seconds}s."

    def get(self, key):
        if key not in self.cache:
            return None, "❌ Chave não encontrada (Cache Miss)."

        value, expiry_time = self.cache[key]
        
        # USA O RELÓGIO FALSO AQUI
        tempo_restante = max(0, expiry_time - get_current_time())
        
        # Verifica a expiração usando o Relógio Falso
        if get_current_time() > expiry_time:
            del self.cache[key]
            return None, f"⚠️ EXPIRADO: Chave '{key}' removida. (Cache Miss)" 
        
        mensagem = f"👍 HIT! TTL Restante: {tempo_restante:.2f} segundos."
        return value, mensagem
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            return f"🧹 DELETE: Registro '{key}' invalidado com sucesso."
        return f"⚠️ Registro '{key}' não estava na cache."

    def get_status_data(self):
        data = []
        for key, (value, expiry_time) in self.cache.items():
            # USA O RELÓGIO FALSO AQUI
            tempo_restante = max(0, expiry_time - get_current_time())
            status = "VÁLIDO" if tempo_restante > 0 else "EXPIRADO"
            
            data.append({
                'Chave (Item)': key,
                'Valor Registrado': value,
                'TTL Restante (s)': f"{tempo_restante:.1f}",
                'Status': status,
                'Expira em': time.ctime(expiry_time)
            })
        return pd.DataFrame(data)

# --- FUNÇÃO DE INICIALIZAÇÃO DE DADOS (BIBLIOTECA) ---

def inicializar_cache(cache_obj):
    st.subheader("Configuração Inicial do Cache")
    
    # TTLs mais realistas (em segundos)
    dados_precos = {
        'preco_maca': ('R$ 8.99/kg', 3 * SEGUNDOS_POR_HORA),           
        'preco_tomate': ('R$ 2.99/kg', 1 * SEGUNDOS_POR_DIA),         
        'preco_alface': ('R$ 4.50/kg', 30 * SEGUNDOS_POR_MINUTO),     
        'preco_morango': ('R$ 12.00/bandeja', 1 * SEGUNDOS_POR_HORA),  
        'preco_uva': ('R$ 15.00/kg', 5 * SEGUNDOS_POR_DIA),          
    }
    
    dados_estoque = {
        'estoque_maca': ('25 caixas', 6 * SEGUNDOS_POR_HORA),         
        'estoque_tomate': ('30 caixas', 2 * SEGUNDOS_POR_DIA),        
        'estoque_alface': ('20 caixas', 5 * SEGUNDOS_POR_MINUTO),     
        'estoque_morango': ('25 caixas', 4 * SEGUNDOS_POR_HORA),       
        'estoque_uva': ('10 caixas', 10 * SEGUNDOS_POR_MINUTO),       
    }

    dados_totais = {**dados_precos, **dados_estoque} 
    
    for chave, (valor, ttl) in dados_totais.items():
        cache_obj.set(chave, valor, ttl)
    
    st.success("Cache Inicializado com 10 dados de Preço e Estoque.")

# --- INTERFACE STREAMLIT (DASHBOARD) ---

# 1. Configuração e Inicialização
if 'cache' not in st.session_state:
    st.session_state.cache = CacheSimulador()
    inicializar_cache(st.session_state.cache)

st.title("👨‍🌾 Dashboard de Controle: Simulação Avançada de TTL (Relógio Falso)")
st.subheader("Simulação de Cache com TTL para Otimização de Consultas | Luca Atanazio - Lucas Faria - Pablo Henrique")
st.caption("UC3: Realizar a gerência de grandes volumes de dados utilizando tecnologias de Big Data e ferramentas de computação em nuvem, otimizando o processamento e a análise de dados.")

# --- 2. VISUALIZAÇÃO DA CACHE ATIVA ---
st.header("Status da Cache (Memória) - Tempo Lógico Atual")
df_cache = st.session_state.cache.get_status_data()

# Exibe o tempo simulado atual
st.info(f"⏰ **Tempo Lógico Atual:** {time.ctime(get_current_time())} (Offset Total: {st.session_state.time_offset/SEGUNDOS_POR_DIA:.2f} dias)")

st.dataframe(df_cache, use_container_width=True, hide_index=True)


# --- 3. FERRAMENTAS DO FUNCIONÁRIO (SET, GET, SALTO DE TEMPO) ---
st.header("Ferramentas de Registro e Salto Temporal")

col_set, col_get, col_sleep = st.columns(3)

# 3.1. SET (Registro/Atualização do Estoque/Preço)
with col_set:
    st.markdown("#### Novo Registro (SET)")
    with st.form("set_form", clear_on_submit=True):
        key_set = st.text_input("Chave/Item (ex.: preco_manga)", value="estoque_kiwi").lower()
        value_set = st.text_input("Valor (ex.: R$ 10.99/kg ou 50 caixas)", value="100 caixas") 
        ttl_set = st.number_input("Validade (TTL em Segundos)", min_value=1, value=3600)
        submitted_set = st.form_submit_button("REGISTRAR (SET)")
        
        if submitted_set:
            resultado = st.session_state.cache.set(key_set, value_set, ttl_set)
            st.success(resultado)

# 3.2. GET (Consulta Rápida)
with col_get:
    st.markdown("#### Consultar (GET)")
    with st.form("get_form", clear_on_submit=True):
        key_get = st.text_input("Chave para Consultar", value="preco_uva").lower()
        submitted_get = st.form_submit_button("CONSULTAR (GET)")
        
        if submitted_get:
            value, msg = st.session_state.cache.get(key_get)
            
            if value:
                st.success(f"DADO: {value} | {msg}")
            else:
                st.warning(f"FALHA: {msg}")

# 3.3. SALTO DE TEMPO (Avançar 86400s em 10s)
with col_sleep:
    st.markdown("#### Salto Temporal (TTL Avançado)")
    
    with st.form("delete_form", clear_on_submit=True):
        key_delete = st.text_input("Chave para Invalidar (DELETE)", value="preco_tomate").lower()
        submitted_delete = st.form_submit_button("INVALIDAR MANUALMENTE")
        if submitted_delete:
            resultado_delete = st.session_state.cache.delete(key_delete)
            st.info(resultado_delete)

    with st.form("time_jump_form", clear_on_submit=True):
        jump_time = st.number_input("Avançar Tempo Lógico (Segundos)", min_value=1, value=604800) 
        submitted_jump = st.form_submit_button("EXECUTAR SALTO TEMPORAL")
        
        if submitted_jump:
            st.session_state.time_offset += jump_time
            
            time.sleep(10) 
            
            st.success(f"✅ Salto Temporal de {jump_time}s concluído! O tempo lógico avançou.")
            st.rerun() 
            
st.markdown("---")
if st.button("Atualizar Visão Geral"):
    st.rerun()