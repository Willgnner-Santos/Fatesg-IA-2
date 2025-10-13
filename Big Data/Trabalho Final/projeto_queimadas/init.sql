-- ============================================================
-- init.sql - Inicialização do PostgreSQL para ETL Queimadas
-- ============================================================

-- Cria banco de dados (se não existir)
SELECT 'CREATE DATABASE queimadas_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'queimadas_db')\gexec

-- Conecta ao banco
\c queimadas_db;

-- Cria tabela para armazenar dados de queimadas
CREATE TABLE IF NOT EXISTS fact_queimadas (
    id SERIAL PRIMARY KEY,
    localidade VARCHAR(255) NOT NULL,
    "2017" INTEGER DEFAULT 0,
    "2018" INTEGER DEFAULT 0,
    "2019" INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para otimizar consultas
CREATE INDEX IF NOT EXISTS idx_localidade ON fact_queimadas(localidade);
CREATE INDEX IF NOT EXISTS idx_2017 ON fact_queimadas("2017");
CREATE INDEX IF NOT EXISTS idx_2018 ON fact_queimadas("2018");
CREATE INDEX IF NOT EXISTS idx_2019 ON fact_queimadas("2019");

-- View será criada após primeira carga de dados

-- Grant de permissões
GRANT ALL PRIVILEGES ON DATABASE queimadas_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Mensagem de sucesso
\echo '✅ Banco de dados inicializado com sucesso!'