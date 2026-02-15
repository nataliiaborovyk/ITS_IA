SELECT
    dt.data_completa,
    dt.mese,
    dt.giorno_settimana,
    dt.is_weekend,
    COUNT(fn.noleggio_key) AS total_rental,
    AVG(fn.durata_minuti) AS avg_duration
FROM dw.fact_noleggi fn
JOIN dw.dim_tempo dt
    ON fn.tempo_key = dt.tempo_key
GROUP BY
    dt.data_completa,
    dt.mese,
    dt.giorno_settimana,
    dt.is_weekend
ORDER BY
    dt.data_completa;


SELECT
    t.data_completa,
    t.mese,
    t.giorno_settimana,
    t.is_weekend,
    COUNT(*) AS total_rentals,
    AVG(f.durata_minuti) AS avg_duration
FROM dw.fact_noleggi f
JOIN dw.dim_tempo t
    ON f.tempo_key = t.tempo_key
GROUP BY
    t.data_completa,
    t.mese,
    t.giorno_settimana,
    t.is_weekend
ORDER BY t.data_completa;
