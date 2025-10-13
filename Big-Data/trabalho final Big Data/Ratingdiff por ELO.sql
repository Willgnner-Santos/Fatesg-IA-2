SELECT
    CONCAT(
        CAST(FLOOR((WhiteElo + BlackElo) / 2 / 500) * 500 AS STRING),
        '-',
        CAST(FLOOR((WhiteElo + BlackElo) / 2 / 500) * 500 + 499 AS STRING)
    ) AS Faixa_Elo_Media,
    
    AVG(WhiteRatingDiff) AS Media_Variacao_Elo_Brancas,
    
    AVG(BlackRatingDiff) AS Media_Variacao_Elo_Pretas,
    
    COUNT(*) AS Total_Partidas

FROM
    `4200.chess_games`
    
GROUP BY 1
ORDER BY MIN((WhiteElo + BlackElo) / 2);