import os
import time
import glob
import sys
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime
import pyspark.sql.functions as F
from pyspark.sql.types import TimestampType, LongType

# ==============================================================================
# 1. CONFIGURAÇÃO DO SPARK (SIMPLIFICADA)
# ==============================================================================
print("--- 1. Inicializando Spark Session ---")

# Configuração mínima para evitar erros de ambiente (JVM/Committer)
spark = SparkSession.builder.appName("CryptoDataProcessor_Hibrido_Final") \
    .config("spark.sql.session.timeZone", "UTC") \
    .getOrCreate()
print("Spark Session criada.")

# ==============================================================================
# 2. FUNÇÃO DE DOWNSAMPLING (COM DF SPARK)
# ==============================================================================
TIMESTAMP_FINAL_NAME = 'open_time'

def downsample_30min(df, arquivo_nome):
    """Realiza o downsampling em um DataFrame Spark que JÁ TEM a coluna 'open_time'."""

    # 1. CONVERSÃO DE TEMPO (O Pandas já tratou, apenas garantimos o tipo)
    df = df.withColumn(
        TIMESTAMP_FINAL_NAME,
        col(TIMESTAMP_FINAL_NAME).cast(LongType())
    )
    
    # 2. Downsampling em intervalos de 30 minutos (1800 segundos)
    df = df.withColumn("time_30min", (col(TIMESTAMP_FINAL_NAME) / 1800).cast("long") * 1800)

    # 3. Limpeza de dados
    df = df.filter((col("close").isNotNull()) & (col("close") > 0))

    # 4. Agrupamento OHLCV Expandido
    df_down = df.groupBy("time_30min").agg(
        F.first("open").alias("open"),
        F.max("high").alias("high"),
        F.min("low").alias("low"),
        F.last("close").alias("close"),
        F.sum("volume").alias("volume"),
        F.sum("quote_asset_volume").alias("quote_asset_volume"),
        F.sum("number_of_trades").alias("number_of_trades"),
        F.sum("taker_buy_base_asset_volume").alias("taker_buy_base_asset_volume"),
        F.sum("taker_buy_quote_asset_volume").alias("taker_buy_quote_asset_volume")
    )

    # 5. Converte o timestamp de volta para formato legível (TimestampType)
    df_down = df_down.withColumn(TIMESTAMP_FINAL_NAME, from_unixtime(col("time_30min")).cast(TimestampType()))
    
    colunas_finais = [
        TIMESTAMP_FINAL_NAME, "open", "high", "low", "close", "volume",
        "quote_asset_volume", "number_of_trades", 
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume"
    ]
    return df_down.select(*colunas_finais)


# ==============================================================================
# 3. CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
PASTA_ENTRADA = r"C:\Users\eopab\Downloads\CRIPTO\DADOS_CRIPTO_BRL"
PASTA_SAIDA = r"C:\Users\eopab\Downloads\CRIPTO\DADOS_CRIPTO_BRL\tratados_pyspark_hibrido_final" # Nova pasta
os.makedirs(PASTA_SAIDA, exist_ok=True)

arquivos_para_processar = glob.glob(os.path.join(PASTA_ENTRADA, "*.parquet"))
if not arquivos_para_processar:
    print(f"ERRO: Nenhum arquivo Parquet encontrado em {PASTA_ENTRADA}")
    spark.stop()
    sys.exit(1)

# ==============================================================================
# 4. LOOP PRINCIPAL DE PROCESSAMENTO (ABORDAGEM HÍBRIDA FINAL)
# ==============================================================================
total_arquivos = len(arquivos_para_processar)
inicio_total = time.time()
print(f"\n--- 4. Iniciando Processamento Híbrido Final de {total_arquivos} arquivos ---")

for i, arquivo in enumerate(arquivos_para_processar):
    nome_arquivo = os.path.basename(arquivo)
    print(f"[{i+1}/{total_arquivos}] Processando {nome_arquivo}...")

    try:
        # 1. HÍBRIDO: Usar Pandas para ler o arquivo e o índice
        pdf = pd.read_parquet(arquivo)
        
        # 2. HÍBRIDO: Converter o índice (que contém o timestamp em MS) para coluna e renomear
        pdf = pdf.reset_index(names=[TIMESTAMP_FINAL_NAME])
        
        # 3. HÍBRIDO: Converter o Pandas DataFrame para Spark DataFrame
        # Nota: O Spark fará a inferência do tipo. O timestamp deve ser lido como Long/BigInt.
        df_spark = spark.createDataFrame(pdf)
        
        print(f"    [INFO] Colunas lidas pelo Spark após conversão: {df_spark.columns}")

        # 4. Aplica o downsampling no DataFrame Spark
        df_30min = downsample_30min(df_spark, nome_arquivo)

        if df_30min is None:
            print(f"    [SKIPPED] {nome_arquivo} ignorado devido a erro no downsample.")
            continue

        caminho_escrita = os.path.join(PASTA_SAIDA, nome_arquivo.replace(".parquet", ""))
        
        # 5. Salva o resultado
        df_30min.write.mode("overwrite").parquet(caminho_escrita)
        print(f"    [SUCESSO] {nome_arquivo} escrito em {caminho_escrita}")

    except Exception as e:
        # Erros de I/O, de conversão de Pandas/Spark, ou erros de coluna
        print(f"❌ ERRO no processamento de {nome_arquivo}: {e}")
        print(f"    [SKIPPED] {nome_arquivo} ignorado e continuando com os próximos arquivos.")
        continue

fim_loop = time.time()
print(f"\n🎉 Processamento do Loop concluído em {fim_loop - inicio_total:.2f} segundos")

# ==============================================================================
# 5. ENCERRAMENTO
# ==============================================================================
spark.stop()
print("\nSessão Spark encerrada.")

