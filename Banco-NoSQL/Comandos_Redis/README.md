Documentação: Execução de Comandos Essenciais do Redis
Este documento formaliza a execução dos comandos básicos do Redis por meio da CLI, abordando as principais estruturas de dados: Strings, Lists e Hashes. A análise foca na Complexidade Assintótica (O) das operações e na gestão do ciclo de vida das chaves (TTL), elementos críticos em arquiteturas de cache e sistemas de alta disponibilidade.

1. Tipo de Dado String (Chave-Valor e Atomicidade)
O tipo STRING é a fundação do Redis, suportando operações atômicas indispensáveis para a implementação de contadores e mecanismos de limitação de acesso.

Comando	Descrição	Complexidade Assintótica	Aplicação Típica
SET chave valor	Armazena um valor escalar associado a uma chave.	O(1)	Cache de dados de sessão.
INCR chave	Incrementa o valor numérico da chave em uma unidade, garantindo atomicidade.	O(1)	Contagem de eventos, Rate Limiting.
EXPIRE chave segundos	Define o Time To Live (TTL) da chave em segundos.	O(1)	Gestão de expiração de dados temporários.

Exportar para as Planilhas
2. Tipo de Dado List (Estrutura de Fila/Pilha)
O LIST é implementado como uma Lista Ligada (Linked List), permitindo inserções e remoções rápidas nas extremidades, tornando-o eficiente para modelar filas (FIFO) ou pilhas (LIFO).

Comando	Descrição	Complexidade Assintótica	Aplicação Típica
LPUSH chave valor(es)	Insere um ou mais elementos no cabeçalho (esquerda) da lista.	O(1)	Implementação de Pilhas (Stacks) e filas de processamento.
LRANGE chave início fim	Recupera um subconjunto de elementos dentro de um range específico.	O(N), onde N é o número de elementos retornados.	Paginação, exibição de feeds.

Exportar para as Planilhas
Resultado da Execução (List)
Snippet de código

> LPUSH frutas "maçã" "banana" "laranja"
(integer) 3
> LRANGE frutas 0 -1
1) "laranja"
2) "banana"
3) "maçã"
3. Tipo de Dado Hash (Objetos Estruturados)
O HASH é uma estrutura de dados otimizada para armazenar múltiplos pares campo-valor sob uma única chave. É preferível para representar objetos complexos em cache, pois reduz a sobrecarga de memória em comparação com múltiplas chaves STRING.

Comando	Descrição	Complexidade Assintótica	Benefício Estrutural
HSET chave campo valor ...	Define múltiplos campos dentro de um hash.	O(N), onde N é o número de campos definidos.	Redução do overhead de memória.
HGETALL chave	Recupera todos os campos e seus valores correspondentes.	O(N), onde N é o número total de campos.	Serialização/Desserialização eficiente de objetos.

Exportar para as Planilhas
Resultado da Execução (Hash)
Snippet de código

> HSET usuario:123 nome "Maria" idade "30" cidade "São Paulo"
(integer) 3
> HGETALL usuario:123
1) "nome"
2) "Maria"
3) "idade"
4) "30"
5) "cidade"
6) "São Paulo"
🔍 Nota Técnica de Codificação
Ressalta-se que a exibição de caracteres não-ASCII (ex: ã, ç) pode ser representada em sequências de escape (\xc3\xa3) pelo Redis CLI, dependendo da configuração de codificação do terminal do sistema operacional. Esta representação não compromete a integridade dos dados armazenados no servidor Redis.