SELECT
    Event,
    COUNTIF(Result = '1-0') AS Vitorias_Brancas,
    COUNTIF(Result = '0-1') AS Vitorias_Pretas,
    COUNTIF(Result = '1/2-1/2') AS Empate
FROM
    `4200.chess_games`
GROUP BY
    Event
ORDER BY
    Event;