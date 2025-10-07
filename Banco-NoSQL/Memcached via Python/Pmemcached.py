import json
import time
from pymemcache.client.base import Client


def conectar_memcached():
    try:
        client = Client(('localhost', 11211))
        client.set('teste', 'ok'.encode('utf-8'))
        client.delete('teste')
        print("Conectado ao Memcached")
        return client
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None


def operacoes_basicas(client):
    print("\nOPERAÇÕES BÁSICAS")
    
    client.set('nome', 'João Guilherme'.encode('utf-8'))
    client.set('idade', '19'.encode('utf-8'))
    
    nome = client.get('nome').decode('utf-8')
    idade = client.get('idade').decode('utf-8')
    print(f"Nome: {nome}, Idade: {idade}")
    
    usuario = {'id': 1, 'nome': 'João', 'email': 'joaoman11@email.com'}
    client.set('usuario:1', json.dumps(usuario).encode('utf-8'))
    
    usuario_recuperado = json.loads(client.get('usuario:1').decode('utf-8'))
    print(f"Usuário: {usuario_recuperado}")
    
    client.set('temporario', 'expira em 10s'.encode('utf-8'), expire=10)
    print("Dado temporário armazenado (expira em 10s)")


def exemplo_cache_performance(client):
    print("\nTESTE DE PERFORMANCE")
    
    def consulta_lenta(user_id):
        time.sleep(0.5)  # Simula latência
        return {'id': user_id, 'nome': f'Usuario_{user_id}'}
    
    def buscar_usuario(user_id, usar_cache=True):
        cache_key = f'user:{user_id}'
        
        if usar_cache:
            cached = client.get(cache_key)
            if cached:
                print("CACHE HIT - Dados encontrados no cache")
                return json.loads(cached.decode('utf-8'))
        
        print("CACHE MISS - Consultando fonte de dados")
        dados = consulta_lenta(user_id)
        
        if usar_cache:
            client.set(cache_key, json.dumps(dados).encode('utf-8'), expire=60)
        
        return dados
    
    user_id = 123
    
    inicio = time.time()
    buscar_usuario(user_id)
    tempo1 = time.time() - inicio
    
    inicio = time.time()
    buscar_usuario(user_id)
    tempo2 = time.time() - inicio
    
    print(f"Primeira consulta: {tempo1:.3f}s")
    print(f"Segunda consulta: {tempo2:.3f}s")
    print(f"Melhoria: {((tempo1-tempo2)/tempo1*100):.0f}% mais rápido")


def exemplo_sessoes(client):
    print("\nGERENCIAMENTO DE SESSÕES")
    
    session_id = 'sess_abc123'
    session_data = {
        'user_id': 456,
        'username': 'admin',
        'login_time': int(time.time())
    }
    
    client.set(f'session:{session_id}', json.dumps(session_data).encode('utf-8'), expire=1800)
    print(f"Sessão criada para: {session_data['username']}")
    
    session = client.get(f'session:{session_id}')
    if session:
        dados = json.loads(session.decode('utf-8'))
        print(f"Sessão ativa para: {dados['username']}")
    
    client.delete(f'session:{session_id}')
    print("Sessão removida")


def estatisticas(client):
    print("\nESTATÍSTICAS")
    
    try:
        stats = client.stats()
        
        def get_stat_value(key):
            value = stats.get(key.encode() if isinstance(key, str) else key)
            if isinstance(value, bytes):
                return value.decode('utf-8')
            return str(value) if value is not None else 'N/A'
        
        print(f"Versão: {get_stat_value('version')}")
        print(f"Itens armazenados: {get_stat_value('curr_items')}")
        print(f"Conexões ativas: {get_stat_value('curr_connections')}")
        
        hits_key = b'get_hits'
        misses_key = b'get_misses'
        
        if hits_key in stats and misses_key in stats:
            hits_value = stats[hits_key]
            misses_value = stats[misses_key]
            
            hits = int(hits_value.decode('utf-8') if isinstance(hits_value, bytes) else hits_value)
            misses = int(misses_value.decode('utf-8') if isinstance(misses_value, bytes) else misses_value)
            
            total = hits + misses
            if total > 0:
                hit_rate = (hits / total) * 100
                print(f"Taxa de acerto: {hit_rate:.1f}%")
                
    except Exception as e:
        print(f"Erro ao obter estatísticas: {e}")


def main():
    print("INTEGRAÇÃO MEMCACHED COM PYTHON")
    
    client = conectar_memcached()
    if not client:
        print("Falha na conexão. Verifique se o Memcached está rodando.")
        return
    
    try:
        operacoes_basicas(client)
        exemplo_cache_performance(client)
        exemplo_sessoes(client)
        estatisticas(client)
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()