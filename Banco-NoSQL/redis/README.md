# Explicação dos Comandos Redis Executados

Vamos revisar os comandos utilizados no terminal Redis, destacando cada tipo de estrutura de dados manipulada e, ao final, comentar sobre o problema ao imprimir o nome "São Paulo".

## 1. Armazenando e Recuperando uma String
* `SET nome "Joao"`: Salva o valor "Joao" na chave "nome".
* `GET nome`: Recupera o valor da chave "nome", retornando "Joao".

## 2. Trabalhando com Listas
* `LPUSH frutas "melancia" "banana" "laranja"`: Adiciona "melancia", "banana" e "laranja" no início da lista chamada "frutas".
* `LRANGE frutas 0 -1`: Retorna todos os elementos da lista "frutas" (de 0 até o último elemento), exibindo os itens na ordem em que foram inseridos.

## 3. Manipulando Hashes
* `HSET usuario:123 nome "Maria"`: Adiciona o campo "nome" com valor "Maria" ao hash "usuario:123".
* `HSET usuario:123 idade "30"` e `HSET usuario:123 cidade "São Paulo"`: Adiciona os campos "idade" e "cidade" ao mesmo hash.
* `HGET usuario:123 nome`: Recupera apenas o valor do campo "nome" do hash.
* `HGETALL usuario:123`: Retorna todos os campos e valores do hash. Porém, na saída do terminal, o valor da cidade aparece como `"S\xca\ao Paulo"` em vez de "São Paulo".

> ### 📌 Falha ao imprimir "São Paulo"
> A string da cidade "São Paulo" contém o caractere especial "ã" (com "til"). Como o Redis CLI e/ou o terminal podem não estar configurados corretamente para Unicode/UTF-8, o resultado é uma impressão incorreta do caractere. Ele aparece como `\xca`, mostrando um problema de compatibilidade ou interpretação de acentuação.
>
> **Como evitar:** Certifique-se que o terminal e o Redis estão usando UTF-8 como padrão, especialmente ao lidar com nomes e palavras acentuadas do português.

## 4. Usando um contador
* `SET visitas 0`: Inicializa a chave "visitas" com o valor "0".
* `INCR visitas`: Incrementa o valor da chave "visitas" em 1 (agora é 1).
* `GET visitas`: Retorna o valor atual da chave "visitas".

---

### Resumo das operações:
* Salvou e leu uma string simples.
* Criou e listou elementos de uma lista.
* Trabalhou com hashes (campos estruturados de um usuário) e encontrou problema ao gravar caracteres especiais (acentos).
* Utilizou um contador para página (exemplo visitas).
