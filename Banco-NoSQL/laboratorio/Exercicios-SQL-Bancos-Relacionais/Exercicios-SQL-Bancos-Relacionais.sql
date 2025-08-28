CREATE TABLE departamento (
	id_departamento SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL
)

CREATE TABLE funcionario (
	id_funcionario SERIAL PRIMARY KEY
	nome VARCHAR(150) NOT NULL,
	cargo VARCHAR(100),
	salario DECIMAL(10,2) CHECK (salario >= 0),
	id_departamento INT,
	CONSTRAINT fk_departamento FOREIGN KEY (id_departamento) REFERENCES departamento ON DELETE SET NULL
)

CREATE TABLE projeto (
	id_projeto SERIAL PRIMARY KEY,
	nome VARCHAR(150) NOT NULL,
	descricao TEXT,
	id_departamento INT,
	CONSTRAINT fk_projeto_departamento FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE
)

INSERT INTO departamento (nome) VALUES ('Recursos Humanos');
INSERT INTO departamento (nome) VALUES ('TI');
INSERT INTO departamento (nome) VALUES ('Marketing');

INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Ana Clara','Analista',7000.00, 1);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Carlos Silva', 'Desenvolvedor',4500.00, 1);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Mariana Costa', 'Designer', 4000.00, 3);

INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Website Corporativo', 'Criação de site institucional', 2);
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Capanha Publicitária', 'Marketing digital nas redes sociais', 3)

INSERT INTO departamento (nome) VALUES ('Comercial');
INSERT INTO departamento (nome) VALUES ('Gerencia');
INSERT INTO departamento (nome) VALUES ('Vendas');

INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('João Martins', 'Gerente de Vendas', 8500.00, 4);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Sofia Guedes', 'Estagiária', 2000.00, 4);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Felipe Alves', 'Analista de RH', 5000.00, 1);

INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Sistema de Pagamentos', 'Desenvolvimento de uma plataforma de pagamentos interna', 2);
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Treinamento de Liderança', 'Programa de capacitação para gerentes e supervisores', 1);
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Estratégia de Expansão', 'Planejamento de vendas para novos mercados', 4);

SELECT
    funcionario.nome,
    funcionario.cargo,
    funcionario.salario,
    departamento.nome AS departamento
FROM
    funcionario
LEFT JOIN
    departamento ON funcionario.id_departamento = departamento.id_departamento;

SELECT
    projeto.nome AS projeto,
    projeto.descricao,
    departamento.nome AS departamento
FROM
    projeto
LEFT JOIN
    departamento ON projeto.id_departamento = departamento.id_departamento;
