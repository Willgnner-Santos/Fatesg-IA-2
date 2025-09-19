# Processo de Análise e Modelagem de Dados com Apache Hive

Este documento descreve o processo que utilizei para criar e manipular tabelas no **Apache Hive**, uma ferramenta essencial no ecossistema de Big Data. O objetivo do exercício foi criar um esquema de dados para uma escola, representando alunos, professores e cursos, e, em seguida, executar consultas para analisar a relação entre eles. As etapas detalhadas abaixo me permitiram compreender a modelagem de dados e a execução de consultas em um ambiente de Data Warehouse distribuído.

## Metodologia e Execução

O trabalho foi conduzido em uma interface web que me conecta a uma instância do Hive, como visto nas evidências anexadas. A progressão das tarefas foi lógica e seguiu o fluxo de trabalho típico de um engenheiro de dados, desde a criação das tabelas até a análise final.

### 1. Criação das Tabelas

A primeira etapa foi a criação das tabelas necessárias para o esquema. Iniciei com a tabela `alunos`, que armazena informações básicas dos estudantes, como seu ID, nome e o curso em que estão matriculados. Em seguida, criei a tabela `professores`, que registrou os dados de cada professor, incluindo seu ID, nome e a disciplina que leciona.

### 2. Inserção e Validação dos Dados

Após a criação das tabelas, o passo seguinte foi popular os dados. Inseri informações de exemplo nas tabelas `alunos` e `professores`, como demonstrado nas evidências. A validação foi um ponto crucial: executei consultas simples, como `SELECT * FROM professores;` e `SELECT * FROM cursos;`, para me certificar de que os dados foram inseridos corretamente em cada tabela.

### 3. Análise e Validação das Consultas

O ponto central deste exercício foi a execução de consultas mais complexas para analisar a relação entre as entidades. As consultas realizadas me permitiram praticar as operações de JOIN e GROUP BY, que são fundamentais em análise de dados.

-   **Consulta 1 (`evidencia 04.png`)**: Uma consulta que utiliza `JOIN` para relacionar alunos e professores com base na disciplina. A consulta `SELECT a.nome AS nome_aluno, a.curso AS curso_aluno, p.nome AS nome_professor FROM alunos a JOIN professores p ON a.curso = p.disciplina;` me permitiu visualizar a relação entre alunos e seus respectivos professores.

-   **Consulta 2 (`evidencia 05.png`)**: Uma consulta que utiliza `JOIN` e `GROUP BY` para contar o número de alunos por professor e disciplina. A consulta `SELECT p.nome AS nome_professor, p.disciplina AS disciplina_lecionada, COUNT(a.id) AS total_alunos FROM professores p JOIN alunos a ON p.disciplina = a.curso GROUP BY p.nome, p.disciplina;` me deu uma visão agregada dos dados, confirmando que pude realizar análises mais profundas e não apenas consultas simples.

O exercício me proporcionou um conhecimento prático valioso sobre como modelar e manipular dados em um ambiente Hive. Entender a sintaxe e a lógica do HiveQL, assim como a estrutura das tabelas em um data warehouse, foi um passo importante na minha jornada de aprendizado em Big Data.