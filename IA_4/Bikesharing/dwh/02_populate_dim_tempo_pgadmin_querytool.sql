-- ============================================================================
-- CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
-- Parte 2: Popolamento della Dimensione Tempo (pgAdmin)
-- ============================================================================

-- Nota: in pgAdmin NON si usa "\c".
-- Assicurati di essere connesso al DB: bikesharing_dwh

-- (Opzionale) evita duplicati se rilanci lo script
-- TRUNCATE dw.dim_tempo RESTART IDENTITY;

INSERT INTO dw.dim_tempo (
    data_completa, anno, mese, giorno, trimestre, settimana,
    giorno_settimana, nome_giorno, nome_mese, is_weekend
)
SELECT
    d::date AS data_completa,
    EXTRACT(YEAR FROM d)::int AS anno,
    EXTRACT(MONTH FROM d)::int AS mese,
    EXTRACT(DAY FROM d)::int AS giorno,
    EXTRACT(QUARTER FROM d)::int AS trimestre,
    EXTRACT(WEEK FROM d)::int AS settimana,
    EXTRACT(ISODOW FROM d)::int AS giorno_settimana, -- 1=Lunedì, 7=Domenica
    TRIM(TO_CHAR(d, 'Day')) AS nome_giorno,
    TRIM(TO_CHAR(d, 'Month')) AS nome_mese,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM
    generate_series(
        '2018-01-01'::date,
        '2024-12-31'::date,
        '1 day'::interval
    ) AS d
ON CONFLICT (data_completa) DO NOTHING;

