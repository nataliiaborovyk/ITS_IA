# Manuale Studente: Case Study Bike Sharing Europeo

---

## 📚 Introduzione

Benvenuto al case study completo sul Sistema di Bike Sharing Europeo! In questo progetto lavorerai con **dati reali** provenienti da 267 sistemi di bike sharing in tutta Europa, per un totale di oltre 25 milioni di noleggi.

Attraverso questo case study, imparerai a costruire un sistema completo di Business Intelligence, dal database transazionale fino alla dashboard interattiva e alla preparazione dei dati per il Machine Learning.

---

## 🎯 Cosa Imparerai

1. Come importare e gestire dati reali di grandi dimensioni
2. La differenza tra OLTP (database transazionale) e OLAP (data warehouse)
3. Come progettare uno schema a stella per l'analisi
4. Come implementare un processo ETL (Extract, Transform, Load)
5. Come scrivere query SQL per rispondere a domande di business
6. Come creare dashboard interattive con Metabase
7. Come preparare i dati per il Machine Learning

---

## ⚙️ Setup Iniziale

### 1. Verifica dei Prerequisiti

Assicurati di avere installato:

- Git

per installare: sudo apt install git
---

## 📥 Parte 1: Database Transazionale (OLTP)

### Obiettivo

Creare un database transazionale che simula il sistema operativo di un servizio di bike sharing, importando i dati reali dal dataset europeo.

### Step 1.0: Scarica il materiale nella cartella dove svolgi le esercitazioni
Apri   ../olpt/bash 01_download_dataset.sh e personalizza il percorso 

### Step 1.1: Download del Dataset

Apri un terminale e naviga nella directory del case study:

```bash
cd /path/to/case_study_bikesharing_real/oltp
bash 01_download_dataset.sh
```

Questo script:
1. Clona il repository GitHub del dataset
2. Copia i file sample (1000 righe) nella directory `/tmp/bikesharing_data/`

**Nota:** Per questo case study useremo i file sample per velocità. Il dataset completo (2.3 GB) può essere scaricato successivamente.

### Step 1.2: Creazione dello Schema OLTP

in pgAdmin, crea il database bikesharing_oltp:

tasto destro su Databases → Create → Database…

Name: bikesharing_oltp → Save

Ora seleziona il database bikesharing_oltp e apri il Query Tool su quel database:

tasto destro su bikesharing_oltp → Query Tool

copia e incolla lo script 02_create_oltp_schema.sql


Questo script crea:
- Database `bikesharing_oltp`
- 7 tabelle: `cities`, `bike_types`, `bikes`, `stations`, `trips`, `utenti`, `station_status`
- Indici per migliorare le performance

**Verifica:** Controlla che il database sia stato creato:


Dovresti vedere le 7 tabelle elencate.

### Step 1.3: Import dei Dati

modifica lo script 03_import_data.py aggiornando la Directory contenente i file CSV (path reale DENTRO il container its_dev)
DATA_DIR = Path('/home/...../data')

Esegui lo script Python da /path/to/case_study_bikesharing_real/oltp per importare i CSV:

```bash
python3 03_import_data.py
```

Lo script:
1. Importa i dati da `cities.csv`, `bike_types.csv`, `bikes.csv`, `stations.csv`, `trips.csv`
2. Genera sinteticamente la tabella `utenti` (non presente nel dataset originale per privacy)



**Verifica:** Controlla che i dati siano stati importati:

```sql
SELECT COUNT(*) FROM trips;
-- Dovresti vedere circa 1000 righe (file sample)
```

---

## 🏢 Parte 2: Data Warehouse (DWH)

### Obiettivo

Progettare e creare un Data Warehouse con schema a stella ottimizzato per l'analisi.

### Step 2.1: Creazione dello Schema a Stella

in pgAdmin, crea il database bikesharing_dwh:

tasto destro su Databases → Create → Database…

Esegui  01_create_dwh_schema.sql


Questo crea:

- Schema `dw`
- 5 dimensioni: `dim_utente`, `dim_citta`, `dim_stazione`, `dim_bicicletta`, `dim_tempo`
- 1 fact table: `fact_noleggi`

**Verifica:**

che le tabelle siano state correttamente create
```

### Step 2.2: Popolamento della Dimensione Tempo

Esegui lo script:

 02_populate_dim_tempo.sql


Questo popola `dim_tempo` con tutte le date dal 2018 al 2024.

**Verifica:**

```sql
SELECT COUNT(*) FROM dw.dim_tempo;
-- Dovresti vedere 2557 righe (7 anni)




## 🔄 Parte 3: Processo ETL

### Obiettivo

Implementare il processo ETL per trasferire e trasformare i dati dall'OLTP al DWH.

Step 3.1: 
Step 3.1: Abilitazione dell'Estensione dblink

