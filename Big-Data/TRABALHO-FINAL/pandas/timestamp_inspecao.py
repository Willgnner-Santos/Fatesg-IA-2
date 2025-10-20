import pyarrow.parquet as pq

arquivo = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto\ETH-USDT.parquet"

pq_file = pq.ParquetFile(arquivo)
print("Colunas do arquivo:", pq_file.schema.names)

# Possíveis nomes de timestamp
possiveis_ts = ['open_time', 'timestamp', 'time', 'date', 'T', 'OpenTime', 'kline_start_time']

# Detecta colunas de timestamp
ts_detectadas = [col for col in pq_file.schema.names if col in possiveis_ts]
print("Colunas que parecem ser timestamp:", ts_detectadas)

# Lê apenas o primeiro row group
if ts_detectadas:
    rg = pq_file.read_row_group(0, columns=ts_detectadas)
    df_amostra = rg.to_pandas()
    print("Amostra (primeiras linhas do primeiro row group):")
    print(df_amostra.head())


