import os
from pymemcache.client import base

MEMCACHED_HOST = os.getenv('MEMCACHED_HOST', 'memcached')
MEMCACHED_PORT = int(os.getenv('MEMCACHED_PORT', 11211))

try:
    client = base.Client((MEMCACHED_HOST, MEMCACHED_PORT))
    
    
    client.set('mensagem', 'Olá, Memcached!'.encode('utf-8'))
    
    valor = client.get('mensagem')
    print("Valor em cache:", valor.decode('utf-8'))

except Exception as e:
    print("Erro na conexão:", e)