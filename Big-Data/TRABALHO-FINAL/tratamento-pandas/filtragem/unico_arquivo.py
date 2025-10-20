import pandas as pd
import os

# Caminho completo do arquivo Parquet que você quer converter
ARQUIVO_PARQUET = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto\DASH-ETH.parquet"

# Caminho de saída (mesmo nome, mas extensão .csv)
ARQUIVO_CSV = os.path.splitext(ARQUIVO_PARQUET)[0] + ".csv"

print(f"Lendo arquivo: {ARQUIVO_PARQUET} ...")
try:
    # Lê o Parquet inteiro com todas as colunas
    df = pd.read_parquet(ARQUIVO_PARQUET)

    print("\nColunas encontradas:")
    print(df.columns.tolist())

    print(f"\nSalvando em CSV: {ARQUIVO_CSV} ...")
    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")

    print("\n✅ Conversão concluída com sucesso!")
    print(f"Arquivo salvo em: {ARQUIVO_CSV}")

except Exception as e:
    print(f"\n❌ Erro ao converter o arquivo: {e}")
