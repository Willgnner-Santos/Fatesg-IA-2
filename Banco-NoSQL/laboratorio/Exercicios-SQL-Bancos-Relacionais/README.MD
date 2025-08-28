Exercício de Modelagem e Manipulação de Dados em SQL

Este projeto contém a solução para um exercício prático de SQL, utilizando o banco de dados PostgreSQL. O objetivo é criar um esquema de banco de dados simples para gerenciar departamentos, funcionários e projetos de uma empresa, além de inserir e consultar dados.

Estrutura do Projeto

O projeto é composto por um único arquivo SQL que inclui todos os comandos necessários para:
- Criar o banco de dados.
- Criar as tabelas (`departamento`, `funcionario`, `projeto`).
- Inserir dados de exemplo.
- Realizar consultas para testar o modelo.

Passo a Passo da Solução

1. Criação do Banco de Dados
A primeira etapa é criar o banco de dados no PostgreSQL.

```sql
CREATE DATABASE empresa_db;

-- Tabela de Departamentos
CREATE TABLE departamento (
    id_departamento SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela de Funcionários
CREATE TABLE funcionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2) CHECK (salario >= 0),
    id_departamento INT,
    CONSTRAINT fk_departamento FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE SET NULL
);

-- Tabela de Projetos
CREATE TABLE projeto (
    id_projeto SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    id_departamento INT,
    CONSTRAINT fk_projeto_departamento FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE
);

Inserindo departamentos
INSERT INTO departamento (nome) VALUES ('Recursos Humanos');
INSERT INTO departamento (nome) VALUES ('TI');
INSERT INTO departamento (nome) VALUES ('Marketing');

Inserindo funcionários
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Ana Souza', 'Analista', 4500.00, 1);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Carlos Silva', 'Desenvolvedor', 7000.00, 2);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Mariana Costa', 'Designer', 4000.00, 3);

Inserindo projetos
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Website Corporativo', 'Criação do site institucional', 2);
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Campanha Publicitária', 'Marketing digital nas redes sociais', 3);

Exibir todos os funcionários e seus departamentos
SELECT
    funcionario.nome,
    funcionario.cargo,
    funcionario.salario,
    departamento.nome AS departamento
FROM
    funcionario
LEFT JOIN
    departamento ON funcionario.id_departamento = departamento.id_departamento;

-- Exibir todos os projetos e seus departamentos
SELECT
    projeto.nome AS projeto,
    projeto.descricao,
    departamento.nome AS departamento
FROM
    projeto
LEFT JOIN
    departamento ON projeto.id_departamento = departamento.id_departamento;

