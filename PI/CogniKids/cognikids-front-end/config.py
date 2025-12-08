"""
Arquivo de configuração do CogniKids Frontend
"""

# Configurações da API Backend
API_CONFIG = {
    "BASE_URL": "http://localhost:5001/api",
    "TIMEOUT": 10,  # segundos
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY": 1,  # segundos
}

# Configurações do aplicativo
APP_CONFIG = {
    "TITLE": "CogniKids - Aprendendo com Diversao",
    "ICON": "C",
    "LAYOUT": "wide",
    "LOGO_PATH": "assets/images/logo CogniKids.png",
    "THEME": {
        "primaryColor": "#8B5CF6",
        "backgroundColor": "#F9FAFB",
        "secondaryBackgroundColor": "#FFFFFF",
        "textColor": "#1F2937",
    }
}

# Configurações de cores
COLORS = {
    "roxo": "#8B5CF6",
    "rosa": "#EC4899",
    "amarelo": "#FACC15",
    "azul": "#3B82F6",
    "verde": "#10B981",
    "vermelho": "#EF4444",
    "laranja": "#F59E0B",
    "cinza": "#6B7280",
}

# Temas disponíveis para atividades
TEMAS_ATIVIDADES = [
    "Matemática",
    "Português",
    "Lógica",
    "Memória",
    "Ciências"
]

# Avatares por tipo de usuário
AVATARS = {
    "aluno": "👧👦",
    "professor": "👨‍🏫👩‍🏫",
    "pai": "👨👩",
    "responsavel": "👨👩"
}

# Configurações de performance
PERFORMANCE = {
    "CACHE_TTL": 300,  # 5 minutos
    "MAX_RETRIES": 3,
    "REQUEST_TIMEOUT": 10
}

# Modo de desenvolvimento
DEBUG = True

# Fallback local
USE_LOCAL_FALLBACK = True
LOCAL_DATA_DIR = "data"


