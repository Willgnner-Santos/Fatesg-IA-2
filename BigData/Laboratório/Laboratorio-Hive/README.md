# Relatório Técnico: Otimização de Queries e Análise em Larga Escala com Apache Hive

##  Visão Geral
Este documento detalha a implementação de um laboratório prático de engenharia de dados utilizando o Apache Hive. O objetivo foi não apenas processar e analisar datasets de voos e clima, mas também aplicar boas práticas de otimização para garantir eficiência em larga escala. A infraestrutura base foi construída sobre o Hadoop Distributed File System (HDFS).

---

## 1. Preparação do Ambiente e Ingestão de Dados

O primeiro passo foi a ingestão controlada dos dados, seguindo o padrão EL (Extract/Load) do fluxo ETL. O dataset de voos (`flightdelays.csv`) e o de clima (`sfo_weather.csv`) foram obtidos e preparados para serem transferidos para o ecossistema Hadoop.

###  Estruturação Lógica do HDFS
Criei os diretórios de destino no HDFS para separar logicamente os datasets, uma prática recomendada para futuros pipelines de ingestão e particionamento.

```bash
hdfs dfs -mkdir -p /user/maria_dev/datasets/voos
hdfs dfs -mkdir -p /user/maria_dev/datasets/clima
 Ingestão de Dados
Os arquivos foram transferidos do sistema de arquivos local (/home/maria_dev/arquiteturadedados/) para os diretórios HDFS recém-criados. O comando hdfs dfs -put garante que os dados estejam disponíveis para processamento distribuído.

bash
hdfs dfs -put /home/maria_dev/arquiteturadedados/flightdelays.csv /user/maria_dev/datasets/voos/
hdfs dfs -put /home/maria_dev/arquiteturadedados/sfo_weather.csv /user/maria_dev/datasets/clima/
 2. Modelagem de Dados e Otimização no Hive
A modelagem no Hive não se limitou à criação de tabelas, mas incluiu a escolha de formatos de arquivo e estratégias de particionamento e bucketing para maximizar a performance das consultas.

 Tabela de Voos: flightdelays
A tabela flightdelays foi criada como uma tabela externa. Essa abordagem é ideal para garantir que os metadados no Hive (a estrutura da tabela) estejam desacoplados dos dados brutos no HDFS. Isso previne a perda de dados caso a tabela seja acidentalmente removida (DROP TABLE).

sql
DROP TABLE IF EXISTS flightdelays;
CREATE EXTERNAL TABLE flightdelays (
    -- Tipos de dados rigorosamente definidos para otimização de armazenamento e consulta.
    Year INT, Month INT, DayofMonth INT, DayOfWeek INT,
    DepTime INT, CRSDepTime INT, ArrTime INT, CRSArrTime INT,
    UniqueCarrier STRING, FlightNum INT, TailNum STRING,
    ActualElapsedTime INT, CRSElapsedTime INT, AirTime INT,
    ArrDelay INT, DepDelay INT, Origin STRING, Dest STRING,
    Distance INT, TaxiIn INT, TaxiOut INT, Cancelled INT,
    CancellationCode STRING, Diverted INT, CarrierDelay INT,
    WeatherDelay INT, NASDelay INT, SecurityDelay INT,
    LateAircraftDelay INT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/datasets/voos/';
 Tabela de Clima: sfo_weather
Para a tabela de clima, apliquei uma estratégia de conversão de formato de arquivo. O arquivo CSV (TEXTFILE), que é ineficiente para leitura analítica, foi ingerido em uma tabela temporária. Em seguida, os dados foram convertidos para o formato Optimized Row Columnar (ORC), um formato de armazenamento otimizado para o ecossistema Hadoop.

 Benefícios do ORC:
Compressão: Reduz o tamanho do arquivo no disco, economizando espaço e diminuindo o tempo de I/O.

Armazenamento Colunar: Permite que o Hive leia apenas as colunas necessárias para uma consulta, em vez de escanear toda a linha, o que acelera drasticamente as queries.

sql
-- Etapa 1: Tabela temporária para ingestão do CSV
DROP TABLE IF EXISTS sfo_weather_txt;
CREATE TABLE sfo_weather_txt (
    station_name STRING, Year INT, Month INT, DayOfMonth INT,
    precipitation INT, temperature_max INT, temperature_min INT
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA INPATH '/user/maria_dev/datasets/clima/sfo_weather.csv'
OVERWRITE INTO TABLE sfo_weather_txt;

-- Etapa 2: Tabela final em formato ORC
DROP TABLE IF EXISTS sfo_weather;
CREATE TABLE sfo_weather (
    station_name STRING, Year INT, Month INT, DayOfMonth INT,
    precipitation INT, temperature_max INT, temperature_min INT
)
STORED AS ORC;

-- Inserção e conversão de formato
INSERT INTO TABLE sfo_weather SELECT * FROM sfo_weather_txt;
 3. Análise e Otimização de Consultas (HiveQL)
As consultas foram planejadas não apenas para extrair dados, mas também para demonstrar as vantagens do processamento distribuído e da otimização.

 Análise de Desempenho
A otimização de consultas no Hive depende diretamente do motor de execução utilizado (MapReduce, Tez ou Spark). Para este laboratório, o ideal é configurar o Tez, que é o padrão e mais performático para o processamento de DAGs (Directed Acyclic Graphs).

 Exemplos de Consultas Analíticas
 Atraso Médio de Voos por Destino Específico:
Essa consulta simples demonstra o poder do processamento em massa. A cláusula WHERE restringe a leitura de dados, e a função de agregação AVG é executada de forma distribuída.

sql
SELECT AVG(ArrDelay) AS media_atraso_den
FROM flightdelays
WHERE Dest = 'DEN';
 Atraso Médio de Voos em Rota Específica:
Uma consulta mais complexa que une duas condições para obter uma métrica mais granular.

sql
SELECT AVG(ArrDelay) AS media_atraso_lax_sfo
FROM flightdelays
WHERE Origin = 'LAX' AND Dest = 'SFO';
 Análise de Top N e Desempenho:
O uso de ORDER BY com LIMIT força uma operação de ordenação global, que pode ser custosa. Em um ambiente de produção, seria crucial analisar o plano de execução para garantir que a ordenação seja eficiente, possivelmente utilizando sort-merge ou outras otimizações do motor Tez.

sql
SELECT ArrDelay
FROM flightdelays
ORDER BY ArrDelay DESC
LIMIT 10;

 