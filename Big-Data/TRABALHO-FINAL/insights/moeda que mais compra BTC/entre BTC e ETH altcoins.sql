WITH BtcVolume AS (
    -- Calcula o volume total (em BTC) para a compra de cada altcoin
    SELECT
        SUBSTRING(symbol FROM 1 FOR LENGTH(symbol) - 3) AS altcoin_comprado,
        -- Volume total em BTC: Volume da Altcoin * Preço de Fechamento
        ROUND(SUM(volume * close)::numeric, 2) AS volume_total_btc
    FROM dados_kline_30min
    WHERE symbol LIKE '%BTC'
    -- Exclui moedas de cotação longas e garante que não estamos somando ETHBTC
    AND LENGTH(symbol) <= 7 AND symbol <> 'ETHBTC' AND symbol <> 'BTCUSDT' -- Ajuste os símbolos de exclusão conforme necessário
    GROUP BY 1
),

EthVolume AS (
    -- Calcula o volume total (em ETH) para a compra de cada altcoin
    SELECT
        SUBSTRING(symbol FROM 1 FOR LENGTH(symbol) - 3) AS altcoin_comprado,
        -- Volume total em ETH: Volume da Altcoin * Preço de Fechamento
        ROUND(SUM(volume * close)::numeric, 2) AS volume_total_eth
    FROM dados_kline_30min
    WHERE symbol LIKE '%ETH'
    -- Exclui pares como ETHBTC e ETHUSDT
    AND symbol <> 'ETHBTC' AND symbol <> 'ETHUSDT' AND LENGTH(symbol) <= 7
    GROUP BY 1
)

-- Combina os resultados para uma visão geral: Altcoin, Volume BTC e Volume ETH
SELECT
    COALESCE(b.altcoin_comprado, e.altcoin_comprado) AS altcoin,
    b.volume_total_btc,
    e.volume_total_eth
FROM BtcVolume b
FULL JOIN EthVolume e -- FULL JOIN garante que altcoins só negociadas em BTC ou ETH também apareçam
    ON b.altcoin_comprado = e.altcoin_comprado
ORDER BY 
    COALESCE(b.volume_total_btc, 0) DESC, -- Ordena primariamente pelo volume BTC
    COALESCE(e.volume_total_eth, 0) DESC; -- Ordena secundariamente pelo volume ETH