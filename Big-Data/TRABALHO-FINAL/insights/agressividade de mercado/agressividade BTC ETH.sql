SELECT
    DATE(open_time) AS dia,
    AVG(close) AS preco_medio_eth_btc,
    -- Calcula a variação percentual diária do preço
    (MAX(close) - MIN(close)) / MIN(close) * 100 AS variacao_diaria_percentual,
    -- Calcula a agressividade de compra líquida: (compras - vendas) / total
    SUM(taker_buy_base_asset_volume - (volume - taker_buy_base_asset_volume)) / SUM(volume) AS agressividade_liquida
FROM
    dados_kline_30min
WHERE
    symbol = 'ETHBTC' -- Se o seu par for 'ETHBTC'
    -- OU symbol = 'BTCETH' -- Se o seu par for 'BTCETH' (inverso)
GROUP BY
    dia
ORDER BY
    variacao_diaria_percentual DESC;
