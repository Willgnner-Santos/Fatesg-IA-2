# Análise de Chess Games com Big Data

# Projeto acadêmico de análise exploratória de grandes volumes de partidas de xadrez, utilizando técnicas de Big Data, SQL Analytics e processamento PySpark.

# 

# Objetivo

# O projeto visa investigar padrões, estatísticas e tendências em partidas de xadrez a partir de um grande conjunto de dados, utilizando transformações, queries analíticas e visualização dos resultados.

# 

# Base de Dados

# Fonte: Kaggle - Chess Games Dataset (arevel/chess-games)

# 

# Formato Original: CSV

# 

# Estrutura do Projeto

# 00.-Pyspark-transform.py: Script Python/PySpark para:

# 

# Limpeza e transformação dos dados brutos;

# 

# Remoção de colunas e linhas irrelevantes ou nulas;

# 

# Conversão e criação de colunas de timestamp;

# 

# Processamento dos movimentos anotados dos jogadores (criação de colunas WhiteMoves e BlackMoves a partir do campo AN);

# 

# Exportação do dataset final como chessgamestransformed.csv.​

# 

# Arquivos .csv de saída, correspondendo a diferentes etapas ou perguntas analisadas:

# 

# Brancas-vs-Pretas.csv: Tabela de vitórias de brancas, pretas e empates por tipo de evento.

# 

# Ratingdiff-por-ELO.csv: Variação média de Rating por faixas de Elo.

# 

# Aberturas-por-ELO.csv: Aberturas mais usadas em cada faixa de Elo.

# 

# Termino-por-evento.csv: Modos de término de partida por tipo de evento.

# 

# Pecas-Checkmate.csv: Peças mais usadas para dar mate.

# 

# Consultas SQL (imagens .jpg anexas): Queries utilizadas nas etapas analíticas, com exemplos de:

# 

# Agrupamentos e contagens por Resultado (vitórias, empates);

# 

# Cálculo de métricas e agrupamento por faixa de Elo;

# 

# Identificação das aberturas principais por faixa de Elo;

# 

# Estatísticas de modo de término das partidas;

# 

# Análise dos mates por peça responsável.

# 

# Visualizações (.jpg):

# 

# Gráficos demonstrando resultados de queries, como: média de variação do Elo, mates por peça, modos de término por evento.

# 

# Principais Bibliotecas Utilizadas

# PySpark (estrutura SparkSession, funções SQL e UDFs)

# 

# SQL/BigQuery para análise e queries sobre os dados

# 

# Ferramentas de visualização como Power BI, Tableau ou similares (para construção dos gráficos finais)

# 

# Como Executar

# Pré-requisitos:

# 

# Ambiente configurado com Python 3.x e PySpark

# 

# Dataset original baixado do Kaggle: Chess Games Dataset

# 

# Processamento inicial:

# 

# Executar o script 00.-Pyspark-transform.py para limpar e processar os dados brutos.

# 

# O resultado será salvo como chessgamestransformed.csv.

# 

# Análises:

# 

# Utilizar as queries SQL fornecidas para gerar os outputs desejados.

# 

# As tabelas resultantes e gráficos estão nos arquivos .csv e .jpg anexos.

# 

# Visualização:

# 

# Recomenda-se importar os CSVs em uma ferramenta de BI para replicar e customizar as visualizações.

# 

# Créditos

# Autores: Bruno Matheus, Jorge Vinícius , José Roberto Pasian Neto, Rafael Machado , Lucas Faria

# 

# Dataset: Kaggle Chess Games Dataset

