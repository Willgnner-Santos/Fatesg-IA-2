import paho.mqtt.client as mqtt
import time
import random
import json
import numpy as np
from datetime import datetime, timedelta
import pytz

print("\n--- Gerador IoT Inteligente (Intervalo Dinamico 30s/60s) ---")
print("--- Logica: 60s se estavel (Calmo) | 30s se risco (Ativo/Tenso/Crise) ---")

# ============================================================
# 1. CONFIGURACOES
# ============================================================

MQTT_BROKER_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "cognikids/iot/data"

TOTAL_REGISTROS = 500000
RUIDO_SENSOR = 0.15
DIAS_DE_HISTORICO = 60  # Aumentamos para 60 dias pois o intervalo médio aumentou

TZ_SAO_PAULO = pytz.timezone("America/Sao_Paulo")

# IDs Reais (Sincronizados com o banco)
DISPOSITIVOS_ALUNOS = [
    {"dispositivo_id": "68e265c13d5ad301f1a4c636", "nome": "ANA_CALMA", "persona": "ANA_CALMA"},
    {"dispositivo_id": "68fed345506b170be8ff6a22", "nome": "LUCAS_ANSIOSO", "persona": "LUCAS_ANSIOSO"},
    {"dispositivo_id": "690f4e1ed1696437d51d2ca0", "nome": "CLARA_NORMAL", "persona": "CLARA_NORMAL"},
    {"dispositivo_id": "690fc770359ad327aa244550", "nome": "DIOGO_MODERADO", "persona": "DIOGO_MODERADO"}
]

# ============================================================
# 2. LOGICA DE DADOS E ESTADOS
# ============================================================

# No arquivo iot_simulator.py
ESTADOS = {
    'CALMO': {'bpm_range': (55, 100), 'gsr_range': (0.1, 1.0), 'movement_range': (0.1, 1.4)},
    'ATIVO': {'bpm_range': (85, 165), 'gsr_range': (0.4, 3.0), 'movement_range': (0.5, 4.5)},
    'TENSO': {'bpm_range': (90, 160), 'gsr_range': (1.0, 3.8), 'movement_range': (0.0, 2.0)}, 
    'CRISE': {'bpm_range': (120, 190), 'gsr_range': (2.2, 6.5), 'movement_range': (0.0, 3.5)}
}

PERSONAS = {
    'ANA_CALMA': {'CALMO': [0.95, 0.05, 0.0, 0.0], 'ATIVO': [0.90, 0.10, 0.0, 0.0], 'TENSO': [0.80, 0.0, 0.20, 0.0], 'CRISE': [1.0, 0.0, 0.0, 0.0]},
    'LUCAS_ANSIOSO': {'CALMO': [0.80, 0.05, 0.15, 0.0], 'ATIVO': [0.75, 0.05, 0.20, 0.0], 'TENSO': [0.10, 0.0, 0.80, 0.10], 'CRISE': [0.0, 0.0, 0.70, 0.30]},
    'CLARA_NORMAL': {'CALMO': [0.90, 0.08, 0.02, 0.0], 'ATIVO': [0.90, 0.10, 0.0, 0.0], 'TENSO': [0.50, 0.0, 0.50, 0.0], 'CRISE': [0.50, 0.0, 0.50, 0.0]},
    'DIOGO_MODERADO': {'CALMO': [0.85, 0.05, 0.10, 0.0], 'ATIVO': [0.80, 0.05, 0.15, 0.0], 'TENSO': [0.30, 0.0, 0.65, 0.05], 'CRISE': [0.10, 0.0, 0.80, 0.10]}
}

