-- ============================================================================
-- CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
-- Parte 1: Database Transazionale OLTP
-- ============================================================================
-- Descrizione: Schema OLTP per importare il dataset reale European Bike Sharing

-- (Opzionale ma consigliato) Pulizia se rilanci lo script
-- DROP TABLE IF EXISTS station_status CASCADE;
-- DROP TABLE IF EXISTS trips CASCADE;
-- DROP TABLE IF EXISTS utenti CASCADE;
-- DROP TABLE IF EXISTS stations CASCADE;
-- DROP TABLE IF EXISTS bikes CASCADE;
-- DROP TABLE IF EXISTS bike_types CASCADE;
-- DROP TABLE IF EXISTS cities CASCADE;

-- ============================================================================
-- Tabella: cities
-- ============================================================================
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    lat DECIMAL(10, 7),
    lon DECIMAL(10, 7),
    timezone VARCHAR(100),
    country VARCHAR(3),
    return_to_official_only BOOLEAN
);

-- ============================================================================
-- Tabella: bike_types
-- ============================================================================
CREATE TABLE bike_types (
    id INTEGER PRIMARY KEY,
    vehicle_image VARCHAR(500),
    name VARCHAR(200),
    description TEXT,
    form_factor VARCHAR(50),
    rider_capacity INTEGER,
    propulsion_type VARCHAR(50),
    max_range INTEGER,
    battery_capacity INTEGER
);

-- ============================================================================
-- Tabella: bikes
-- ============================================================================
CREATE TABLE bikes (
    id INTEGER PRIMARY KEY,
    bike_type_id INTEGER REFERENCES bike_types(id),
    computer_id VARCHAR(100)
);

-- ============================================================================
-- Tabella: stations
-- ============================================================================
CREATE TABLE stations (
    id INTEGER PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    name VARCHAR(200),
    app_number VARCHAR(50),
    terminal_type VARCHAR(100),
    place_type VARCHAR(100),
    bike_racks INTEGER,
    special_racks INTEGER,
    lon DECIMAL(10, 7),
    lat DECIMAL(10, 7)
);

-- ============================================================================
-- Tabella: utenti (GENERATA SINTETICAMENTE)
-- ============================================================================
-- Nota: nel dataset reale non esiste per motivi privacy.
-- Qui modelliamo utenti realistici: molti utenti, molti viaggi, nessun legame 1:1 con bikes.
CREATE TABLE utenti (
    id SERIAL PRIMARY KEY,
    -- bike_id opzionale (non univoco): può essere NULL, e non deve essere UNIQUE
    bike_id INTEGER REFERENCES bikes(id),

    nome VARCHAR(100),
    cognome VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    data_nascita DATE,
    citta VARCHAR(100),
    data_registrazione TIMESTAMP,
    tipo_abbonamento VARCHAR(50) CHECK (tipo_abbonamento IN ('Mensile', 'Annuale')),
    stato VARCHAR(20) CHECK (stato IN ('Attivo', 'Sospeso')) DEFAULT 'Attivo'
);

-- ============================================================================
-- Tabella: trips (FACT TABLE in OLTP)
-- ============================================================================
CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    bike_id INTEGER REFERENCES bikes(id),
    city_id INTEGER REFERENCES cities(id),
    time_start BIGINT NOT NULL, -- Unix timestamp UTC
    lon_start DECIMAL(10, 7),
    lat_start DECIMAL(10, 7),
    lon_end DECIMAL(10, 7),
    lat_end DECIMAL(10, 7),
    station_id_start INTEGER REFERENCES stations(id),
    station_id_end INTEGER REFERENCES stations(id),
    battery_start INTEGER,
    battery_end INTEGER,
    duration INTEGER, -- secondi
    distance INTEGER, -- metri

    -- Nuovo: collegamento realistico a utenti
    user_id INTEGER REFERENCES utenti(id)
);

-- ============================================================================
-- Tabella: station_status (OPZIONALE)
-- ============================================================================
CREATE TABLE station_status (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES stations(id),
    time BIGINT, -- Unix timestamp UTC
    bikes INTEGER,
    booked_bikes INTEGER,
    bikes_available_to_rent INTEGER,
    free_racks INTEGER,
    free_special_racks INTEGER,
    maintenance BOOLEAN
);

-- ============================================================================
-- Indici per migliorare le performance
-- ============================================================================
CREATE INDEX idx_trips_bike_id ON trips(bike_id);
CREATE INDEX idx_trips_city_id ON trips(city_id);
CREATE INDEX idx_trips_time_start ON trips(time_start);
CREATE INDEX idx_trips_station_start ON trips(station_id_start);
CREATE INDEX idx_trips_station_end ON trips(station_id_end);
CREATE INDEX idx_trips_user_id ON trips(user_id);

CREATE INDEX idx_stations_city_id ON stations(city_id);
CREATE INDEX idx_bikes_type_id ON bikes(bike_type_id);

CREATE INDEX idx_utenti_bike_id ON utenti(bike_id);
CREATE INDEX idx_utenti_stato ON utenti(stato);
CREATE INDEX idx_utenti_tipo_abbonamento ON utenti(tipo_abbonamento);

-- ============================================================================
-- Vista: trips_readable
-- ============================================================================
CREATE OR REPLACE VIEW trips_readable AS
SELECT
    t.id,
    t.bike_id,
    t.user_id,
    t.city_id,
    c.name AS city_name,
    TO_TIMESTAMP(t.time_start) AS time_start_readable,
    t.lon_start,
    t.lat_start,
    t.lon_end,
    t.lat_end,
    t.station_id_start,
    t.station_id_end,
    t.battery_start,
    t.battery_end,
    t.duration,
    t.distance
FROM trips t
JOIN cities c ON t.city_id = c.id;

-- ============================================================================
-- Fine dello script
-- ============================================================================


