from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CriptoIngestao").getOrCreate()

# Lê múltiplos arquivos Parquet
df = spark.read.parquet("C:/Users/eopab/Downloads/CRIPTO/DadosCripto/*.parquet")

df.printSchema()
df.show(5)
