
CREATE TABLE dim_data (
    data_sk SERIAL PRIMARY KEY,
    data DATE UNIQUE,
    anno INT,
    mese INT,
    giorno INT,
    trimestre INT,
    mese_nome TEXT,
    giorno_settimana INT,
    giorno_nome TEXT
);


-- Inserisco nella tabella dim_data le colonne:
--  data (la data vera),
--  anno, mese, giorno, trimestre,
--  mese_nome, giorno_settimana, giorno_nome
INSERT INTO dim_data (
    data,               -- la data reale (es: 2023-05-10)
    anno,               -- anno numerico estratto dalla data
    mese,               -- mese numerico (1-12)
    giorno,             -- giorno del mese (1-31)
    trimestre,          -- trimestre dell’anno (1-4)
    mese_nome,          -- nome del mese, formato stringa
    giorno_settimana,   -- giorno della settimana (0=Sunday, 1=Monday...)
    giorno_nome         -- nome del giorno (Monday...)
)
-- Questa SELECT genera le righe da inserire nella tabella
SELECT
    d,                      -- la data generata da generate_series
                            -- (d è una colonna che contiene una data)
    EXTRACT(YEAR FROM d),   -- ricava l'anno da quella data
    EXTRACT(MONTH FROM d),  -- ricava il numero del mese (1-12)
    EXTRACT(DAY FROM d),    -- ricava il giorno del mese
    EXTRACT(QUARTER FROM d),-- ricava il trimestre (1=Jan-Mar ... 4=Oct-Dec)
    TO_CHAR(d, 'Month'),    -- converte la data in un testo con il nome del mese
                            -- (es: 'January')
    EXTRACT(DOW FROM d),    -- giorno della settimana (0=domenica)
    TO_CHAR(d, 'Day')       -- nome completo del giorno (es: 'Monday')
                            -- attenzione: 'Day' aggiunge anche spazi finali
                            -- (si possono togliere con TRIM() se serve)
FROM generate_series(
        '2020-01-01'::date,     -- data di inizio della serie
        '2026-12-31'::date,     -- data di fine della serie
        '1 day'::interval       -- passo: 1 giorno alla volta
    ) AS d;                     -- alias d: la tabella e la colonna si chiamano d
                                -- d è sia il nome della tabella virtuale
                                -- sia il nome dell'unica colonna prodotta


CREATE TABLE dim_cliente (
    cliente_sk   SERIAL PRIMARY KEY, -- chiave surrogata del DW
    cliente_id   INT UNIQUE,         -- id originale dell'OLTP (tabella clienti)
    nome         TEXT,
    cognome      TEXT,
    citta        TEXT,
    regione      TEXT,
    data_nascita DATE,               -- arricchimento (non esiste nell'OLTP)
    eta          INT,                -- arricchimento (calcolata)
    fascia_eta   TEXT                -- arricchimento (età raggruppata)
);

-- 1) Carico i clienti dal database OLTP (techstore_2) dentro dim_cliente
INSERT INTO dim_cliente 
    (cliente_id, nome, cognome, citta, regione)
SELECT
    cliente_id,   -- id originale del cliente (dal sistema OLTP)
    nome,
    cognome,
    citta,
    regione
FROM dblink(
    'dbname=techstore_2 user=postgres password=postgres host=localhost',
    'SELECT cliente_id, nome, cognome, citta, regione FROM clienti'
) AS t(
    cliente_id INT,
    nome       TEXT,
    cognome    TEXT,
    citta      TEXT,
    regione    TEXT
);


-- 2) Arricchisco con una data di nascita casuale
UPDATE dim_cliente
SET data_nascita =
    date '1942-01-01'              -- data iniziale (1 gennaio 1942)
    + (random() * 23725)::int;     -- aggiungo da 0 a ~65 anni di giorni

-- 3) Calcolo l'età a partire dalla data di nascita
UPDATE dim_cliente
SET eta = EXTRACT(
    YEAR FROM age(CURRENT_DATE, data_nascita)
);

-- 4) Raggruppo i clienti in fasce di età
UPDATE dim_cliente
SET fascia_eta = CASE
    WHEN eta < 25 THEN '18-24'
    WHEN eta BETWEEN 25 AND 39 THEN '25-39'
    WHEN eta BETWEEN 40 AND 59 THEN '40-59'
    ELSE '60+'
END;


CREATE TABLE dim_prodotto (
    prodotto_sk SERIAL PRIMARY KEY,   -- chiave surrogata DW (ID interno)
    product_id INT UNIQUE,            -- chiave naturale del prodotto (ID OLTP)
    nome TEXT,
    categoria TEXT,
    marca TEXT
);

