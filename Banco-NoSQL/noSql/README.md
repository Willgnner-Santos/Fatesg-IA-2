# 1. Definição e Características

### a) O que caracteriza um banco de dados não-relacional?
Um banco de dados não-relacional é aquele que não utiliza o modelo tradicional de tabelas com linhas e colunas dos bancos relacionais. Ele armazena dados de formas variadas, como documentos, pares chave-valor, colunas ou grafos, permitindo maior flexibilidade e adaptabilidade para diferentes tipos de dados.

### b) Quais são as vantagens desse tipo de banco em relação aos bancos relacionais?
* **Flexibilidade de esquema:** não exige estrutura fixa para os dados.
* **Alta escalabilidade:** especialmente horizontal, facilitando o crescimento do sistema.
* **Melhor desempenho** para grandes volumes de dados não estruturados ou semi-estruturados.

### c) Cite ao menos 3 situações práticas em que um banco de dados não-relacional é mais indicado.
* Armazenamento de dados de redes sociais, onde as relações entre usuários são complexas e dinâmicas.
* Sistemas de recomendação, que exigem análise rápida de grandes volumes de dados.
* Aplicações que lidam com dados semi-estruturados, como logs de aplicações ou documentos JSON.

---

# 2. Tipos de Bancos de Dados Não-Relacionais

### a) Explique as diferenças entre os quatro principais tipos:
* **Orientados a Documentos:** Armazenam dados em documentos (geralmente JSON ou BSON), cada um com estrutura flexível. Exemplo: MongoDB.
* **Chave-Valor:** Armazenam dados como pares de chave e valor, ideais para cache e sessões. Exemplo: Redis.
* **Colunas Amplas:** Armazenam dados em colunas, facilitando consultas analíticas em grandes volumes. Exemplo: Cassandra.
* **Grafos:** Armazenam dados como vértices e arestas, ideais para representar relações complexas. Exemplo: Neo4j.

### b) Dê exemplos de ferramentas populares para cada tipo.

| Tipo | Exemplo Popular |
| :--- | :--- |
| Orientado a Documentos | MongoDB |
| Chave-Valor | Redis |
| Colunas Amplas | Cassandra |
| Grafos | Neo4j |

---

# 3. Comparação Prática

### a) Qual a principal diferença entre o modelo relacional e o modelo de grafos?
O modelo relacional organiza dados em tabelas com linhas e colunas, enquanto o modelo de grafos representa dados como vértices e arestas, facilitando a navegação por relações complexas.

### b) Em um cenário de redes sociais, qual tipo de banco de dados seria mais adequado? Justifique.
O banco de dados de grafos é mais adequado, pois permite mapear e consultar facilmente as conexões entre usuários, amigos, seguidores e interações.

---

# 4. Escalabilidade e Flexibilidade

### a) Explique como a escalabilidade horizontal funciona em bancos não-relacionais.
A escalabilidade horizontal consiste em adicionar mais servidores para distribuir a carga e armazenar mais dados, sem depender de um único servidor central. Bancos não-relacionais são projetados para facilitar esse tipo de expansão.

### b) Por que a flexibilidade de schema é importante em bancos orientados a documentos?
Permite que diferentes documentos tenham estruturas variadas, facilitando a evolução do sistema e a integração de novos tipos de dados sem grandes mudanças na base.

---

# 5. Estudo de Caso

### a) Pesquise um caso de uso real de uma empresa que utiliza bancos de dados não-relacionais.
A Netflix utiliza bancos de dados não-relacionais, como Cassandra, para armazenar grandes volumes de dados de usuários e garantir alta disponibilidade global.

### b) Descreva como esse banco é utilizado e quais foram os benefícios obtidos.
O Cassandra permite à Netflix distribuir dados por múltiplos datacenters, garantindo escalabilidade, tolerância a falhas e desempenho para milhões de usuários simultâneos.
