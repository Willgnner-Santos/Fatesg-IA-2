# Análise de Logs da NASA com PySpark

## Visão Geral do Projeto

Este projeto demonstra um pipeline de processamento de Big Data usando **PySpark** para analisar logs de acesso HTTP da NASA. A análise é baseada em arquivos de log dos meses de julho e agosto de 1995. O objetivo é extrair métricas de negócio relevantes, como a quantidade de hosts únicos, o total de bytes transferidos e os erros mais comuns (HTTP 404).

## Conceitos Fundamentais Utilizados

O pipeline foi construído para ensinar conceitos essenciais do Spark, com uma abordagem prática e intuitiva:

* [cite_start]**O Problema da Planilha Gigante:** Analisar arquivos de logs massivos em um computador comum seria impossível[cite: 5, 6]. [cite_start]O PySpark resolve isso, dividindo o conjunto de dados em pedaços menores, chamados **partições** [cite: 9][cite_start], que são distribuídos para processamento paralelo[cite: 14].

* [cite_start]**RDDs (Resilient Distributed Datasets):** A análise utiliza RDDs, a API de baixo nível do Spark [cite: 15][cite_start], que são coleções de dados distribuídas e imutáveis[cite: 15]. [cite_start]Cada linha de log é tratada como um elemento de um RDD[cite: 16].

* [cite_start]**Transformações vs. Ações:** O Spark trabalha com um modelo de **avaliação preguiçosa**[cite: 21]. [cite_start]As **transformações** (`map`, `filter`, `reduceByKey`) [cite: 22] [cite_start]apenas definem o plano de execução [cite: 20] [cite_start]e não processam os dados imediatamente[cite: 20]. [cite_start]O processamento só é disparado quando uma **ação** (`count`, `collect`) [cite: 24] [cite_start]é chamada, permitindo que o Spark otimize o trabalho antes de executá-lo[cite: 31].

* [cite_start]**"Shuffle" e "Combiner":** Para agregar dados, o Spark precisa mover as informações entre os "trabalhadores" (executors), um processo chamado *shuffle*[cite: 35, 36]. [cite_start]O `reduceByKey()` utiliza um **"Combiner"** [cite: 38][cite_start], que faz uma agregação local nas partições antes do *shuffle* [cite: 39][cite_start], tornando o processo de contagem e soma muito mais eficiente do que enviar todos os dados[cite: 40, 41]. [cite_start]Por isso, o `reduceByKey()` é preferível ao `groupByKey()`[cite: 42].

* [cite_start]**Cache/Persist:** O comando `.cache()` é utilizado para armazenar os RDDs na memória[cite: 45]. [cite_start]Isso é crucial para evitar que o Spark recompute os mesmos dados várias vezes, melhorando a performance de operações subsequentes[cite: 46].

## Análises Realizadas

O pipeline extrai as seguintes métricas dos logs:

* Contagem de hosts únicos.
* Total de bytes transferidos por mês.
* Número de erros HTTP 404.
* As 5 URLs que mais geraram erros 404.
* A distribuição de erros 404 por dia.

## Relatório e Impressões

[cite_start]A metodologia aplicada é uma excelente introdução ao universo do Big Data[cite: 50]. [cite_start]Abordar um problema real de análise de logs demonstra de forma prática os fundamentos do Spark, como RDDs, transformações, ações e otimizações de performance[cite: 51]. [cite_start]Essa é uma abordagem didática que constrói o conhecimento passo a passo, desde a configuração do ambiente até a extração de métricas de negócio importantes[cite: 52].