INSERT INTO dim_prodotto (product_id, nome, categoria, marca)
SELECT *
FROM dblink(
    'dbname=techstore_2 user=postgres password=postgres host=localhost',
    '
    SELECT 
        p.prodotto_id,
        p.nome_prodotto,
        c.nome_categoria,
        p.marca
    FROM prodotti p
    JOIN categorie c ON p.categoria_id = c.categoria_id
    '
) AS t(product_id INT, nome TEXT, categoria TEXT, marca TEXT);

CREATE TABLE dim_spedizione (
  spedizione_sk SERIAL PRIMARY KEY,      -- chiave surrogata DW
  spedizione_id INT UNIQUE,              -- id originale dal OLTP
  corriere TEXT,                         -- SDA, DHL, GLS...
  costo NUMERIC(10,2),                   -- costo della spedizione
  data_spedizione DATE,                  -- quando è stata spedita
  data_consegna DATE,                    -- quando è arrivata
  tempo_consegna_giorni INT,             -- differenza in giorni
  fascia_tempo_consegna TEXT             -- es. "1-2 giorni", "3-5", ecc.
);


INSERT INTO dim_spedizione 
    (spedizione_id, corriere, costo, data_spedizione, data_consegna)
SELECT *
FROM dblink(
  'dbname=techstore_2 user=postgres password=postgres host=localhost',
  'SELECT s.spedizione_id,
          s.corriere,
          s.costo_spedizione,
          s.data_spedizione,
          s.data_consegna
   FROM spedizioni s'
) AS t(
    spedizione_id INT,
    corriere TEXT,
    costo NUMERIC(10,2),
    data_spedizione DATE,
    data_consegna DATE
);

UPDATE dim_spedizione
SET tempo_consegna_giorni = data_consegna - data_spedizione;

UPDATE dim_spedizione
SET fascia_tempo_consegna = CASE
  WHEN tempo_consegna_giorni <= 2 THEN '1-2 giorni'
  WHEN tempo_consegna_giorni BETWEEN 3 AND 5 THEN '3-5 giorni'
  WHEN tempo_consegna_giorni BETWEEN 6 AND 10 THEN '6-10 giorni'
  ELSE '10+ giorni'
END;

CREATE TABLE fact_vendite (
  vendita_sk SERIAL PRIMARY KEY,
  cliente_sk INT REFERENCES dim_cliente(cliente_sk),
  prodotto_sk INT REFERENCES dim_prodotto(prodotto_sk),
  data_sk INT REFERENCES dim_data(data_sk),
  spedizione_sk INT REFERENCES dim_spedizione(spedizione_sk),
  quantita INT,
  ordine_id INT,
  prezzo_unitario NUMERIC(10,2),
  sconto NUMERIC(5,2),
  ricavi NUMERIC(12,2)
);


WITH oltp AS (
  SELECT *
  FROM dblink(
    'dbname=techstore_2 user=postgres password=postgres host=localhost',
    '
    SELECT
      o.ordine_id,
      o.cliente_id,
      o.data_ordine,
      s.spedizione_id,
      d.prodotto_id,
      d.quantita,
      d.prezzo_unitario,
      d.sconto
    FROM ordini o
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    JOIN spedizioni s      ON s.ordine_id = o.ordine_id
    '
  ) AS t(
    ordine_id       INT,
    cliente_id      INT,
    data_ordine     DATE,
    spedizione_id   INT,
    prodotto_id     INT,
    quantita        INT,
    prezzo_unitario NUMERIC(10,2),
    sconto          NUMERIC(5,2)
  )
)
INSERT INTO fact_vendite (
  cliente_sk,
  prodotto_sk,
  data_sk,
  spedizione_sk,
  quantita,
  prezzo_unitario,
  sconto,
  ricavi,
  ordine_id
)
SELECT
  dc.cliente_sk,
  dp.prodotto_sk,
  dd.data_sk,
  ds.spedizione_sk,
  o.quantita,
  o.prezzo_unitario,
  o.sconto,
  (o.quantita * o.prezzo_unitario * (1 - o.sconto/100.0)) AS ricavi,
  o.ordine_id
FROM oltp o
JOIN dim_cliente    dc ON dc.cliente_id    = o.cliente_id
JOIN dim_prodotto   dp ON dp.product_id    = o.prodotto_id
JOIN dim_spedizione ds ON ds.spedizione_id = o.spedizione_id
JOIN dim_data       dd ON dd.data          = o.data_ordine;

