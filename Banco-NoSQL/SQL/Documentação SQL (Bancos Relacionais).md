# Documentação - Criação de Banco de Dados Relacional com PostgreSQL e DBeaver

## Objetivo
Esta Documentação demonstra a criação de um sistema de banco de dados relacional para uma empresa, incluindo tabelas para departamentos, funcionários e projetos, utilizando PostgreSQL através da interface DBeaver.

## Ferramentas Utilizadas
- **PostgreSQL**: Sistema de gerenciamento de banco de dados
- **DBeaver**: Interface gráfica para administração de banco de dados
- **SQL**: Linguagem de consulta estruturada

## Estrutura do Banco de Dados

### Relacionamentos
- **Departamento** ← **Funcionário** (1:N)
- **Departamento** ← **Projeto** (1:N)

## Passo a Passo da Implementação

### 1. Criação do Banco de Dados

Primeiro, foi criado o banco de dados principal:

```sql
-- Criando um novo banco de dados chamado 'empresa_db'
CREATE DATABASE empresa_db;
```

**Observação:** Após a criação, é necessário selecionar o banco de dados no DBeaver antes de prosseguir com a criação das tabelas.

### 2. Criação da Tabela Departamento

```sql
-- Criando a tabela 'departamento'
CREATE TABLE departamento (
    id_departamento SERIAL PRIMARY KEY, -- Identificador único automático
    nome VARCHAR(100) NOT NULL -- Nome do departamento (obrigatório)
);
```

**Características da tabela:**
- `SERIAL PRIMARY KEY`: Gera IDs únicos automaticamente
- `VARCHAR(100) NOT NULL`: Campo obrigatório de até 100 caracteres

### 3. Criação da Tabela Funcionário

```sql
-- Criando a tabela 'funcionario'
CREATE TABLE funcionario (
    id_funcionario SERIAL PRIMARY KEY, -- Identificador único para cada funcionário
    nome VARCHAR(150) NOT NULL, -- Nome do funcionário (obrigatório)
    cargo VARCHAR(100), -- Cargo do funcionário (opcional)
    salario DECIMAL(10,2) CHECK (salario >= 0), -- Salário não pode ser negativo
    id_departamento INT, -- Chave estrangeira para departamento
    CONSTRAINT fk_departamento FOREIGN KEY (id_departamento) 
        REFERENCES departamento(id_departamento) ON DELETE SET NULL
);
```

**Características importantes:**
- `DECIMAL(10,2)`: Permite até 10 dígitos totais com 2 casas decimais
- `CHECK (salario >= 0)`: Impede salários negativos
- `FOREIGN KEY`: Estabelece relação com a tabela departamento
- `ON DELETE SET NULL`: Mantém o funcionário se o departamento for excluído

### 4. Criação da Tabela Projeto

```sql
-- Criando a tabela 'projeto'
CREATE TABLE projeto (
    id_projeto SERIAL PRIMARY KEY, -- Identificador único para cada projeto
    nome VARCHAR(150) NOT NULL, -- Nome do projeto (obrigatório)
    descricao TEXT, -- Descrição detalhada (opcional)
    id_departamento INT, -- Departamento responsável pelo projeto
    CONSTRAINT fk_projeto_departamento FOREIGN KEY (id_departamento) 
        REFERENCES departamento(id_departamento) ON DELETE CASCADE
);
```

**Diferencial:**
- `TEXT`: Permite descrições longas e detalhadas
- `ON DELETE CASCADE`: Remove projetos automaticamente se o departamento for excluído

## Inserção de Dados

### 5. Populando a Tabela Departamento

```sql
-- Inserindo departamentos
INSERT INTO departamento (nome) VALUES ('Recursos Humanos');
INSERT INTO departamento (nome) VALUES ('TI');
INSERT INTO departamento (nome) VALUES ('Marketing');
```

### 6. Populando a Tabela Funcionário

**Problema Identificado no DBeaver:**
Durante a inserção de múltiplos registros em um único comando, o DBeaver apresentou comportamento inconsistente, sobrescrevendo dados na mesma linha.

**Solução Implementada:**
Execução de comandos INSERT individuais para cada funcionário:

