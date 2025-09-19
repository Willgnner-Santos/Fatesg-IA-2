# Exercício de BigQuery: Análise de Dados de Filmes e Séries

Este projeto documenta meu processo de aprendizado e a execução de consultas em BigQuery para analisar um conjunto de dados do IMDB. O objetivo foi explorar, filtrar e agregar dados para obter informações relevantes sobre filmes e séries. As consultas foram executadas no console do Google Cloud, e os resultados foram documentados em capturas de tela.

## Caminho de Aprendizagem

Minha jornada com este exercício foi dividida em etapas, começando com consultas simples para entender a estrutura dos dados e evoluindo para análises mais complexas.

### 1. Primeiras Consultas e Exploração

Para começar, explorei o conjunto de dados para entender sua estrutura. A primeira consulta que executei foi uma seleção simples para ver as colunas `Series_Title`, `Released_Year`, e `IMDB_Rating`. O `LIMIT 5` foi crucial para garantir que a consulta retornasse apenas uma pequena amostra, o que é uma boa prática ao trabalhar com grandes conjuntos de dados.

```sql
-- Consulta inicial para explorar as colunas relevantes
SELECT
  Series_Title,
  Released_Year,
  IMDB_Rating
FROM
  `clear-variety-470900.s_2025_2.IMD_top_10000`
LIMIT 5;