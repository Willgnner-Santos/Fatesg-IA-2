# Documentação - Comandos Básicos do Redis

## Objetivo
Esta decumentação demonstra o uso prático dos principais comandos do Redis para manipulação de diferentes estruturas de dados: strings, listas, hashes e contadores.

## Ambiente de Execução
- **Sistema Operacional**: Arch Linux
- **Interface**: redis-cli via Konsole
- **Servidor Redis**: Localhost (127.0.0.1:6379)

## Observação Importante sobre Encoding
Durante a execução dos comandos no redis-cli através do Konsole do Arch Linux, foi identificado um problema com caracteres acentuados. Mesmo configurando o terminal para UTF-8, o redis-cli não processa corretamente caracteres com acentuação. Por essa razão, todos os exemplos utilizam apenas caracteres ASCII padrão.

## Comandos Executados

### 1. Armazenamento e Recuperação de Strings

**Comando de Armazenamento:**
```redis
SET nome "Miguel"
```

**Resultado:** `OK`

**Comando de Recuperação:**
```redis
GET nome
```

**Resultado:** `"Miguel"`

**Explicação:**
- `SET`: Associa uma chave a um valor string
- `GET`: Recupera o valor associado a uma chave
- Estrutura mais básica do Redis para dados simples

### 2. Manipulação de Listas

**Primeiro teste (posteriormente removido):**
```redis
LPUSH frutas "banana" "laranja" "morango"
```

**Resultado:** `(integer) 3`

**Remoção da lista:**
```redis
DEL frutas
```

**Resultado:** `(integer) 1`

**Recriação da lista:**
```redis
LPUSH frutas "banana" "laranja" "morango"
```

**Resultado:** `(integer) 3`

**Visualização da lista:**
```redis
LRANGE frutas 0 -1
```

**Resultado:**
```
1) "morango"
2) "laranja"
3) "banana"
```

**Explicação:**
- `LPUSH`: Insere elementos no início da lista (ordem reversa)
- `LRANGE 0 -1`: Exibe todos os elementos da lista (do índice 0 ao final)
- `DEL`: Remove completamente uma chave do Redis
- Elementos são exibidos em ordem LIFO (Last In, First Out)

### 3. Estruturas Hash (Dados Estruturados)

**Criação dos hash:**
```redis
HSET usuario:123 nome "Maria"
HSET usuario:123 idade "30"
HSET usuario:123 cidade "Rio de Janeiro"
```

**Resultado para cada comando:** `(integer) 0` ou `(integer) 1`

**Recuperação de campo específico:**
```redis
HGET usuario:123 nome
```

**Resultado:** `"Maria"`

**Recuperação de todos os campos:**
```redis
HGETALL usuario:123
```

**Resultado:**
```
1) "nome"
2) "Maria"
3) "idade"
4) "30"
5) "cidade"
6) "Rio de Janeiro"
```

**Explicação:**
- `HSET`: Cria ou atualiza campos em uma estrutura hash
- `HGET`: Recupera valor de um campo específico
- `HGETALL`: Retorna todos os pares campo-valor do hash
- Ideal para representar objetos com múltiplos atributos

### 4. Contador Numérico

**Inicialização do contador:**
```redis
SET visitas 0
```

**Resultado:** `OK`

**Incremento do contador:**
```redis
INCR visitas
```

**Resultado:** `(integer) 1`

**Verificação do valor:**
```redis
GET visitas
```

**Resultado:** `"1"`

**Explicação:**
- `SET`: Inicializa o contador com valor zero
- `INCR`: Incrementa automaticamente o valor em 1
- Útil para contadores de acesso, visualizações, etc.

## Análise dos Resultados

### Comportamento das Estruturas de Dados

| Estrutura | Comando Principal | Característica | Uso Típico |
|-----------|------------------|----------------|------------|
| String | SET/GET | Valor simples | Configurações, tokens |
| Lista | LPUSH/LRANGE | Ordenada, permite duplicatas | Filas, históricos |
| Hash | HSET/HGET | Estrutura chave-valor | Objetos, perfis de usuário |
| Contador | INCR | Incremento automático | Estatísticas, métricas |

### Observações Técnicas

**Problemas Identificados:**
1. **Encoding de caracteres**: redis-cli não processa acentuação corretamente no Konsole
2. **Escape de caracteres**: Alguns caracteres especiais requerem tratamento específico

**Soluções Aplicadas:**
1. **Uso de ASCII puro**: Evitar caracteres acentuados
2. **Testes iterativos**: Validação de cada comando antes de prosseguir

## Comandos de Administração Utilizados

### Limpeza de Dados
```redis
DEL chave_nome
```
Remove completamente uma chave e seus dados associados.

### Verificação de Tipos
O Redis permite verificar o tipo de dados armazenado em uma chave:
```redis
TYPE nome_da_chave
```


## Conclusão

O Redis mostrou-se uma ferramenta eficaz para diferentes tipos de armazenamento de dados, com comandos intuitivos e performance excelente para operações básicas. A experiência destacou a importância de considerar limitações do ambiente (como encoding de caracteres) ao trabalhar com ferramentas de linha de comando.
