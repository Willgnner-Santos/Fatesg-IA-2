SELECT
  Event,
  Termination,
  COUNT(1) AS TotalPartidas
FROM
  `4200.chess_games`
GROUP BY
  Event,
  Termination
ORDER BY
  Event,
  TotalPartidas DESC