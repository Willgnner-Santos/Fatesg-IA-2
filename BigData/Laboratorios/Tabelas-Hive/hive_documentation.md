# Documentação - Manipulação de Dados com Apache Hive via Ambari

## Objetivo
Esta documentação demonstra o uso do Apache Hive para criação e manipulação de tabelas de dados estruturados, incluindo diferentes tipos de dados e resolução de problemas de conectividade e encoding.

## Ambiente de Execução
- **Plataforma**: Hortonworks Sandbox via Ambari
- **Interface**: Hive CLI através de SSH
- **Usuário**: maria_dev
- **Banco de dados**: default

## Problema Inicial e Solução

### Problema de Conectividade
**Descrição:** Inicialmente, a conexão com o Hive estava sendo recusada, impedindo a execução de qualquer comando.

**Diagnóstico:** O serviço do Hive não vem ativado por padrão no Hortonworks Sandbox.

**Solução Aplicada:**
1. Acessar a interface web do Ambari
2. Navegar até os serviços e localizar o **Hive**
3. Clicar em **Service Actions**
4. Iniciar o serviço do Hive

**Resultado:** Conexão estabelecida com sucesso, permitindo a execução dos comandos.

## Execução do Tutorial Base

### 1. Seleção do Banco de Dados
```sql
USE default;
```

**Resultado:** `OK` - Banco de dados padrão selecionado
**Tempo de execução:** 0.997 segundos

### 2. Criação da Tabela de Exemplo (alunos)

