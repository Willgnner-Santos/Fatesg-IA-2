import redis
import json
import time
import os
import joblib
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

print("Iniciando o Consumidor (alert_monitor.py)...")

# Conexao com o Redis (servico 'redis' do Docker)
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("[OK] Consumidor: Conectado ao Redis.")
except Exception as e:
    print(f"[ERRO] Consumidor: Falha ao conectar ao Redis: {e}")
    exit(1)

# Conexao com o MongoDB (servico 'db' do Docker)
try:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://db:27017/cognikidsDB')
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_default_database()
    db.command('ping')
    print("[OK] Consumidor: Conectado ao MongoDB.")
except Exception as e:
    print(f"[ERRO] Consumidor: Falha ao conectar ao MongoDB: {e}")
    exit(1)

# Carregamento do Modelo de Machine Learning
try:
    model = joblib.load('model.joblib')
    print(f"[OK] Consumidor: Modelo 'model.joblib' carregado com sucesso.")
except FileNotFoundError:
    print("[ERRO] Consumidor: Arquivo 'model.joblib' nao encontrado. Execute 'train_model.py' primeiro.")
    exit(1)
except Exception as e:
    print(f"[ERRO] Consumidor: Erro ao carregar 'model.joblib': {e}")
    exit(1)

# Colecoes do MongoDB para armazenamento
col_raw_data = db.iot_raw_data
col_alerts = db.alerts

def processar_mensagem(raw_data):
    """
    Processa mensagem da fila Redis, realiza inferencia ML e armazena resultados.
    
    Etapas:
        1. Decodificacao do JSON
        2. Armazenamento no Data Lake (iot_raw_data)
        3. Inferencia do modelo de ML
        4. Geracao de alerta se crise detectada
    
    Args:
        raw_data (str): Dados brutos em formato JSON string.
    """
    try:
        # Decodificacao do JSON
        data = json.loads(raw_data)
        dados_bio = data.get('dados_biometricos', {})
        
        # Armazenamento no Data Lake
        data_to_save = data.copy()
        data_to_save['aluno_id'] = ObjectId(data['aluno_id'])
        data_to_save['dispositivo_id'] = ObjectId(data['dispositivo_id'])
        data_to_save['timestamp_processado_utc'] = datetime.datetime.utcnow()
        col_raw_data.insert_one(data_to_save)
        
        # Inferencia do Modelo de ML
        # Preparacao das features no formato esperado pelo modelo
        features = pd.DataFrame([{
            'bpm': dados_bio.get('bpm', 0),
            'gsr': dados_bio.get('gsr', 0),
            'movement_score': dados_bio.get('movement_score', 0)
        }])
        
        previsao = model.predict(features)[0]
        
        # Geracao de Alerta
        if previsao == 1:
            print(f"[ALERTA] CRISE DETECTADA - Aluno: {data['aluno_id']}, BPM: {dados_bio.get('bpm')}")
            alerta = {
                "aluno_id": ObjectId(data['aluno_id']),
                "data_hora": datetime.datetime.utcnow(),
                "dados_biometricos": dados_bio,
                "motivo": "Predicao do Modelo de ML"
            }
            col_alerts.insert_one(alerta)
        else:
            print(f"[OK] Dados normais - Aluno: {data['aluno_id']}, BPM: {dados_bio.get('bpm')}")

    except json.JSONDecodeError:
        print("     Erro: Dado mal formatado recebido do Redis.")
    except Exception as e:
        print(f"     Erro ao processar mensagem: {e}")

# Loop Principal do Consumidor
def iniciar_consumidor():
    """
    Inicia o loop principal do consumidor de mensagens.
    
    Aguarda dados na fila Redis de forma bloqueante (BRPOP)
    e processa cada mensagem recebida.
    """
    while True:
        try:
            # BRPOP - Blocking Right Pop: aguarda eficientemente por um item
            # O parametro '0' indica espera indefinida
            print("Aguardando dados na fila 'iot_queue'...")
            item_enfileirado = redis_client.brpop('iot_queue', 0)
            
            # item_enfileirado retorna tupla (nome_da_fila, dados)
            dados_brutos = item_enfileirado[1]
            
            processar_mensagem(dados_brutos)

        except redis.exceptions.ConnectionError:
            print("[ERRO] Perda de conexao com o Redis. Tentando reconectar em 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"[ERRO] Erro critico no loop do consumidor: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_consumidor()