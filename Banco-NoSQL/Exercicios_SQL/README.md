# Processo de Análise e Modelagem de Dados com PostgreSQL

Este documento detalha o processo de criação e manipulação de um banco de dados relacional, demonstrando a construção de tabelas, inserção de dados e execução de consultas para análise. O objetivo foi estabelecer uma estrutura de dados que representasse uma empresa, com informações sobre departamentos, funcionários e projetos, utilizando o **PostgreSQL** e a ferramenta **pgAdmin 4**.

## Metodologia e Execução

O trabalho foi conduzido no ambiente do pgAdmin 4, que me permitiu interagir com o banco de dados `empresa_db` de forma eficiente. O processo seguiu uma sequência lógica, desde a criação do esquema até a validação das consultas.

### 1. Estrutura do Banco de Dados

Primeiramente, construí as tabelas necessárias para o projeto, definindo colunas, tipos de dados e chaves. O script `Exercicio_sql.sql` contém a estrutura completa, incluindo:

-   **`DEPARTAMENTO`**: Tabela principal com um `id_departamento` como chave primária.
-   **`funcionario`**: Tabela que armazena dados de funcionários, com um `id_funcionario` como chave primária e uma chave estrangeira (`id_departamento`) que referencia a tabela `DEPARTAMENTO`.
-   **`projeto`**: Tabela que detalha os projetos da empresa, com `id_projeto` como chave primária e uma chave estrangeira (`id_departamento`) que se conecta à tabela `DEPARTAMENTO`.

### 2. Inserção de Dados

Após criar as tabelas, populei o banco de dados com informações de exemplo, conforme demonstrado no script. Isso incluiu:

-   A inserção de três departamentos: 'Recursos Humanos', 'TI' e 'Marketing'.
-   A adição de três funcionários com seus respectivos cargos, salários e departamentos.
-   A criação de dois projetos, associados aos departamentos de 'TI' e 'Marketing'.

### 3. Análise e Validação das Consultas

O ponto principal do exercício foi a execução de consultas para extrair e analisar os dados. As imagens (`Evidencia01.png`, `Evidencia02.png`, `Evidencia03.png`) documentam a execução dessas consultas no pgAdmin.

-   **Consulta 1 (`Evidencia01.png`)**: Uma consulta que utiliza `LEFT JOIN` para listar o nome, cargo, salário e departamento de cada funcionário. Isso me permitiu visualizar a relação entre as tabelas `funcionario` e `departamento`, garantindo que a associação por `id_departamento` estava funcionando corretamente.

-   **Consulta 2 (`Evidencia02.png`)**: Outra consulta com `LEFT JOIN`, desta vez para listar o nome e a descrição dos projetos junto ao nome do departamento associado. Esta etapa validou a relação entre as tabelas `projeto` e `departamento`, confirmando a integridade dos dados.

-   **Consulta 3 (`Evidencia03.png`)**: Uma consulta simples para listar todos os registros da tabela `departamento`, ordenada pelo `id_departamento`. Esta consulta serviu para verificar se a inserção de dados na tabela de departamentos foi bem-sucedida.

As evidências visuais confirmaram que as consultas foram executadas com sucesso, retornando os resultados esperados e demonstrando a correta modelagem e relacionamento entre as tabelas. Este exercício foi fundamental para reforçar meu conhecimento prático em SQL e gerenciamento de bancos de dados relacionais.