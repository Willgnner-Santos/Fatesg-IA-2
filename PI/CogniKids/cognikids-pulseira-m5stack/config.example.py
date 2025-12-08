# --- Configurações de Rede e Endpoints da API ---
# COPIE ESTE ARQUIVO PARA config.py E PREENCHA COM SUAS CREDENCIAIS
# NÃO COMMITE O config.py NO GIT!

WIFI_NETWORKS = [
    {
        "ssid": "SUA_REDE_WIFI",
        "password": "SUA_SENHA_WIFI",
        "api_endpoint": "http://SEU_IP:5001/api/iot/data"
    },
    # Adicione mais redes se necessário
    # {
    #     "ssid": "OUTRA_REDE",
    #     "password": "OUTRA_SENHA",
    #     "api_endpoint": "http://OUTRO_IP:5001/api/iot/data"
    # },
]

# --- Identificação do Dispositivo ---
# Obtenha o DEVICE_ID do MongoDB após registrar o dispositivo
DEVICE_ID = "SEU_DEVICE_ID_DO_MONGODB"

# API Key para autenticação (definida no backend .env)
API_KEY = "SUA_API_KEY"

# --- Intervalos (em segundos) ---
READ_INTERVAL_SECONDS = 5    # Intervalo de leitura dos sensores
SEND_INTERVAL_SECONDS = 30   # Intervalo de envio para a API
