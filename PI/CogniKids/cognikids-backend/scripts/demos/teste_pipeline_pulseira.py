"""
=============================================================================
TESTE COMPLETO DO PIPELINE DA PULSEIRA REAL
=============================================================================
Este script simula o payload EXATO da pulseira M5Stack e testa todo o caminho:

    Pulseira → MQTT → Bridge → Redis → Consumer → MongoDB

Etapas testadas:
1. Conexão com MQTT (Mosquitto)
2. Publicação do payload real da pulseira
3. Verificação no Redis (fila iot_queue)
4. Verificação no MongoDB (collections iot_raw_data e alerts)
=============================================================================
"""

import paho.mqtt.client as mqtt
import json
import time
import redis
from pymongo import MongoClient
from datetime import datetime
import pytz

# ============= CONFIGURAÇÕES =============
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "cognikids/iot/data"  # Tópico correto que o bridge escuta

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_QUEUE = "iot_queue"

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "cognikids"

# IDs reais do sistema
DEVICE_ID = "68fed345506b170be8ff6a22"  # ID da pulseira real

# ============= CORES PARA TERMINAL =============
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_step(num, text):
    print(f"{Colors.BLUE}[PASSO {num}]{Colors.END} {text}")

def print_success(text):
    print(f"  {Colors.GREEN}[OK] {text}{Colors.END}")

def print_error(text):
    print(f"  {Colors.RED}[ERRO] {text}{Colors.END}")

def print_warning(text):
    print(f"  {Colors.YELLOW}[AVISO] {text}{Colors.END}")

def print_info(text):
    print(f"  {Colors.CYAN}[INFO] {text}{Colors.END}")

# ============= PAYLOAD DA PULSEIRA REAL =============
def criar_payload_pulseira(bpm=120, mov=85, batt=100):
    """
    Cria o payload EXATO que a pulseira M5Stack real envia.
    
    Formato real da pulseira (abreviado para economizar bateria):
    - id: ID do dispositivo
    - bpm: Batimentos por minuto
    - mov: Movimento/aceleração
    - ts: Timestamp Unix
    - batt: Nível de bateria (%)
    """
    return {
        "id": DEVICE_ID,      # Formato abreviado (não device_id)
        "bpm": bpm,
        "mov": mov,           # Formato abreviado (não movement)
        "ts": int(time.time()),  # Formato abreviado (não timestamp)
        "batt": batt
    }

# ============= TESTE 1: MQTT =============
def testar_mqtt(payload):
    """Testa conexão e publicação no MQTT"""
    print_step(1, "Testando conexão MQTT (Mosquitto)...")
    
    resultado = {"sucesso": False, "mensagem": ""}
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            resultado["conectou"] = True
        else:
            resultado["erro_conexao"] = rc
    
    def on_publish(client, userdata, mid):
        resultado["publicou"] = True
    
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_publish = on_publish
        
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        time.sleep(1)  # Aguarda conexão
        
        if resultado.get("conectou"):
            print_success(f"Conectado ao broker MQTT em {MQTT_BROKER}:{MQTT_PORT}")
            
            # Publica o payload
            info = client.publish(MQTT_TOPIC, json.dumps(payload))
            info.wait_for_publish()
            
            if resultado.get("publicou"):
                print_success(f"Payload publicado no tópico: {MQTT_TOPIC}")
                print_info(f"Payload: {json.dumps(payload, indent=2)}")
                resultado["sucesso"] = True
            else:
                print_error("Falha ao publicar no MQTT")
        else:
            print_error(f"Falha na conexão MQTT (código: {resultado.get('erro_conexao', 'desconhecido')})")
        
        client.loop_stop()
        client.disconnect()
        
    except Exception as e:
        print_error(f"Erro MQTT: {str(e)}")
        resultado["mensagem"] = str(e)
    
    return resultado["sucesso"]

# ============= TESTE 2: REDIS =============
def testar_redis():
    """Verifica se o dado chegou na fila Redis"""
    print_step(2, "Verificando fila Redis...")
    
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        
        # Testa conexão
        if r.ping():
            print_success(f"Conectado ao Redis em {REDIS_HOST}:{REDIS_PORT}")
        
        # Verifica tamanho da fila
        queue_size = r.llen(REDIS_QUEUE)
        print_info(f"Tamanho atual da fila '{REDIS_QUEUE}': {queue_size} itens")
        
        # Aguarda o bridge processar (máximo 5 segundos)
        print_info("Aguardando bridge processar (até 5s)...")
        
        for i in range(10):
            time.sleep(0.5)
            new_size = r.llen(REDIS_QUEUE)
            if new_size > queue_size:
                print_success(f"Novo item detectado na fila! (tamanho: {new_size})")
                
                # Peek no último item (sem remover)
                ultimo_item = r.lindex(REDIS_QUEUE, -1)
                if ultimo_item:
                    dados = json.loads(ultimo_item)
                    print_info("Último item na fila:")
                    print(f"       {json.dumps(dados, indent=2, ensure_ascii=False)}")
                
                return True
        
        print_warning("Nenhum novo item na fila após 5s")
        print_info("Isso pode significar:")
        print_info("  - O bridge precisa ser reiniciado para pegar as mudanças")
        print_info("  - O bridge está processando muito rápido")
        return False
        
    except Exception as e:
        print_error(f"Erro Redis: {str(e)}")
        return False

