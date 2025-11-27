# Laboratório de Hive

Este é um registro do meu aprendizado e da execução de um exercício de laboratório utilizando **Hive**, uma ferramenta de *data warehouse* construída sobre o Hadoop. O objetivo foi explorar, processar e analisar dados de voos e clima, simulando um ambiente de big data.

---

## 1. Configuração do Ambiente e Ingestão de Dados

A primeira etapa foi preparar o ambiente e carregar os dados.

Primeiro, clonei o repositório de dados do GitHub para ter os arquivos necessários localmente:
```bash
git clone [https://github.com/leonardorim/arquiteturadedados.git](https://github.com/leonardorim/arquiteturadedados.git)
Em seguida, criei diretórios no HDFS para armazenar os dados, organizando-os de forma lógica. Utilizei o comando mkdir -p para criar os diretórios flightdelays/ e sfo_weather/ de uma vez.
Bash
hdfs dfs -mkdir -p /user/maria_dev/flightdelays/
hdfs dfs -mkdir -p /user/maria_dev/sfo_weather/
Com os diretórios prontos, carreguei os arquivos CSV correspondentes para o HDFS, utilizando o comando put.
Bash
hdfs dfs -put /user/maria_dev/arquiteturadedados/flightdelays.csv /user/maria_dev/flightdelays/
hdfs dfs -put /user/maria_dev/arquiteturadedados/sfo_weather.csv /user/maria_dev/sfo_weather/
2. Criação das Tabelas no Hive
Com os dados no HDFS, criei as tabelas no Hive para que eu pudesse executar consultas SQL sobre eles.
Para a tabela de atrasos de voos, flightdelays, a criei como uma tabela externa para não gerenciar o ciclo de vida dos dados, mantendo o arquivo original no HDFS. Especifiquei a lista completa de colunas e seus tipos de dados. A tabela usa o delimitador de campos ',' e o formato de arquivo TEXTFILE, com a localização apontando para o diretório no HDFS que criei na etapa anterior.
SQL
DROP TABLE IF EXISTS flightdelays;
CREATE EXTERNAL TABLE flightdelays (
    Year INT,
    Month INT,
    DayofMonth INT,
    DayOfWeek INT,
    DepTime INT,
    CRSDepTime INT,
    ArrTime INT,
    CRSArrTime INT,
    UniqueCarrier STRING,
    FlightNum INT,
    TailNum STRING,
    ActualElapsedTime INT,
    CRSElapsedTime INT,
    AirTime INT,
    ArrDelay INT,
    DepDelay INT,
    Origin STRING,
    Dest STRING,
    Distance INT,
    TaxiIn INT,
    TaxiOut INT,
    Cancelled INT,
    CancellationCode STRING,
    Diverted INT,
    CarrierDelay INT,
    WeatherDelay INT,
    NASDelay INT,
    SecurityDelay INT,
    LateAircraftDelay INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/flightdelays/';
Para os dados de clima de São Francisco, sfo_weather, criei duas tabelas. A primeira, sfo_weather_txt, para carregar os dados diretamente do arquivo CSV, e a segunda, sfo_weather, no formato ORC para otimizar o desempenho das consultas. O formato ORC é ideal para grandes volumes de dados, pois oferece melhor compressão e leitura.
SQL
-- Criando tabela temporária em TEXTFILE para carregar os dados
DROP TABLE IF EXISTS sfo_weather_txt;
CREATE TABLE sfo_weather_txt (
    station_name STRING,
    Year INT,
    Month INT,
    DayOfMonth INT,
    precipitation INT,
    temperature_max INT,
    temperature_min INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Carregando os dados para a tabela TEXTFILE
LOAD DATA LOCAL INPATH '/home/maria_dev/arquiteturadedados/sfo_weather.csv'
OVERWRITE INTO TABLE sfo_weather_txt;

-- Criando a tabela final em formato ORC
DROP TABLE IF EXISTS sfo_weather;
CREATE TABLE sfo_weather (
    station_name STRING,
    Year INT,
    Month INT,
    DayOfMonth INT,
    precipitation INT,
    temperature_max INT,
    temperature_min INT
)
STORED AS ORC;

-- Inserindo os dados da tabela TEXTFILE na tabela ORC
INSERT INTO TABLE sfo_weather SELECT * FROM sfo_weather_txt;
Finalmente, verifiquei se os dados foram carregados corretamente nas tabelas flightdelays e sfo_weather.
3. Consultas de Análise (Exemplos)
Com as tabelas criadas e os dados carregados, executei algumas consultas para extrair informações.
Consulta 1: Atraso médio de voos para o destino 'DEN'. Esta consulta calcula a média dos atrasos de chegada (ArrDelay) para todos os voos que tiveram como destino o aeroporto de Denver.
SQL
SELECT AVG(ArrDelay) FROM flightdelays WHERE Dest = 'DEN';
Consulta 2: Atraso médio de voos entre 'LAX' e 'SFO'. Aqui, calculei o atraso médio para voos que partiram de Los Angeles (LAX) e chegaram em São Francisco (SFO).
SQL
SELECT AVG(ArrDelay) FROM flightdelays WHERE Origin = 'LAX' AND Dest = 'SFO';
Consulta 3: Top 10 voos com maior atraso de chegada. Esta consulta ordenou os voos por atraso de chegada (ArrDelay) em ordem decrescente (DESC) e me mostrou os 10 voos com os maiores atrasos.
SQL
SELECT ArrDelay FROM flightdelays ORDER BY ArrDelay DESC LIMIT 10;


