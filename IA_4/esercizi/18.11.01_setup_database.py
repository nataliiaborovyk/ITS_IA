"""
Esercitazione 1 - Setup Database OLTP TechStore
================================================

Questo script crea e popola il database operazionale (OLTP) di TechStore.

Esecuzione:
    python 01_setup_database.py

Output:
    - techstore_oltp.db (database SQLite)
    - Log di creazione e popolamento
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import sys

# Configurazione
DB_PATH = '../techstore_oltp.db'
N_CLIENTI = 20000
N_ORDINI = 100000
SEED = 42  # Serve per avere sempre gli stessi numeri casuali

# Setup
random.seed(SEED)   # imposta il punto di partenza della sequenza casuale.
fake = Faker('it_IT')  # crea un oggetto fake per generare dati finti in stile italiano
Faker.seed(SEED)     # è simile a random.seed(SEED), ma per la libreria Faker.


def print_progress(message, step=None, total=None):
    """Stampa messaggio di progresso."""
    if step and total:
        percentage = (step / total) * 100
        print(f"[{percentage:5.1f}%] {message}")   # larghezza minima di 5 caratteri (serve per allineare bene in stampa)
    else: 
        print(f"[INFO] {message}")


def create_tables(cursor):
    """Crea le tabelle del database OLTP."""
    print_progress("Creazione tabelle...")
    
    # Drop tabelle se esistono
    tables_to_drop = [
        'dettagli_ordini', 'spedizioni', 'pagamenti', 'ordini',
        'prodotti', 'categorie', 'clienti'
    ]
    for table in tables_to_drop:                              # cursor è, in pratica, un traduttore tra Python e SQL.
        cursor.execute(f"DROP TABLE IF EXISTS {table}")      # cursor.execute(...) è il metodo usato per eseguire un singolo comando SQL
    
    # CATEGORIE
    cursor.execute("""
    CREATE TABLE categorie (
        categoria_id INTEGER PRIMARY KEY,
        nome_categoria VARCHAR(100) NOT NULL,
        descrizione TEXT
    )
    """)
    
    # CLIENTI
    cursor.execute("""
    CREATE TABLE clienti (
        cliente_id INTEGER PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        cognome VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        telefono VARCHAR(20),
        citta VARCHAR(100),
        regione VARCHAR(50),
        cap VARCHAR(10),
        data_registrazione DATE NOT NULL,
        segmento VARCHAR(20)
    )
    """)
    
    # PRODOTTI
    cursor.execute("""
    CREATE TABLE prodotti (
        prodotto_id INTEGER PRIMARY KEY,
        nome_prodotto VARCHAR(200) NOT NULL,
        categoria_id INTEGER NOT NULL,
        prezzo DECIMAL(10,2) NOT NULL,
        costo DECIMAL(10,2) NOT NULL,
        marca VARCHAR(100),
        quantita_stock INTEGER DEFAULT 0,
        FOREIGN KEY (categoria_id) REFERENCES categorie(categoria_id)
    )
    """)
    
    # ORDINI
    cursor.execute("""
    CREATE TABLE ordini (
        ordine_id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        data_ordine DATETIME NOT NULL,
        stato VARCHAR(20) NOT NULL,
        canale VARCHAR(20),
        FOREIGN KEY (cliente_id) REFERENCES clienti(cliente_id)
    )
    """)
    
    # DETTAGLI_ORDINI
    cursor.execute("""
    CREATE TABLE dettagli_ordini (
        dettaglio_id INTEGER PRIMARY KEY,
        ordine_id INTEGER NOT NULL,
        prodotto_id INTEGER NOT NULL,
        quantita INTEGER NOT NULL,
        prezzo_unitario DECIMAL(10,2) NOT NULL,
        sconto DECIMAL(5,2) DEFAULT 0,
        FOREIGN KEY (ordine_id) REFERENCES ordini(ordine_id),
        FOREIGN KEY (prodotto_id) REFERENCES prodotti(prodotto_id)
    )
    """)
    
    # SPEDIZIONI
    cursor.execute("""
    CREATE TABLE spedizioni (
        spedizione_id INTEGER PRIMARY KEY,
        ordine_id INTEGER NOT NULL,
        data_spedizione DATE,
        data_consegna DATE,
        corriere VARCHAR(50),
        costo_spedizione DECIMAL(10,2),
        FOREIGN KEY (ordine_id) REFERENCES ordini(ordine_id)
    )
    """)
    
    # PAGAMENTI
    cursor.execute("""
    CREATE TABLE pagamenti (
        pagamento_id INTEGER PRIMARY KEY,
        ordine_id INTEGER NOT NULL,
        metodo_pagamento VARCHAR(50) NOT NULL,
        importo DECIMAL(10,2) NOT NULL,
        data_pagamento DATETIME NOT NULL,
        stato_pagamento VARCHAR(20) NOT NULL,
        FOREIGN KEY (ordine_id) REFERENCES ordini(ordine_id)
    )
    """)
    
    print_progress("✓ Tabelle create con successo")


def populate_categorie(cursor):
    """Popola la tabella categorie."""
    print_progress("Popolamento categorie...")
    
    categorie_data = [
        (1, 'Laptop', 'Computer portatili e notebook'),
        (2, 'Smartphone', 'Telefoni cellulari e smartphone'),
        (3, 'Tablet', 'Tablet e e-reader'),
        (4, 'Accessori', 'Accessori per dispositivi elettronici'),
        (5, 'Componenti', 'Componenti hardware per PC'),
        (6, 'Audio', 'Cuffie, speaker e dispositivi audio'),
        (7, 'Gaming', 'Console e accessori gaming'),
        (8, 'Smartwatch', 'Orologi intelligenti e fitness tracker')
    ]
    
    # cursor.executemany(query_string, sequence_of_sequences) - Esegue la stessa query per ogni elemento della lista.
    cursor.executemany("INSERT INTO categorie VALUES (?, ?, ?)", categorie_data)  # esegui la query una volta per ogni tupla sostituendo i ? con gli elementi della tupla.
    # esegui N volte:
    # INSERT INTO ... VALUES (lista[i][0], lista[i][1], lista[i][2]), dove N = len(lista)

    
    print_progress(f"✓ Inserite {len(categorie_data)} categorie")


def populate_prodotti(cursor):
    """Popola la tabella prodotti."""
    print_progress("Popolamento prodotti...")
    
    prodotti_templates: dict = {
        1: [  # Laptop
            ('Dell XPS 13', 'Dell', 1299.99, 850),
            ('MacBook Air M2', 'Apple', 1499.99, 1000),
            ('Lenovo ThinkPad X1', 'Lenovo', 1399.99, 900),
            ('HP Pavilion 15', 'HP', 699.99, 450),
            ('ASUS ZenBook', 'ASUS', 899.99, 600),
        ],
        2: [  # Smartphone
            ('iPhone 14 Pro', 'Apple', 1299.99, 850),
            ('Samsung Galaxy S23', 'Samsung', 999.99, 650),
            ('Google Pixel 7', 'Google', 699.99, 450),
            ('Xiaomi 13', 'Xiaomi', 599.99, 380),
            ('OnePlus 11', 'OnePlus', 799.99, 520),
        ],
        3: [  # Tablet
            ('iPad Pro 12.9', 'Apple', 1199.99, 780),
            ('Samsung Galaxy Tab S8', 'Samsung', 799.99, 520),
            ('iPad Air', 'Apple', 699.99, 450),
            ('Amazon Fire HD 10', 'Amazon', 199.99, 120),
        ],
        4: [  # Accessori
            ('Mouse Logitech MX Master', 'Logitech', 99.99, 50),
            ('Tastiera Meccanica RGB', 'Corsair', 149.99, 80),
            ('Webcam HD 1080p', 'Logitech', 79.99, 40),
            ('Hub USB-C 7 porte', 'Anker', 49.99, 25),
            ('Custodia Laptop 15"', 'Case Logic', 29.99, 12),
        ],
        5: [  # Componenti
            ('SSD Samsung 1TB', 'Samsung', 129.99, 70),
            ('RAM DDR4 16GB', 'Corsair', 79.99, 45),
            ('Scheda Video RTX 3060', 'NVIDIA', 499.99, 320),
            ('Processore Intel i7', 'Intel', 399.99, 250),
        ],
        6: [  # Audio
            ('AirPods Pro', 'Apple', 279.99, 150),
            ('Sony WH-1000XM5', 'Sony', 399.99, 220),
            ('JBL Flip 6', 'JBL', 129.99, 70),
            ('Bose QuietComfort', 'Bose', 349.99, 190),
        ],
        7: [  # Gaming
            ('PlayStation 5', 'Sony', 549.99, 380),
            ('Xbox Series X', 'Microsoft', 549.99, 380),
            ('Nintendo Switch OLED', 'Nintendo', 349.99, 230),
            ('Controller Xbox Elite', 'Microsoft', 179.99, 100),
        ],
        8: [  # Smartwatch
            ('Apple Watch Series 8', 'Apple', 499.99, 320),
            ('Samsung Galaxy Watch 5', 'Samsung', 299.99, 180),
            ('Fitbit Sense 2', 'Fitbit', 299.99, 180),
            ('Garmin Fenix 7', 'Garmin', 699.99, 450),
        ]
    }
    
    prodotti_data = []
    prodotto_id = 1
    
    for categoria_id, prodotti in prodotti_templates.items():
        for nome, marca, prezzo, costo in prodotti:
            stock = random.randint(10, 200)
            prodotti_data.append((
                prodotto_id, nome, categoria_id, prezzo, costo, marca, stock
            ))
            prodotto_id += 1

    # .executemany() → ripete lo stesso comando molte volte, con dati diversi     
    cursor.executemany("INSERT INTO prodotti VALUES (?, ?, ?, ?, ?, ?, ?)", prodotti_data)
    print_progress(f"✓ Inseriti {len(prodotti_data)} prodotti")
    
    return len(prodotti_data)


def populate_clienti(cursor, n_clienti):
    """Popola la tabella clienti."""
    print_progress(f"Popolamento {n_clienti:,} clienti...") # :, formatta il numero con il separatore delle migliaia → 20000 diventa 20,000 (in ambiente inglese)
    
    clienti_data = []
    segmenti = ['Bronze', 'Silver', 'Gold', 'Platinum']
    pesi_segmenti = [0.5, 0.3, 0.15, 0.05]   # probabilità relative

    # Lista semplice di regioni italiane 
    regioni = [ "Lombardia", "Lazio", "Piemonte", "Campania", "Veneto", 
               "Emilia-Romagna", "Toscana", "Sicilia", "Puglia", "Liguria", 
               "Marche", "Abruzzo", "Calabria", "Sardegna", "Umbria", 
               "Trentino-Alto Adige", "Friuli-Venezia Giulia", "Basilicata", 
               "Molise", "Valle d'Aosta"
    ]
    
    # Intervallo di date per la registrazione
    data_inizio = datetime.now() - timedelta(days=1095)
    data_fine = datetime.now()
    
    for i in range(1, n_clienti + 1):
        nome = fake.first_name()
        cognome = fake.last_name()
        email = f"{nome.lower()}.{cognome.lower()}{i}@{fake.free_email_domain()}"
        telefono = fake.phone_number()
        citta = fake.city()
        regione = random.choice(regioni)
        cap = fake.postcode()
        data_reg = fake.date_between(start_date=data_inizio, end_date=data_fine)
        segmento = random.choices(segmenti, weights=pesi_segmenti)[0] 
        # random.choices(lista, weights=..., k=1) restituisce una lista di elementi scelti secondo i pesi.
        # k di default è 1, quindi ottieni una lista lunga 1
        # Per avere il valore singolo dalla lista, prendono [0]

        clienti_data.append((
            i, nome, cognome, email, telefono, citta, regione, cap, data_reg, segmento
        ))
        
        if i % 5000 == 0:
            print_progress(f"Generati clienti...", i, n_clienti)
    
    cursor.executemany(
        "INSERT INTO clienti VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        clienti_data
    )
    print_progress(f"✓ Inseriti {n_clienti:,} clienti")


def populate_ordini(cursor, n_ordini, n_clienti, n_prodotti):
    """Popola le tabelle ordini, dettagli_ordini, spedizioni e pagamenti."""
    print_progress(f"Popolamento {n_ordini:,} ordini e transazioni...")
    
    ordini_data = []
    dettagli_data = []
    spedizioni_data = []
    pagamenti_data = []
    
    stati_ordine = ['Completato', 'In Elaborazione', 'Spedito', 'Consegnato', 'Cancellato']
    pesi_stati = [0.7, 0.05, 0.1, 0.12, 0.03]
    canali = ['Web', 'Mobile App', 'Telefono']
    pesi_canali = [0.6, 0.35, 0.05]
    corrieri = ['DHL', 'UPS', 'FedEx', 'Poste Italiane', 'BRT']
    metodi_pagamento = ['Carta di Credito', 'PayPal', 'Bonifico', 'Contrassegno']
    pesi_pagamento = [0.5, 0.3, 0.1, 0.1]
    
    data_inizio = datetime.now() - timedelta(days=730)
    data_fine = datetime.now()
    
    dettaglio_id = 1   # Ogni riga di dettagli_ordini avrà un proprio dettaglio_id univoco
    
    # Prezzi prodotti (per velocità)
    prezzi_prodotti = {i: random.uniform(50, 1500) for i in range(1, n_prodotti + 1)}
    # Crea un dizionario con chiave = prodotto_id,  valore = un prezzo casuale tra 50 e 1500 (float)
    
    for ordine_id in range(1, n_ordini + 1):
        # Ordine
        cliente_id = random.randint(1, n_clienti)
        data_ordine = fake.date_time_between(start_date=data_inizio, end_date=data_fine)
        stato = random.choices(stati_ordine, weights=pesi_stati)[0]
        canale = random.choices(canali, weights=pesi_canali)[0]
        
        ordini_data.append((ordine_id, cliente_id, data_ordine, stato, canale))
        
        # Dettagli ordine
        n_prodotti_ordine = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.2, 0.07, 0.03])[0]  # quanti prodotti
        prodotti_ordine = random.sample(range(1, n_prodotti + 1), n_prodotti_ordine)  # quali prodotti (id)
        # random.sample(sequenza, k) restituisce k elementi diversi, presi senza ripetizioni, dalla sequenza.

        importo_totale = 0
        
        for prodotto_id in prodotti_ordine:
            quantita = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
            prezzo = prezzi_prodotti[prodotto_id]
            sconto = random.choices([0, 5, 10, 15, 20], weights=[0.6, 0.2, 0.1, 0.07, 0.03])[0]
            
            dettagli_data.append((
                dettaglio_id, ordine_id, prodotto_id, quantita, prezzo, sconto
            ))
            
            importo_totale += quantita * prezzo * (1 - sconto/100)
            dettaglio_id += 1
        
        # Spedizione
        if stato != 'Cancellato':
            data_spedizione = data_ordine + timedelta(days=random.randint(1, 3))
            # Perché solo un ordine consegnato ha una data di consegna.
            data_consegna = data_spedizione + timedelta(days=random.randint(2, 7)) if stato == 'Consegnato' else None
            corriere = random.choice(corrieri)
            costo_spedizione = random.choice([0, 4.99, 9.99])
            
            spedizioni_data.append((
                ordine_id, ordine_id, data_spedizione.date(),
                data_consegna.date() if data_consegna else None,
                corriere, costo_spedizione
            ))
        
        # Pagamento
        metodo = random.choices(metodi_pagamento, weights=pesi_pagamento)[0]
        data_pagamento = data_ordine + timedelta(minutes=random.randint(1, 30))
        stato_pagamento = 'Completato' if stato != 'Cancellato' else 'Rimborsato'
        
        pagamenti_data.append((
            ordine_id, ordine_id, metodo, importo_totale, data_pagamento, stato_pagamento
        ))
        
        if ordine_id % 20000 == 0:
            print_progress(f"Generati ordini...", ordine_id, n_ordini)
    
    # Inserimento batch
    print_progress("Inserimento dati nel database...")
    
    cursor.executemany("INSERT INTO ordini VALUES (?, ?, ?, ?, ?)", ordini_data)  # esegue molti comandi simili molto velocemente
    print_progress("  ✓ Ordini inseriti")
    
    cursor.executemany("INSERT INTO dettagli_ordini VALUES (?, ?, ?, ?, ?, ?)", dettagli_data)
    print_progress("  ✓ Dettagli ordini inseriti")
    
    cursor.executemany("INSERT INTO spedizioni VALUES (?, ?, ?, ?, ?, ?)", spedizioni_data)
    print_progress("  ✓ Spedizioni inserite")
    
    cursor.executemany("INSERT INTO pagamenti VALUES (?, ?, ?, ?, ?, ?)", pagamenti_data)
    print_progress("  ✓ Pagamenti inseriti")
    
    print_progress(f"✓ Inseriti {n_ordini:,} ordini con {len(dettagli_data):,} righe")


def main():
    """Funzione principale."""
    print("=" * 70)
    print("SETUP DATABASE OLTP - TechStore E-commerce")
    print("=" * 70)
    print()
    
    try:
        # Connessione database
        print_progress(f"Creazione database: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)  # se il file non esiste → lo crea, se esiste → lo apre. Crea la connessione al file .db
        cursor = conn.cursor()    # crea il "traduttore" che esegue SQL
        
        # Creazione tabelle
        create_tables(cursor)
        conn.commit()           #  se non faccio commit, i dati non vengono salvati.
        
        # Popolamento
        populate_categorie(cursor)
        conn.commit()   # salva tutto nel file
        
        n_prodotti = populate_prodotti(cursor)
        conn.commit()
        
        populate_clienti(cursor, N_CLIENTI)
        conn.commit()
        
        populate_ordini(cursor, N_ORDINI, N_CLIENTI, n_prodotti)
        conn.commit()
        
        # Statistiche finali
        print()
        print("=" * 70)
        print("DATABASE CREATO CON SUCCESSO!")
        print("=" * 70)
        print()
        print("Statistiche:")
        print(f"  - Categorie:       8")
        print(f"  - Prodotti:        {n_prodotti}")
        print(f"  - Clienti:         {N_CLIENTI:,}")
        print(f"  - Ordini:          {N_ORDINI:,}")
        print(f"  - Database:        {DB_PATH}")
        print()
        print("Prossimo passo: esegui 02_esplora_oltp.py")
        print()
        
        # Chiusura
        conn.close()
        
    except Exception as e:
        print(f"\n[ERRORE] {str(e)}", file=sys.stderr)
        sys.exit(1)

        # sys è un modulo per interagire con l’interprete Python e il sistema:
        #     sys.stderr → lo “stream” degli errori (stampare errori separati dall’output normale).
        #     sys.exit(1) → uscire dal programma con codice di errore.


if __name__ == "__main__":
    main()