```sql
CREATE TABLE alunos (
    id INT,
    nome STRING,
    curso STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

**Resultado:** `OK` - Tabela criada com sucesso
**Tempo de execução:** 0.337 segundos

### 3. Inserção de Dados de Teste

```sql
INSERT INTO alunos VALUES
(1, 'Maria', 'Big Data'),
(2, 'João', 'Engenharia de Dados'),
(3, 'Ana', 'Ciência de Dados');
```

**Resultado:** Job executado com sucesso no cluster YARN
- **Query ID:** maria_dev_20250923181125_c8354081-71c4-4595-8c4e-40438a63b2d2
- **Status:** SUCCEEDED (1 Map task executado)

### 4. Consulta dos Dados Inseridos

```sql
SELECT * FROM alunos;
```

**Resultado:**
| ID | Nome | Curso |
|----|------|-------|
| 1 | Maria | Big Data |
| 2 | João | Engenharia de Dados |
| 3 | Ana | Ciência de Dados |

**Tempo de execução:** 0.133 segundos

### 5. Limpeza da Tabela de Teste

```sql
DROP TABLE alunos;
```

**Resultado:** `OK` - Tabela removida com sucesso
**Tempo de execução:** 0.526 segundos

## Implementação das Tabelas Solicitadas

### Tabela 1: Cidades

#### Criação da Estrutura
```sql
CREATE TABLE cidades (
    id INT,
    nome STRING,
    estado STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

**Resultado:** `OK` - Tabela criada
**Tempo de execução:** 0.286 segundos

#### Inserção dos Dados
```sql
INSERT INTO cidades VALUES
(1, 'Goiânia', 'Goiás'),
(2, 'São Paulo', 'São Paulo'),
(3, 'Londrina', 'Paraná');
```

**Resultado:** Job MapReduce executado com sucesso
- **Query ID:** maria_dev_20250923183407_46280271-4571-4177-8e6e-51a7e838eb63
- **Status:** SUCCEEDED
- **Dados carregados:** 3 linhas, 61 bytes

#### Consulta dos Resultados
```sql
SELECT * FROM cidades;
```

**Resultado:**
| ID | Nome | Estado |
|----|------|--------|
| 1 | Goiânia | Goiás |
| 2 | São Paulo | São Paulo |
| 3 | Londrina | Paraná |

### Tabela 2: Filmes

#### Tentativa Inicial com Problema de Encoding
```sql
CREATE TABLE filmes (
    nota FLOAT,
    nome STRING,
    lançamento INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

**Problema Identificado:** O Hive apresentou erro ao processar o caractere "ç" na palavra "lançamento".

**Erro obtido:**
```
NoViableAltException(26@[])
FAILED: ParseException Error near 'çamento' 'INT'
```

#### Solução e Correção
**Diagnóstico:** O Hive não processa corretamente caracteres especiais em nomes de colunas.

**Correção aplicada:** Substituição de "lançamento" por "ano"

```sql
USE default;
CREATE TABLE filmes (
    nota FLOAT,
    nome STRING,
    ano INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

**Resultado:** `OK` - Tabela criada com sucesso
**Tempo de execução:** 0.33 segundos

#### Inserção dos Dados
```sql
INSERT INTO filmes VALUES
(8.8, 'Pulp Fiction', 1994),
(9.0, 'Senhor dos Anéis III', 2003),
(9.1, 'Batman Dark Knight', 2008);
```

**Resultado:** Job executado com sucesso
- **Query ID:** maria_dev_20250923185117_50450c41-9c05-42dd-9a30-577d016c416e
- **Status:** SUCCEEDED
- **Dados carregados:** 3 linhas, 81 bytes

#### Consulta dos Resultados Finais
```sql
SELECT * FROM filmes;
```

**Resultado:**
| Nota | Nome | Ano |
|------|------|-----|
| 8.8 | Pulp Fiction | 1994 |
| 9.0 | Senhor dos Anéis III | 2003 |
| 9.1 | Batman Dark Knight | 2008 |

**Tempo de execução:** 0.165 segundos

## Análise Técnica dos Problemas Encontrados

### 1. Conectividade com Hive
**Problema:** Serviço não inicializado por padrão
**Solução:** Ativação manual via Ambari
**Impacto:** Bloqueio total inicial das operações

### 2. Encoding de Caracteres Especiais
**Problema:** Caractere "ç" não suportado em nomes de colunas
**Solução:** Substituição por caracteres ASCII padrão
**Impacto:** Necessidade de adaptação da nomenclatura

### 3. Performance dos Jobs MapReduce
**Observação:** Cada INSERT gera um job MapReduce completo
**Resultado:** Processamento distribuído mesmo para pequenos volumes de dados

## Tipos de Dados Utilizados

| Tipo | Exemplo | Uso |
|------|---------|-----|
| INT | id, ano | Números inteiros |
| STRING | nome, estado | Texto variável |
| FLOAT | nota | Números decimais |


## Comandos de Gerenciamento Utilizados

### Administração de Tabelas
```sql
-- Listar tabelas
SHOW TABLES;

-- Descrever estrutura
DESCRIBE nome_tabela;

-- Remover tabela
DROP TABLE nome_tabela;
```

### Consultas de Dados
```sql
-- Selecionar todos os dados
SELECT * FROM nome_tabela;

-- Contar registros
SELECT COUNT(*) FROM nome_tabela;
```

## Lições Aprendidas

### Melhores Práticas Identificadas:
1. **Verificar serviços:** Sempre confirmar se o Hive está ativo no Ambari
2. **Nomenclatura:** Usar apenas caracteres ASCII em nomes de colunas
3. **Tipos de dados:** Escolher tipos apropriados (FLOAT para decimais, STRING para texto)
4. **Monitoramento:** Acompanhar jobs via interface YARN

### Problemas Comuns e Soluções:
- **Conectividade:** Ativar serviços via Ambari
- **Encoding:** Evitar caracteres especiais
- **Performance:** Considerar que INSERTs geram jobs MapReduce

## Conclusão

O Apache Hive mostrou-se uma ferramenta robusta para processamento de dados estruturados em ambiente distribuído, executando operações através de jobs MapReduce mesmo para volumes pequenos de dados. A experiência destacou a importância da configuração adequada do ambiente e da atenção aos detalhes de encoding ao trabalhar com dados em português.
