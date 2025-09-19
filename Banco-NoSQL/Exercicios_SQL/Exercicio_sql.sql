CREATE TABLE 
	DEPARTAMENTO(
		id_departamento SERIAL PRIMARY KEY,
		nome VARCHAR (100) NOT NULL

);

CREATE TABLE
	funcionario(
		id_funcionario SERIAL PRIMARY KEY,
		nome VARCHAR(150) NOT NULL,
		cargo VARCHAR(100),
		salario DECIMAL(10,2) CHECK (salario >=0),
		id_departamento INT,
		CONSTRAINT fk_departamento FOREIGN KEY (id_departamento)
		REFERENCES departamento ON DELETE SET NULL
);

CREATE TABLE
	projeto(
		id_projeto SERIAL PRIMARY KEY,
		nome VARCHAR(150) NOT NULL,
		descricao TEXT,
		id_departamento INT,
		CONSTRAINT fk_projeto_departamento FOREIGN KEY (id_departamento)
		REFERENCES departamento(id_departamento) ON DELETE CASCADE
	);

INSERT INTO departamento (nome) VALUES ('Recursos Humanos');
INSERT INTO departamento (nome) VALUES ('TI');
INSERT INTO departamento (nome) VALUES ('Marketing');


INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Ana Souza', 'Analista', 4500.00, 1);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Carlos Silva', 'Desenvolvedor', 7000.00, 2);
INSERT INTO funcionario (nome, cargo, salario, id_departamento) VALUES ('Mariana Costa', 'Designer', 4000.00, 3);


INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Website Corporativo', 'Criação do site institucional', 2);
INSERT INTO projeto (nome, descricao, id_departamento) VALUES ('Campanha Publicitária', 'Marketing digital nas redes sociais', 3);

 
SELECT funcionario.nome, funcionario.cargo, funcionario.salario, departamento.nome AS departamento
FROM funcionario
LEFT JOIN departamento ON funcionario.id_departamento = departamento.id_departamento;


SELECT projeto.nome AS projeto, projeto.descricao, departamento.nome AS departamento
FROM projeto
LEFT JOIN departamento ON projeto.id_departamento = departamento.id_departamento;

SELECT * FROM public.departamento
ORDER BY id_departamento ASC 

 