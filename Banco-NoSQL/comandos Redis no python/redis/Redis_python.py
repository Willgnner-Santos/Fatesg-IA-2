import redis      # Biblioteca para se conectar e interagir com o Redis
import time       # Biblioteca para medir o tempo de execução
import base64     # Biblioteca para codificar e decodificar dados em Base64

# Conexão com o Redis local
# decode_responses=True converte os valores retornados de bytes para strings automaticamente
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# =============================
# TESTE DE ALTO DESEMPENHO
# =============================
print("=== Testando Alto Desempenho ===")
start_time = time.time()

redis_client.set("chave_teste", "valor_teste")
retrieved_value = redis_client.get("chave_teste")

end_time = time.time()
print(f"Valor armazenado: {retrieved_value}")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n")

# =============================
# TESTE DE ESCALABILIDADE
# =============================
print("=== Testando Escalabilidade ===")
for i in range(1000):  # reduzi para 1000 para não sobrecarregar seu Redis local
    redis_client.set(f"chave_{i}", f"valor_{i}")

print(f"Exemplo de valor armazenado: {redis_client.get('chave_500')}\n")

# =============================
# TESTE DE FLEXIBILIDADE
# =============================
print("=== Testando Flexibilidade ===")

# String
redis_client.set("string_exemplo", "Hello Redis!")
print(f"String armazenada: {redis_client.get('string_exemplo')}")

# Lista
redis_client.delete("lista_exemplo")  # limpa se já existir
redis_client.rpush("lista_exemplo", "item1", "item2", "item3")
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}")

# Hash
redis_client.hset("hash_exemplo", "campo1", "valor1")
redis_client.hset("hash_exemplo", "campo2", "valor2")
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}")

# Binário (exemplo com base64)
image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")
redis_client.set("imagem_binario", image_data)
print(f"Imagem (binário armazenado): {redis_client.get('imagem_binario')[:20]}... [Cortado]\n")

# =============================
# TESTE DE BAIXA LATÊNCIA (CACHE)
# =============================
print("=== Testando Baixa Latência ===")
redis_client.set("configuracao_cache", "config_inicial")

for _ in range(5):
    start_time = time.time()
    cache_value = redis_client.get("configuracao_cache")
    end_time = time.time()
    print(f"Cache acessado: {cache_value} | Tempo de execução: {end_time - start_time:.6f} segundos")

# =============================
# FINAL
# =============================
print("\nTeste concluído com sucesso!")
