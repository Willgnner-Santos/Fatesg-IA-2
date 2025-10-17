# Exercício de BigQuery: Análise de Dados de Filmes e Séries

[cite_start]Este projeto documenta meu processo de aprendizado e a execução de consultas em **BigQuery** para analisar um conjunto de dados do IMDB[cite: 1]. [cite_start]O objetivo principal foi explorar, filtrar e agregar dados para extrair informações relevantes sobre filmes e séries[cite: 2]. [cite_start]Todas as consultas foram executadas diretamente no console do Google Cloud, com os resultados documentados em capturas de tela[cite: 3].

---

## Metodologia e Processo de Análise

[cite_start]A metodologia adotada para este exercício seguiu um fluxo de trabalho estruturado, progredindo de uma exploração inicial dos dados para análises mais aprofundadas[cite: 4].

### 1. Exploração Inicial do Conjunto de Dados

[cite_start]A primeira etapa consistiu em uma exploração para compreender a estrutura e o conteúdo do conjunto de dados[cite: 5]. [cite_start]Para isso, foi utilizada uma consulta inicial para visualizar as colunas `Series_Title`, `Released_Year` e `IMDB_Rating`[cite: 6]. [cite_start]A cláusula `LIMIT 5` foi empregada estrategicamente para restringir o resultado a uma pequena amostra, o que é considerada uma boa prática ao lidar com grandes volumes de dados[cite: 7].

```sql
-- Consulta inicial para explorar as colunas relevantes
SELECT
  Series_Title,
  Released_Year,
  IMDB_Rating
FROM
  `clear-variety-470900.s_2025_2.IMD_top_10000`
LIMIT 5;
[cite_start]``` [cite: 8]