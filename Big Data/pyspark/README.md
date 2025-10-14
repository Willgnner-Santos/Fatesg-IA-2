# Relatório de Análise de Logs do Servidor da NASA com PySpark

**Autor:** Pedro Henrique PIres Vieira  
**Projeto:** Análise de dados dos logs de acesso dos servidores da NASA utilizando Apache Spark e sua API RDD.

---

## 1. Introdução

O objetivo deste projeto foi realizar uma análise exploratória sobre um conjunto de dados públicos contendo os logs de acesso aos servidores da NASA durante os meses de julho e agosto de 1995. Para lidar com o grande volume de dados, a ferramenta escolhida foi o **Apache Spark**, utilizando sua interface Python, o **PySpark**.

A análise foi conduzida especificamente com a API de baixo nível do Spark, os **Conjuntos de Dados Distribuídos Resilientes (RDDs)**. Essa escolha é particularmente adequada para o processamento de dados não estruturados ou semi-estruturados, como é o caso de arquivos de log em formato texto, permitindo grande flexibilidade e controle sobre as operações de transformação e agregação dos dados.

---

## 2. Descrição do Pipeline de Análise

O processo de análise foi estruturado em um pipeline executado em ambiente Google Colab. As etapas principais são descritas a seguir.

### 2.1. Preparação do Ambiente

A primeira célula do notebook foi dedicada à configuração do ambiente de execução, incluindo:
- **Instalação do OpenJDK 8:** O Apache Spark é executado sobre a Máquina Virtual Java (JVM), tornando a instalação do Java um pré-requisito obrigatório.
- **Instalação do PySpark:** Instalação da biblioteca Python que permite a comunicação com o motor do Spark.
- **Download e Descompactação dos Dados:** Os arquivos de log, originalmente compactados (`.gz`), foram baixados de um repositório Git e descompactados para leitura como arquivos de texto plano.

### 2.2. Inicialização do Spark e Carregamento dos Dados

Com o ambiente pronto, o próximo passo foi inicializar o Spark e carregar os dados:
- **`SparkConf` e `SparkContext`:** Um objeto `SparkContext` foi criado, servindo como ponto de entrada principal para as funcionalidades do Spark. Ele foi configurado para execução em modo local (`.setMaster("local")`), utilizando os recursos da máquina virtual do Colab.
- **Criação dos RDDs:** Os dois arquivos de log (`NASA_access_log_Jul95` e `NASA_access_log_Aug95`) foram carregados usando o método `sc.textFile()`. Cada arquivo foi transformado em um RDD, onde cada elemento corresponde a uma linha do arquivo de log (uma string).
- **Uso de `.cache()`:** Após a criação, os RDDs foram mantidos em memória usando o método `.cache()`. Essa otimização evita a releitura dos arquivos do disco a cada nova ação, acelerando significativamente as consultas subsequentes.

### 2.3. Transformações e Ações

O núcleo da análise foi realizado por meio de uma sequência de transformações (que definem operações a serem feitas) e ações (que executam as operações e retornam resultados).

Principais operações utilizadas:
- **`map(func)`:** Aplicada para extrair partes específicas de cada linha de log, como endereço IP do host, URL da requisição, código de status HTTP e dia da requisição.
- **`filter(func)`:** Utilizada para selecionar apenas elementos que satisfazem determinada condição, como requisições que resultaram em erro "404 Not Found".
- **`distinct()`:** Retorna um novo RDD contendo apenas elementos únicos do RDD original, sendo usada para contar o número de hosts únicos.
- **`reduceByKey(func)`:** Transformação fundamental para agregação em RDDs de pares chave-valor `(chave, valor)`. Foi utilizada para contar a frequência de URLs com erro 404 e o total de erros por dia, mapeando cada item de interesse para um par `(item, 1)` e somando os valores por chave.
- **`sortBy(keyFunc)`:** Usada para ordenar elementos do RDD, como no ranqueamento das URLs com mais erros (Top 5).
- **Ações (`count()`, `take()`, `reduce()`):** Comandos como `count()` (contar elementos), `take(n)` (obter os n primeiros elementos) e `reduce()` (agregar todos os elementos) foram usados para disparar os cálculos e trazer os resultados para o driver.

---

## 3. Apresentação dos Resultados

A execução do pipeline permitiu extrair as seguintes informações dos logs:

1. **Número de Hosts Distintos:**
   - Julho de 1995: **81.983** hosts únicos.
   - Agosto de 1995: **75.060** hosts únicos.

2. **Total de Erros 404 (Página não encontrada):**
   - Julho de 1995: **10.845** requisições.
   - Agosto de 1995: **10.056** requisições.

3. **Top 5 URLs que mais geraram Erros 404 em Agosto:**
   1. `/pub/winvn/readme.txt` (1337 ocorrências)
   2. `/pub/winvn/release.txt` (1185 ocorrências)
   3. `/shuttle/missions/STS-69/mission-STS-69.html` (683 ocorrências)
   4. `/images/nasa-logo.gif` (319 ocorrências)
   5. `/shuttle/missions/sts-68/ksc-upclose.gif` (253 ocorrências)

4. **Total de Bytes Transferidos:**
   - Julho de 1995: **38.695.973.491 bytes** (~38,7 GB).
   - Agosto de 1995: **26.828.341.424 bytes** (~26,8 GB).

---

## 4. Impressões sobre o Uso do PySpark com RDD

Trabalhar com a API de RDD do PySpark proporcionou uma visão fundamental sobre o funcionamento interno do Spark.

- **Pontos Positivos:** A abordagem funcional, baseada em transformações como `map` e `filter`, é extremamente poderosa e expressiva para manipulação de dados. A capacidade de encadear operações de forma clara e a execução "preguiçosa" (lazy evaluation), que otimiza o plano de execução, são características marcantes. Para dados brutos e não estruturados como logs, a flexibilidade do RDD é uma grande vantagem, pois não exige a definição de um esquema rígido.

- **Desafios:** A principal curva de aprendizado está em assimilar o paradigma de programação distribuída. A necessidade de estruturar as operações em transformações e ações, e entender que a computação só ocorre no momento da ação, pode ser confusa inicialmente. Além disso, operações de agregação, como contar frequências, exigem uma mentalidade de "chave-valor" (`reduceByKey`), que é menos direta do que em ferramentas como o Pandas.

- **Conclusão sobre a Ferramenta:** O RDD se mostrou uma ferramenta robusta e eficiente para a tarefa proposta. Embora APIs de mais alto nível como DataFrames e Spark SQL possam oferecer uma sintaxe mais simples e otimizações automáticas, compreender o RDD é essencial para entender a base do Spark e para resolver problemas que exigem um controle mais granular sobre o processamento dos dados.
