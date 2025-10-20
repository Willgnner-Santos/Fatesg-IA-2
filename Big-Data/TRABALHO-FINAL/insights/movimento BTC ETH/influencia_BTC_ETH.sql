 WITH btc_precos AS (
        SELECT open_time, close AS btc_close 
        FROM dados_kline_30min 
        WHERE symbol = 'BTCUSDT'
    ),
    eth_precos AS (
        SELECT open_time, close AS eth_close 
        FROM dados_kline_30min 
        WHERE symbol = 'ETHUSDT'
    )
    SELECT
        b.open_time,
        b.btc_close,
        e.eth_close
    FROM
        btc_precos b
    JOIN
        eth_precos e 
        ON b.open_time = e.open_time
    ORDER BY
        b.open_time;
    