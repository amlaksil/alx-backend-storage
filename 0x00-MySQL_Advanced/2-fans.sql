-- Create a view to rank country origins of bands, ordered by the number of fans.

CREATE VIEW ranked_origins AS
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

-- Rank the origins by nb_fans
SELECT origin, nb_fans FROM ranked_origins;
