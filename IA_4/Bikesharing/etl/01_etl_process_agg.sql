-- ============================================================================
-- ETL OLTP -> DWH (pgAdmin)
-- ============================================================================

-- 0) PULIZIA (fact prima, poi dimensioni)
TRUNCATE dw.fact_noleggi;

TRUNCATE dw.dim_stazione CASCADE;
TRUNCATE dw.dim_bicicletta CASCADE;
TRUNCATE dw.dim_utente CASCADE;
TRUNCATE dw.dim_citta CASCADE;
-- dim_tempo NON la truncare normalmente (si popola una volta e basta)
-- TRUNCATE dw.dim_tempo RESTART IDENTITY;

-- ============================================================================
-- 1) dim_utente
-- ============================================================================
INSERT INTO dw.dim_utente (
    id_utente, bike_id, nome_completo, email,
    eta, fascia_eta, citta_residenza, tipo_abbonamento_corrente
)
SELECT
    u.id,
    u.bike_id,
    u.nome || ' ' || u.cognome,
    u.email,
    EXTRACT(YEAR FROM AGE(u.data_nascita))::int,
    CASE
        WHEN EXTRACT(YEAR FROM AGE(u.data_nascita)) BETWEEN 18 AND 25 THEN '18-25'
        WHEN EXTRACT(YEAR FROM AGE(u.data_nascita)) BETWEEN 26 AND 35 THEN '26-35'
        WHEN EXTRACT(YEAR FROM AGE(u.data_nascita)) BETWEEN 36 AND 50 THEN '36-50'
        ELSE '50+'
    END,
    u.citta,
    u.tipo_abbonamento
FROM dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, bike_id, nome, cognome, email, data_nascita, citta, tipo_abbonamento FROM utenti'
) AS u(
    id INT, bike_id INT, nome VARCHAR, cognome VARCHAR,
    email VARCHAR, data_nascita DATE, citta VARCHAR, tipo_abbonamento VARCHAR
);

-- ============================================================================
-- 2) dim_citta
-- ============================================================================
INSERT INTO dw.dim_citta (id_citta, nome_sistema, timezone, paese)
SELECT
    c.id AS id_citta,
    c.name AS nome_sistema,
    c.timezone,
    CASE c.country
        WHEN 'DEU' THEN 'Germania'
        WHEN 'FRA' THEN 'Francia'
        WHEN 'ESP' THEN 'Spagna'
        WHEN 'ITA' THEN 'Italia'
        WHEN 'GBR' THEN 'Regno Unito'
        ELSE c.country
    END AS paese
FROM dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, name, timezone, country FROM cities'
) AS c(id INT, name VARCHAR, timezone VARCHAR, country VARCHAR);

-- ============================================================================
-- 3) dim_stazione
-- ============================================================================
INSERT INTO dw.dim_stazione (id_stazione, nome_stazione, latitudine, longitudine, capacita_totale, citta_key)
SELECT
    s.id AS id_stazione,
    s.name AS nome_stazione,
    s.lat,
    s.lon,
    COALESCE(s.bike_racks,0) + COALESCE(s.special_racks,0) AS capacita_totale,
    dc.citta_key
FROM dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, name, lat, lon, bike_racks, special_racks, city_id FROM stations'
) AS s(id INT, name VARCHAR, lat DECIMAL, lon DECIMAL, bike_racks INT, special_racks INT, city_id INT)
JOIN dw.dim_citta dc ON s.city_id = dc.id_citta;

-- ============================================================================
-- 4) dim_bicicletta
-- ============================================================================
INSERT INTO dw.dim_bicicletta (id_bicicletta, tipo_bici, propulsione, capacita_persone)
SELECT
    b.id AS id_bicicletta,
    bt.name AS tipo_bici,
    bt.propulsion_type AS propulsione,
    bt.rider_capacity AS capacita_persone
FROM dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, bike_type_id FROM bikes'
) AS b(id INT, bike_type_id INT)
LEFT JOIN dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, name, propulsion_type, rider_capacity FROM bike_types'
) AS bt(id INT, name VARCHAR, propulsion_type VARCHAR, rider_capacity INT)
ON b.bike_type_id = bt.id;

-- ============================================================================
-- 5) RECORD UNKNOWN (DOPO i load, così non vengono cancellati)
-- ============================================================================
-- dim_utente
INSERT INTO dw.dim_utente (utente_key, id_utente, nome_completo)
SELECT -1, -1, 'UNKNOWN'
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_utente WHERE utente_key = -1);

-- dim_bicicletta
INSERT INTO dw.dim_bicicletta (bicicletta_key, id_bicicletta)
SELECT -1, -1
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_bicicletta WHERE bicicletta_key = -1);

-- dim_citta
INSERT INTO dw.dim_citta (citta_key, id_citta, nome_sistema)
SELECT -1, -1, 'UNKNOWN'
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_citta WHERE citta_key = -1);

-- dim_stazione
INSERT INTO dw.dim_stazione (stazione_key, id_stazione)
SELECT -1, -1
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_stazione WHERE stazione_key = -1);

-- dim_tempo (solo se non esiste già)
INSERT INTO dw.dim_tempo (tempo_key, data_completa, anno, mese, giorno, trimestre, settimana, giorno_settimana, nome_giorno, nome_mese, is_weekend)
SELECT -1, '1900-01-01', 1900, 1, 1, 1, 1, 1, 'UNKNOWN', 'UNKNOWN', FALSE
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_tempo WHERE tempo_key = -1);

-- ============================================================================
-- 6) fact_noleggi (join su user_id!)
-- ============================================================================
INSERT INTO dw.fact_noleggi (
    id_noleggio,
    utente_key,
    bicicletta_key,
    citta_key,
    stazione_partenza_key,
    stazione_arrivo_key,
    tempo_key,
    durata_minuti,
    distanza_km,
    batteria_inizio,
    batteria_fine
)
SELECT
    t.id,
    COALESCE(du.utente_key, -1),
    COALESCE(db.bicicletta_key, -1),
    COALESCE(dc.citta_key, -1),
    COALESCE(ds_p.stazione_key, -1),
    COALESCE(ds_a.stazione_key, -1),
    COALESCE(dt.tempo_key, -1),
    (t.duration / 60),
    (t.distance / 1000.0),
    t.battery_start,
    t.battery_end
FROM dblink(
    'dbname=bikesharing_oltp',
    'SELECT id, user_id, bike_id, city_id, station_id_start, station_id_end,
            time_start, duration, distance, battery_start, battery_end
     FROM trips'
) AS t(
    id INT, user_id INT, bike_id INT, city_id INT,
    station_id_start INT, station_id_end INT,
    time_start BIGINT, duration INT, distance INT,
    battery_start INT, battery_end INT
)
LEFT JOIN dw.dim_utente du      ON t.user_id = du.id_utente
LEFT JOIN dw.dim_bicicletta db ON t.bike_id = db.id_bicicletta
LEFT JOIN dw.dim_citta dc      ON t.city_id = dc.id_citta
LEFT JOIN dw.dim_stazione ds_p ON t.station_id_start = ds_p.id_stazione
LEFT JOIN dw.dim_stazione ds_a ON t.station_id_end = ds_a.id_stazione
LEFT JOIN dw.dim_tempo dt      ON TO_TIMESTAMP(t.time_start)::date = dt.data_completa;

