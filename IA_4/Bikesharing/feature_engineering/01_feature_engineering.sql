-- ============================================================================
-- CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
-- Parte 6: Feature Engineering per Machine Learning
-- ============================================================================

-- Descrizione: Estrazione di feature dal DWH per predire il churn degli utenti

-- Creazione di una vista (o tabella) con le feature per il ML
CREATE OR REPLACE VIEW ml.customer_features AS
WITH last_trip AS (
    SELECT
        utente_key,
        MAX(t.data_completa) AS data_ultimo_noleggio
    FROM dw.fact_noleggi f
    JOIN dw.dim_tempo t ON f.tempo_key = t.tempo_key
    GROUP BY utente_key
),
user_aggregates AS (
    SELECT
        f.utente_key,
        COUNT(f.noleggio_key) AS totale_noleggi,
        SUM(f.durata_minuti) AS totale_minuti,
        SUM(f.distanza_km) AS totale_km,
        AVG(f.durata_minuti) AS durata_media_minuti,
        AVG(f.distanza_km) AS distanza_media_km,
        COUNT(DISTINCT f.bicicletta_key) AS totale_bici_usate,
        COUNT(DISTINCT f.citta_key) AS totale_citta_visitate
    FROM dw.fact_noleggi f
    GROUP BY f.utente_key
)
SELECT
    u.utente_key,
    u.id_utente,
    u.eta,
    u.tipo_abbonamento_corrente,
    
    -- Feature RFM
    (SELECT MAX(data_completa) FROM dw.dim_tempo) - lt.data_ultimo_noleggio AS recency_giorni,
    ua.totale_noleggi AS frequency,
    ua.totale_minuti AS monetary_minuti,
    
    -- Feature Comportamentali
    ua.durata_media_minuti,
    ua.distanza_media_km,
    ua.totale_bici_usate,
    ua.totale_citta_visitate,
    
    -- Variabile Target (is_churn)
    -- Un utente è considerato "churned" se non ha fatto noleggi negli ultimi 90 giorni
    CASE
        WHEN (SELECT MAX(data_completa) FROM dw.dim_tempo) - lt.data_ultimo_noleggio > 90 THEN 1
        ELSE 0
    END AS is_churn
FROM dw.dim_utente u
JOIN last_trip lt ON u.utente_key = lt.utente_key
JOIN user_aggregates ua ON u.utente_key = ua.utente_key;


