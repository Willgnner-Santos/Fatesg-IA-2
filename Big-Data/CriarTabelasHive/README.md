# Exercício de Criação de Tabelas no Apache Hive

Este repositório documenta a execução de um exercício da disciplina de Big Data, focado na utilização do Apache Hive para a criação e manipulação de tabelas. O objetivo é praticar os comandos básicos da HiveQL, como **CREATE TABLE**, **INSERT**, e **SELECT**, em um ambiente Hadoop gerenciado pelo Ambari.

## 📝 Descrição da Atividade

A atividade proposta consiste em seguir um roteiro para criar uma tabela de exemplo (`alunos`), inserir dados e consultá-los. Posteriormente, o exercício pede a criação de duas tabelas adicionais para solidificar o conhecimento.

## 🚀 Passos Executados

O processo foi realizado seguindo as instruções fornecidas na plataforma Google Classroom.

### 1. Criação da Tabela alunos

O primeiro passo foi definir a estrutura da tabela `alunos` para armazenar informações de matrícula, nome e curso. O comando utilizado foi:

CREATE TABLE alunos (
matricula INT,
nome STRING,
curso STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

text

### 2. Inserção de Dados

Com a tabela criada, foram inseridos três registros de alunos fictícios, conforme o exemplo:

INSERT INTO alunos VALUES
(1, 'Maria', 'Big Data'),
(2, 'João', 'Engenharia de Dados'),
(3, 'Ana', 'Ciência de Dados');

text

### 3. Consulta e Verificação dos Dados

Para verificar se os dados foram inseridos corretamente, foi executada a consulta:

SELECT * FROM alunos;

text

**Resultado:**

A consulta retornou os dados inseridos. Conforme observado na imagem `hive1.png`, o comando de inserção foi executado duas vezes, resultando em registros duplicados. Além disso, foram identificados problemas de codificação de caracteres (encoding) na exibição dos resultados, que substituíram caracteres acentuados por `??`.
