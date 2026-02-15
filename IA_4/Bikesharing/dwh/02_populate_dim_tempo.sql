-- ============================================================================
-- CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
-- Parte 2: Popolamento della Dimensione Tempo
-- ============================================================================

-- Descrizione: Popola la tabella dim_tempo per un periodo di 5 anni (2018-2022)

\c bikesharing_dwh

-- Popolamento della tabella dim_tempo
INSERT INTO dw.dim_tempo (data_completa, anno, mese, giorno, trimestre, settimana, giorno_settimana, nome_giorno, nome_mese, is_weekend)
SELECT
    d AS data_completa,
    EXTRACT(YEAR FROM d) AS anno,
    EXTRACT(MONTH FROM d) AS mese,
    EXTRACT(DAY FROM d) AS giorno,
    EXTRACT(QUARTER FROM d) AS trimestre,
    EXTRACT(WEEK FROM d) AS settimana,
    EXTRACT(ISODOW FROM d) AS giorno_settimana, -- 1=Lunedì, 7=Domenica
    TO_CHAR(d, 'Day') AS nome_giorno,
    TO_CHAR(d, 'Month') AS nome_mese,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM
    generate_series(
        '2018-01-01'::date,
        '2022-12-31'::date,
        '1 day'::interval
    ) AS d;
