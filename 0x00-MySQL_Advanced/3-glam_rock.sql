-- Lists all bands with Glam rock as their main style, ranked by their longevity

CREATE VIEW galm_rock AS
SELECT band_name, 
  CASE WHEN split IS NULL THEN 2022 - formed
  ELSE split - formed END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

SELECT band_name, lifespan FROM galm_rock;