```bash
psql -U postgres -d bikesharing_dwh -c "CREATE EXTENSION IF NOT EXISTS dblink;"

Step 3.2: Esecuzione del Processo ETL (pgAdmin)
Obiettivo

Eseguire il processo ETL per trasferire e trasformare i dati dal database OLTP (bikesharing_oltp) al Data Warehouse (bikesharing_dwh).

Come procedere (usando pgAdmin)

Apri pgAdmin

Connettiti al database bikesharing_dwh

Tasto destro sul database → Query Tool

Apri il file:

copia e incolla l’intero contenuto dello script ETL nel Query Editor

Esegui lo script cliccando su ▶ Execute

⚠️ Importante:
Lo script va eseguito tutto insieme, non riga per riga, perché:

usa TRUNCATE per ripulire le tabelle

carica prima le dimensioni

inserisce i record UNKNOWN

carica infine la fact table

🔍 Cosa fa lo script ETL

Lo script:

Legge i dati dal database OLTP tramite dblink

Popola le dimensioni del DWH:

dim_utente

dim_citta

dim_stazione

dim_bicicletta

(usa dim_tempo già popolata)

Inserisce i record UNKNOWN per la gestione dei valori mancanti

Popola la fact table fact_noleggi

✅ Verifica del risultato

Al termine dell’esecuzione, nel Query Tool, esegui:

SELECT COUNT(*) 
FROM dw.fact_noleggi;


📌 Risultato atteso:
Circa 1000 righe (una per ciascun noleggio del dataset di esempio).

 Nota didattica 
Se rilanci lo script ETL più volte:

i dati vengono rigenerati da zero

il risultato finale rimane coerente
Questo è il comportamento tipico di un ETL full refresh.



## 📊 Parte 4: Analisi OLAP

### Obiettivo

Scrivere query SQL per rispondere a domande di business.

### Step 4.1: Esecuzione delle Query

Apri il file `analisi/01_olap_queries.sql` in pgAdmin ed esegui le query una per una.

### Esercizi

**Esercizio 1: KPI Generali**

Calcola:
- Numero totale di noleggi
- Durata media dei noleggi
- Distanza media percorsa

**Esercizio 2: Analisi Temporale**

Analizza:
- Numero di noleggi per anno
- Numero di noleggi per giorno della settimana

**Esercizio 3: Analisi Geografica**

Identifica:
- Le 10 città con più noleggi
- Le 10 stazioni di partenza più popolari

**Esercizio 4: Analisi degli Utenti**

Comprendi:
- Numero di noleggi per tipo di abbonamento
- Numero di noleggi per fascia d'età

**Esercizio 5: Analisi delle Biciclette**

Analizza:
- Numero di noleggi per tipo di propulsione
- Durata e distanza media per tipo di propulsione

---

## 📈 Parte 5: Dashboard Metabase

### Obiettivo

Creare una dashboard interattiva per monitorare i KPI.

### Step 5.1: Connessione a Metabase

1. Apri Metabase nel browser
2. Aggiungi una nuova connessione database:
   - Tipo: PostgreSQL
   - Nome: Bike Sharing DWH
   - Host: its_postgresql
   - Port: 5432
   - Database: bikesharing_dwh
   - Username: postgres
   - Password: postgres

### Step 5.2: Creazione delle Domande

Segui la guida in `metabase/01_metabase_dashboard_guide.md` per creare le 8 domande.

### Step 5.3: Creazione della Dashboard

Assembla le domande in una dashboard interattiva con filtri per periodo e paese.

---

## 🤖 Parte 6: Feature Engineering

### Obiettivo

Estrarre feature dal DWH per preparare un dataset per il Machine Learning.

### Step 6.1: Esecuzione dello Script

```bash
cd ../feature_engineering
psql -U postgres -d bikesharing_dwh -f 01_feature_engineering.sql
```

### Step 6.2: Esportazione in CSV

In pgAdmin, esegui:

```sql
COPY (SELECT * FROM ml.customer_features) TO '/tmp/customer_features.csv' WITH (FORMAT CSV, HEADER);
```

Il file CSV sarà salvato in `/tmp/customer_features.csv` e potrà essere usato nelle unità successive per il Machine Learning.

---

## 🆘 Troubleshooting

### Problema: "database does not exist"

**Soluzione:** Verifica di aver eseguito lo script di creazione del database.

### Problema: "permission denied"

**Soluzione:** Verifica i permessi dell'utente PostgreSQL o usa `sudo`.

### Problema: "dblink extension not found"

**Soluzione:** Installa l'estensione:

```bash
sudo apt-get install postgresql-contrib
```

### Problema: "ModuleNotFoundError: No module named 'pandas'"

**Soluzione:** Installa le librerie Python:

```bash
pip install pandas psycopg2-binary faker
```

---

## ✅ Checklist di Completamento

- [ ] Database OLTP creato e popolato
- [ ] Data Warehouse creato con schema a stella
- [ ] Processo ETL eseguito con successo
- [ ] Query OLAP eseguite e risultati verificati
- [ ] Dashboard Metabase creata e funzionante
- [ ] Dataset per ML estratto e esportato in CSV

---

**Congratulazioni!** Hai completato il case study completo sul Sistema di Bike Sharing Europeo! 



Bikesharing

1. 
	- cambiare path in 01_download_dataset.sh indicando path verso  cartella data da docker 
	- lanciare: bash 01_download_dataset.sh

2. 
	- creare database  bikesharing_oltp nel pgadmin
	- coppiare il codice nel query tools da 02_create_oltp_schema.sql

3. 
	- aggiungere Faker==33.3.0 e psycopg2-binary==2.9.10 nel python_requirements.txt nella cartella con esercizi
	- docher compose down
	- docker compose up --build -d
	- cambiare path in script 03_import_data.py  indicando path verso  cartella data da docker 
	- lanciare: python3 03_import_data.py 

4. 
	- creare database bikesharing_dwh nel pg admin
	- copiare il codice da 01_create_dwh_schema_pgadmin_query_tool.sql nel query tools
	- copiare 02_populate_dim_tempo_pgadmin_querytool.sql nel query tools

5. 
	- eseguire CREATE EXTENSION IF NOT EXISTS dblink; nel query tools
	- copiare 01_etl_process_agg.sql nel query tools