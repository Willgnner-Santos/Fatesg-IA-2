from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, concat_ws, to_timestamp, udf
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder \
    .appName("ChessGamesTransform") \
    .getOrCreate()
df = spark.read.csv("chess_games.csv", header=True, inferSchema=True)

df = df.withColumn("Event", trim(col("Event"))) # Remover espaços em branco da coluna 'Event'

df = df.drop("White", "Black") # Remover colunas 'White' e 'Black'

df = df.filter(col("Result") != "*") # Remover linhas onde o 'Result' é '*'

df = df.withColumn("Timestamp",
    to_timestamp(concat_ws(" ", col("UTCDate"), col("UTCTime")), "yyyy.MM.dd HH:mm:ss") ) # Criar coluna Timestamp combinando UTCDate e UTCTime

df = df.drop("UTCDate", "UTCTime") # Remover colunas originais de data/hora

df = df.dropna(subset=["WhiteRatingDiff", "BlackRatingDiff"]) # Remover linhas com valores nulos em WhiteRatingDiff ou BlackRatingDiff

def processar_movimentos(an): # Processar movimentos
    if an is None:
        return ("", "")
    tokens = an.split()
    movimentos_filtrados = [
        t for t in tokens
        if not any(x in t for x in [".", "[", "]"]) and t not in ["..", "1-0", "0-1", "1/2-1/2", "*"]
    ]
    movimentos_brancas = ",".join(movimentos_filtrados[0::2])
    movimentos_pretas = ",".join(movimentos_filtrados[1::2])
    return (movimentos_brancas, movimentos_pretas)

# Registrar UDF no Spark
processar_movimentos_udf = udf(processar_movimentos,
    StructType([
        StructField("WhiteMoves", StringType()),
        StructField("BlackMoves", StringType())
    ])
)

df = df.withColumn("parsed", processar_movimentos_udf(col("AN"))) # Aplicar a função UDF à coluna 'AN'

# Separar as colunas resultantes do struct
df = df.withColumn("WhiteMoves", col("parsed.WhiteMoves")) \
       .withColumn("BlackMoves", col("parsed.BlackMoves")) \
       .drop("parsed")

df = df.drop("AN") # Remover coluna 'AN'

df.write.mode("overwrite").option("header", True).csv("chess_games_transformed.csv") # Salvar o resultado em CSV

print("Arquivo 'chess_games_transformed.csv' salvo com sucesso.")
spark.stop()


