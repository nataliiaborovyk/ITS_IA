CREATE SCHEMA IF NOT EXISTS dw;

-- (opzionale) se vuoi ricreare da zero lo schema dw:
-- DROP SCHEMA IF EXISTS dw CASCADE;
-- CREATE SCHEMA dw;

CREATE TABLE dw.dim_utente (
    utente_key SERIAL PRIMARY KEY,
    id_utente INTEGER NOT NULL,
    bike_id INTEGER,
    nome_completo VARCHAR(200),
    email VARCHAR(150),
    eta INTEGER,
    fascia_eta VARCHAR(10),
    citta_residenza VARCHAR(100),
    tipo_abbonamento_corrente VARCHAR(50)
);

CREATE TABLE dw.dim_citta (
    citta_key SERIAL PRIMARY KEY,
    id_citta INTEGER NOT NULL,
    nome_sistema VARCHAR(200),
    timezone VARCHAR(100),
    paese VARCHAR(100)
);

CREATE TABLE dw.dim_stazione (
    stazione_key SERIAL PRIMARY KEY,
    id_stazione INTEGER NOT NULL,
    nome_stazione VARCHAR(200),
    latitudine DECIMAL(10, 7),
    longitudine DECIMAL(10, 7),
    capacita_totale INTEGER,
    citta_key INTEGER REFERENCES dw.dim_citta(citta_key)
);

CREATE TABLE dw.dim_bicicletta (
    bicicletta_key SERIAL PRIMARY KEY,
    id_bicicletta INTEGER NOT NULL,
    tipo_bici VARCHAR(50),
    propulsione VARCHAR(50),
    capacita_persone INTEGER
);

CREATE TABLE dw.dim_tempo (
    tempo_key SERIAL PRIMARY KEY,
    data_completa DATE NOT NULL UNIQUE,
    anno INTEGER NOT NULL,
    mese INTEGER NOT NULL,
    giorno INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    settimana INTEGER NOT NULL,
    giorno_settimana INTEGER NOT NULL,
    nome_giorno VARCHAR(20),
    nome_mese VARCHAR(20),
    is_weekend BOOLEAN
);

CREATE TABLE dw.fact_noleggi (
    noleggio_key SERIAL PRIMARY KEY,
    id_noleggio INTEGER NOT NULL,

    utente_key INTEGER NOT NULL REFERENCES dw.dim_utente(utente_key),
    bicicletta_key INTEGER NOT NULL REFERENCES dw.dim_bicicletta(bicicletta_key),
    citta_key INTEGER NOT NULL REFERENCES dw.dim_citta(citta_key),
    stazione_partenza_key INTEGER REFERENCES dw.dim_stazione(stazione_key),
    stazione_arrivo_key INTEGER REFERENCES dw.dim_stazione(stazione_key),
    tempo_key INTEGER NOT NULL REFERENCES dw.dim_tempo(tempo_key),

    durata_minuti INTEGER,
    distanza_km DECIMAL(10, 2),
    batteria_inizio INTEGER,
    batteria_fine INTEGER
);

CREATE INDEX idx_fact_noleggi_utente ON dw.fact_noleggi(utente_key);
CREATE INDEX idx_fact_noleggi_bicicletta ON dw.fact_noleggi(bicicletta_key);
CREATE INDEX idx_fact_noleggi_citta ON dw.fact_noleggi(citta_key);
CREATE INDEX idx_fact_noleggi_stazione_partenza ON dw.fact_noleggi(stazione_partenza_key);
CREATE INDEX idx_fact_noleggi_stazione_arrivo ON dw.fact_noleggi(stazione_arrivo_key);
CREATE INDEX idx_fact_noleggi_tempo ON dw.fact_noleggi(tempo_key);


