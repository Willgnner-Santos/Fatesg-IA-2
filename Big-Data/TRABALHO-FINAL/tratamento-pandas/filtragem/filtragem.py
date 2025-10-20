import os
import glob
import pandas as pd

# --- CONFIGURAÇÃO DE PASTAS ---
PASTA_ENTRADA = r"C:\Users\eopab\Downloads\CRIPTO\DadosCripto"
PASTA_SAIDA = r"C:\Users\eopab\Downloads\CRIPTO\tratamento\dados"
os.makedirs(PASTA_SAIDA, exist_ok=True)

# --- CONFIGURAÇÕES DE DADOS ---
POSSIVEIS_TS_COLUNAS = [
    'open_time', 'timestamp', 'time', 'T', 'OpenTime',
    'kline_start_time', 'CloseTime', 'ts', 'index'
]

COLUNAS_AGREGADAS = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum',
    'quote_asset_volume': 'sum',
    'number_of_trades': 'sum',
    'taker_buy_base_asset_volume': 'sum',
    'taker_buy_quote_asset_volume': 'sum'
}

MOEDAS_FILTRO = ['BTC', 'ETH']
INTERVALO_MINUTOS = '30T'

def encontrar_coluna_ts(df, colunas_disponiveis):
    for col in POSSIVEIS_TS_COLUNAS:
        if col in colunas_disponiveis:
            return col
    for col in colunas_disponiveis:
        if df[col].dtype in ['int64', 'int32', 'float64'] and df[col].max() > 1000000000000:
            return col
    return None

def processar_parquet(filepath):
    nome_arquivo = os.path.basename(filepath)
    print(f"--- Processando {nome_arquivo} ---")
    
    # 1. Leitura do Parquet e reset do índice imediatamente
    df = pd.read_parquet(filepath).reset_index()
    
    # 2. Detecção da Coluna de Timestamp
    colunas_disponiveis = df.columns.tolist()
    ts_col = encontrar_coluna_ts(df, colunas_disponiveis)
    
    if ts_col is None:
        raise ValueError(f"❌ Nenhuma coluna de timestamp válida encontrada. Colunas disponíveis: {colunas_disponiveis}")
    
    if ts_col != 'open_time':
        df.rename(columns={ts_col: 'open_time'}, inplace=True)
    
    # 3. Conversão e Limpeza
    if df['open_time'].dtype not in ['datetime64[ns]', 'datetime64[ms]']:
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms', errors='coerce')
    
    df.dropna(subset=['open_time'], inplace=True)
    if 'volume' in df.columns:
        df = df[df['volume'] > 0]
    
    # 4. Agregação por 30 minutos
    df.set_index('open_time', inplace=True)
    colunas_map = {k: v for k, v in COLUNAS_AGREGADAS.items() if k in df.columns}
    df_agg = df.resample(INTERVALO_MINUTOS).agg(colunas_map).dropna()
    
    # 5. Saída
    nome_saida = os.path.splitext(nome_arquivo)[0] + "-tratado.csv"
    caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)
    df_agg.to_csv(caminho_saida, index=True)
    
    print(f"✅ Arquivo salvo em: {caminho_saida} | Linhas: {len(df_agg)}")
    print(df_agg.head())

# --- LOOP PRINCIPAL ---
arquivos_parquet = glob.glob(os.path.join(PASTA_ENTRADA, "*.parquet"))

if not arquivos_parquet:
    print(f"ERRO: Nenhum arquivo .parquet encontrado na pasta: {PASTA_ENTRADA}")
else:
    print(f"Iniciando processamento em {len(arquivos_parquet)} arquivos...")
    for arquivo in arquivos_parquet:
        nome_arquivo = os.path.basename(arquivo).upper()
        if not any(moeda in nome_arquivo for moeda in MOEDAS_FILTRO):
            continue
        try:
            processar_parquet(arquivo)
        except ValueError as ve:
            print(f"❌ FALHA no arquivo {os.path.basename(arquivo)}: {ve}")
        except Exception as e:
            print(f"❌ FALHA crítica no arquivo {os.path.basename(arquivo)}: {e}")
    
    print("\n=== PROCESSAMENTO CONCLUÍDO ===")

