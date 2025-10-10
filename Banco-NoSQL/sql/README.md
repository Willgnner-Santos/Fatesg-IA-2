# Guia Rápido: Banco de Dados PostgreSQL com DBeaver

Este documento explica cada etapa para criar, popular e consultar um banco de dados relacional usando DBeaver e PostgreSQL.

---

## 1. Criação do Banco de Dados e Conexão

- Abra o DBeaver e conecte-se ao PostgreSQL usando seu usuário e senha.
- Crie um banco chamado `empresa_db` (pode ser feito via interface gráfica ou comando):
  ```
  CREATE DATABASE empresa_db;
  ```

---

## 2. Criação das Tabelas no Schema `public`

Dentro do banco, execute os comandos abaixo para criar as três tabelas de exemplo:

```
CREATE TABLE departamento (
  id_departamento INT PRIMARY KEY,
  nome VARCHAR(50)
);

CREATE TABLE funcionario (
  nome VARCHAR(50),
  cargo VARCHAR(50),
  salario FLOAT,
  id_departamento INT,
  CONSTRAINT fk_funcionario_departamento FOREIGN KEY (id_departamento)
    REFERENCES departamento(id_departamento)
    ON DELETE CASCADE
);

CREATE TABLE projeto (
  nome VARCHAR(50),
  descricao VARCHAR(100),
  id_departamento INT,
  CONSTRAINT fk_projeto_departamento FOREIGN KEY (id_departamento)
    REFERENCES departamento(id_departamento)
    ON DELETE CASCADE
);
```

---

## 3. Inserção de Dados nas Tabelas

Adicione alguns registros nas tabelas para testes:

```
INSERT INTO departamento (id_departamento, nome) VALUES
  (1, 'Recursos Humanos'),
  (2, 'TI'),
  (3, 'Marketing');

INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES
  ('Ana Souza', 'Analista', 4500.00, 1),
  ('Carlos Silva', 'Desenvolvedor', 7000.00, 2),
  ('Mariana Costa', 'Designer', 4000.00, 3);

INSERT INTO projeto (nome, descricao, id_departamento) VALUES
  ('Website Corporativo', 'Criação do site institucional', 2),
  ('Campanha Publicitária', 'Marketing digital nas redes sociais', 3);
```

---

## 4. Consultas com JOIN

Veja como consultar dados relacionados entre as tabelas usando JOIN:

### Funcionários e seus Departamentos

```
SELECT funcionario.nome, funcionario.cargo, funcionario.salario, departamento.nome AS departamento
FROM funcionario
LEFT JOIN departamento
ON funcionario.id_departamento = departamento.id_departamento;
```

### Projetos e seus Departamentos

```
SELECT projeto.nome AS projeto, projeto.descricao, departamento.nome AS departamento
FROM projeto
LEFT JOIN departamento
ON projeto.id_departamento = departamento.id_departamento;
```

---

## 5. Visualização dos Resultados

- Execute as queries acima no editor SQL do DBeaver.
- Observe os resultados utilizando o modo de visualização em grade para cada tabela.

---

## 6. Exportação dos Dados

- No DBeaver, é possível exportar dados das consultas para formatos como CSV, Excel e SQL.
- Use o botão “Export Data” no painel de resultados após rodar uma query.

---

### Observações

- Sempre revise as constraints de relacionamento para manter a integridade dos dados.
- O DBeaver facilita múltiplas operações, incluindo edição visual, execução de scripts e análise de dados.

```
