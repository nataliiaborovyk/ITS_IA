SELECT 
    d.anno,
    d.mese,
    p.categoria,
    SUM(f.ricavi) AS ricavi_totali
FROM fact_vendite f
JOIN dim_data d 
    ON f.data_sk = d.data_sk
JOIN dim_prodotto p
    ON f.prodotto_sk = p.prodotto_sk
WHERE d.anno = 2024
GROUP BY d.anno, d.mese, p.categoria
ORDER BY d.mese, ricavi_totali DESC;


