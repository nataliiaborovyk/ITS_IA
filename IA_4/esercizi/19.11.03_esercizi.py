"""
Esercitazione 1 - Esercizi Pratici
===================================

Esercizi pratici per applicare i concetti appresi.

Esecuzione:
    python 03_esercizi.py

Per vedere le soluzioni:
    python 03_soluzioni.py
"""

import sqlite3
import pandas as pd

# Configurazione
DB_PATH = './data/techstore_oltp.db'


def print_exercise(number, title, description, requirements):
    """Stampa intestazione esercizio."""
    print("\n" + "=" * 70)
    print(f"ESERCIZIO {number}: {title}")
    print("=" * 70)
    print()
    print(description)
    print()
    print("La query deve restituire:")
    for req in requirements:
        print(f"  - {req}")
    print()


def esercizio_1():
    """Esercizio 1: Analisi Canali di Vendita."""
    print_exercise(
        1,
        "Analisi Canali di Vendita",
        "Scrivi una query per analizzare le vendite per canale (Web, Mobile App, Telefono) negli ultimi 6 mesi.",
        [
            "Canale",
            "Numero ordini",
            "Ricavi totali",
            "Valore medio ordine"
        ]
    )
    
    print("SUGGERIMENTI:")
    print("  - Usa le tabelle: ordini, dettagli_ordini")
    print("  - Filtra per data: date('now', '-6 months')")
    print("  - Escludi ordini cancellati")
    print("  - Raggruppa per canale")
    print()
    
    # Area per scrivere la query
    query = """
    SELECT 
        o.canale AS canale,
        COUNT(DISTINCT o.ordine_id) AS n_ordini,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS ricavi_totali,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) 
            / COUNT(DISTINCT o.ordine_id) AS valore_medio_ordine
    FROM ordini o
        JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    WHERE o.data_ordine >= date('now', '-6 months')
        AND o.stato != 'Cancellato'
    GROUP BY o.canale
    ORDER BY ricavi_totali DESC
    """
    
    print("QUERY DA COMPLETARE:")
    print(query)
    print()
    print("Modifica la query sopra e riesegui lo script.")
    print("Per vedere la soluzione, esegui: python 03_soluzioni.py")
    print()


def esercizio_2():
    """Esercizio 2: Analisi Geografica."""
    print_exercise(
        2,
        "Analisi Geografica",
        "Scrivi una query per analizzare le vendite per regione.",
        [
            "Regione",
            "Numero clienti unici",
            "Numero ordini",
            "Ricavi totali"
        ]
    )
    
    print("SUGGERIMENTI:")
    print("  - Usa le tabelle: clienti, ordini, dettagli_ordini")
    print("  - Usa COUNT(DISTINCT ...) per clienti unici")
    print("  - Escludi ordini cancellati")
    print("  - Ordina per ricavi decrescenti")
    print("  - Limita ai top 10")
    print()
    
    # Area per scrivere la query
    query = """
    SELECT 
        c.regione AS regione,
        COUNT(DISTINCT c.cliente_id) AS n_clienti_unici,
        COUNT(DISTINCT o.ordine_id) AS n_ordini,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS ricavi_totali
    FROM clienti c
        JOIN ordini o ON c.cliente_id = o.cliente_id
        JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    WHERE o.stato != 'Cancellato'
    GROUP BY c.regione
    ORDER BY ricavi_totali DESC
    LIMIT 10
    """
    
    print("QUERY DA COMPLETARE:")
    print(query)
    print()
    print("Modifica la query sopra e riesegui lo script.")
    print("Per vedere la soluzione, esegui: python 03_soluzioni.py")
    print()


def esercizio_3():
    """Esercizio 3: Segmentazione Clienti."""
    print_exercise(
        3,
        "Analisi Segmentazione Clienti",
        "Analizza il comportamento d'acquisto per segmento di clienti (Bronze, Silver, Gold, Platinum).",
        [
            "Segmento",
            "Numero clienti",
            "Numero medio ordini per cliente",
            "Valore medio ordine",
            "Ricavi totali"
        ]
    )
    
    print("SUGGERIMENTI:")
    print("  - Usa le tabelle: clienti, ordini, dettagli_ordini")
    print("  - Calcola ordini per cliente: COUNT(ordini) / COUNT(clienti)")
    print("  - Usa AVG() per valore medio ordine")
    print("  - Ordina per segmento (Platinum, Gold, Silver, Bronze)")
    print()
    
    # Area per scrivere la query
    query = """
    SELECT 
        c.segmento AS segmento,
        COUNT(DISTINCT c.cliente_id) AS n_clienti,
        COUNT(DISTINCT o.ordine_id) * 1.0 
            / COUNT(DISTINCT c.cliente_id) AS n_medio_ordini_per_cliente,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100))
            / COUNT(DISTINCT o.ordine_id) AS valore_medio_ordine,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS ricavi_totali,
    FROM clienti c
        JOIN ordini o ON c.cliente_id = o.cliente_id
        JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    WHERE o.stato != 'Cancellato'
    GROUP BY c.segmento
    ORDER BY 
        (c.segmento = 'Platinum') DESC,
        (c.segmento = 'Gold')     DESC,
        (c.segmento = 'Silver')   DESC,
        (c.segmento = 'Bronze')   DESC
    """
    
    print("QUERY DA COMPLETARE:")
    print(query)
    print()
    print("Modifica la query sopra e riesegui lo script.")
    print("Per vedere la soluzione, esegui: python 03_soluzioni.py")
    print()


def esercizio_bonus():
    """Esercizio Bonus: Query a scelta."""
    print("\n" + "=" * 70)
    print("ESERCIZIO BONUS: Analisi a Scelta")
    print("=" * 70)
    print()
    print("Proponi e implementa un'analisi a tua scelta!")
    print()
    print("Idee:")
    print("  - Trend vendite giornaliere/settimanali")
    print("  - Prodotti più venduti per categoria")
    print("  - Tasso di cancellazione ordini")
    print("  - Analisi metodi di pagamento")
    print("  - Confronto performance corrieri")
    print("  - Analisi sconti applicati")
    print()


def main():
    """Funzione principale."""
    print("=" * 70)
    print("ESERCIZI PRATICI - Database OLTP")
    print("=" * 70)
    print()
    print("Questi esercizi ti aiuteranno a praticare query analitiche su database OLTP.")
    print("Noterai come le query diventano complesse e richiedono molti JOIN.")
    print()
    print("ISTRUZIONI:")
    print("  1. Leggi attentamente ogni esercizio")
    print("  2. Scrivi la query SQL richiesta")
    print("  3. Testa la query sul database")
    print("  4. Confronta con le soluzioni (03_soluzioni.py)")
    print()
    
    try:
        # Verifica connessione database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordini")
        n_ordini = cursor.fetchone()[0]
        print(f"✓ Database connesso: {n_ordini:,} ordini trovati")
        conn.close()
        print()
        
        # Esercizi
        esercizio_1()
        input("Premi INVIO per il prossimo esercizio...")
        
        esercizio_2()
        input("Premi INVIO per il prossimo esercizio...")
        
        esercizio_3()
        input("Premi INVIO per l'esercizio bonus...")
        
        esercizio_bonus()
        
        print()
        print("=" * 70)
        print("ESERCIZI COMPLETATI!")
        print("=" * 70)
        print()
        print("Per vedere le soluzioni complete con visualizzazioni:")
        print("  python 03_soluzioni.py")
        print()
        
    except Exception as e:
        print(f"\n[ERRORE] {str(e)}")
        print("\nAssicurati di aver eseguito prima: python 01_setup_database.py")


if __name__ == "__main__":
    main()

