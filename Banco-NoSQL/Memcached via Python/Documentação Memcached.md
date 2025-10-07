# Documentação - Integração Memcached com Python

## Índice

1. [Visão Geral](#visão-geral)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Estrutura do Código](#estrutura-do-código)
4. [Funções Implementadas](#funções-implementadas)
5. [Problemas Encontrados e Soluções](#problemas-encontrados-e-soluções)
6. [Conceitos Aprendidos](#conceitos-aprendidos)
7. [Execução](#execução)

---

## Visão Geral

Projeto de integração do Memcached com Python demonstrando operações básicas, cache de dados, gerenciamento de sessões e análise de performance.

**Tecnologias utilizadas:**
- Python 3.x
- Memcached
- Biblioteca pymemcache
- JSON para serialização

---

## Instalação e Configuração

### No Arch Linux

```bash
sudo pacman -S memcached

sudo systemctl start memcached

sudo systemctl status memcached
```

### Configuração do ambiente Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install pymemcache
```

---

## Estrutura do Código

### Imports necessários

```python
import json          # Serialização de dados complexos
import time          # Medição de performance
from pymemcache.client.base import Client  # Cliente Memcached
```

---

## Funções Implementadas

### 1. `conectar_memcached()`

**Objetivo:** Estabelece conexão com o servidor Memcached.

**Funcionamento:**
- Cria cliente conectando em `localhost:11211`
- Testa conexão com operação SET/DELETE
- Retorna o cliente se sucesso, `None` se falha

**Código:**
```python
def conectar_memcached():
    try:
        client = Client(('localhost', 11211))
        client.set('teste', 'ok'.encode('utf-8'))
        client.delete('teste')
        return client
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None
```

**Conceitos técnicos:**
- Porta padrão 11211
- Protocolo TCP/IP
- Validação de conectividade

---

### 2. `operacoes_basicas()`

**Objetivo:** Demonstra operações fundamentais do Memcached.

**Operações implementadas:**

#### SET - Armazenar dados
```python
client.set('nome', 'João Guilherme'.encode('utf-8'))
```
- Converte string para bytes com UTF-8
- Armazena par chave-valor
- Sem expiração (padrão)

#### GET - Recuperar dados
```python
nome = client.get('nome').decode('utf-8')
```
- Busca valor pela chave
- Decodifica bytes de volta para string
- Retorna `None` se chave não existe

#### Dados complexos (JSON)
```python
usuario = {'id': 1, 'nome': 'João'}
client.set('usuario:1', json.dumps(usuario).encode('utf-8'))
```
- Serializa dicionário para JSON
- Converte JSON string para bytes
- Padrão de chave com namespace (`usuario:1`)

#### TTL - Time To Live
```python
client.set('temporario', 'expira'.encode('utf-8'), expire=10)
```
- Define tempo de expiração em segundos
- Memcached remove automaticamente após TTL

---

### 3. `exemplo_cache_performance()`

**Objetivo:** Demonstra ganho de performance com cache.

**Componentes:**

#### Simulação de consulta lenta
```python
def consulta_lenta(user_id):
    time.sleep(0.5)
    return {'id': user_id, 'nome': f'Usuario_{user_id}'}
```

#### Função de busca com cache
```python
def buscar_usuario(user_id, usar_cache=True):
    cache_key = f'user:{user_id}'
    
    # Tenta buscar no cache
    if usar_cache:
        cached = client.get(cache_key)
        if cached: 
            return json.loads(cached.decode('utf-8'))
    
    # CACHE MISS - busca fonte original
    dados = consulta_lenta(user_id)
    
    # Armazena no cache
    if usar_cache:
        client.set(cache_key, json.dumps(dados).encode('utf-8'), expire=60)
    
    return dados
```

**Conceitos:**
- **Cache Hit:** Dados encontrados no cache (rápido)
- **Cache Miss:** Precisa buscar fonte original (lento)
- **Padrão Cache-Aside:** Aplicação gerencia o cache
- **TTL de 60s:** Balanceia performance vs atualização

**Resultado típico:**
- Primeira consulta: ~0.5s (miss)
- Segunda consulta: ~0.04s (hit)
- Melhoria: ~92%

---

### 4. `exemplo_sessoes()`

**Objetivo:** Gerenciamento de sessões de usuário.

**Implementação:**
```python
session_data = {
    'user_id': 456,
    'username': 'admin',
    'login_time': int(time.time())
}

# Criar sessão (30 minutos)
client.set(f'session:{session_id}', 
           json.dumps(session_data).encode('utf-8'), 
           expire=1800)

# Validar sessão
session = client.get(f'session:{session_id}')

# Logout - remover sessão
client.delete(f'session:{session_id}')
```

**Vantagens:**
- Expiração automática (30 minutos)
- Acesso ultra-rápido
- Compartilhamento entre servidores web
- Sem necessidade de limpeza manual

---

### 5. `estatisticas()`

**Objetivo:** Monitorar métricas do servidor Memcached.

**Implementação:**
```python
def get_stat_value(key):
    value = stats.get(key.encode() if isinstance(key, str) else key)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value) if value is not None else 'N/A'
```

**Métricas principais:**
- **version:** Versão do Memcached
- **curr_items:** Itens armazenados atualmente
- **curr_connections:** Conexões ativas
- **get_hits/get_misses:** Para calcular hit rate

**Cálculo de Hit Rate:**
```python
hit_rate = (hits / (hits + misses)) * 100
```
- Taxa acima de 80% indica cache bem otimizado
- Taxa baixa sugere TTL inadequado ou dados pouco reutilizados

---

## Problemas Encontrados e Soluções

### Problema 1: Erro de ambiente externally-managed

**Erro:**
```
error: externally-managed-environment
```

**Causa:** Arch Linux protege o ambiente Python do sistema.

**Solução:**
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate
pip install pymemcache
```

---

### Problema 2: Erro de encoding

**Erro:**
```
Data values must be binary-safe: 'ascii' codec can't encode character
```

**Causa:** Memcached aceita apenas bytes, não strings Python.

**Solução:**
```python
# Errado
client.set('chave', 'valor')

# Correto
client.set('chave', 'valor'.encode('utf-8'))
```

**Regra:** Sempre use `.encode('utf-8')` ao armazenar e `.decode('utf-8')` ao recuperar.

---

### Problema 3: Erro nas estatísticas

**Erro:**
```
'int' object has no attribute 'decode'
```

**Causa:** Alguns valores de estatísticas são inteiros, não bytes.

**Solução:**
```python
def get_stat_value(key):
    value = stats.get(key)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value) if value is not None else 'N/A'
```

**Técnica:** Verificar tipo antes de decodificar.

---

## Conceitos Aprendidos

### Memcached

- **Arquitetura:** Sistema de cache em memória RAM distribuído
- **Modelo de dados:** Chave-valor simples
- **Protocolo:** TCP/IP baseado em texto na porta 11211
- **Volatilidade:** Dados são perdidos ao reiniciar
- **LRU:** Remove dados menos usados quando memória esgota
- **Limitações:** Valores até 1MB, chaves até 250 caracteres

### Padrões de uso

- **Cache-Aside:** Aplicação controla cache e fonte de dados
- **TTL estratégico:** Balancear performance vs atualidade
- **Namespacing:** Usar `:` para organizar chaves (`user:123`)
- **Serialização:** JSON para dados complexos

### Python

- **pymemcache:** Biblioteca simples e eficiente
- **Encoding/Decoding:** UTF-8 para compatibilidade
- **JSON:** Serialização de objetos Python
- **Tratamento de erros:** Try-except para robustez
- **Ambiente virtual:** Isolamento de dependências

---

## Execução

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar script
python Pmemcached.py
```

**Saída esperada:**
- Confirmação de conexão
- Operações básicas com dados
- Teste de performance com melhoria de ~92%
- Gerenciamento de sessão
- Estatísticas do servidor

---

## Conclusão

O projeto demonstra integração completa do Memcached com Python, incluindo operações CRUD, otimização de performance através de cache, gerenciamento de sessões e monitoramento. Os principais desafios foram compreender o protocolo de bytes do Memcached e lidar com variações de tipos nas estatísticas. O resultado é um sistema funcional que reduz drasticamente o tempo de resposta em consultas repetidas.

## Grupo:
- Miguel Alves
- Felipe Augusto
- Eduardo Sena
- Pedro Vaz
