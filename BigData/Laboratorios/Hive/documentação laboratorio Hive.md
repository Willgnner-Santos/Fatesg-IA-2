# Documentação Técnica - Laboratório de Apache Hive

## Índice
1. [Visão Geral](#visão-geral)
2. [Atividades](#atividades)
3. [Conceitos Desenvolvidos](#conceitos-desenvolvidos)
4. [Resultados Obtidos](#resultados-obtidos)
5. [Conclusão](#conclusão)

---

## Visão Geral

Este laboratório demonstra técnicas avançadas de análise de dados usando Apache Hive, incluindo criação de tabelas externas, queries analíticas, formatos de armazenamento otimizados (ORC), joins complexos e particionamento de dados.

**Dataset utilizado:**
- `flight_delays1.csv`, `flight_delays2.csv`, `flight_delays3.csv` - Dados de voos
- `sfo_weather.csv` - Dados meteorológicos do aeroporto de San Francisco

---

## Objetivos de Aprendizagem

1. **Engenharia de Dados**: Ingestão e organização de dados no HDFS
2. **Modelagem de Data Warehouse**: Criação de schemas e tabelas otimizadas
3. **Query Optimization**: Uso de diferentes formatos de armazenamento (TEXTFILE vs ORC)
4. **Análise de Dados em Larga Escala**: Consultas agregadas e joins em ambientes distribuídos
5. **Particionamento de Dados**: Técnicas para otimização de queries em big data
6. **Computação Distribuída**: Utilização do Tez como engine de execução

---

## Arquitetura e Tecnologias

### Stack Tecnológico
- **HDFS** (Hadoop Distributed File System): Armazenamento distribuído
- **Apache Hive**: Data warehouse e SQL engine
- **Apache Tez**: Engine de execução de queries (substituto do MapReduce)
- **YARN**: Gerenciamento de recursos do cluster
- **ORC Format**: Formato columnar otimizado para analytics

### Fluxo de Dados
```
Dados Locais → HDFS → Hive External Tables → Hive Managed Tables (ORC) → Queries & Analysis
```

---

## Atividades

### Atividade 01: Ingestão de Dados no HDFS

**Comandos executados:**
```bash
git clone https://github.com/leonardoamorim/arquiteturadebigdata.git
cd arquiteturadebigdata
hdfs dfs -mkdir /user/maria_dev/flightdelays
hdfs dfs -mkdir /user/maria_dev/sfo_weather
hdfs dfs -put flight_delays* /user/maria_dev/flightdelays
hdfs dfs -put sfo_weather.csv /user/maria_dev/sfo_weather
```

- Clonagem de repositório Git
- Criação de estrutura de diretórios no HDFS
- Upload de arquivos CSV para o sistema distribuído

---

### Atividade 02: Criação de Tabela Externa

**DDL utilizado:**
```sql
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
```

**Pontos importantes:**
- **EXTERNAL TABLE**: Os dados permanecem no HDFS mesmo se a tabela for dropada
- **ROW FORMAT DELIMITED**: Define o parser para CSV
- **LOCATION**: Aponta diretamente para o diretório no HDFS

---

### Atividade 03: Análise de Dados com Queries

#### Query 1: Atraso médio em Denver (DEN)
```sql
SELECT AVG(arrdelay) FROM flightdelays WHERE dest = 'DEN';
```
**Resultado:** 7.26 minutos de atraso médio

#### Query 2: Atraso médio LAX → SFO
```sql
SELECT AVG(arrdelay) FROM flightdelays WHERE origin = 'LAX' AND dest = 'SFO';
```
**Resultado:** 62.5 minutos de atraso médio

#### Query 3: Aeroporto com maior atraso médio
```sql
SELECT AVG(arrdelay) AS delay, dest 
FROM flightdelays 
GROUP BY dest 
ORDER BY delay DESC 
LIMIT 1;
```
**Resultado:** SFO com 54.98 minutos de atraso médio

**Técnicas utilizadas:**
- Agregações (AVG)
- Filtros com WHERE
- Agrupamento com GROUP BY
- Ordenação DESC
- Limitação de resultados

---

### Atividade 04: Tabelas ORC e Performance

**Estratégia em duas etapas:**

**Etapa 1: Tabela intermediária em TEXTFILE**
```sql
CREATE TABLE sfo_weather_txt(
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

LOAD DATA LOCAL INPATH '/home/maria_dev/arquiteturadebigdata/sfo_weather.csv'
OVERWRITE INTO TABLE sfo_weather_txt;
```

**Etapa 2: Conversão para ORC**
```sql
CREATE TABLE sfo_weather(
    station_name STRING,
    Year INT, 
    Month INT, 
    DayOfMonth INT, 
    precipitation INT, 
    temperature_max INT, 
    temperature_min INT
)
STORED AS ORC;

INSERT INTO TABLE sfo_weather SELECT * FROM sfo_weather_txt;
```

**Vantagens do formato ORC:**
- Compressão columnar eficiente
- Predicate pushdown para filtros mais rápidos
- Melhor performance em queries analíticas
- Redução significativa de I/O

---

### Atividade 05: Join de Dados com Tez Engine

```sql
SET hive.execution.engine=tez;

DROP TABLE IF EXISTS flights_weather;
CREATE TABLE flights_weather 
STORED AS TEXTFILE AS 
SELECT 
    fd.*,
    sw.temperature_max, 
    sw.temperature_min 
FROM flightdelays fd 
JOIN sfo_weather sw
    ON fd.year = sw.year 
    AND fd.month = sw.month 
    AND fd.dayofmonth = sw.dayofmonth
WHERE fd.origin = 'SFO' OR fd.dest = 'SFO';
```

**Resultado:** 456 registros combinando dados de voos e meteorologia

**Características técnicas:**
- **Tez Engine**: DAG (Directed Acyclic Graph) para otimização de joins
- **Multi-column join**: Year, Month, DayOfMonth
- **Filtro no WHERE**: Apenas voos com origem ou destino em SFO
- **CTAS (Create Table As Select)**: Criação e população em uma única operação

---

### Atividade 06: Particionamento de Dados

```sql
CREATE TABLE weather_partitioned(
    station_name string,
    dayofmonth int,
    precipitation int,
    temperature_max int,
    temperature_min int
)
PARTITIONED BY (year int, month int)
STORED AS ORC;

INSERT INTO TABLE weather_partitioned 
PARTITION(year=2008, month=1) 
SELECT 
    station_name, 
    dayofmonth, 
    precipitation, 
    temperature_max, 
    temperature_min 
FROM sfo_weather 
WHERE year = 2008 AND month = 1;
```

**Resultado:** 31 registros inseridos na partição (janeiro/2008)

**Benefícios do particionamento:**
- **Partition Pruning**: Queries filtradas por year/month leem apenas dados relevantes
- **Redução de scan**: Evita leitura de toda a tabela
- **Organização lógica**: Estrutura hierárquica no HDFS
- **Performance**: Queries com filtros nas colunas de partição são drasticamente mais rápidas

---

## Conceitos Desenvolvidos

### 1. **Tabelas Externas vs Gerenciadas**
- **Externas**: Metadados gerenciados pelo Hive, dados permanecem no HDFS
- **Gerenciadas**: Hive controla ciclo de vida completo (metadados + dados)

### 2. **Formatos de Armazenamento**
- **TEXTFILE**: Simples, human-readable, menos eficiente
- **ORC**: Columnar, comprimido, otimizado para analytics

### 3. **Engines de Execução**
- **MapReduce**: Tradicional, múltiplos stages
- **Tez**: DAG otimizado, menos overhead, melhor para queries complexas

### 4. **Otimização de Queries**
- Uso de particionamento para partition pruning
- Formato columnar para predicate pushdown
- Indexes implícitos em formatos ORC

### 5. **ETL em Big Data**
- Staging tables (TEXTFILE)
- Tabelas finais otimizadas (ORC)
- Transformações via SQL

---

## Resultados Obtidos

### Métricas de Performance

| Operação | Tempo | Engine | Resultado |
|----------|-------|--------|-----------|
| CREATE EXTERNAL TABLE | 1.077s | - | Sucesso |
| Query AVG (DEN) | 5.716s | YARN | 7.26 min |
| Query AVG (LAX-SFO) | 1.3s | YARN | 62.5 min |
| Query GROUP BY | 3.882s | YARN | SFO: 54.98 min |
| LOAD DATA | 1.466s | - | 22929 rows |
| INSERT ORC | 2.88s | YARN | 366 rows |
| JOIN (Tez) | 3.21s | Tez | 456 rows |
| Partitioned INSERT | 1.50s | YARN | 31 rows |

### Insights dos Dados

1. **SFO é o aeroporto com maior atraso médio** (54.98 minutos)
2. **Voos LAX → SFO têm atrasos significativos** (62.5 minutos em média)
3. **Denver tem atrasos moderados** (7.26 minutos)
4. **366 dias de dados meteorológicos** processados para 2008
5. **Correlação voos-clima**: 456 registros matched para análise

---

## Conclusão

Este laboratório demonstrou a aplicação prática de conceitos fundamentais de Big Data e Data Warehousing usando o ecossistema Hadoop. Habilidades interessantes que eu aprendi:

- Manipulação de HDFS via linha de comando  
- Design de schemas para data warehouses  
- Otimização de queries com formatos columnares  
- Implementação de estratégias de particionamento  
- Uso de engines modernos (Tez) para performance  
- Realização de joins complexos em dados distribuídos  
- Análise exploratória de dados em escala  
