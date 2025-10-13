WITH FaixasDeElo AS (
    SELECT
        Opening,
        CAST(FLOOR(WhiteElo / 500) * 500 AS STRING) AS faixa_elo
    FROM
        `4200.chess_games`
)
SELECT
    faixa_elo,
    Opening,
    contagem_abertura
FROM
    (
        SELECT
            faixa_elo,
            Opening,
            COUNT(*) AS contagem_abertura,
            
            ROW_NUMBER() OVER(
                PARTITION BY faixa_elo 
                ORDER BY COUNT(*) DESC
            ) AS rank_abertura
        FROM
            FaixasDeElo
        GROUP BY
            faixa_elo, 
            Opening
    )
WHERE
    rank_abertura <= 3
ORDER BY
    CAST(faixa_elo AS INT64),
    contagem_abertura DESC;