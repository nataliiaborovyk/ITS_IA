# Sistema di previsione delle cancellazioni delle prenotazioni alberghiere (Machine Learning)

Questo progetto ha l'obiettivo di prevedere se una prenotazione alberghiera verrà **confermata o cancellata** utilizzando tecniche di Machine Learning.

L'idea è costruire un modello in grado di stimare la probabilità di cancellazione e supportare decisioni di business basate sui dati.

---

# Descrizione del progetto

Le cancellazioni delle prenotazioni rappresentano un problema importante per gli hotel perché influenzano:

- la previsione dei ricavi
- la gestione dell’occupazione delle camere
- le strategie di prezzo

In questo progetto è stato sviluppato un modello di Machine Learning per prevedere il comportamento delle prenotazioni utilizzando dati storici.

Il modello è stato addestrato su un dataset storico e successivamente applicato a un **dataset più recente (2024)** per simulare un utilizzo reale del modello su nuovi dati.

---

# Fasi principali del progetto

## 1. Preparazione dei dati

- pulizia del dataset
- gestione dei valori mancanti
- rimozione di record inconsistenti
- trasformazione delle variabili

## 2. Feature Engineering

Sono state create nuove variabili per migliorare la capacità predittiva del modello, tra cui:

- gruppi di paesi (`country_group`)
- gruppi di agenti (`agent_group`)
- gruppi di richieste speciali (`special_requests_group`)
- gruppi di cancellazioni precedenti (`previous_cancellation_group`)
- tipo di hotel (`hotel_group`)
- indicatori del comportamento dei clienti

## 3. Addestramento del modello

È stato utilizzato un modello **LightGBM (Gradient Boosting)** per la previsione delle cancellazioni.

Il modello è stato configurato e addestrato utilizzando:

- gestione dello sbilanciamento delle classi
- parametri ottimizzati
- pipeline di preprocessing

## 4. Valutazione del modello

Le prestazioni del modello sono state valutate utilizzando diverse metriche:

- ROC AUC
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

Sono stati inoltre creati diversi grafici per interpretare il comportamento del modello.

## 5. Test su nuovi dati

Per simulare uno scenario reale:

- è stato utilizzato un dataset più recente (2024)
- è stata ricostruita la stessa pipeline di preprocessing
- il modello addestrato è stato applicato ai nuovi dati
- le previsioni sono state confrontate con i risultati reali

---

# Tecnologie utilizzate

- Python
- Pandas
- Scikit-learn
- LightGBM
- Matplotlib
- Dataiku

---

# Struttura della repository
Progetto_Hotel_Booking
│
├── Dataiku
│ Workflow di preparazione dati e modello sviluppato in Dataiku
│
├── Python
│ Implementazione completa della pipeline di Machine Learning in Python
│
├── hotel_booking_cancellation_ml_project_presentation.pdf
│ Slide di presentazione del progetto e delle strategie di business


---

# Risultati principali

Il modello ha identificato alcune variabili particolarmente importanti per la previsione delle cancellazioni, tra cui:

- tipo di deposito
- paese di provenienza del cliente
- segmento di mercato
- agente di prenotazione
- anticipo della prenotazione (lead time)
- richieste speciali del cliente

Sulla base di queste informazioni sono state proposte alcune **strategie di business**, ad esempio:

- politiche di deposito per ridurre le cancellazioni
- pricing dinamico basato sulla probabilità di conferma
- strategie differenziate per canali di prenotazione
- offerte personalizzate per clienti più affidabili

---

# Autore

Natalia Borovyk  
Studente di Data Analysis / Machine Learning