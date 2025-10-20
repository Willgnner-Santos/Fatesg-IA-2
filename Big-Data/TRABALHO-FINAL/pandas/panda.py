import pandas as pd
import pyarrow.parquet as pq
import os

# Caminhos
arquivo_parquet = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto\WAVES-ETH.parquet"
arquivo_saida = r"C:\Users\eopab\Downloads\CRIPTO\pandas\WAVES-ETH-tratado.parquet"

# Colunas que queremos manter
colunas = ['open', 'high', 'low', 'close', 'volume']

# Tipos para reduzir memória
tipos = {
    'open': 'float32',
    'high': 'float32',
    'low': 'float32',
    'close': 'float32',
    'volume': 'float32'
}

# Ler parquet em pedaços
batch_size = 500_000  # ajustar conforme RAM disponível
parquet_file = pq.ParquetFile(arquivo_parquet)

dfs = []
for i in range(parquet_file.num_row_groups):
    batch = parquet_file.read_row_group(i, columns=colunas)
    df = batch.to_pandas()  # converte para pandas
    # Converter os tipos para reduzir memória
    for col, dtype in tipos.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    dfs.append(df)

# Concatenar todos os pedaços
df_final = pd.concat(dfs, ignore_index=True)

# Exemplo de tratamento: remover linhas com volume <= 0
df_final = df_final[df_final['volume'] > 0]

# Salvar novamente em Parquet
df_final.to_parquet(arquivo_saida, index=False)

print(f"Processamento concluído. Arquivo salvo em {arquivo_saida}")


