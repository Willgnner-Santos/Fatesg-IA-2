import os, sys, time, gc
import M5
from M5 import Lcd, Widgets
from machine import ADC, Pin
import math
import network
import json
from umqtt.simple import MQTTClient


import config

# ==========================================
#  CALIBRAÇÃO DO SENSOR (CONFIRMADA)
# ==========================================
OFFSET = 110                 
RESET_DROP = 40              
BASELINE_ALPHA = 0.05        
SAMPLE_MS = 20               
MIN_BEAT_MS = 300            
MAX_BEAT_MS = 2500           


MQTT_TOPIC = "fatesg/cognikids/telemetry"

# Cores / pinos
COR_FUNDO     = 0x000033
COR_TEXTO     = 0xFFFFFF
PINO_SENSOR   = 33
PINO_POWER    = 32

# ==========================================
#  ESTADO GLOBAL
# ==========================================
state = {
    # Sensor
    "adc": None,
    "t_sample": 0,
    "t_screen": 0,
    "bpm": 0,
    "pulse": False,
    "last_beat_ms": 0,
    "baseline": None,
    "threshold": None,
    
    # Movimento
    "mov_score": 0.0,
    "prev_acc": (0.0, 0.0, 0.0),
    
    # Rede
    "wifi_connected": False,
    "mqtt_client": None,
    "t_send": 0,
    "msg_lock": 0  
}

# Widgets
lbl_bat = None
lbl_bpm_val = None
lbl_movi_val = None
lbl_gsr_val = None
lbl_status = None

# ==========================================
#  FUNÇÕES DE REDE (WIFI & MQTT)
# ==========================================
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Se já estava conectado, avisa qual é
    if wlan.isconnected():
        rede_atual = wlan.config('essid')
        print(f">> JÁ CONECTADO EM: {rede_atual}")
        lbl_status.setText(rede_atual[:10] + "..") 
        lbl_status.setColor(0x00FF00, COR_FUNDO)
        return True

    print(">> Escaneando redes...")
    lbl_status.setText("Buscando Wifi...")
    
    try:
        available = wlan.scan() 
        available_ssids = [x[0].decode('utf-8') for x in available]
    except:
        available_ssids = []
    
    for net in config.WIFI_NETWORKS:
        ssid = net["ssid"]
        pwd = net["password"]
        
        if ssid in available_ssids:
            print(f">> Tentando conectar: {ssid}")
            lbl_status.setText(f"Entrando: {ssid[:6]}..")
            
            try:
                wlan.connect(ssid, pwd)
                for _ in range(50):
                    if wlan.isconnected():
                       
                        rede_final = wlan.config('essid')
                        print(f">> SUCESSO! REDE: {rede_final}")
                        
                        
                        lbl_status.setText(rede_final[:12]) 
                        lbl_status.setColor(0x00FF00, COR_FUNDO)
                        
                        time.sleep(2) 
                        return True
                    time.sleep(0.1)
            except: pass
                
    print("!! Nenhuma rede conhecida.")
    lbl_status.setText("Sem Wifi")
    lbl_status.setColor(0xFF0000, COR_FUNDO)
    return False

def conectar_mqtt():
    if not state["wifi_connected"]: return False
    
    try:
        # Usa IP e ID do config
        client = MQTTClient(config.DEVICE_ID, config.MQTT_BROKER_IP, port=1883, keepalive=60)
        client.connect()
        state["mqtt_client"] = client
        print(">> MQTT Conectado!")
        return True
    except Exception as e:
        print(f"!! Erro MQTT: {e}")
        return False

def enviar_telemetria():
    # Só tenta se tiver wifi
    if not state["wifi_connected"]:
        state["wifi_connected"] = conectar_wifi()
        if not state["wifi_connected"]: return

    # Tenta conectar MQTT se não tiver cliente
    if state["mqtt_client"] is None:
        conectar_mqtt()
    
    if state["mqtt_client"]:
        try:
            # Monta JSON com dados reais
            payload = {
                "device_id": config.DEVICE_ID,
                "bpm": state["bpm"],
                "movement": round(state["mov_score"], 2),
                "raw_sensor": state.get("baseline", 0),
                "timestamp": time.time()
            }
            json_str = json.dumps(payload)
            
           
            state["mqtt_client"].publish(MQTT_TOPIC, json_str)
            print(f">> Enviado: {json_str}")
            
            
            lbl_status.setText("ENVIADO OK!")
            lbl_status.setColor(0x00FF00, COR_FUNDO) 
            state["msg_lock"] = time.ticks_ms() + 2000 
            
        except Exception as e:
            print(f"!! Falha envio: {e}")
            lbl_status.setText("ERRO ENVIO")
            lbl_status.setColor(0xFF0000, COR_FUNDO) 
            state["msg_lock"] = time.ticks_ms() + 2000
            state["mqtt_client"] = None 

