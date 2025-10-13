-- Limpeza
DROP TABLE IF EXISTS flightdelays;
DROP TABLE IF EXISTS sfo_weather_txt;
DROP TABLE IF EXISTS sfo_weather;
DROP TABLE IF EXISTS flights_weather;
DROP TABLE IF EXISTS weather_partitioned;

-- Criação flightdelays
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