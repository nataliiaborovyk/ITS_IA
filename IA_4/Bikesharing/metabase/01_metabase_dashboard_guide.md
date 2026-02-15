# Guida alla Creazione Dashboard Metabase (Dataset Reale)

---

## 🎯 Obiettivo

Creare una dashboard interattiva in Metabase per monitorare i KPI e analizzare i dati del DWH del sistema di bike sharing.

## ⚙️ Prerequisiti

1. Metabase installato e configurato
2. Connessione al database `bikesharing_dwh` stabilita
3. DWH popolato tramite lo script ETL

## 📊 Dashboard: "Monitoraggio Bike Sharing Europeo"

### Parte 1: Creazione delle Domande (Analisi)

Crea le seguenti 8 domande in Metabase, salvandole una per una.

**1. Totale Noleggi (Numero)**
- **Tipo:** Numero
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe

**2. Durata Media Noleggio (min) (Numero)**
- **Tipo:** Numero
- **Dati:** `fact_noleggi`
- **Metrica:** Media di `durata_minuti`

**3. Distanza Media Noleggio (km) (Numero)**
- **Tipo:** Numero
- **Dati:** `fact_noleggi`
- **Metrica:** Media di `distanza_km`

**4. Noleggi per Giorno (Grafico a Linee)**
- **Tipo:** Grafico a Linee
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe
- **Raggruppa per:** `dim_tempo.data_completa` (per Giorno)

**5. Noleggi per Giorno della Settimana (Grafico a Barre)**
- **Tipo:** Grafico a Barre
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe
- **Raggruppa per:** `dim_tempo.nome_giorno`

**6. Top 10 Città per Noleggi (Tabella)**
- **Tipo:** Tabella
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe
- **Raggruppa per:** `dim_citta.nome_sistema`
- **Limite:** 10
- **Ordina per:** Conteggio (discendente)

**7. Noleggi per Tipo di Propulsione (Grafico a Torta)**
- **Tipo:** Grafico a Torta
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe
- **Raggruppa per:** `dim_bicicletta.propulsione`

**8. Mappa delle Stazioni di Partenza (Mappa)**
- **Tipo:** Mappa
- **Dati:** `fact_noleggi`
- **Metrica:** Conteggio delle righe
- **Raggruppa per:** `dim_stazione.nome_stazione`
- **Campi mappa:** `dim_stazione.latitudine`, `dim_stazione.longitudine`

### Parte 2: Creazione della Dashboard

1. Crea una nuova dashboard chiamata "Monitoraggio Bike Sharing Europeo"
2. Aggiungi le 8 domande create alla dashboard
3. Organizza la dashboard come segue:

```
+--------------------------------+--------------------------------+--------------------------------+
| Totale Noleggi (Numero)        | Durata Media Noleggio (Numero) | Distanza Media Noleggio (Numero) |
+--------------------------------+--------------------------------+--------------------------------+
| Noleggi per Giorno (Grafico a Linee)                                                             |
+--------------------------------------------------------------------------------------------------+
| Noleggi per Giorno della Settimana (Grafico a Barre) | Top 10 Città per Noleggi (Tabella)         |
+------------------------------------------------------+------------------------------------------+
| Noleggi per Tipo di Propulsione (Grafico a Torta)    | Mappa delle Stazioni di Partenza (Mappa)   |
+------------------------------------------------------+------------------------------------------+
```

### Parte 3: Aggiunta dei Filtri

1. Aggiungi un filtro di tipo **Tempo** alla dashboard
   - **Nome:** "Periodo"
   - **Collega a:** `dim_tempo.data_completa` di tutte le domande

2. Aggiungi un filtro di tipo **Testo** alla dashboard
   - **Nome:** "Paese"
   - **Collega a:** `dim_citta.paese` di tutte le domande

## ✅ Risultato Finale

Una dashboard interattiva che permette di:
- Visualizzare i KPI principali del servizio
- Analizzare i trend temporali dei noleggi
- Identificare le città e le stazioni più attive
- Filtrare i dati per periodo e paese
- Comprendere la distribuzione dei noleggi per tipo di bici