# ==========================================
#  FUNÇÕES VISUAIS
# ==========================================
def desenhar_coracao(x, y, tamanho_escala=1, cor=0xFF0000):
    r = 6 * tamanho_escala
    x_offset = 12 * tamanho_escala
    try:
        Lcd.fillCircle(int(x + r), int(y + r), int(r), cor)
        Lcd.fillCircle(int(x + r + x_offset), int(y + r), int(r), cor)
        Lcd.fillTriangle(
            int(x), int(y + r + 2),
            int(x + 2 * r + x_offset), int(y + r + 2),
            int(x + r + (x_offset // 2)), int(y + r * 3.5),
            cor
        )
    except: pass

def atualizar_status_visual(estado):
    # Só atualiza se a mensagem de "ENVIADO" não estiver travando a tela
    if time.ticks_ms() < state["msg_lock"]:
        return 

    if lbl_status:
        if estado == 0:
            lbl_status.setText("Monitorando...")
            lbl_status.setColor(0xAAAAAA, COR_FUNDO)
        elif estado == 1:
            lbl_status.setText("DETECTADO!")
            lbl_status.setColor(0x00FF00, COR_FUNDO)

# ==========================================
# LÓGICA DO SENSOR (CALIBRADO OFFSET 110)
# ==========================================
def process_ppg(val, now):
    b = state.get("baseline")
    if b is None: state["baseline"] = val
    else: state["baseline"] = int(b * (1 - BASELINE_ALPHA) + val * BASELINE_ALPHA)

    state["threshold"] = state["baseline"] + OFFSET

    # Detecta Batida
    if (val > state["threshold"]) and (state["pulse"] is False):
        state["pulse"] = True

        delta = time.ticks_diff(now, state["last_beat_ms"])
        state["last_beat_ms"] = now

        if MIN_BEAT_MS < delta < MAX_BEAT_MS:
            inst_bpm = 60000 // delta
            if state["bpm"] == 0: state["bpm"] = inst_bpm
            else: state["bpm"] = int(state["bpm"] * 0.7 + inst_bpm * 0.3)

            if lbl_bpm_val:
                lbl_bpm_val.setText(str(state["bpm"]))
                lbl_bpm_val.setColor(COR_TEXTO, COR_FUNDO)
                
            desenhar_coracao(15, 120, tamanho_escala=1.4, cor=0xFF66FF)
            atualizar_status_visual(1)
            print(f"️ BPM: {state['bpm']}")

    # Reset
    if (val < (state["threshold"] - RESET_DROP)) and (state["pulse"] is True):
        state["pulse"] = False
        desenhar_coracao(15, 120, tamanho_escala=1.4, cor=0xFF0000)
        atualizar_status_visual(0)

def ler_imu():
    try:
        acc = M5.Imu.getAccel()
        delta = abs(acc[0]-state["prev_acc"][0]) + abs(acc[1]-state["prev_acc"][1]) + abs(acc[2]-state["prev_acc"][2])
        state["prev_acc"] = acc
        state["mov_score"] = (state["mov_score"] * 0.9) + (delta * 10 * 0.1)
    except: pass

# ==========================================
#  SETUP
# ==========================================
def setup():
    M5.begin()
    Lcd.setRotation(0)  
    Lcd.fillScreen(COR_FUNDO)

    print(f">> COGNIKIDS IOT - OFFSET {OFFSET}")

    # Força LED
    try:
        p_led = Pin(PINO_POWER, Pin.OUT)
        p_led.value(1)
    except: pass

    # ADC
    try:
        state["adc"] = ADC(Pin(PINO_SENSOR))
        state["adc"].atten(ADC.ATTN_11DB)
        print(">> Sensor OK")
    except: print("!! Erro Sensor")

    # Interface
    Widgets.Label("COGNIKIDS", 5, 2, 1.0, 0xFFFFFF, COR_FUNDO, Widgets.FONTS.DejaVu12)
    global lbl_bat, lbl_bpm_val, lbl_movi_val, lbl_gsr_val, lbl_status
    lbl_bat = Widgets.Label("100%", 95, 2, 1.0, 0xAAAAAA, COR_FUNDO, Widgets.FONTS.DejaVu12)
    Lcd.drawLine(0, 18, 135, 18, 0xFFFFFF)
    try: Widgets.Image("logo.png", 10, 25)
    except: Widgets.Label("LOGO", 50, 60, 1.0, 0x555555, COR_FUNDO, Widgets.FONTS.DejaVu12)
    desenhar_coracao(15, 120, tamanho_escala=1.4, cor=0xFF0000)
    Widgets.Label("BPM", 75, 122, 1.0, 0xAAAAAA, COR_FUNDO, Widgets.FONTS.DejaVu12)
    lbl_bpm_val = Widgets.Label("--", 75, 135, 1.0, 0xFFFFFF, COR_FUNDO, Widgets.FONTS.DejaVu24)
    Widgets.Label("MOVI:", 10, 170, 1.0, 0xAAAAAA, COR_FUNDO, Widgets.FONTS.DejaVu12)
    lbl_movi_val = Widgets.Label("0.0", 60, 170, 1.0, 0xFFFFFF, COR_FUNDO, Widgets.FONTS.DejaVu12)
    Widgets.Label("GSR:", 10, 190, 1.0, 0xAAAAAA, COR_FUNDO, Widgets.FONTS.DejaVu12)
    lbl_gsr_val = Widgets.Label("0.0", 60, 190, 1.0, 0xFFFFFF, COR_FUNDO, Widgets.FONTS.DejaVu12)
    Lcd.drawLine(5, 215, 130, 215, 0x444444)
    
    # Label Status
    lbl_status = Widgets.Label("Iniciando...", 45, 220, 1.0, 0xAAAAAA, COR_FUNDO, Widgets.FONTS.DejaVu12)

    # Conecta Wifi no boot
    state["wifi_connected"] = conectar_wifi()

    # Inicializa Timers
    now = time.ticks_ms()
    state["t_sample"] = now
    state["t_screen"] = now
    state["t_send"] = now
    state["last_beat_ms"] = now - 1000 

    # Baseline Inicial
    try: raw = state["adc"].read()
    except: raw = 0
    state["baseline"] = raw
    state["threshold"] = state["baseline"] + OFFSET

# ---------- LOOP ----------
def safe_adc_read():
    try: return int(state["adc"].read())
    except: return 0

def loop():
    M5.update()
    now = time.ticks_ms()

    # 1. Leitura Rápida (Sensor)
    if time.ticks_diff(now, state["t_sample"]) >= SAMPLE_MS:
        state["t_sample"] = now
        if state.get("adc"):
            process_ppg(safe_adc_read(), now)
        ler_imu()

    # 2. Atualização Lenta (Tela)
    if time.ticks_diff(now, state["t_screen"]) >= 500:
        state["t_screen"] = now
        if lbl_movi_val:
            lbl_movi_val.setText("{:.1f}".format(state["mov_score"]))
            lbl_movi_val.setColor(0xFFFFFF, COR_FUNDO)
        if state["bpm"] == 0 and not state["pulse"]:
            atualizar_status_visual(0)

    # 3. ENVIO MQTT (Usa intervalo do config.py)
    # config.SEND_INTERVAL_SECONDS * 1000 para converter para milissegundos
    if time.ticks_diff(now, state["t_send"]) >= (config.SEND_INTERVAL_SECONDS * 1000):
        state["t_send"] = now
        lbl_status.setText("ENVIANDO...")
        print(f">> ALVO DO MQTT: {config.MQTT_BROKER_IP}")
        lbl_status.setColor(0xFFFF00, COR_FUNDO) # Amarelo
        enviar_telemetria()

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except Exception as e:
        print(e)