# ============= TESTE 3: MONGODB =============
def testar_mongodb(timestamp_inicio):
    """Verifica se os dados chegaram no MongoDB"""
    print_step(3, "Verificando MongoDB...")
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        # Testa conexão
        client.admin.command('ping')
        print_success(f"Conectado ao MongoDB em {MONGO_URI}")
        
        # Aguarda consumer processar (máximo 10 segundos)
        print_info("Aguardando consumer processar (até 10s)...")
        
        encontrou_raw = False
        encontrou_alert = False
        
        for i in range(20):
            time.sleep(0.5)
            
            # Verifica iot_raw_data
            raw_data = db.iot_raw_data.find_one(
                {"dispositivo_id": DEVICE_ID},
                sort=[("_id", -1)]
            )
            
            if raw_data and raw_data.get("timestamp_original_unix", 0) >= timestamp_inicio:
                if not encontrou_raw:
                    print_success("Dados encontrados em 'iot_raw_data'!")
                    print_info(f"ID: {raw_data.get('_id')}")
                    print_info(f"Dispositivo: {raw_data.get('dispositivo_id')}")
                    print_info(f"BPM: {raw_data.get('dados_biometricos', {}).get('bpm')}")
                    print_info(f"Movement Score: {raw_data.get('dados_biometricos', {}).get('movement_score')}")
                    print_info(f"Timestamp SP: {raw_data.get('timestamp_pulseira_sp')}")
                    encontrou_raw = True
            
            # Verifica alerts
            alert = db.alerts.find_one(
                {"dispositivo_id": DEVICE_ID},
                sort=[("_id", -1)]
            )
            
            if alert:
                # Verifica se é recente (criado após início do teste)
                created = alert.get("created_at")
                if created and created.timestamp() >= timestamp_inicio:
                    if not encontrou_alert:
                        print_success("Alerta gerado em 'alerts'!")
                        print_info(f"Tipo: {alert.get('tipo_alerta')}")
                        print_info(f"Severidade: {alert.get('severidade')}")
                        print_info(f"Descrição: {alert.get('descricao')}")
                        encontrou_alert = True
            
            if encontrou_raw:
                break
        
        client.close()
        
        if not encontrou_raw:
            print_warning("Dados não encontrados em iot_raw_data")
            print_info("O consumer pode precisar ser reiniciado para pegar as mudanças")
        
        if not encontrou_alert:
            print_info("Nenhum alerta gerado (BPM pode estar na faixa normal)")
        
        return encontrou_raw
        
    except Exception as e:
        print_error(f"Erro MongoDB: {str(e)}")
        return False

# ============= TESTE COMPLETO =============
def executar_teste_completo():
    """Executa todos os testes em sequência"""
    print_header("TESTE DO PIPELINE DA PULSEIRA REAL")
    
    print(f"{Colors.BOLD}Configurações:{Colors.END}")
    print(f"  • MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"  • Redis: {REDIS_HOST}:{REDIS_PORT}")
    print(f"  • MongoDB: {MONGO_URI}{MONGO_DB}")
    print(f"  • Device ID: {DEVICE_ID}")
    print()
    
    # Marca timestamp de início
    timestamp_inicio = time.time()
    
    # Cria payload de crise (BPM alto para gerar alerta)
    print_info("Criando payload de CRISE (BPM=140) para testar geração de alerta...")
    payload = criar_payload_pulseira(bpm=140, mov=95, batt=85)
    
    # Teste 1: MQTT
    mqtt_ok = testar_mqtt(payload)
    
    if mqtt_ok:
        # Teste 2: Redis
        redis_ok = testar_redis()
        
        # Teste 3: MongoDB (sempre tenta, mesmo que Redis não detecte)
        mongo_ok = testar_mongodb(timestamp_inicio)
    else:
        print_warning("Pulando testes de Redis e MongoDB (MQTT falhou)")
        redis_ok = False
        mongo_ok = False
    
    # Resumo
    print_header("RESUMO DO TESTE")
    
    print(f"  MQTT (Mosquitto):  {'[OK]' if mqtt_ok else '[FALHOU]'}")
    print(f"  Redis (Fila):      {'[OK]' if redis_ok else '[NAO DETECTADO]'}")
    print(f"  MongoDB (Storage): {'[OK]' if mongo_ok else '[NAO ENCONTRADO]'}")
    
    print()
    
    if mqtt_ok and mongo_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}PIPELINE FUNCIONANDO CORRETAMENTE!{Colors.END}")
    elif mqtt_ok and not mongo_ok:
        print(f"{Colors.YELLOW}{Colors.BOLD}MQTT OK, mas dados nao chegaram ao MongoDB{Colors.END}")
        print()
        print("Possíveis causas:")
        print("  1. O container 'bridge' precisa ser reiniciado para carregar as mudanças")
        print("  2. O container 'consumer' precisa ser reiniciado")
        print()
        print("Execute:")
        print(f"  {Colors.CYAN}docker-compose restart bridge consumer{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}PIPELINE COM PROBLEMAS{Colors.END}")
        print("Verifique se todos os containers estão rodando")
    
    print()

# ============= MAIN =============
if __name__ == "__main__":
    executar_teste_completo()
