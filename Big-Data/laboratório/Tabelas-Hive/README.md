# Processo de Análise e Modelagem de Dados com Apache Hive

Este documento descreve o processo detalhado de criação e manipulação de tabelas no **Apache Hive**, uma ferramenta central para a gestão de dados em ambientes de Big Data. O objetivo deste exercício foi simular um cenário de análise de dados em uma instituição educacional, criando um esquema que representasse alunos, disciplinas e turmas. Em seguida, foram executadas consultas específicas para extrair insights valiosos e validar o modelo de dados. Esse processo permitiu uma compreensão prática da modelagem de dados e da execução de consultas em um ambiente de Data Warehouse distribuído.

## Metodologia e Execução

As atividades foram realizadas em uma interface de usuário web que se conecta a uma instância do Hive, conforme demonstrado nas imagens. A metodologia seguiu uma sequência lógica, típica do fluxo de trabalho de um analista ou engenheiro de dados: desde a concepção do esquema e a criação das tabelas até a inserção, validação e, finalmente, a análise dos dados.

---

### 1. Criação e Estruturação das Tabelas

A primeira fase consistiu em projetar e criar as tabelas fundamentais para o modelo de dados da escola.

-   **Tabela `alunos`**: Esta tabela foi criada para armazenar informações essenciais sobre os estudantes. Incluiu colunas como `alunos.id` para identificação única, `alunos.nome` para o nome completo do aluno e `alunos.curso` para registrar o curso no qual o estudante está matriculado.
-   **Tabela `disciplinas`**: Projetada para organizar os dados das disciplinas oferecidas. As colunas criadas foram `disciplinas.id` para a identificação da disciplina, `disciplinas.nome_disciplina` para seu nome e `disciplinas.carga_horaria` para a quantidade de horas de aula.
-   **Tabela `turmas`**: Esta tabela foi adicionada para categorizar os alunos por turmas. As colunas incluídas foram `turmas.id` para o identificador da turma, `turmas.nome_turma` para o nome da turma e `turmas.ano_inicio` para registrar o ano em que a turma foi iniciada.

---

### 2. Inserção e Verificação dos Dados

Após a definição da estrutura, o próximo passo foi popular as tabelas com dados de exemplo e garantir sua integridade.

-   **População das tabelas**: Dados fictícios foram inseridos em todas as tabelas (`alunos`, `disciplinas` e `turmas`) para simular um conjunto de dados real.
-   **Validação**: A validação foi um passo crítico. Para cada tabela, a consulta `SELECT * FROM [nome_da_tabela];` foi executada. Essa operação permitiu verificar visualmente se os dados foram inseridos corretamente, confirmando que cada registro estava no local e formato esperados.

---

### 3. Análise e Validação das Consultas

A fase final e mais importante do exercício foi a execução de consultas mais complexas, demonstrando a capacidade de análise do Hive.

-   **Filtragem de Dados (`prova 05.jpeg`)**: A primeira análise buscou filtrar dados específicos usando a cláusula `WHERE`. A consulta `SELECT * FROM alunos WHERE curso = 'Big Data';` foi utilizada para isolar e exibir apenas os alunos que estavam matriculados no curso de 'Big Data', confirmando o uso correto de filtros em consultas.
-   **Agregação de Dados (`prova 04.jpeg`)**: A segunda análise teve como objetivo agregar informações para obter um resumo dos dados. A consulta `SELECT curso, COUNT(*) AS total_alunos FROM alunos GROUP BY curso;` demonstrou a capacidade de contar o número de alunos em cada curso. O uso da função de agregação `COUNT(*)` e da cláusula `GROUP BY` por curso forneceu uma visão consolidada, mostrando o total de estudantes por área de estudo.

Este exercício proporcionou um valioso conhecimento prático sobre como modelar, popular e manipular dados em um ambiente Hive. A experiência com a sintaxe do HiveQL e a lógica de um data warehouse distribuído é fundamental para qualquer profissional de dados.