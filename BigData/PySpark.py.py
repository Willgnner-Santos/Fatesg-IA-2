!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
!tar xf spark-3.5.0-bin-hadoop3.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.5.0-bin-hadoop3"
import findspark
findspark.init()

# Configura variáveis de ambiente
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.5.0-bin-hadoop3"

# Inicializa Spark
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local[*]") \
                  .setAppName("Exercicio Nasa Logs") \
                  .set("spark.executor.memory", "5g")

sc = SparkContext(conf=conf)
!wget -q https://raw.githubusercontent.com/aulapython/datasets/master/NASA_access_log_Jul95
!wget -q https://raw.githubusercontent.com/aulapython/datasets/master/NASA_access_log_Aug95
julho = sc.textFile("NASA_access_log_Jul95").cache()
agosto = sc.textFile("NASA_access_log_Aug95").cache()
hosts_julho = julho.map(lambda l: l.split(" ")[0]).distinct().count()
hosts_agosto = agosto.map(lambda l: l.split(" ")[0]).distinct().count()
print("Hosts únicos em julho:", hosts_julho)
print("Hosts únicos em agosto:", hosts_agosto)
def is_404(line):
    parts = line.split(" ")
    return len(parts) > 8 and parts[-2] == "404"

erros_julho = julho.filter(is_404)
erros_agosto = agosto.filter(is_404)
total_404 = erros_julho.count() + erros_agosto.count()
print("Total de erros 404:", total_404)
urls_404 = erros_julho.union(erros_agosto) \
    .map(lambda l: l.split('"')[1].split(" ")[1]) \
    .map(lambda url: (url, 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: -x[1]) \
    .take(5)

print("Top 5 URLs com erro 404:")
for url, count in urls_404:
    print(url, "-", count)
dias_404 = erros_julho.union(erros_agosto) \
    .map(lambda l: l.split("[")[1].split(":")[0]) \
    .map(lambda dia: (dia, 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .collect()

dias_ordenados = sorted(dias_404, key=lambda x: -x[1])
print("Dias com mais erros 404:")
for dia, count in dias_ordenados[:5]:
    print(dia, "-", count)
def extrai_bytes(line):
    try:
        bytes_str = line.split(" ")[-1]
        return int(bytes_str) if bytes_str != "-" else 0
    except:
        return 0

total_bytes = julho.union(agosto).map(extrai_bytes).reduce(lambda a, b: a + b)
print("Total de bytes transferidos:", total_bytes)
