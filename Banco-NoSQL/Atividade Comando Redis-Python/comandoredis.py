import redis  # Biblioteca para se conectar e interagir com o Redis
import time   # Biblioteca para medir o tempo de execução
import base64  # Biblioteca para codificar e decodificar dados em Base64

# Conexão com o Redis
# Aqui conectamos ao servidor Redis que está rodando localmente na máquina (localhost)
# 'decode_responses=True' converte os valores retornados pelo Redis de binários (bytes) para strings automaticamente.
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# ALTO DESEMPENHO
# Testando o Redis para armazenar e recuperar dados rapidamente.
print("=== Testando Alto Desempenho ===")
start_time = time.time()  # Marca o tempo inicial para medir a execução

# Armazena um valor no Redis usando a chave "chave_teste" e o valor "valor_teste"
redis_client.set("chave_teste", "valor_teste")

# Recupera o valor armazenado usando a chave "chave_teste"
retrieved_value = redis_client.get("chave_teste")

end_time = time.time()  # Marca o tempo final
print(f"Valor armazenado: {retrieved_value}")  # Mostra o valor recuperado

# Calcula o tempo gasto entre armazenar e recuperar o dado
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n")

# ESCALABILIDADE
# Simula o armazenamento de muitos dados para mostrar como o Redis lida com alta carga.
print("=== Testando Escalabilidade ===")
for i in range(1000000):  # Um loop que executa 1 milhão de vezes
    # Armazena valores no formato chave/valor (exemplo: chave_0 → valor_0, chave_1 → valor_1)
    redis_client.set(f"chave_{i}", f"valor_{i}")

# Recupera o valor de uma das 1 milhão de chaves armazenadas, neste caso, "chave_500"
print(f"Exemplo de valor armazenado: {redis_client.get('chave_500')}\n")

# FLEXIBILIDADE
# Mostra como o Redis pode armazenar diferentes tipos de dados.
print("=== Testando Flexibilidade ===")

# Armazenando uma string
# Usa o comando SET para armazenar um texto simples ("Hello Redis!") com a chave "string_exemplo"
redis_client.set("string_exemplo", "Hello Redis!")

# Recupera o valor armazenado e imprime
print(f"String armazenada: {redis_client.get('string_exemplo')}")

# Armazenando uma lista
# Adiciona itens à lista chamada "lista_exemplo" usando o comando RPUSH (adiciona ao final da lista)
redis_client.rpush("lista_exemplo", "item1", "item2", "item3")

# Recupera todos os itens da lista usando LRANGE (0 significa início, -1 significa final)
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}")

# Armazenando um hash (estrutura semelhante a um dicionário ou JSON)
# Adiciona pares de chave/valor em um hash chamado "hash_exemplo"
redis_client.hset("hash_exemplo", "campo1", "valor1")  # Campo 1
redis_client.hset("hash_exemplo", "campo2", "valor2")  # Campo 2

# Recupera todos os pares de chave/valor do hash usando HGETALL
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}")

# Armazenando dados binários (exemplo: um arquivo ou imagem)
# Simula o armazenamento de um arquivo codificado em Base64
# Base64 é uma forma de converter dados binários (como uma imagem) em texto para facilitar o armazenamento
image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")  # Codifica o dado

# Armazena o dado codificado no Redis com a chave "imagem_binario"
redis_client.set("imagem_binario", image_data)

# Recupera e exibe parte do dado armazenado (os 20 primeiros caracteres) para demonstração
print(f"Imagem (binário armazenado): {redis_client.get('imagem_binario')[:20]}... [Cortado]\n")

# BAIXA LATÊNCIA
# Demonstra o uso do Redis como cache, onde dados podem ser acessados rapidamente várias vezes.
print("=== Testando Baixa Latência ===")

# Armazena um valor que será usado como "cache"
redis_client.set("configuracao_cache", "config_inicial")

for _ in range(5):  # Simula 5 acessos rápidos ao mesmo dado
    start_time = time.time()  # Marca o tempo antes de acessar o dado
    cache_value = redis_client.get("configuracao_cache")  # Recupera o valor do cache
    end_time = time.time()  # Marca o tempo após acessar o dado

    # Exibe o valor recuperado e o tempo de acesso
    print(f"Cache acessado: {cache_value} | Tempo de execução: {end_time - start_time:.6f} segundos")

# Mensagem final
print("\nTeste concluído com sucesso!")
