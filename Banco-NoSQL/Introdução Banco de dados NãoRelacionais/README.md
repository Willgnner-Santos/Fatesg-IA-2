# Atividade: Introdução aos Bancos de Dados Não-Relacionais

**Aluno:** Frederico Lemes Rosa 

## Visão Geral

Este repositório contém as respostas para um questionário sobre os fundamentos dos bancos de dados não-relacionais (NoSQL). A atividade aborda desde a definição e características até um estudo de caso prático, explorando as vantagens, tipos e a aplicabilidade desses bancos de dados em cenários modernos.

---

## Questões Abordadas

### 1. Definição e Características
* **O que é um banco de dados não-relacional?**
    * É um banco de dados flexível que armazena informações sem uma estrutura fixa ou com dados semi-organizados
* **Vantagens em relação aos bancos relacionais:**
    * Alta escalabilidade, robustez para grandes volumes de dados e agilidade no processamento.
* **Situações práticas de uso:**
    * Processamento de grande volume de dados de sensores (IoT).
    * Catálogos de produtos ou conteúdos variados, onde cada item pode ter atributos diferentes.
    * Aplicações que exigem alta velocidade, como gerenciamento de sessões de usuários e carrinhos de compra em tempo real.

### 2. Tipos de Bancos de Dados Não-Relacionais
* **Orientados a Documentos:** Armazenam dados em formatos como JSON ou BSON. Exemplo: MongoDB.
* **Chave-Valor:** Ideais para armazenar cache e sessões. Exemplo: Redis.
* **Colunas Amplas:** Organizam informações por colunas, otimizados para análise de grandes volumes de dados. Exemplo: Cassandra.
* **Grafos:** Armazenam dados como nós e arestas, perfeitos para modelar relacionamentos complexos.Exemplo: Neo4j.

### 3. Comparação Prática
* **Diferença entre modelo relacional e de grafos:**
    * O modelo relacional utiliza uma estrutura linear com tabelas, enquanto o modelo de grafos armazena dados em nós, facilitando a representação de conexões complexas.
* **Banco de dados para redes sociais:**
    * O modelo de grafos é mais adequado, pois o formato de armazenamento espelha a estrutura de interações e conexões da rede.

### 4. Escalabilidade e Flexibilidade
* **Escalabilidade Horizontal:**
    * Consiste em distribuir o armazenamento de dados em múltiplos servidores, permitindo um crescimento flexível e econômico.
* **Flexibilidade de Schema (Bancos Orientados a Documentos):**
    * Permite que a própria aplicação defina a estrutura dos dados no momento da escrita, sendo ideal para lidar com dados polimórficos e semi-estruturados sem a rigidez de um esquema pré-definido.

### 5. Estudo de Caso: Caixa Econômica Federal e o Auxílio Emergencial
* **Empresa:** Caixa Econômica Federal.
* **Contexto:** Pagamento do Auxílio Emergencial em 2020, que exigiu o cadastro e o pagamento de dezenas de milhões de brasileiros em um curto período durante a pandemia.
* **Utilização de Bancos Não-Relacionais:**
    * **Orientado a Documentos (ex: MongoDB):** Usado para o cadastro massivo de cidadãos, aproveitando o schema flexível para lidar com dados de fontes e qualidades distintas.
    * **Chave-Valor (ex: Redis):** Utilizado para gerenciar filas virtuais e milhões de sessões de usuário no aplicativo Caixa Tem, garantindo baixa latência e alta performance.
    * **Ecossistemas de Big Data (ex: Hadoop/HBase):** Empregados para processar e analisar grandes volumes de dados para determinar a elegibilidade dos cidadãos.
* **Benefícios Obtidos:**
    * **Velocidade de Desenvolvimento:** A flexibilidade do NoSQL permitiu construir e adaptar a aplicação rapidamente.
    * **Escalabilidade Extrema:** A arquitetura escalou horizontalmente para suportar o acesso simultâneo de milhões de usuários, adicionando mais servidores conforme a demanda aumentava.
    * **Alta Disponibilidade:** Mecanismos de replicação e tolerância a falhas garantiram que o sistema continuasse operando sem interrupções.
    * **Custo-Eficiência:** A escalabilidade horizontal em nuvem com hardware comum permitiu um gerenciamento de custos mais eficiente.