# Guia Completo: Do Básico de Redis à Execução com Python e Venv

Este guia reúne todos os passos para instalar, entender e executar comandos Redis, tanto via terminal (CLI) quanto com um script Python, utilizando as melhores práticas como o uso de ambientes virtuais (`venv`).

---

## Parte 1: Entendendo os Comandos Essenciais do Redis (via CLI)

Antes de automatizar com Python, é fundamental conhecer os comandos básicos.

### 1. Strings (Chave-Valor Simples)
- **Objetivo**: Armazenar e recuperar um valor simples, como um nome ou um contador.
- **Comandos**:
    - `SET chave "valor"`: Associa um valor a uma chave. Ex: `SET nome "João"`.
    - `GET chave`: Recupera o valor associado a uma chave. Ex: `GET nome`.
    - `INCR chave`: Incrementa o valor numérico de uma chave em 1. Usado para contadores. Ex: `INCR visitas`.

### 2. Listas
- **Objetivo**: Armazenar e manipular uma coleção ordenada de itens.
- **Comandos**:
    - `LPUSH chave "item1" "item2"`: Insere um ou mais itens no *início* de uma lista. Ex: `LPUSH frutas "maçã" "banana"`.
    - `RPUSH chave "item1" "item2"`: Insere um ou mais itens no *final* de uma lista.
    - `LRANGE chave inicio fim`: Recupera um intervalo de itens da lista. Para ver todos os itens, use `LRANGE chave 0 -1`.

### 3. Hashes
- **Objetivo**: Armazenar dados estruturados, como um objeto ou dicionário.
- **Comandos**:
    - `HSET chave campo "valor"`: Define um par de campo-valor dentro de um hash. Ex: `HSET usuario:123 nome "Maria"`.
    - `HGET chave campo`: Recupera o valor de um campo específico no hash. Ex: `HGET usuario:123 nome`.
    - `HGETALL chave`: Recupera todos os campos e valores de um hash. Ex: `HGETALL usuario:123`.

---


## Parte 2: Executando Redis com Python usando Venv

Vamos rodar o script Python de forma organizada, isolando suas dependências.

### Passo 1: Preparar o Ambiente Virtual (`venv`)

1.  **Crie uma pasta para o projeto** e entre nela:
    ```sh
    mkdir projeto-redis
    cd projeto-redis
    ```
2.  **Crie o ambiente virtual**:
    ```sh
    python3 -m venv venv
    ```
3.  **Ative o ambiente virtual**:
    - **No Linux/macOS**: `source venv/bin/activate`
    - **No Windows**: `.\venv\Scripts\activate`

4.  **Instale a biblioteca `redis`** (ela será instalada apenas no `venv` ativo):
    ```sh
    pip install redis
    ```

### Passo 2: O Código Python

Salve o código abaixo em um arquivo chamado `teste_redis.py` dentro da sua pasta `projeto-redis`.

```python
import redis   # Biblioteca para se conectar e interagir com o Redis
import time    # Biblioteca para medir o tempo de execução
import base64  # Biblioteca para codificar e decodificar dados em Base64

# Conexão com o Redis local
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Testando Alto Desempenho
print("=== Testando Alto Desempenho ===")
start_time = time.time()
redis_client.set("chave_teste", "valor_teste")
retrieved_value = redis_client.get("chave_teste")
end_time = time.time()
print(f"Valor armazenado: {retrieved_value}")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n")

# Testando Escalabilidade
print("=== Testando Escalabilidade ===")
for i in range(100000):
    redis_client.set(f"chave_{i}", f"valor_{i}")
print(f"Exemplo de valor armazenado: {redis_client.get('chave_500')}\n")

# Testando Flexibilidade
print("=== Testando Flexibilidade ===")
# String
redis_client.set("string_exemplo", "Hello Redis!")
print(f"String armazenada: {redis_client.get('string_exemplo')}")
# Lista
redis_client.rpush("lista_exemplo", "item1", "item2", "item3")
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}")
# Hash
redis_client.hset("hash_exemplo", "campo1", "valor1")
redis_client.hset("hash_exemplo", "campo2", "valor2")
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}")
# Binário (simulado)
image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")
redis_client.set("imagem_binario", image_data)
print(f"Imagem (binário armazenado): {redis_client.get('imagem_binario')[:20]}... [Cortado]\n")

# Testando Baixa Latência (Cache)
print("=== Testando Baixa Latência ===")
redis_client.set("configuracao_cache", "config_inicial")
for _ in range(5):
    start_time = time.time()
    cache_value = redis_client.get("configuracao_cache")
    end_time = time.time()
    print(f"Cache acessado: {cache_value} | Tempo de execução: {end_time - start_time:.6f} segundos")

print("\nTeste concluído com sucesso!")
