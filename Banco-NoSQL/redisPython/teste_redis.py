import redis   # Biblioteca para se conectar e interagir com o Redis
import time    # Biblioteca para medir o tempo de execução
import base64  # Biblioteca para codificar e decodificar dados em Base64

# --- Conexão com o Redis ---
# Conecta ao servidor Redis rodando localmente (localhost)[cite: 5].
# 'decode_responses=True' converte as respostas de bytes para strings[cite: 6].
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# --- ALTO DESEMPENHO ---
# Testa a rapidez do Redis para armazenar e recuperar dados[cite: 9].
print("=== Testando Alto Desempenho ===")
start_time = time.time()  # Marca o tempo inicial [cite: 11]
redis_client.set("chave_teste", "valor_teste")  # Armazena um valor [cite: 13]
retrieved_value = redis_client.get("chave_teste")  # Recupera o valor [cite: 15]
end_time = time.time()  # Marca o tempo final [cite: 16]
print(f"Valor armazenado: {retrieved_value}")  # Mostra o valor recuperado [cite: 17]
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n") # Calcula o tempo gasto [cite: 19]

# --- ESCALABILIDADE ---
# Simula o armazenamento de muitos dados para testar a carga[cite: 21].
print("=== Testando Escalabilidade ===")
for i in range(100000):  # O documento sugere 1.000.000, mas 100.000 é mais rápido para um teste inicial.
    # Armazena múltiplos pares chave/valor [cite: 25]
    redis_client.set(f"chave_{i}", f"valor_{i}")
# Recupera um valor de exemplo para confirmar o armazenamento [cite: 27]
print(f"Exemplo de valor armazenado: {redis_client.get('chave_500')}\n")

# --- FLEXIBILIDADE ---
# Demonstra o armazenamento de diferentes tipos de dados[cite: 29].
print("=== Testando Flexibilidade ===")
# Armazenando uma string [cite: 31]
redis_client.set("string_exemplo", "Hello Redis!") # [cite: 33]
print(f"String armazenada: {redis_client.get('string_exemplo')}") # [cite: 35]

# Armazenando uma lista [cite: 36]
redis_client.rpush("lista_exemplo", "item1", "item2", "item3") # [cite: 38]
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}") # [cite: 40]

# Armazenando um hash (dicionário) [cite: 41]
redis_client.hset("hash_exemplo", "campo1", "valor1") # [cite: 43]
redis_client.hset("hash_exemplo", "campo2", "valor2") # [cite: 44]
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}") # [cite: 46]

# Armazenando dados binários (simulado com Base64) [cite: 47, 48]
# Base64 converte dados binários em texto para armazenamento[cite: 49].
image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8") # [cite: 50]
redis_client.set("imagem_binario", image_data) # [cite: 52]
print(f"Imagem (binário armazenado): {redis_client.get('imagem_binario')[:20]}... [Cortado]\n") # [cite: 54]

# --- BAIXA LATÊNCIA ---
# Demonstra o uso do Redis como um cache rápido[cite: 56].
print("=== Testando Baixa Latência ===")
redis_client.set("configuracao_cache", "config_inicial") # [cite: 59]
for _ in range(5):  # Simula 5 acessos rápidos ao mesmo dado [cite: 60]
    start_time = time.time() # [cite: 61]
    cache_value = redis_client.get("configuracao_cache") # [cite: 62]
    end_time = time.time() # [cite: 63]
    print(f"Cache acessado: {cache_value} | Tempo de execução: {end_time - start_time:.6f} segundos") # [cite: 65]

print("\nTeste concluído com sucesso!") # [cite: 67]