def gerar_dados(estado):
    c = ESTADOS[estado]
    bpm = np.random.randint(c['bpm_range'][0], c['bpm_range'][1])
    gsr = np.random.uniform(c['gsr_range'][0], c['gsr_range'][1])
    mov = np.random.uniform(c['movement_range'][0], c['movement_range'][1])
    
    # Ruído 15%
    bpm += np.random.normal(0, bpm * RUIDO_SENSOR)
    gsr += np.random.normal(0, gsr * RUIDO_SENSOR)
    mov += np.random.normal(0, mov * RUIDO_SENSOR)
    
    return {'bpm': bpm, 'gsr': gsr, 'movement_score': mov}

def proximo_estado(atual, persona):
    return random.choices(['CALMO', 'ATIVO', 'TENSO', 'CRISE'], weights=PERSONAS[persona][atual], k=1)[0]

# ============================================================
# 3. EXECUCAO COM INTERVALO DINAMICO (Smart Battery)
# ============================================================

def run_load_test():
    client = mqtt.Client(client_id="smart-band-simulator")
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_PORT, 60)
        print("OK: Conectado! Iniciando simulacao de bateria inteligente...")
    except Exception as e:
        print(f"ERRO: {e}")
        return

    # Define a data inicial (60 dias atrás)
    data_inicio = datetime.now(TZ_SAO_PAULO) - timedelta(days=DIAS_DE_HISTORICO)
    
    # Estados e Relógios Individuais para cada aluno
    # Cada aluno tem o seu próprio "tempo atual" que avança conforme o estado dele
    alunos_simulacao = {}
    for d in DISPOSITIVOS_ALUNOS:
        alunos_simulacao[d['nome']] = {
            "estado": 'CALMO', 
            "ultimo_timestamp": data_inicio
        }
    
    start_real_time = time.time()
    
    print(f"Data Simulada de Inicio: {data_inicio.strftime('%d/%m/%Y')}")

    for i in range(TOTAL_REGISTROS):
        # Round Robin (seleciona um aluno por vez)
        aluno_config = DISPOSITIVOS_ALUNOS[i % 4]
        nome = aluno_config['nome']
        sim_data = alunos_simulacao[nome] # Pega os dados de simulação desse aluno
        
        estado_atual = sim_data["estado"]
        
        # 1. Gera dados baseados no estado atual
        dados = gerar_dados(estado_atual)
        
        # 2. DEFINE O INTERVALO (A Lógica de Economia de Bateria)
        if estado_atual == 'CALMO':
            intervalo = 60 # Tudo bem? Dorme 60s
        else:
            intervalo = 30 # Ativo, Tenso ou Crise? Monitora a cada 30s!
            
        # 3. Avança o relógio DO ALUNO
        novo_ts = sim_data["ultimo_timestamp"] + timedelta(seconds=intervalo)
        # Adiciona milissegundos aleatórios para realismo
        novo_ts_final = novo_ts + timedelta(milliseconds=random.randint(0, 500))
        
        # Atualiza para a próxima volta
        sim_data["ultimo_timestamp"] = novo_ts
        
        payload = {
            "dispositivo_id": aluno_config['dispositivo_id'],
            "dados_biometricos": dados,
            "timestamp_sao_paulo": novo_ts_final.isoformat()
        }
        
        client.publish(MQTT_TOPIC, json.dumps(payload))
        
        # Evolui estado
        sim_data["estado"] = proximo_estado(estado_atual, aluno_config['persona'])
        
        if (i + 1) % 5000 == 0:
            print(f"Progresso: {i+1}/{TOTAL_REGISTROS} | {nome} em {novo_ts_final.strftime('%d/%m %H:%M')} ({estado_atual}: {intervalo}s)")

    print(f"\nSimulacao Concluida!")
    print(f"Total Enviado: {TOTAL_REGISTROS}")
    # Mostra onde cada aluno parou no tempo
    for nome, dados in alunos_simulacao.items():
        print(f"   - {nome} parou em: {dados['ultimo_timestamp'].strftime('%d/%m/%Y %H:%M')}")
        
    client.disconnect()

if __name__ == "__main__":
    run_load_test()