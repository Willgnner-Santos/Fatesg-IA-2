import os
import glob
import pandas as pd
import pyarrow.parquet as pq

# === CONFIGURAÇÃO ===
PASTA_ENTRADA = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto"

# Possíveis nomes de colunas de tempo
POSSIVEIS_TS_COLUNAS = [
    'open_time', 'timestamp', 'time', 'date', 'T', 'OpenTime',
    'kline_start_time', 'CloseTime', 'ts', 'open_time_ms'
]

def inspecionar_arquivo(filepath):
    """
    Inspeciona um arquivo .parquet, mostra o esquema de colunas e
    tenta identificar qual coluna é o timestamp.
    """
    nome_arquivo = os.path.basename(filepath)
    print("=" * 70)
    print(f"| ARQUIVO: {nome_arquivo}")
    print("=" * 70)

    try:
        pq_file = pq.ParquetFile(filepath)
        schema = pq_file.schema

        print("\n--- TIPOS DE COLUNAS ---")

        # 🔧 Compatibilidade total entre versões do PyArrow
        if hasattr(schema, "names") and hasattr(schema, "column"):
            # PyArrow 15+ estilo (usa schema.column(i) para acessar cada campo)
            for i in range(schema.num_columns):
                field = schema.column(i)
                print(f"  {field.name} ({field.physical_type})")
            colunas_disponiveis = schema.names
        else:
            # Fallback para versões antigas
            for field in schema:
                print(f"  {field.name} ({field.type})")
            colunas_disponiveis = [field.name for field in schema]

        # Detecta possíveis colunas de timestamp
        colunas_suspeitas = [col for col in POSSIVEIS_TS_COLUNAS if col in colunas_disponiveis]

        # Se encontrou colunas suspeitas, mostra amostra
        if colunas_suspeitas:
            print("\n--- AMOSTRA DAS COLUNAS DE TIMESTAMP SUSPEITAS (5 Linhas) ---")
            # lê até 5 linhas apenas dessas colunas
            tabela = pq_file.read(columns=colunas_suspeitas)
            amostra_df = tabela.to_pandas().head(5)
            print(amostra_df.to_string(index=False))
            print(f"\nColunas de timestamp detectadas: {colunas_suspeitas}")
        else:
            print("\nAVISO: Nenhuma coluna de timestamp conhecida foi encontrada neste arquivo.")
            print(f"Colunas disponíveis: {colunas_disponiveis}")

        print("\n" + "-" * 70 + "\n")

    except Exception as e:
        print(f"❌ ERRO ao inspecionar o arquivo {nome_arquivo}: {e}")
        print("\n" + "-" * 70 + "\n")


# === LOOP PRINCIPAL ===
arquivos_parquet = glob.glob(os.path.join(PASTA_ENTRADA, "*.parquet"))

if not arquivos_parquet:
    print(f"ERRO: Nenhum arquivo .parquet encontrado na pasta: {PASTA_ENTRADA}")
else:
    print(f"Iniciando inspeção de {len(arquivos_parquet)} arquivos...\n")
    for arquivo in arquivos_parquet:
        inspecionar_arquivo(arquivo)
    print("=== INSPEÇÃO CONCLUÍDA ===")

