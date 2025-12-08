"""
Script simples para gerar alertas de crise para DEMONSTRAÇÃO.
Gera 2 alertas (Ana Sofia e Lucas Silva) automaticamente.
"""
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import random

print("=" * 80)
print("GERANDO ALERTAS DE CRISE PARA DEMONSTRAÇÃO")
print("=" * 80)

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cognikidsDB"]

# IDs dos alunos
ana_id = ObjectId("69111874ca4398a1897afba3")
lucas_id = ObjectId("69111874ca4398a1897afba4")

# Limpar alertas antigos primeiro
db.alerts.delete_many({'aluno_id': {'$in': [ana_id, lucas_id]}})
print("\n[OK] Alertas antigos removidos")

# IMPORTANTE: Usar datetime.utcnow() para compatibilidade com o backend
timestamp_utc = datetime.utcnow()

# Gerar alertas
alertas = [
    {
        'aluno_id': ana_id,
        'device_id': 'pulseira_ana_001',
        'data_hora': timestamp_utc,  # UTC!
        'alert_type': 'crisis',
        'severity': 'high',
        'dados_biometricos': {
            'bpm': 145.5,
            'heart_rate': 145.5,
            'gsr': 3.2,
            'temperature': 37.1
        },
        'ml_confidence': 0.92,
        'motivo': 'Batimentos elevados + Alta condutância da pele',
        'created_at': timestamp_utc
    },
    {
        'aluno_id': lucas_id,
        'device_id': 'pulseira_lucas_002',
        'data_hora': timestamp_utc,  # UTC!
        'alert_type': 'crisis',
        'severity': 'high',
        'dados_biometricos': {
            'bpm': 158.3,
            'heart_rate': 158.3,
            'gsr': 4.1,
            'temperature': 37.3
        },
        'ml_confidence': 0.95,
        'motivo': 'Estado crítico - Batimentos e GSR extremos',
        'created_at': timestamp_utc
    }
]

# Inserir no banco
result = db.alerts.insert_many(alertas)

print(f"\n[OK] {len(result.inserted_ids)} alertas inseridos com IDs:")
for id in result.inserted_ids:
    print(f"   - {id}")

# Verificar se foram inseridos
alertas_verificacao = list(db.alerts.find({'aluno_id': {'$in': [ana_id, lucas_id]}}))
print(f"\n[INFO] Verificacao: {len(alertas_verificacao)} alertas encontrados no banco")

print("\n[ALERTA] ALERTAS GERADOS COM SUCESSO!")
print("\n1. Ana Sofia")
print(f"   BPM: {alertas[0]['dados_biometricos']['bpm']}")
print(f"   GSR: {alertas[0]['dados_biometricos']['gsr']}")

print("\n2. Lucas Silva")
print(f"   BPM: {alertas[1]['dados_biometricos']['bpm']}")
print(f"   GSR: {alertas[1]['dados_biometricos']['gsr']}")

print("\n" + "=" * 80)
print("[OK] Agora atualize o dashboard do Professor Carlos!")
print("   Os alertas devem aparecer na seção 'Alertas de Crise'")
print("=" * 80)
