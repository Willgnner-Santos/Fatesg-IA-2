import pyarrow.parquet as pq

arquivo = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto\ETH-USDT.parquet"
pq_file = pq.ParquetFile(arquivo)

# Lê apenas o primeiro row group completo
rg = pq_file.read_row_group(0)
df_amostra = rg.to_pandas()

print("Colunas disponíveis no DataFrame:", df_amostra.columns)
print("Índice do DataFrame (timestamps):")
print(df_amostra.index[:5])