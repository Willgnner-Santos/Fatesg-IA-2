WITH last_moves AS (
  SELECT
    Result,
    -- Último movimento das brancas
    SPLIT(WhiteMoves, ',')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT(WhiteMoves, ',')) - 1)] AS last_white_move,
    -- Último movimento das pretas
    SPLIT(BlackMoves, ',')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT(BlackMoves, ',')) - 1)] AS last_black_move
  FROM `4200.chess_games`
)

, mate_moves AS (
  SELECT
    CASE 
      WHEN Result = '1-0' AND last_white_move LIKE '%#' THEN last_white_move
      WHEN Result = '0-1' AND last_black_move LIKE '%#' THEN last_black_move
      ELSE NULL
    END AS mate_move
  FROM last_moves
)

SELECT
  CASE
    WHEN mate_move LIKE 'Q%' THEN 'Rainha'
    WHEN mate_move LIKE 'N%' THEN 'Cavalo'
    WHEN mate_move LIKE 'R%' THEN 'Torre'
    WHEN mate_move LIKE 'B%' THEN 'Bispo'
    WHEN mate_move LIKE 'K%' THEN 'Rei'
    WHEN mate_move LIKE 'O%' THEN 'Castling'
    ELSE 'Peão'
  END AS peca_final,
  COUNT(*) AS total_mates
FROM mate_moves
WHERE mate_move IS NOT NULL
GROUP BY peca_final
ORDER BY total_mates DESC;