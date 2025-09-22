# Análise de Conceitos do Apache Spark com Paralelos a Bancos de Dados

[cite_start]Este repositório contém uma análise de conceitos fundamentais do Apache Spark, traçando paralelos com conhecimentos de bancos de dados para facilitar a compreensão[cite: 1].

## RDDs (Resilient Distributed Datasets)

[cite_start]Eu entendo os RDDs como uma estrutura análoga a uma tabela, porém distribuída e imutável[cite: 2]. [cite_start]Cada linha da fonte de dados se torna um registro, e as partições funcionam como subconjuntos desses dados[cite: 2]. [cite_start]Embora seja uma API de baixo nível, ela oferece controle total sobre as operações, o que é um grande diferencial[cite: 3].

## O Modelo de Execução: Transformações vs. Ações

[cite_start]A principal distinção no modelo de funcionamento do Spark está na sua execução "preguiçosa" (Lazy Evaluation)[cite: 4].

* **Transformações**: Operações como `map` e `filter` são declarativas. [cite_start]Elas podem ser comparadas à criação de uma `VIEW` ou à escrita de uma query em um banco de dados[cite: 5]. [cite_start]Eu defino a lógica do que quero fazer, mas nada é executado de imediato[cite: 5].
* [cite_start]**Ações**: A execução de fato só ocorre quando uma ação como `count` ou `collect` é chamada[cite: 6]. [cite_start]Esse momento é o equivalente a rodar o `SELECT` final que materializa o resultado[cite: 6].

[cite_start]Essa abordagem permite que o Spark otimize todo o plano de execução antes de iniciar o processamento, resultando em uma redução significativa do tráfego de rede e da latência[cite: 7].

## Otimização de Agregação: Shuffle e Combiner

[cite_start]A análise da contagem de URLs com erro 404 foi essencial para entender a otimização por trás da operação `reduceByKey`[cite: 8].

* [cite_start]**Shuffle**: Em um SGBD tradicional, agrupar dados exigiria uma operação custosa como um `JOIN` ou uma agregação complexa[cite: 9]. [cite_start]No Spark, o processo de mover os dados entre as partições para que fiquem no lugar certo para a agregação é chamado de "shuffle", e é uma operação de alto custo[cite: 10].
* [cite_start]**Combiner**: A grande vantagem do `reduceByKey()` é sua capacidade de usar um "combiner"[cite: 11]. [cite_start]Ele agrega os dados localmente em cada partição *antes* de iniciar o shuffle[cite: 11]. [cite_start]Isso minimiza a quantidade de dados que precisa ser transferida pela rede[cite: 11]. [cite_start]Essa lógica funciona como uma pré-agregação inteligente, similar a uma boa estratégia de indexação que otimiza consultas em bancos de dados[cite: 12].

## Persistência em Memória com `.cache()`

[cite_start]Outro ponto que chamou a atenção foi o uso de `.cache()` para persistência em memória[cite: 13]. [cite_start]Quando um mesmo RDD, como o `erros404_julho`, precisa ser utilizado em múltiplas operações, o Spark armazena seu resultado[cite: 14]. [cite_start]Isso evita que todas as transformações que o geraram sejam reexecutadas a cada nova ação, proporcionando um ganho de performance crucial[cite: 14, 15].