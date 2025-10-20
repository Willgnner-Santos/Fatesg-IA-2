import os
import glob
import pandas as pd
from sqlalchemy import create_engine, types
import time

# --- CONFIGURAÇÕES DE BANCO DE DADOS (POSTGRESQL) ---
# **ATENÇÃO: Mantenha estas credenciais em segredo em um projeto real.**
DB_USER = "postgres"      # Seu usuário do PostgreSQL
DB_PASSWORD = "142020"     # Sua senha
DB_HOST = "localhost"                 # Geralmente 'localhost' se estiver rodando localmente
DB_PORT = "5433"                      # Porta padrão do PostgreSQL
DB_NAME = "bigdata_cripto"            # Nome do seu banco de dados
TABLE_NAME = "dados_kline_30min"       # Nome da tabela que será criada

# --- CONFIGURAÇÕES DE PASTAS ---
# Pasta onde estão os CSVs gerados pelo script anterior
PASTA_ENTRADA = r"C:\Users\eopab\Downloads\CRIPTO\tratamento\dados" 

# --- CONEXÃO COM O BANCO DE DADOS ---
# String de conexão usando SQLAlchemy
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
try:
    engine = create_engine(DB_URL)
    print(f"✅ Conexão com o banco de dados {DB_NAME} estabelecida.")
except Exception as e:
    print(f"❌ ERRO ao conectar ao banco de dados: {e}")
    print("Verifique se o PostgreSQL está rodando, se as credenciais estão corretas e se o banco de dados existe.")
    exit()

def carregar_csv_para_postgres():
    """Lê todos os CSVs da pasta de entrada e insere na tabela PostgreSQL."""
    arquivos_csv = glob.glob(os.path.join(PASTA_ENTRADA, "*.csv"))
    
    if not arquivos_csv:
        print(f"ERRO: Nenhum arquivo .csv encontrado na pasta: {PASTA_ENTRADA}")
        return

    print(f"Iniciando a ingestão de {len(arquivos_csv)} arquivos para a tabela '{TABLE_NAME}'...")
    
    contador_sucesso = 0
    
    for i, arquivo in enumerate(arquivos_csv):
        nome_arquivo = os.path.basename(arquivo)
        print(f"[{i+1}/{len(arquivos_csv)}] Lendo e Inserindo: {nome_arquivo}")
        
        try:
            # 1. Leitura do CSV
            # O índice 'open_time' é lido como a coluna de data
            df = pd.read_csv(arquivo, index_col=0) 
            df.index.name = 'open_time'
            
            # Adicionar a coluna 'symbol' para identificar o par de moedas
            # Ex: 'BTCUSDT-tratado.csv' -> 'BTCUSDT'
            symbol = nome_arquivo.split('-tratado.csv')[0].replace('-', '').upper()
            df['symbol'] = symbol
            
            # 2. Mapeamento de Tipos e Limpeza Final
            
            # Garante que o índice (open_time) é um objeto datetime
            df.index = pd.to_datetime(df.index, errors='coerce')

            # Cria um dicionário de tipos para forçar o PostgreSQL a aceitar float para valores
            # e Timestamp para a coluna de tempo
            dtype_map = {
                'open_time': types.DateTime(),
                'open': types.Float(precision=10),
                'high': types.Float(precision=10),
                'low': types.Float(precision=10),
                'close': types.Float(precision=10),
                'volume': types.Float(precision=10),
                'quote_asset_volume': types.Float(precision=10),
                'number_of_trades': types.BigInteger(),
                'taker_buy_base_asset_volume': types.Float(precision=10),
                'taker_buy_quote_asset_volume': types.Float(precision=10),
                'symbol': types.String(length=15)
            }
            
            # 3. Inserção no PostgreSQL
            # 'if_exists='append'' garante que os dados de cada CSV sejam adicionados à mesma tabela.
            # 'index=True' salva o índice 'open_time' como uma coluna no banco.
            df.to_sql(
                name=TABLE_NAME, 
                con=engine, 
                if_exists='append', 
                index=True, 
                dtype=dtype_map, # Mapeamento de tipos para resolver o OperationalError
            )
            
            contador_sucesso += 1
            print(f"✅ Inserção de {len(df)} linhas bem-sucedida.")
            
        except Exception as e:
            # Imprime o erro detalhado para debugging
            print(f"❌ FALHA na ingestão do arquivo {nome_arquivo}: OperationalError provável. Detalhe: {e}")
            
    print("\n=== INGESTÃO CONCLUÍDA ===")
    print(f"Total de arquivos processados com sucesso: {contador_sucesso}/{len(arquivos_csv)}")


# --- EXECUÇÃO ---
if __name__ == "__main__":
    carregar_csv_para_postgres()
