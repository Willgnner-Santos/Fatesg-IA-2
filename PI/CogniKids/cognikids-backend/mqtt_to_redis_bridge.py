import paho.mqtt.client as mqtt
import redis
import json
import time
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import pytz  # Para conversão de timezone

print("Iniciando a Ponte MQTT-Redis-Bridge...")

# Configuracao de timezone para Sao Paulo
TZ_SAO_PAULO = pytz.timezone('America/Sao_Paulo')

# Conexao com o MongoDB (servico 'db' do Docker)
try:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://db:27017/cognikidsDB')
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_default_database()
    db.command('ping')
    print(f"[OK] Ponte: Conectado ao MongoDB (Servico: {MONGO_URI})")
except Exception as e:
    print(f"[ERRO] Ponte: Falha ao conectar ao MongoDB: {e}")
    exit(1)

# Conexao com o Redis (servico 'redis' do Docker)
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("[OK] Ponte: Conectado ao Redis (Servico: 'redis')")
except Exception as e:
    print(f"[ERRO] Ponte: Falha ao conectar ao Redis: {e}")
    exit(1)

# --- Lógica do MQTT ---
MQTT_BROKER_HOST = "mosquitto" # Nome do serviço no docker-compose
MQTT_TOPIC = "cognikids/iot/data"

def transformar_payload_pulseira(data):
    """
    Transforma o payload da pulseira M5Stack para o formato padrao do sistema.
    
    Aceita dois formatos de entrada:
    
    Formato 1 - Abreviado (pulseira M5Stack):
        - id: Identificador do dispositivo
        - bpm: Batimentos por minuto
        - mov: Score de movimento
        - ts: Timestamp Unix
        - batt: Nivel de bateria
    
    Formato 2 - Completo:
        - device_id: Identificador do dispositivo
        - bpm: Batimentos por minuto
        - movement: Score de movimento
        - raw_sensor: Dado bruto do sensor
        - timestamp: Timestamp Unix
    
    Args:
        data (dict): Payload recebido da pulseira.
    
    Returns:
        dict: Payload padronizado para o sistema CogniKids.
    """
    # Aceita ambos os formatos: 'id' ou 'device_id'
    device_id = data.get('id') or data.get('device_id')
    
    # Aceita ambos os formatos: 'ts' ou 'timestamp'
    timestamp_unix = data.get('ts') or data.get('timestamp') or time.time()
    
    # Aceita ambos os formatos: 'mov' ou 'movement'
    movement = data.get('mov') or data.get('movement', 0)
    
    # Converte timestamp Unix para DateTime no fuso de São Paulo
    dt_utc = datetime.datetime.utcfromtimestamp(timestamp_unix)
    dt_sp = pytz.utc.localize(dt_utc).astimezone(TZ_SAO_PAULO)
    
    # Monta o payload no formato esperado pelo sistema
    return {
        'dispositivo_id': device_id,
        'dados_biometricos': {
            'bpm': data.get('bpm', 0),
            'gsr': 0,  # Sensor GSR nao implementado - valor padrao
            'movement_score': movement,
            'raw_ppg': data.get('raw_sensor', 0)  # Dado bruto do sensor PPG
        },
        'timestamp_pulseira_sp': dt_sp.isoformat(),
        'timestamp_original_unix': timestamp_unix,
        'bateria': data.get('batt', 100)
    }

def on_connect(client, userdata, flags, rc):
    """
    Callback executado apos conexao com o Broker MQTT.
    
    Args:
        client: Instancia do cliente MQTT.
        userdata: Dados do usuario definidos no cliente.
        flags: Flags de resposta do broker.
        rc: Codigo de resultado da conexao.
    """
    if rc == 0:
        print(f"[OK] Ponte: Conectado ao MQTT Broker '{MQTT_BROKER_HOST}'")
        client.subscribe(MQTT_TOPIC)
        print(f"     Inscrito no topico '{MQTT_TOPIC}'")
    else:
        print(f"[ERRO] Ponte: Falha ao conectar ao MQTT Broker, codigo: {rc}")

def on_message(client, userdata, msg):
    """
    Callback executado ao receber uma mensagem MQTT.
    
    Processa dados biometricos recebidos da pulseira ou simulador,
    valida o dispositivo e enfileira no Redis para processamento.
    
    Args:
        client: Instancia do cliente MQTT.
        userdata: Dados do usuario definidos no cliente.
        msg: Mensagem recebida contendo topico e payload.
    """
    try:
        payload_str = msg.payload.decode('utf-8')
        print(f"\nRecebido de MQTT: {payload_str}")
        
        data = json.loads(payload_str)
        
        # Detecta e transforma payload da pulseira M5Stack para formato padrao
        is_pulseira_real = ('id' in data or 'device_id' in data) and 'bpm' in data
        if is_pulseira_real:
            print("     Payload de pulseira M5Stack detectado. Transformando...")
            data = transformar_payload_pulseira(data)
            print(f"     Payload transformado: {json.dumps(data, default=str)}")
        
        # Validacao do ID do dispositivo
        dispositivo_id = data.get('dispositivo_id')
        if not dispositivo_id or not ObjectId.is_valid(dispositivo_id):
            print(f"     REJEITADO: ID de dispositivo invalido ({dispositivo_id})")
            return

        # Verifica existencia do dispositivo e obtem o ID do aluno associado
        dispositivo = db.dispositivos.find_one({"_id": ObjectId(dispositivo_id)})
        
        if not dispositivo:
            print(f"     REJEITADO: Dispositivo {dispositivo_id} nao registrado")
            return
            
        aluno_id = dispositivo.get('aluno_id')
        if not aluno_id:
            print(f"     REJEITADO: Dispositivo {dispositivo_id} nao associado a um aluno")
            return

        # Enriquece o payload com dados complementares
        data['aluno_id'] = str(aluno_id)
        data['dispositivo_id'] = str(dispositivo_id)
        data['timestamp_bridge_utc'] = datetime.datetime.utcnow().isoformat()
        
        # Enfileira no Redis para processamento assincrono
        redis_client.lpush('iot_queue', json.dumps(data))
        print(f"     VALIDADO: Aluno {aluno_id}. Dados enfileirados no Redis.")

    except json.JSONDecodeError:
        print("     REJEITADO: Payload MQTT nao e um JSON valido")
    except Exception as e:
        print(f"     ERRO na Ponte (on_message): {e}")

# Loop Principal da Ponte MQTT-Redis
def iniciar_ponte():
    """
    Inicializa e executa o loop principal da ponte MQTT-Redis.
    
    Estabelece conexao com o broker MQTT e aguarda mensagens
    de forma bloqueante.
    """
    mqtt_client = mqtt.Client(client_id="cognikids-bridge")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    # Aguarda disponibilidade do broker MQTT
    connected = False
    while not connected:
        try:
            mqtt_client.connect(MQTT_BROKER_HOST, 1883, 60)
            connected = True
        except Exception as e:
            print(f"Aguardando MQTT Broker '{MQTT_BROKER_HOST}'... (Erro: {e})")
            time.sleep(5)
            
    # Bloqueia o script, ouvindo para sempre
    mqtt_client.loop_forever()

if __name__ == "__main__":
    iniciar_ponte()