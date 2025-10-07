# Código para: app/main.py

import time
import requests
from flask import Flask, render_template
from memcache import Client

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configura e conecta ao servidor Memcached.
# Certifique-se de que o serviço Memcached esteja rodando em '127.0.0.1:11211'
memcached_client = Client(['127.0.0.1:11211'], debug=0)

# URL da API externa que vamos consultar
API_URL = "https://jsonplaceholder.typicode.com/users"

@app.route('/')
def get_users():
    """
    Busca dados de usuários, utilizando Memcached como cache.
    """
    start_time = time.time()
    cache_key = 'all_users' # Chave única para identificar esses dados no cache
    
    # 1. Tenta obter os dados do cache primeiro
    users_data = memcached_client.get(cache_key)
    
    source = None
    
    if users_data is None:
        # 2. CACHE MISS: Se os dados não estão no cache
        source = 'API Externa'
        print("CACHE MISS: Buscando dados da API...")
        
        try:
            # Faz a requisição para a API externa
            response = requests.get(API_URL)
            response.raise_for_status() # Lança um erro para respostas HTTP ruins (4xx ou 5xx)
            users_data = response.json()
            
            # 3. Armazena os dados obtidos no cache para futuras requisições
            # O 'time=30' define que o cache expirará em 30 segundos
            memcached_client.set(cache_key, users_data, time=30)
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            users_data = [] # Retorna lista vazia em caso de erro

    else:
        # 4. CACHE HIT: Se os dados foram encontrados no cache
        source = 'Memcached'
        print("CACHE HIT: Servindo dados do cache.")

    # Calcula o tempo total da operação
    duration = time.time() - start_time
    
    # Renderiza o template HTML, passando os dados para a página
    return render_template('index.html', users=users_data, source=source, duration=duration)