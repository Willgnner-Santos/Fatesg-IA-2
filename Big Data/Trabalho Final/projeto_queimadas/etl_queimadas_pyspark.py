from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, regexp_replace, when, lit
import os
import sys

# ============================================================
# Configurações do PostgreSQL
# ============================================================
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "queimadas_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_TABLE = "fact_queimadas"

POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Determina caminho do CSV
if os.path.exists("/app/data/queimadas.csv"):
    CSV_PATH = "/app/data/queimadas.csv"
    print("📦 Executando dentro do Docker")
else:
    CSV_PATH = r"C:\Users\felip\Downloads\Faculdade\Big Data\Trabalho Final\projeto_queimadas\data\queimadas.csv"
    print("💻 Executando localmente")

# ============================================================
# Inicializa Spark
# ============================================================
spark = SparkSession.builder \
    .appName("ETL_Queimadas_PySpark") \
    .config("spark.jars", "/opt/postgresql-42.7.3.jar") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

print("✅ Sessão Spark iniciada")

# ============================================================
# Leitura CSV com encoding correto
# ============================================================
try:
    # Tenta diferentes encodings
    for encoding in ["latin1", "iso-8859-1", "cp1252"]:
        try:
            df = spark.read.csv(
                CSV_PATH, 
                header=True, 
                inferSchema=True, 
                sep=";", 
                encoding=encoding
            )
            print(f"✅ CSV carregado com encoding: {encoding}")
            break
        except:
            continue
    
    df.printSchema()
    print(f"📊 Total de linhas: {df.count()}")
    df.show(5, truncate=False)
    
except Exception as e:
    print(f"❌ Erro ao carregar CSV: {e}")
    sys.exit(1)

# ============================================================
# Teste de conexão PostgreSQL
# ============================================================
try:
    test_df = spark.read.format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "pg_catalog.pg_tables") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    print("✅ Conexão PostgreSQL OK")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")
    sys.exit(1)

# ============================================================
# Limpeza e Transformação
# ============================================================
df_clean = df.dropna(how="all")

# Padroniza nomes de colunas (remove aspas e normaliza)
for c in df_clean.columns:
    novo_nome = c.strip('"').lower().strip()
    novo_nome = novo_nome.replace(" ", "_").replace("ã", "a").replace("á", "a")
    novo_nome = novo_nome.replace("ó", "o").replace("ô", "o").replace("ê", "e")
    novo_nome = novo_nome.replace("ç", "c").replace("í", "i").replace("ú", "u")
    df_clean = df_clean.withColumnRenamed(c, novo_nome)

print("📝 Colunas após padronização:", df_clean.columns)

# Remove espaços em localidade
if "localidade" in df_clean.columns:
    df_clean = df_clean.withColumn("localidade", trim(col("localidade")))

# Processa colunas de anos (converte "-" para 0 e cast para integer)
anos = ["2017", "2018", "2019"]
for ano in anos:
    if ano in df_clean.columns:
        df_clean = df_clean.withColumn(
            ano, 
            when(col(ano).isNull() | (col(ano) == "-") | (col(ano) == ""), 0)
            .otherwise(regexp_replace(col(ano), "[^0-9]", ""))
        )
        df_clean = df_clean.withColumn(ano, col(ano).cast("integer"))

# Remove coluna "variavel" se existir (não é necessária)
if "variavel" in df_clean.columns:
    df_clean = df_clean.drop("variavel")

print("✅ Dados transformados")
df_clean.show(10, truncate=False)

# ============================================================
# Escrita no PostgreSQL (com tratamento de views)
# ============================================================
try:
    # Primeiro, tenta dropar a view se existir
    from pyspark.sql import Row
    
    try:
        drop_view_query = "DROP VIEW IF EXISTS vw_queimadas_resumo CASCADE"
        spark.read.format("jdbc") \
            .option("url", POSTGRES_URL) \
            .option("query", drop_view_query) \
            .option("user", POSTGRES_USER) \
            .option("password", POSTGRES_PASSWORD) \
            .option("driver", "org.postgresql.Driver") \
            .load()
    except:
        pass  # Ignora se não conseguir dropar
    
    # Agora grava os dados
    df_clean.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", POSTGRES_TABLE) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    print("✅ Dados gravados no PostgreSQL")
    
    # Recria a view após inserir os dados
    try:
        create_view = """
        CREATE OR REPLACE VIEW vw_queimadas_resumo AS
        SELECT 
            localidade,
            "2017",
            "2018",
            "2019",
            ("2017" + "2018" + "2019") AS total_geral,
            ROUND(("2017" + "2018" + "2019")::NUMERIC / 3, 2) AS media_anual
        FROM fact_queimadas
        ORDER BY total_geral DESC
        """
        
        # Usa conexão JDBC para executar SQL direto
        import psycopg2
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(create_view)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ View vw_queimadas_resumo recriada")
    except Exception as ve:
        print(f"⚠️ Aviso ao recriar view: {ve}")
        
except Exception as e:
    print(f"❌ Erro ao gravar: {e}")
    sys.exit(1)

# ============================================================
# Validação e Estatísticas
# ============================================================
try:
    # Conta registros
    count_df = spark.read.format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("query", f"SELECT COUNT(*) AS total FROM {POSTGRES_TABLE}") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    total = count_df.collect()[0]['total']
    print(f"📊 Total de registros no PostgreSQL: {total}")
    
    # Preview dos dados
    preview_df = spark.read.format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("query", f"SELECT * FROM {POSTGRES_TABLE} LIMIT 10") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    print("📋 Preview PostgreSQL:")
    preview_df.show(truncate=False)

except Exception as e:
    print(f"⚠️ Erro na validação: {e}")

# ============================================================
# Estatísticas por ano
# ============================================================
print("\n📈 ESTATÍSTICAS:")
print(f"Total de municípios: {df_clean.count()}")

for ano in anos:
    if ano in df_clean.columns:
        total_ano = df_clean.agg({ano: "sum"}).collect()[0][0]
        print(f"Total de focos em {ano}: {total_ano if total_ano else 0}")

# Top 5 municípios em 2019
if "2019" in df_clean.columns and "localidade" in df_clean.columns:
    print("\n🏆 Top 5 municípios com mais focos em 2019:")
    top5 = df_clean.select("localidade", "2019") \
        .orderBy(col("2019").desc()) \
        .limit(5)
    top5.show(truncate=False)

# ============================================================
# Finaliza
# ============================================================
spark.stop()
print("🏁 ETL concluído com sucesso!")