Laboratórios de Apache Hive - Análise de Dados de Voos e Clima
Este repositório documenta a execução de uma série de laboratórios práticos com Apache Hive, focados na ingestão, manipulação, otimização e análise de dados de voos e de informações meteorológicas. As atividades foram realizadas no ambiente HDP (Hortonworks Data Platform) Sandbox.

📝 Descrição Geral
O projeto consiste em seis atividades sequenciais que abordam desde a inserção de dados no HDFS até a criação de tabelas complexas, particionadas e otimizadas com o formato ORCFile.

Atividades Executadas
Atividade 01: Obtenção e Inserção de Dados no HDFS
O primeiro passo foi obter os datasets e carregá-los no HDFS.


Download dos Dados: Os arquivos foram clonados de um repositório Git.


Carga no HDFS: Foram criados diretórios no HDFS e os arquivos .csv (flight_delays e sfo_weather.csv) foram movidos para seus respectivos diretórios.

Bash

# Clonar o repositório com os dados
git clone https://github.com/leonardoamorim/arquiteturadebigdata.git

# Criar diretórios no HDFS
hdfs dfs -mkdir /user/maria_dev/flightdelays
hdfs dfs -mkdir /user/maria_dev/sfo_weather

# Mover arquivos para o HDFS
hdfs dfs -put flight_delays /user/maria_dev/flightdelays
hdfs dfs -put sfo_weather.csv /user/maria_dev/sfo_weather
Atividade 02: Criação de Tabela Externa
Foi criada uma tabela externa (flightdelays) para mapear os dados de atrasos de voos já presentes no HDFS, sem movê-los ou gerenciá-los pelo Hive.

SQL

CREATE EXTERNAL TABLE flightdelays (
  Year INT,
  Month INT,
  DayofMonth INT,
  -- ... (demais colunas)
  LateAircraftDelay INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/flightdelays/';
Atividade 03: Análise de Dados com Hive
Foram executadas consultas analíticas para extrair informações sobre os atrasos de voos.


Atraso médio para Denver (DEN):

SQL

SELECT AVG(arrdelay) FROM flightdelays WHERE dest = 'DEN';

Atraso médio na rota LAX para SFO:

SQL

SELECT AVG(arrdelay) FROM flightdelays WHERE origin = 'LAX' AND dest = 'SFO';

Aeroporto de destino com maior atraso médio:

SQL

SELECT AVG(arrdelay) AS delay, dest FROM flightdelays GROUP BY dest ORDER BY delay DESC LIMIT 1;
Atividade 04: Tabela Gerenciada em Formato ORCFile
Nesta etapa, foi criada uma tabela gerenciada pelo Hive (

sfo_weather) com os dados armazenados no formato ORCFile para otimização. Os dados foram carregados a partir de uma tabela temporária em formato de texto.


SQL

-- Criar tabela temporária para carregar o .csv
CREATE TABLE sfo_weather_txt(station_name STRING, ...);
LOAD DATA LOCAL INPATH '/home/maria_dev/arquiteturadebigdata/sfo_weather.csv' OVERWRITE INTO TABLE sfo_weather_txt;

-- Criar tabela final em formato ORC e inserir os dados
CREATE TABLE sfo_weather(station_name STRING, ...) STORED AS ORC;
INSERT INTO TABLE sfo_weather SELECT * FROM sfo_weather_txt;
Atividade 05: Junção de Dados (Join)
Foi criada uma nova tabela (

flights_weather) contendo o resultado da junção (JOIN) das tabelas flightdelays e sfo_weather. A junção foi feita para voos com origem ou destino em SFO, cruzando com os dados de clima para o mesmo dia.



SQL

SET hive.execution.engine=tez;
CREATE TABLE flights_weather STORED AS TEXTFILE AS
SELECT
  fd.*,
  sw.temperature_max,
  sw.temperature_min
FROM flightdelays fd
JOIN sfo_weather sw ON fd.year = sw.year AND fd.month = sw.month AND fd.dayofmonth = sw.dayofmonth
WHERE fd.origin = 'SFO' OR fd.dest = 'SFO';
Atividade 06: Tabelas Particionadas
Para otimizar ainda mais as consultas, foi criada a tabela 

weather_partitioned, com o mesmo esquema da sfo_weather, mas particionada por ano e mês.

SQL

CREATE TABLE weather_partitioned(
  station_name string,
  dayofmonth int,
  precipitation int,
  temperature_max int,
  temperature_min int)
PARTITIONED BY (year int, month int)
STORED AS ORC;
Em seguida, os dados de Janeiro de 2008 foram inseridos na partição correspondente.

SQL

INSERT INTO TABLE weather_partitioned PARTITION(year=2008, month=1)
SELECT station_name, dayofmonth, precipitation, temperature_max, temperature_min FROM sfo_weather
WHERE year=2008 AND month=1;
✅ Resultados e Verificação
A imagem abaixo demonstra a conclusão bem-sucedida do exercício. Foram executados os comandos DESCRIBE weather_partitioned para verificar o esquema da tabela final, incluindo as colunas de partição, e SELECT * FROM weather_partitioned LIMIT 5; para visualizar uma amostra dos dados carregados.
