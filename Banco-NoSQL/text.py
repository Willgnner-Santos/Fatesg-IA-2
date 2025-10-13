"""
Script para:
1. Criar um banco de dados no PostgreSQL
2. Criar uma tabela automaticamente com base nas colunas de um CSV
3. Inserir os dados do CSV nessa tabela

Dependências:
    pip install psycopg2-binary pandas
"""

import psycopg2  # Biblioteca oficial do PostgreSQL em Python (permite conectar e rodar SQL)
import pandas as pd  # Biblioteca para ler arquivos CSV e manipular tabelas de dados (DataFrame)

# -------------------------
# CONFIGURAÇÕES DO BANCO
# -------------------------
DB_NAME = "imdb_db"       # Nome do banco de dados que será criado
USER = "postgres"         # Usuário padrão do PostgreSQL
PASSWORD = "aluno"        # Senha do banco (no seu caso é "admin")
HOST = "localhost"        # Onde o banco está rodando (localhost = sua máquina)
PORT = "5432"             # Porta padrão do PostgreSQL

CSV_FILE = "imdb_top_1000.csv"  # Nome do arquivo CSV que será lido

# -------------------------
# ETAPA 1 - Criar o banco de dados
# -------------------------

# conn = objeto de conexão com o banco
# psycopg2.connect() é a função que abre a "ponte" entre Python e PostgreSQL
conn = psycopg2.connect(dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT)

# Por padrão, comandos SQL só são aplicados quando damos "commit".
# O autocommit = True garante que comandos como CREATE DATABASE rodem direto.
conn.autocommit = True  

# cursor = objeto que executa comandos SQL dentro da conexão
cursor = conn.cursor()

# Cria o banco de dados do zero (apaga se já existir)
cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")  # DROP DATABASE = excluir banco
cursor.execute(f"CREATE DATABASE {DB_NAME};")  # CREATE DATABASE = criar banco
print(f"Banco {DB_NAME} criado com sucesso!")

# Fecha o cursor (não vamos mais usar essa conexão)
cursor.close()   # Fecha o "executor de comandos SQL"
conn.close()     # Fecha a "ponte" com o banco

# -------------------------
# ETAPA 2 - Criar a tabela no novo banco
# -------------------------

# Lê o arquivo CSV usando pandas → gera um DataFrame (tabela em memória)
df = pd.read_csv(CSV_FILE)

# Agora conectamos no banco que acabamos de criar
conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
cursor = conn.cursor()

# Criar uma tabela chamada "imdb_movies"
# Vamos transformar cada nome de coluna do CSV em uma coluna do banco, do tipo TEXT
columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
# Exemplo: se o CSV tem colunas Title, Rating → vira: "Title" TEXT, "Rating" TEXT

cursor.execute("DROP TABLE IF EXISTS imdb_movies;")  # Remove tabela antiga, se existir
cursor.execute(f"CREATE TABLE imdb_movies ({columns});")  # Cria a nova tabela
print("Tabela imdb_movies criada com sucesso!")

# -------------------------
# ETAPA 3 - Inserir os dados do CSV
# -------------------------

# Vamos inserir cada linha do CSV no banco
for i, row in df.iterrows():
    # row.values → lista com os valores da linha
    # str(v).replace("'", "''") → converte para texto e evita erro com apóstrofos
    values = [str(v).replace("'", "''") for v in row.values]

    # "', '".join(values) → junta todos os valores em uma única string
    # Exemplo: ["Batman", "9.0"] → 'Batman', '9.0'
    values_str = "', '".join(values)

    # Executa o INSERT no banco
    cursor.execute(f"INSERT INTO imdb_movies VALUES ('{values_str}');")

print("Dados inseridos com sucesso!")

# Salva alterações (commit) e fecha conexões
conn.commit()   # Grava todas as mudanças no banco
cursor.close()  # Fecha o "executor"
conn.close()    # Fecha a "ponte"