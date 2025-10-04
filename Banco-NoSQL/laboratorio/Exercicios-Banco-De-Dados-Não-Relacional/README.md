📚 Introdução aos Bancos de Dados Não-Relacionais (NoSQL)
Este repositório contém a resolução de exercícios práticos e conceituais sobre Bancos de Dados Não-Relacionais (NoSQL), abordando suas definições, características, vantagens, tipos e aplicações em cenários reais como Redes Sociais e E-commerce.

🎯 Objetivo
O principal objetivo desta atividade é compreender as diferenças fundamentais entre os modelos de dados Relacionais (SQL) e Não-Relacionais (NoSQL) e identificar os cenários mais adequados para a aplicação de cada um dos quatro principais tipos de bancos NoSQL.

💡 Conceitos Chave Abordados
A atividade se concentra nos seguintes pilares do NoSQL:

1. Definição e Vantagens
Flexibilidade de Schema: A capacidade de armazenar diferentes tipos de dados e ter um esquema dinâmico, em contraste com o esquema rígido dos bancos relacionais.

Escalabilidade Horizontal (Scale-out): A facilidade de adicionar mais servidores (máquinas comuns) para lidar com um volume maciço de dados e alto tráfego, garantindo alta disponibilidade e desempenho.

2. Os 4 Tipos Principais de NoSQL
Tipo de Banco	Descrição e Foco	Exemplo de Ferramenta
Orientado a Documentos	Melhor em consultas mais complexas, armazena dados em documentos (JSON/BSON).	MongoDB
Chave-Valor	Melhor para consultas simples e rápidas, ideal para caching e sessões.	Redis
Colunas Amplas	Melhor em bancos com um grande volume de dados distribuídos.	Cassandra
Grafos	Melhor para achar conexões do banco de forma rápida, ideal para modelar relacionamentos complexos.	Neo4j

Exportar para as Planilhas
📝 Questões e Resoluções (Resumo)
Comparação de Modelos
Pergunta	Resposta Principal
Relacional vs. Grafos	O modelo relacional prioriza entidades (tabelas) com esquema rígido. O modelo de grafos prioriza relacionamentos (arestas) entre entidades (nós), sendo mais eficiente para dados altamente conectados.
NoSQL em Redes Sociais	Grafos é o mais adequado. Redes sociais dependem da modelagem de conexões complexas (quem segue quem, quem curtiu o quê), onde a travessia de grafos é muito mais rápida que múltiplas junções em tabelas.

Exportar para as Planilhas
Escalabilidade e Flexibilidade
Conceito	Explicação
Escalabilidade Horizontal	Consiste em adicionar mais servidores de baixo custo a um cluster para distribuir a carga e os dados. Isso garante que o sistema suporte o aumento de tráfego sem a necessidade de modificar um único servidor verticalmente.
Flexibilidade de Schema (Documentos)	Essencial para lidar com atributos variados (ex: catálogo de produtos onde cada item tem campos únicos) e suportar um desenvolvimento ágil, permitindo rápidas mudanças no modelo sem migrações complexas.

Exportar para as Planilhas
Estudo de Caso
Empresa: Medium (Plataforma de publicação de conteúdo).

Uso: Utiliza o banco de Grafos Neo4j. O banco modela as conexões e relacionamentos entre usuários e artigos.

Benefício: Criação de um sistema de recomendação altamente eficiente, que sugere conteúdo relevante para o usuário em tempo real, melhorando o engajamento na plataforma.