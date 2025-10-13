# ============================================================
# Dockerfile - PySpark ETL de Queimadas
# ============================================================

FROM openjdk:11-jre-slim

# Instala Python e dependências
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    libpq-dev \
    gcc \
    && apt-get clean

# Instala PySpark, Psycopg2 e Pandas
RUN pip install --no-cache-dir \
    pyspark==3.5.1 \
    psycopg2-binary==2.9.7 \
    pandas

# Baixa driver JDBC do PostgreSQL
RUN wget -O /opt/postgresql-42.7.3.jar \
    https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

# Define diretório de trabalho
WORKDIR /app

# Copia script ETL e dados
COPY etl_queimadas_pyspark.py /app/
COPY data /app/data

# Variáveis de ambiente
ENV POSTGRES_HOST=db \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=queimadas_db \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres

# Executa o ETL
CMD ["python3", "etl_queimadas_pyspark.py"]