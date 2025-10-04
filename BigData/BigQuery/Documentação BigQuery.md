# Documentação - Exercícios BigQuery

## Índice

1. [Introdução](#introdução)
2. [Ambiente e Configuração](#ambiente-e-configuração)
3. [Exercícios Realizados](#exercícios-realizados)
   - [Exercício 1: Contar o número total de filmes](#exercício-1-contar-o-número-total-de-filmes)
   - [Exercício 2: Agrupar filmes por ano de lançamento](#exercício-2-agrupar-filmes-por-ano-de-lançamento)
   - [Exercício 3: Filtrar filmes por gênero específico](#exercício-3-filtrar-filmes-por-gênero-específico)
4. [Consultas Adicionais Exploradas](#consultas-adicionais-exploradas)
5. [Conclusão](#conclusão)

---

## Introdução

Esta documentação apresenta a realização completa dos exercícios realizados no **Google BigQuery** com foco em consultas SQL sobre um dataset de filmes do IMDB. O objetivo foi praticar operações básicas e intermediárias de SQL, incluindo seleção, filtragem, ordenação, agregação e agrupamento de dados.

---

## Ambiente e Configuração

### Projeto BigQuery
- **Projeto ID**: `projetoa1-470900`
- **Dataset**: `2025_2`
- **Tabela**: `IMDB_TOP_1000`

### Estrutura da Tabela
A tabela contém informações sobre os 1000 filmes mais bem avaliados do IMDB, incluindo:
- `Series_Title`: Título do filme
- `Released_Year`: Ano de lançamento
- `IMDB_Rating`: Avaliação no IMDB
- `Genre`: Gênero(s) do filme
- `Certificate`: Classificação etária
- `Runtime`: Duração do filme
- `Poster_Link`: Link do pôster

---

## Exercícios Realizados

### Exercício 1: Contar o número total de filmes

**Objetivo**: Determinar quantos filmes existem na tabela.

**Consulta SQL**:
```sql
SELECT COUNT(*) AS total_filmes
FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
```

**Resultado**:
- **Total de filmes**: 1000

**Análise**: A tabela contém exatamente 1000 registros, correspondendo aos filmes mais bem avaliados do IMDB.

---

### Exercício 2: Agrupar filmes por ano de lançamento

**Objetivo**: Contar quantos filmes foram lançados em cada ano e ordenar os resultados.

**Consulta SQL**:
```sql
SELECT Released_Year AS ano_lancamento,
  COUNT(*) AS quantidade_filmes
FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
GROUP BY Released_Year
ORDER BY Released_Year DESC
```

**Amostra dos Resultados**:

| ano_lancamento | quantidade_filmes |
|----------------|-------------------|
| 2020           | 6                 |
| 2019           | 23                |
| 2018           | 19                |
| 2017           | 22                |
| 2016           | 28                |
| 2015           | 25                |
| 2014           | 32                |
| 2013           | 28                |

**Análise**: 
- O ano com maior número de filmes no top 1000 foi **2014** (32 filmes)
- Há uma boa distribuição de filmes ao longo das décadas

---

### Exercício 3: Filtrar filmes por gênero específico

**Objetivo**: Buscar filmes que pertencem ao gênero "Thriller".

**Consulta SQL**:
```sql
SELECT Series_Title, Genre, IMDB_Rating
FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
WHERE Genre LIKE '%Thriller%'
```

**Amostra dos Resultados**:

| Series_Title              | Genre                      | IMDB_Rating |
|---------------------------|----------------------------|-------------|
| Gisaengchung             | Comedy, Drama, Thriller    | 8.6         |
| The Silence of the Lambs | Crime, Drama, Thriller     | 8.6         |
| Joker                    | Crime, Drama, Thriller     | 8.5         |
| The Departed             | Crime, Drama, Thriller     | 8.5         |
| The Usual Suspects       | Crime, Mystery, Thriller   | 8.5         |
| Psycho                   | Horror, Mystery, Thriller  | 8.5         |
| Shutter Island           | Mystery, Thriller          | 8.2         |
| Die Hard                 | Action, Thriller           | 8.2         |

**Análise**:
- Foram encontrados **137 filmes** com o gênero Thriller
- As avaliações variam entre 8.1 e 8.6
- Thriller frequentemente aparece combinado com outros gêneros (Drama, Crime, Mystery)

---

## Consultas Adicionais Exploradas

Durante o desenvolvimento dos exercícios, outras consultas foram realizadas para explorar o dataset:

### 1. Filmes com melhor avaliação
```sql
SELECT Series_Title, IMDB_Rating
FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
ORDER BY IMDB_Rating DESC
LIMIT 100
```

**Top 5 Filmes**:
1. The Shawshank Redemption - 9.3
2. The Godfather - 9.2
3. 12 Angry Men - 9.0
4. The Godfather: Part II - 9.0
5. The Dark Knight - 9.0

### 2. Filmes com avaliação acima de 8.0
```sql
SELECT Series_Title, Released_Year, IMDB_Rating
FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
WHERE IMDB_Rating > 8
LIMIT 5
```

### 3. Filmes lançados após 2000
```sql
SELECT * FROM `projetoa1-470900.2025_2.IMDB_TOP_1000`
WHERE CAST(Released_Year AS INT64) > 2000
LIMIT 5
```

---

## Conclusão

Os exercícios foram concluídos com sucesso, demonstrando proficiência nas operações fundamentais de SQL no Google BigQuery. As consultas realizadas permitiram extrair insights valiosos sobre o dataset de filmes do IMDB, incluindo padrões de distribuição temporal, análise de gêneros e identificação dos filmes mais bem avaliados.

O uso do BigQuery mostrou-se eficiente para análise de dados estruturados, com interface intuitiva e execução rápida das consultas, mesmo em datasets maiores.
