"""
Script para popular dados de teste nas coleções corretas (iot_raw_data + alerts)
Simula o fluxo: MQTT → Redis → alert_monitor.py → MongoDB
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import random

print("\n=== POPULANDO DADOS DE TESTE (Data Lake + Data Mart) ===\n")

# Conexão
client = MongoClient("mongodb://localhost:27017/cognikidsDB")
db = client.get_default_database()

# IDs reais do banco (Professor Carlos + seus alunos)
ID_PROFESSOR = ObjectId("69111874ca4398a1897afb9f")
ID_TURMA = ObjectId("69111874ca4398a1897afba1")
ID_ANA_SOFIA = ObjectId("69111874ca4398a1897afba3")
ID_LUCAS_SILVA = ObjectId("69111874ca4398a1897afba4")

# Buscar dispositivos dos alunos
dispositivo_ana = db.dispositivos.find_one({"aluno_id": ID_ANA_SOFIA})
dispositivo_lucas = db.dispositivos.find_one({"aluno_id": ID_LUCAS_SILVA})

if not dispositivo_ana or not dispositivo_lucas:
    print("ERRO: Dispositivos nao encontrados. Execute populate_db.py primeiro.")
    exit(1)

ID_DISPOSITIVO_ANA = dispositivo_ana['_id']
ID_DISPOSITIVO_LUCAS = dispositivo_lucas['_id']

print(f"OK: Dispositivos encontrados:")
print(f"   Ana Sofia: {ID_DISPOSITIVO_ANA}")
print(f"   Lucas Silva: {ID_DISPOSITIVO_LUCAS}\n")

# Limpar dados antigos
db.iot_raw_data.delete_many({})
db.alerts.delete_many({})
print("Colecoes limpas (iot_raw_data, alerts)\n")

# Função para gerar dados biométricos
def gerar_dados_biometricos(tipo='normal'):
    """
    tipo: 'normal', 'estresse', 'crise'
    """
    if tipo == 'normal':
        return {
            'bpm': random.randint(70, 100),
            'gsr': round(random.uniform(0.5, 1.0), 2),
            'movement_score': round(random.uniform(0.3, 1.0), 2)
        }
    elif tipo == 'estresse':
        return {
            'bpm': random.randint(100, 130),
            'gsr': round(random.uniform(1.0, 1.8), 2),
            'movement_score': round(random.uniform(1.0, 2.0), 2)
        }
    else:  # crise
        return {
            'bpm': random.randint(130, 160),
            'gsr': round(random.uniform(1.8, 3.5), 2),
            'movement_score': round(random.uniform(2.0, 3.5), 2)
        }

# Timestamps (últimos 10 minutos)
agora = datetime.datetime.utcnow()
timestamps = [agora - datetime.timedelta(minutes=i) for i in range(10, 0, -1)]

# === CENÁRIO 1: Ana Sofia - CRISE (últimos 2 registros) ===
print("Gerando dados para Ana Sofia (8 normais + 2 CRISES)...")
for i, ts in enumerate(timestamps):
    tipo = 'crise' if i >= 8 else 'normal'
    dados_bio = gerar_dados_biometricos(tipo)
    
    # 1. Salvar no Data Lake (iot_raw_data)
    registro_raw = {
        "aluno_id": ID_ANA_SOFIA,
        "dispositivo_id": ID_DISPOSITIVO_ANA,
        "dados_biometricos": dados_bio,
        "timestamp_processado_utc": ts
    }
    db.iot_raw_data.insert_one(registro_raw)
    
    # 2. Se for crise, salvar no Data Mart (alerts)
    if tipo == 'crise':
        alerta = {
            "aluno_id": ID_ANA_SOFIA,
            "data_hora": ts,
            "dados_biometricos": dados_bio,
            "motivo": "Predição do Modelo de ML"
        }
        db.alerts.insert_one(alerta)
        print(f"   CRISE: BPM={dados_bio['bpm']}, GSR={dados_bio['gsr']} as {ts.strftime('%H:%M:%S')}")

# === CENÁRIO 2: Lucas Silva - NORMAL (todos registros normais) ===
print("\nGerando dados para Lucas Silva (10 normais)...")
for ts in timestamps:
    dados_bio = gerar_dados_biometricos('normal')
    
    registro_raw = {
        "aluno_id": ID_LUCAS_SILVA,
        "dispositivo_id": ID_DISPOSITIVO_LUCAS,
        "dados_biometricos": dados_bio,
        "timestamp_processado_utc": ts
    }
    db.iot_raw_data.insert_one(registro_raw)

print(f"   OK: Lucas estavel: BPM medio ~85, GSR ~0.7")

# === RESUMO ===
print("\n" + "="*60)
print("RESUMO DOS DADOS INSERIDOS:")
print("="*60)
print(f"Data Lake (iot_raw_data): {db.iot_raw_data.count_documents({})} registros")
print(f"Data Mart (alerts):       {db.alerts.count_documents({})} alertas de crise")
print()
print("ALERTAS ESPERADOS NO DASHBOARD:")
alertas_recentes = list(db.alerts.find({"data_hora": {"$gte": agora - datetime.timedelta(minutes=5)}}).sort('data_hora', -1))
print(f"   Crises nos ultimos 5 min: {len(alertas_recentes)}")
for alerta in alertas_recentes:
    aluno_doc = db.users.find_one({"_id": alerta['aluno_id']})
    nome = aluno_doc.get('nome', 'Desconhecido') if aluno_doc else 'Desconhecido'
    dados = alerta['dados_biometricos']
    print(f"      [CRISE] {nome}: BPM={dados['bpm']}, GSR={dados['gsr']}")

print("\nOK: Dados populados com sucesso!")
print("Proximo passo: Reiniciar o backend e testar no Dashboard do Professor Carlos")
print("   Comando: docker-compose restart api (ou streamlit run app.py no frontend)\n")
