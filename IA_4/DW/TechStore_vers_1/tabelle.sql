
CREATE TABLE dim_data (
    data_sk SERIAL PRIMARY KEY, -- Chiave surrogata per il DW
    data DATE UNIQUE, -- Data reale
    anno INT, -- Anno estratto dalla data
    mese INT, -- Mese (1-12)
    giorno INT, -- Giorno del mese (1-31)
    trimestre INT, -- Trimestre (1-4)
    mese_nome TEXT, -- Nome del mese (January, February...)
    giorno_settimana INT, -- 0=Sunday, 1=Monday...
    giorno_nome TEXT -- Nome del giorno (Monday...)
);

INSERT INTO dim_data (data, anno, mese, giorno, trimestre,
    mese_nome, giorno_settimana, giorno_nome)
SELECT
    d, -- La data
    EXTRACT(YEAR FROM d), -- Anno
    EXTRACT(MONTH FROM d), -- Mese numerico
    EXTRACT(DAY FROM d), -- Giorno
    EXTRACT(QUARTER FROM d), -- Trimestre
    TO_CHAR(d, 'Month'), -- Nome del mese
    EXTRACT(DOW FROM d), -- Giorno della settimana
    TO_CHAR(d, 'Day') -- Nome del giorno
FROM generate_series('2020-01-01'::date,
    '2026-12-31'::date,
    '1 day'::interval) AS d;



CREATE TABLE dim_cliente (
    cliente_sk SERIAL PRIMARY KEY, -- Chiave surrogata del DW
    cliente_id INT UNIQUE, -- ID originale dal DB OLTP
    nome TEXT,
    cognome TEXT,
    citta TEXT,
    regione TEXT,
    data_nascita DATE, -- Arricchimento
    eta INT, -- Arricchimento
    fascia_eta TEXT -- Arricchimento
);


INSERT INTO dim_cliente 
(cliente_id, nome, cognome, citta, regione)
SELECT *
FROM dblink(
  'dbname=techstore_oltp user=postgres password=postgres host=localhost',
  'SELECT cliente_id, nome, cognome, citta, regione FROM clienti'
) AS t(cliente_id INT, 
       nome TEXT, 
       cognome TEXT, 
       citta TEXT, 
       regione TEXT);


UPDATE dim_cliente
SET data_nascita =
    date '1942-01-01'
    + (random() * 23725)::int;

UPDATE dim_cliente
SET eta = EXTRACT(YEAR FROM age(CURRENT_DATE, data_nascita));

UPDATE dim_cliente
SET fascia_eta = CASE
    WHEN eta < 25 THEN '18-24'
    WHEN eta BETWEEN 25 AND 39 
    THEN '25-39'
    WHEN eta BETWEEN 40 AND 59 
    THEN '40-59'
    ELSE '60+'
END;

CREATE TABLE dim_prodotto (
    prodotto_sk SERIAL PRIMARY KEY,   -- surrogate key
    product_id INT UNIQUE,            -- natural key dal sistema
    nome TEXT,
    categoria TEXT,
    marca TEXT
);


INSERT INTO dim_prodotto (product_id, nome, categoria, marca)
SELECT *
FROM dblink(
  'dbname=techstore_oltp user=postgres password=postgres host=localhost',
  'SELECT p.prodotto_id,
          p.nome_prodotto,
          c.nome_categoria,
          p.marca
   FROM prodotti p
   JOIN categorie c ON p.categoria_id = c.categoria_id'
) AS t(product_id INT, nome TEXT, categoria TEXT, marca TEXT);

CREATE TABLE dim_spedizione (
  spedizione_sk SERIAL PRIMARY KEY,      -- chiave surrogata DW
  spedizione_id INT UNIQUE,              -- id spedizione dal sistema OLTP
  corriere TEXT,                         -- es. SDA, DHL, UPS...
  costo NUMERIC(10,2),                   -- costo della spedizione
  data_spedizione DATE,                  -- quando è partita la spedizione
  data_consegna DATE,                    -- quando è stata consegnata
  tempo_consegna_giorni INT,             -- differenza in giorni
  fascia_tempo_consegna TEXT             -- es. "0-2 giorni", "3-5 giorni", ecc.
);
-- spedizione_sk → chiave artificiale (solo per il DW), verrà usata nella FACT_VENDITE
-- spedizione_id → l’ID reale, che esiste nel database OLTP (techstore_oltp)
-- corriere, costo → descrivono la spedizione
-- data_spedizione, data_consegna → servono per calcolare il tempo di consegna
-- tempo_consegna_giorni → numero di giorni tra spedizione e consegna
-- fascia_tempo_consegna → raggruppamento (es. “0–2 giorni”, “3–7”, “>7”)

INSERT INTO dim_spedizione 
(spedizione_id, corriere, costo, 
 data_spedizione, data_consegna)
SELECT *
FROM dblink(
  'dbname=techstore_oltp user=postgres password=postgres host=localhost',
  'SELECT s.spedizione_id,
          s.corriere,
          s.costo_spedizione,
          s.data_spedizione,
          s.data_consegna
   FROM spedizioni s'
) AS t(
    spedizione_id BIGINT,
    corriere TEXT,
    costo NUMERIC(10,2),
    data_spedizione DATE,
    data_consegna DATE
);

-- Calcolo del tempo di consegna
UPDATE dim_spedizione
SET tempo_consegna_giorni = data_consegna - data_spedizione;

-- Fasce di consegna
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
                'dbname=techstore_oltp user=postgres password=postgres host=localhost',
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
                JOIN spedizioni s ON s.ordine_id = o.ordine_id
                '
            ) AS t(
                    ordine_id BIGINT,
                    cliente_id BIGINT,
                    data_ordine DATE,
                    spedizione_id BIGINT,
                    prodotto_id BIGINT,
                    quantita INT,
                    prezzo_unitario NUMERIC(10,2),
                    sconto NUMERIC(5,2)
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
JOIN dim_cliente    dc ON dc.cliente_id     = o.cliente_id
JOIN dim_prodotto   dp ON dp.product_id     = o.prodotto_id
JOIN dim_spedizione ds ON ds.spedizione_id  = o.spedizione_id
JOIN dim_data       dd ON dd.data           = o.data_ordine;
