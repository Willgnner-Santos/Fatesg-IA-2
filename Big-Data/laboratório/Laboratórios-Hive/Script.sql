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
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE
LOCATION '/user/maria_dev/flightdelays/';

SELECT AVG(arrdelay) FROM flightdelays WHERE dest = 'DEN';
SELECT AVG(arrdelay) FROM flightdelays WHERE origin = 'LAX' AND dest = 'SFO';
SELECT AVG(arrdelay) AS delay, dest FROM flightdelays GROUP BY dest ORDER BY
delay DESC LIMIT 1;


DROP TABLE IF EXISTS sfo_weather_txt;
CREATE TABLE sfo_weather_txt(station_name STRING,
Year INT, Month INT, DayOfMonth INT, precipitation INT, temperature_max
INT, temperature_min INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
LOAD DATA LOCAL INPATH '/home/maria_dev/arquiteturadebigdata/sfo_weather.csv'
OVERWRITE INTO TABLE sfo_weather_txt;
DROP TABLE IF EXISTS sfo_weather;
CREATE TABLE sfo_weather(station_name STRING,
Year INT, Month INT, DayOfMonth INT, precipitation INT, temperature_max
INT, temperature_min INT)
STORED AS ORC;
INSERT INTO TABLE sfo_weather SELECT * FROM sfo_weather_txt;
SELECT * FROM sfo_weather;

SET hive.execution.engine= tez;
DROP TABLE IF EXISTS flights_weather;
CREATE TABLE flights_weather STORED AS TEXTFILE AS SELECT fd.*,
sw.temperature_max, sw.temperature_min FROM flightdelays fd JOIN sfo_weather sw
ON fd.year = sw.year AND fd.month = sw.month AND fd.dayofmonth = sw.dayofmonth
WHERE fd.origin = 'SFO' OR fd.dest = 'SFO';
SELECT * FROM flights_weather;

DROP TABLE IF EXISTS weather_partitioned;
CREATE TABLE weather_partitioned(
station_name string,
dayofmonth int,
precipitation int,
temperature_max int,
temperature_min int)
PARTITIONED BY (year int, month int)
STORED AS ORC;
INSERT INTO TABLE weather_partitioned PARTITION(year=2008, month=1) SELECT
station_name, dayofmonth, precipitation, temperature_max, temperature_min FROM
sfo_weather WHERE year = 2008 AND month = 1;
SELECT * FROM weather_partitioned;