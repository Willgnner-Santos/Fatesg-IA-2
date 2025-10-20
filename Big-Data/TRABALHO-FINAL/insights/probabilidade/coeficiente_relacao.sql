-- ESTA CONSULTA CALCULA A CORRELAÇÃO DE PEARSON ENTRE BTC E ETH
-- Prova analitica de que o movimento de um "puxa" o do outro.

-- Passo 1: CTE para extrair apenas os preços de Fechamento (CLOSE) do Bitcoin contra USDT
WITH btc_precos AS (
    SELECT 
        open_time, 
        close AS btc_close 
    FROM 
        dados_kline_30min 
    WHERE 
        symbol = 'BTCUSDT' -- VERIFIQUE se 'BTCUSDT' é o nome correto do par na sua tabela
),
-- Passo 2: CTE para extrair apenas os preços de Fechamento (CLOSE) do Ethereum contra USDT
eth_precos AS (
    SELECT 
        open_time, 
        close AS eth_close 
    FROM 
        dados_kline_30min 
    WHERE 
        symbol = 'ETHUSDT' -- VERIFIQUE se 'ETHUSDT' é o nome correto do par na sua tabela
)
-- Passo 3: Junta os dois resultados pelo Timestamp (open_time) e calcula a Correlação
SELECT
    -- CORR(X, Y) retorna o coeficiente de Correlação de Pearson
    CORR(b.btc_close, e.eth_close) AS coeficiente_correlacao_btc_eth,
    -- Contagem para garantir que há um número suficiente de pontos comparados
    COUNT(b.open_time) AS total_pontos_comparados
FROM
    btc_precos b
JOIN
    eth_precos e 
    -- O JOIN é feito pelo tempo de abertura da vela de 30 minutos
    ON b.open_time = e.open_time;
