# Atividades de Consulta SQL com BigQuery

Este repositório contém a resolução de exercícios de SQL utilizando o Google BigQuery. O objetivo foi praticar a manipulação e extração de dados de uma tabela de filmes, aplicando conceitos de contagem, agrupamento e filtragem.

## Descrição dos Exercícios

As consultas foram desenvolvidas para responder a três questões específicas, conforme solicitado no arquivo de exercícios.

### 1. Contagem do Número Total de Filmes

O primeiro exercício consistiu em realizar uma contagem simples para determinar o número total de registros (filmes) presentes na tabela. 

**SQL Query:**

SELECT
COUNT(Series_Title)
FROM
big-data-fatesg.2025_1.top_filmes

text

**Resultado:**

A consulta utilizou a função `COUNT()` na coluna `Series_Title` para contar todas as linhas. O resultado, como visto na imagem `n_de_filmes.png`, foi **1000**, indicando que a tabela contém mil filmes.

---

### 2. Contagem de Filmes por Ano de Lançamento

O segundo exercício buscou agrupar os filmes pelo ano de lançamento e contar a quantidade de produções em cada ano. 

**SQL Query:**

SELECT
Released_Year,
COUNT(*) AS Series_Title
FROM
2025_1.top_filmes
GROUP BY
Released_Year
ORDER BY
Released_Year

text

**Resultado:**

A consulta agrupou os dados pela coluna `Released_Year` e contou (`COUNT(*)`) o número de filmes em cada grupo. O resultado, visível na imagem `n_de_filmes_por_ano.png`, é uma tabela que lista cada ano e o respectivo número de filmes lançados, ordenada cronologicamente.

---

### 3. Filtragem de Filmes por Gênero

O terceiro exercício teve como objetivo filtrar a tabela para exibir apenas os filmes que pertencem a um gênero específico. Para este exemplo, o gênero escolhido foi **"Comedy"**.

**SQL Query:**

SELECT
Series_Title,
IMDB_Rating,
Genre
FROM
2025_1.top_filmes
WHERE
Genre = 'Comedy';

text

**Resultado:**

Utilizando a cláusula `WHERE`, a consulta filtrou a tabela para retornar apenas as linhas em que a coluna `Genre` continha o valor `Comedy`. A imagem `filme_por_genero.png` mostra o resultado: uma lista com o título, a nota do IMDB e o gênero dos filmes que atendem a esse critério.
Se desejar, posso também ajudar a organizar isso em um arquivo .md para download.Aqui está o texto formatado em Markdown (.md) para as Atividades de Consulta SQL com BigQuery:

text
# Atividades de Consulta SQL com BigQuery

Este repositório contém a resolução de exercícios de SQL utilizando o Google BigQuery. O objetivo foi praticar a manipulação e extração de dados de uma tabela de filmes, aplicando conceitos de contagem, agrupamento e filtragem.

## Descrição dos Exercícios

As consultas foram desenvolvidas para responder a três questões específicas, conforme solicitado no arquivo de exercícios.

### 1. Contagem do Número Total de Filmes

O primeiro exercício consistiu em realizar uma contagem simples para determinar o número total de registros (filmes) presentes na tabela. 

**SQL Query:**

SELECT
COUNT(Series_Title)
FROM
big-data-fatesg.2025_1.top_filmes

text

**Resultado:**

A consulta utilizou a função `COUNT()` na coluna `Series_Title` para contar todas as linhas. O resultado, como visto na imagem `n_de_filmes.png`, foi **1000**, indicando que a tabela contém mil filmes.

---

### 2. Contagem de Filmes por Ano de Lançamento

O segundo exercício buscou agrupar os filmes pelo ano de lançamento e contar a quantidade de produções em cada ano. 

**SQL Query:**

SELECT
Released_Year,
COUNT(*) AS Series_Title
FROM
2025_1.top_filmes
GROUP BY
Released_Year
ORDER BY
Released_Year

text

**Resultado:**

A consulta agrupou os dados pela coluna `Released_Year` e contou (`COUNT(*)`) o número de filmes em cada grupo. O resultado, visível na imagem `n_de_filmes_por_ano.png`, é uma tabela que lista cada ano e o respectivo número de filmes lançados, ordenada cronologicamente.

---

### 3. Filtragem de Filmes por Gênero

O terceiro exercício teve como objetivo filtrar a tabela para exibir apenas os filmes que pertencem a um gênero específico. Para este exemplo, o gênero escolhido foi **"Comedy"**.

**SQL Query:**

SELECT
Series_Title,
IMDB_Rating,
Genre
FROM
2025_1.top_filmes
WHERE
Genre = 'Comedy';

text

**Resultado:**

Utilizando a cláusula `WHERE`, a consulta filtrou a tabela para retornar apenas as l
