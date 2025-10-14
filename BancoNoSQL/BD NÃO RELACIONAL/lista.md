Questão 1
Letra A
Um banco de dados não-relacional (NoSQL) é caracterizado por não utilizar um modelo de tabelas relacionais com esquema fixo, permitindo o armazenamento de dados não estruturados ou semi-estruturados. Ele trabalha com estruturas como documentos, chave-valor, colunas ou grafos.

Letra B
Flexibilidade de esquema, alta escalabilidade horizontal, desempenho otimizado para leitura e escrita em grandes volumes de dados e melhor adaptação a dados em tempo real e Big Data.

Letra C
Aplicações de redes sociais com relacionamentos complexos, sistemas que lidam com Big Data ou análise de logs, armazenamento de sessões ou cache em aplicações web.

Questão 2
Letra A
Orientados a Documentos: Armazenam dados em formato JSON ou BSON; cada documento é uma unidade independente e pode ter estrutura diferente dos demais. Chave-Valor: Dados são armazenados como pares chave:valor, ideal para operações simples e rápidas. Colunas Amplas: Organizam dados em colunas em vez de linhas, ótimo para consultas analíticas com grande volume de dados. Grafos: Armazenam dados como nós e arestas, representando relacionamentos complexos entre entidades.

Letra B
Documentos: MongoDB, CouchDB Chave-Valor: Redis, Riak Colunas Amplas: Apache Cassandra, HBase Grafos: Neo4j, ArangoDB

Questão 3
Letra A
O modelo relacional representa os dados em tabelas com chaves estrangeiras para relacionamentos. Já o modelo de grafos representa dados com nós e arestas, armazenando os relacionamentos de forma nativa e mais eficiente para consultas relacionais.

Letra B
O banco de grafos é mais adequado, pois redes sociais possuem relacionamentos complexos e interligados entre usuários. Bancos como o Neo4j permitem consultas rápidas como "quem são os amigos dos amigos", algo que seria mais lento e complexo em um banco relacional.

Questão 4
Letra A
A escalabilidade horizontal consiste em adicionar novos servidores para dividir a carga de dados e processamento. Em bancos NoSQL, isso é feito por meio de sharding, onde os dados são particionados automaticamente entre diferentes nós.

Letra B
Porque permite armazenar documentos com estruturas diferentes na mesma coleção, facilitando alterações e evolução do modelo de dados sem necessidade de migração de esquema, como ocorre em bancos relacionais.

Questão 5
Letra A
A Netflix utiliza o banco de dados Apache Cassandra, que é do tipo colunas amplas.

Letra B
A Netflix utiliza o Cassandra para armazenar dados de usuários, como histórico de reprodução, preferências e recomendações. Os principais benefícios foram: Alta disponibilidade global, desempenho em larga escala com milhões de usuários simultâneos e resistência a falhas e rápida resposta na entrega de conteúdo.