```sql
-- Inserindo funcionários (comandos executados separadamente)
INSERT INTO funcionario (nome, cargo, salario, id_departamento) 
VALUES ('Ana Souza', 'Analista', 4500.00, 1);

INSERT INTO funcionario (nome, cargo, salario, id_departamento) 
VALUES ('Carlos Silva', 'Desenvolvedor', 7000.00, 2);

INSERT INTO funcionario (nome, cargo, salario, id_departamento) 
VALUES ('Mariana Costa', 'Designer', 4000.00, 3);
```

### 7. Populando a Tabela Projeto

**Comando Otimizado Descoberto:**
Durante o processo, foi descoberta uma forma mais eficiente de inserir múltiplos registros:

```sql
-- Inserindo múltiplos projetos em um único comando (método otimizado)
INSERT INTO projeto (nome, descricao, id_departamento) VALUES
('Website Corporativo', 'Criação do site institucional', 3),
('Campanha Publicitária', 'Marketing digital nas redes sociais', 1);
```

**Vantagens deste método:**
- Mais eficiente que comandos separados
- Reduz o número de transações
- Sintaxe mais limpa e organizada
- Funciona corretamente no DBeaver

## Consultas de Verificação

### 8. Consulta de Funcionários com Departamentos

```sql
-- Exibir todos os funcionários e seus departamentos
SELECT 
    funcionario.nome, 
    funcionario.cargo, 
    funcionario.salario,
    departamento.nome AS departamento
FROM funcionario
LEFT JOIN departamento ON funcionario.id_departamento = departamento.id_departamento;
```

**Resultado obtido:**
| Nome | Cargo | Salário | Departamento |
|------|-------|---------|--------------|
| Mariana Costa | Designer | 4.000 | Marketing |
| Ana Souza | Analista | 4.500 | Recursos Humanos |
| Carlos Silva | Desenvolvedor | 7.000 | TI |

### 9. Consulta de Projetos com Departamentos

```sql
-- Exibir todos os projetos e seus departamentos
SELECT 
    projeto.nome AS projeto, 
    projeto.descricao, 
    departamento.nome AS departamento
FROM projeto
LEFT JOIN departamento ON projeto.id_departamento = departamento.id_departamento;
```

**Resultado obtido:**
| Projeto | Descrição | Departamento |
|---------|-----------|--------------|
| Website Corporativo | Criação do site institucional | TI |
| Campanha Publicitária | Marketing digital nas redes sociais | Recursos Humanos |

## Problemas Encontrados e Soluções

### Problema 1: Sobreposição de Dados no DBeaver
**Descrição:** Ao inserir múltiplos registros em um comando, os dados eram sobrescritos na mesma linha.

**Solução:** Executar comandos INSERT separados para cada registro.

### Problema 2: Eficiência na Inserção
**Descoberta:** Método otimizado para inserção múltipla usando VALUES com múltiplas tuplas separadas por vírgula.

**Implementação:** Utilização do formato `VALUES (dados1), (dados2), (dados3);`

## Conceitos SQL Aplicados

### Chaves e Relacionamentos
- **PRIMARY KEY**: Identificação única de registros
- **FOREIGN KEY**: Estabelecimento de relacionamentos entre tabelas
- **SERIAL**: Geração automática de IDs sequenciais

### Constraints (Restrições)
- **NOT NULL**: Campos obrigatórios
- **CHECK**: Validação de valores (ex: salário >= 0)
- **ON DELETE SET NULL**: Comportamento ao excluir registros relacionados
- **ON DELETE CASCADE**: Exclusão em cascata

### Tipos de Dados
- **VARCHAR(n)**: Texto com limite de caracteres
- **TEXT**: Texto sem limite definido
- **DECIMAL(p,s)**: Números decimais com precisão específica
- **INT**: Números inteiros

### Operações JOIN
- **LEFT JOIN**: Incluir todos os registros da tabela à esquerda, mesmo sem correspondência

## Conclusão

O projeto resultou em um sistema funcional de gerenciamento de empresa com relacionamentos adequados entre departamentos, funcionários e projetos, demonstrando competência em design de banco de dados e resolução de problemas práticos.
