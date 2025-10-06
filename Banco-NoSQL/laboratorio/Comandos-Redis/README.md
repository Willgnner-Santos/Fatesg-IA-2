# Exercícios de Comandos Básicos no Redis

Este repositório documenta a execução de comandos fundamentais do **Redis** (Remote Dictionary Server) através do Redis CLI, cobrindo os tipos de dados mais básicos: Strings, Listas, Hashes e Contadores.

---

## 1. Exemplo de String (SET / GET)

[cite_start]Demonstração de como armazenar e recuperar um valor simples usando uma chave[cite: 1, 2].

| Comando | Descrição | Saída do Redis |
| :--- | :--- | :--- |
| `SET nome "João"` | [cite_start]Associa a chave `"nome"` ao valor `"João"`[cite: 5, 6]. | `OK` |
| `GET nome` | [cite_start]Recupera o valor associado à chave `"nome"`[cite: 11, 12]. | `"jo\xc3\xa3o"` (Ou "João", dependendo da codificação) |

---

## 2. Exemplo de Listas (LPUSH / LRANGE)

[cite_start]Demonstração de como manipular uma lista ordenada, adicionando e recuperando itens[cite: 14, 15].

| Comando | Descrição | Saída do Redis |
| :--- | :--- | :--- |
| `LPUSH frutas "maçã" "banana" "laranja"` | [cite_start]Insere os itens no **início** da lista `"frutas"`[cite: 17, 18]. | `(integer) 3` (Tamanho da lista) |
| `LRANGE frutas 0 -1` | [cite_start]Recupera todos os itens (do início `0` ao fim `-1`) da lista[cite: 22, 23, 25, 26]. | ```1) "laranja"
2) "banana"
[cite_start]3) "maçã"``` [cite: 28, 29, 30] |

---

## 3. Exemplo de Hashes (HSET / HGETALL)

[cite_start]Demonstração de como armazenar dados estruturados (como informações de um usuário) em um formato de dicionário[cite: 31, 32].

| Comando | Descrição | Saída do Redis |
| :--- | :--- | :--- |
| `HSET usuario:123 nome "Maria" idade "30" cidade "São Paulo"` | [cite_start]Define múltiplos campos e valores no hash `"usuario:123"`[cite: 34, 35, 36, 37]. | `(integer) 3` (Número de campos definidos) |
| `HGET usuario:123 nome` | [cite_start]Recupera o valor de um campo específico ("nome")[cite: 44, 45, 46]. | [cite_start]`"Maria"` [cite: 47] |
| `HGETALL usuario:123` | [cite_start]Recupera todos os campos e valores do hash[cite: 50, 51]. | ```1) "nome"
2) "Maria"
3) "idade"
4) "30"
5) "cidade"
[cite_start]6) "São Paulo"``` [cite: 53, 54, 55, 56, 57, 58] |

---

## 4. Exemplo de Contadores (SET / INCR)

[cite_start]Demonstração de como usar o Redis para criar e incrementar contadores (úteis para visualizações de página ou limites de acesso)[cite: 59, 60].

| Comando | Descrição | Saída do Redis |
| :--- | :--- | :--- |
| `SET visitas 0` | [cite_start]Inicializa o contador `"visitas"` com o valor `0`[cite: 62, 63]. | `OK` |
| `INCR visitas` | [cite_start]Incrementa o valor associado à chave em 1[cite: 66, 67]. | `(integer) 1` |
| `INCR visitas` (Repetido) | [cite_start]Simula mais uma visita[cite: 69]. | `(integer) 2` |
| `INCR visitas` (Repetido) | [cite_start]Simula mais uma visita[cite: 69]. | `(integer) 3` |
| `GET visitas` | [cite_start]Recupera o valor atual do contador[cite: 71, 72]. | [cite_start]`"3"` [cite: 73] |

---

## 🛠️ Resumo dos Comandos Utilizados

| Tipo de Dado | Comandos Principais | Objetivo |
| :--- | :--- | :--- |
| **String** | [cite_start]`SET`, `GET` [cite: 75] | Chave-valor simples. |
| **Listas** | [cite_start]`LPUSH`, `LRANGE` [cite: 76] | Sequência ordenada de itens. |
| **Hashes** | [cite_start]`HSET`, `HGET`, `HGETALL` [cite: 77] | Estruturas de dados (objetos/dicionários). |
| **Contador** | [cite_start]`INCR` [cite: 78] | Incremento atômico de valores numéricos. |