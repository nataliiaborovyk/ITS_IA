"""
Esercitazione 1 - Esplorazione Database OLTP
=============================================

Questo script esplora il database operazionale con query OLTP e OLAP,
mostrando le differenze prestazionali.

Esecuzione:
    python 02_esplora_oltp.py

Output:
    - Risultati query stampati a console
    - Grafici salvati in ../docs/
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from pathlib import Path

# Configurazione
DB_PATH = '../data/techstore_oltp.db'
OUTPUT_DIR = '../docs'

# Setup visualizzazioni
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Crea directory output
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def print_section(title):
    """Stampa intestazione sezione."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70 + "\n")


def execute_query(conn, query, description, show_time=True):
    """Esegue una query e mostra risultati."""
    print(f"Query: {description}")
    print("-" * 70)
    
    start_time = time.time()
    df = pd.read_sql_query(query, conn)
    elapsed_time = time.time() - start_time
    
    print(df.to_string(index=False))
    
    if show_time:
        if elapsed_time < 1:
            print(f"\n⏱️  Tempo esecuzione: {elapsed_time*1000:.2f} ms")
        else:
            print(f"\n⏱️  Tempo esecuzione: {elapsed_time:.2f} secondi")
    
    print(f"📊 Righe restituite: {len(df)}")
    print()
    
    return df, elapsed_time


def query_oltp_examples(conn):
    """Esempi di query OLTP tipiche."""
    print_section("PARTE 1: QUERY TRANSAZIONALI (OLTP)")
    
    print("Le query OLTP sono:")
    print("  ✓ Veloci (millisecondi)")
    print("  ✓ Semplici (pochi JOIN)")
    print("  ✓ Pochi record")
    print("  ✓ Dati recenti\n")
    
    # Query 1: Dettagli ordine singolo
    query1 = """
    SELECT 
        o.ordine_id,
        o.data_ordine,
        o.stato,
        c.nome || ' ' || c.cognome AS cliente,
        c.email,
        p.nome_prodotto,
        d.quantita,
        d.prezzo_unitario,
        d.sconto
    FROM ordini o
    JOIN clienti c ON o.cliente_id = c.cliente_id
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    JOIN prodotti p ON d.prodotto_id = p.prodotto_id
    WHERE o.ordine_id = 12345
    """
    execute_query(conn, query1, "Dettagli ordine #12345")
    
    # Query 2: Ultimi ordini cliente
    query2 = """
    SELECT 
        o.ordine_id,
        o.data_ordine,
        o.stato,
        COUNT(d.dettaglio_id) AS n_prodotti,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS importo_totale
    FROM ordini o
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    WHERE o.cliente_id = 1000
    GROUP BY o.ordine_id, o.data_ordine, o.stato
    ORDER BY o.data_ordine DESC
    LIMIT 10
    """
    execute_query(conn, query2, "Ultimi 10 ordini del cliente #1000")
    
    # Query 3: Prodotti disponibili
    query3 = """
    SELECT 
        p.prodotto_id,
        p.nome_prodotto,
        p.marca,
        p.prezzo,
        p.quantita_stock
    FROM prodotti p
    JOIN categorie c ON p.categoria_id = c.categoria_id
    WHERE c.nome_categoria = 'Laptop'
    AND p.quantita_stock > 0
    ORDER BY p.prezzo DESC
    """
    execute_query(conn, query3, "Laptop disponibili in stock")
    
    print("💡 Nota: Tutte le query OLTP sono state veloci (< 100 ms)")
    print("   Questo è normale per database operazionali!")


def query_olap_examples(conn):
    """Esempi di query OLAP (analitiche)."""
    print_section("PARTE 2: QUERY ANALITICHE (OLAP)")
    
    print("Le query OLAP sono:")
    print("  ⚠️  Lente (secondi)")
    print("  ⚠️  Complesse (molti JOIN)")
    print("  ⚠️  Molti record")
    print("  ⚠️  Dati storici aggregati\n")
    
    # Query 1: Vendite mensili per categoria
    query1 = """
    SELECT 
        strftime('%Y-%m', o.data_ordine) AS mese,
        cat.nome_categoria,
        COUNT(DISTINCT o.ordine_id) AS n_ordini,
        SUM(d.quantita) AS quantita_venduta,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS ricavi
    FROM ordini o
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    JOIN prodotti p ON d.prodotto_id = p.prodotto_id
    JOIN categorie cat ON p.categoria_id = cat.categoria_id
    WHERE o.data_ordine >= date('now', '-12 months')
    AND o.stato != 'Cancellato'
    GROUP BY mese, cat.nome_categoria
    ORDER BY mese, ricavi DESC
    """
    df1, time1 = execute_query(conn, query1, "Vendite mensili per categoria (ultimi 12 mesi)")
    
    print("⚠️  Nota: Query molto più lenta! Scansiona migliaia di record.")
    print("   Su un database reale sarebbe ancora più lenta.\n")
    
    # Query 2: Top clienti
    query2 = """
    SELECT 
        c.cliente_id,
        c.nome || ' ' || c.cognome AS cliente,
        c.segmento,
        c.citta,
        COUNT(DISTINCT o.ordine_id) AS n_ordini,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS valore_totale,
        AVG(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS valore_medio_ordine,
        MIN(o.data_ordine) AS primo_ordine,
        MAX(o.data_ordine) AS ultimo_ordine
    FROM clienti c
    JOIN ordini o ON c.cliente_id = o.cliente_id
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    WHERE o.stato != 'Cancellato'
    GROUP BY c.cliente_id, c.nome, c.cognome, c.segmento, c.citta
    ORDER BY valore_totale DESC
    LIMIT 10
    """
    df2, time2 = execute_query(conn, query2, "Top 10 clienti per valore totale")
    
    print("⚠️  Nota: Altra query pesante! Scansiona TUTTI i clienti e ordini.\n")
    
    # Query 3: Performance prodotti
    query3 = """
    SELECT 
        p.prodotto_id,
        p.nome_prodotto,
        cat.nome_categoria,
        p.marca,
        COUNT(DISTINCT d.ordine_id) AS n_ordini,
        SUM(d.quantita) AS quantita_venduta,
        SUM(d.quantita * d.prezzo_unitario * (1 - d.sconto/100)) AS ricavi,
        SUM(d.quantita * (d.prezzo_unitario - p.costo) * (1 - d.sconto/100)) AS profitto,
        AVG(d.sconto) AS sconto_medio
    FROM prodotti p
    JOIN categorie cat ON p.categoria_id = cat.categoria_id
    JOIN dettagli_ordini d ON p.prodotto_id = d.prodotto_id
    JOIN ordini o ON d.ordine_id = o.ordine_id
    WHERE o.stato != 'Cancellato'
    GROUP BY p.prodotto_id, p.nome_prodotto, cat.nome_categoria, p.marca
    ORDER BY ricavi DESC
    LIMIT 15
    """
    df3, time3 = execute_query(conn, query3, "Top 15 prodotti per ricavi")
    
    print("⚠️  Nota: Complessità crescente con aggregazioni su più dimensioni.\n")
    
    return (df1, time1), (df2, time2), (df3, time3)


def confronto_oltp_olap(conn):
    """Confronta performance OLTP vs OLAP."""
    print_section("PARTE 3: CONFRONTO OLTP vs OLAP")
    
    print("Misurazione tempi di esecuzione...\n")
    
    # Query OLTP
    print("Query OLTP (transazionali):")
    
    query_oltp_1 = "SELECT * FROM ordini WHERE ordine_id = 12345"
    query_oltp_2 = "SELECT * FROM clienti WHERE cliente_id = 1000"
    query_oltp_3 = "SELECT * FROM prodotti WHERE categoria_id = 1 LIMIT 10"
    
    _, t1 = execute_query(conn, query_oltp_1, "Ordine singolo", show_time=False)
    _, t2 = execute_query(conn, query_oltp_2, "Cliente singolo", show_time=False)
    _, t3 = execute_query(conn, query_oltp_3, "Prodotti categoria", show_time=False)
    
    tempo_medio_oltp = (t1 + t2 + t3) / 3
    print(f"  Tempo medio OLTP: {tempo_medio_oltp*1000:.2f} ms\n")
    
    # Query OLAP
    print("Query OLAP (analitiche):")
    
    query_olap_1 = """
    SELECT strftime('%Y-%m', o.data_ordine) AS mese, 
           SUM(d.quantita * d.prezzo_unitario) AS ricavi
    FROM ordini o
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    GROUP BY mese
    """
    
    query_olap_2 = """
    SELECT c.cliente_id, COUNT(*) AS n_ordini, 
           SUM(d.quantita * d.prezzo_unitario) AS valore_totale
    FROM clienti c
    JOIN ordini o ON c.cliente_id = o.cliente_id
    JOIN dettagli_ordini d ON o.ordine_id = d.ordine_id
    GROUP BY c.cliente_id
    """
    
    query_olap_3 = """
    SELECT p.nome_prodotto, cat.nome_categoria,
           COUNT(DISTINCT d.ordine_id) AS n_ordini,
           SUM(d.quantita) AS quantita_venduta
    FROM prodotti p
    JOIN categorie cat ON p.categoria_id = cat.categoria_id
    JOIN dettagli_ordini d ON p.prodotto_id = d.prodotto_id
    GROUP BY p.nome_prodotto, cat.nome_categoria
    """
    
    _, t4 = execute_query(conn, query_olap_1, "Ricavi mensili", show_time=False)
    _, t5 = execute_query(conn, query_olap_2, "Valore per cliente", show_time=False)
    _, t6 = execute_query(conn, query_olap_3, "Performance prodotti", show_time=False)
    
    tempo_medio_olap = (t4 + t5 + t6) / 3
    print(f"  Tempo medio OLAP: {tempo_medio_olap:.2f} secondi\n")
    
    # Confronto
    ratio = tempo_medio_olap / tempo_medio_oltp
    print("=" * 70)
    print(f"📊 Le query OLAP sono {ratio:.1f}x più lente delle query OLTP!")
    print("=" * 70)
    print()
    
    # Visualizzazione
    create_comparison_chart(tempo_medio_oltp, tempo_medio_olap)
    
    return tempo_medio_oltp, tempo_medio_olap


def create_comparison_chart(tempo_oltp, tempo_olap):
    """Crea grafico di confronto tempi."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Grafico 1: Tempi di esecuzione
    categorie = ['OLTP', 'OLAP']
    tempi = [tempo_oltp * 1000, tempo_olap * 1000]  # in millisecondi
    colori = ['#059669', '#3B82F6']
    
    ax1.bar(categorie, tempi, color=colori, alpha=0.8)
    ax1.set_ylabel('Tempo Medio (ms)', fontsize=12)
    ax1.set_title('Confronto Tempi di Esecuzione', fontsize=14, fontweight='bold')
    ax1.set_yscale('log')  # Scala logaritmica
    
    for i, v in enumerate(tempi):
        ax1.text(i, v, f'{v:.1f} ms', ha='center', va='bottom', fontweight='bold')
    
    # Grafico 2: Differenza percentuale
    ratio = tempo_olap / tempo_oltp
    ax2.bar(['Differenza'], [ratio], color='#EF4444', alpha=0.8)
    ax2.set_ylabel('Volte più lento', fontsize=12)
    ax2.set_title('OLAP vs OLTP', fontsize=14, fontweight='bold')
    ax2.text(0, ratio, f'{ratio:.1f}x', ha='center', va='bottom', fontweight='bold', fontsize=16)
    
    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/confronto_oltp_olap.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Grafico salvato: {output_path}\n")
    plt.close()


def analisi_problemi():
    """Analizza i problemi identificati."""
    print_section("PARTE 4: PROBLEMI IDENTIFICATI")
    
    print("Dalle query analitiche appena eseguite, abbiamo identificato diversi PROBLEMI:")
    print()
    
    print("1. PERFORMANCE")
    print("   ⚠️  Le query analitiche sono LENTE (secondi invece di millisecondi)")
    print("   ⚠️  Su database reali (milioni di record) potrebbero richiedere MINUTI")
    print("   ⚠️  Queste query RALLENTANO il sistema operazionale")
    print()
    
    print("2. COMPLESSITÀ DELLE QUERY")
    print("   ⚠️  Servono MOLTI JOIN per unire dati da tabelle diverse")
    print("   ⚠️  Le query sono LUNGHE e COMPLESSE, difficili da scrivere")
    print("   ⚠️  Ogni analisi richiede di RISCRIVERE query simili")
    print()
    
    print("3. DATI FRAMMENTATI")
    print("   ⚠️  I dati sono NORMALIZZATI (3NF) per evitare ridondanza")
    print("   ⚠️  Ottimo per OLTP, ma PESSIMO per analisi")
    print("   ⚠️  Servono molti JOIN per ricostruire informazioni complete")
    print()
    
    print("4. MANCANZA DI STORICO AGGREGATO")
    print("   ⚠️  Non ci sono AGGREGAZIONI PRE-CALCOLATE")
    print("   ⚠️  Ogni volta dobbiamo RICALCOLARE tutto da zero")
    print("   ⚠️  Non ci sono VISTE MATERIALIZZATE per velocizzare")
    print()
    
    print("5. DIFFICOLTÀ NELL'ANALISI TEMPORALE")
    print("   ⚠️  Analizzare TREND richiede query complesse")
    print("   ⚠️  Non c'è una DIMENSIONE TEMPO strutturata")
    print("   ⚠️  Difficile confrontare periodi diversi")
    print()
    
    print("=" * 70)
    print("SOLUZIONE: DATA WAREHOUSE!")
    print("=" * 70)
    print()
    print("Un Data Warehouse risolve questi problemi con:")
    print("  ✓ Schema DENORMALIZZATO (Star Schema) per query veloci")
    print("  ✓ AGGREGAZIONI PRE-CALCOLATE per performance")
    print("  ✓ DIMENSIONE TEMPO strutturata per analisi temporali")
    print("  ✓ SEPARAZIONE dal sistema operazionale")
    print("  ✓ OTTIMIZZAZIONE specifica per query analitiche")
    print()


def main():
    """Funzione principale."""
    print("=" * 70)
    print("ESPLORAZIONE DATABASE OLTP - TechStore")
    print("=" * 70)
    print()
    
    try:
        # Connessione
        conn = sqlite3.connect(DB_PATH)
        
        # Esplorazione OLTP
        query_oltp_examples(conn)
        
        input("\nPremi INVIO per continuare con le query analitiche...")
        
        # Esplorazione OLAP
        query_olap_examples(conn)
        
        input("\nPremi INVIO per il confronto prestazionale...")
        
        # Confronto
        confronto_oltp_olap(conn)
        
        input("\nPremi INVIO per l'analisi dei problemi...")
        
        # Analisi problemi
        analisi_problemi()
        
        # Chiusura
        conn.close()
        
        print("=" * 70)
        print("ESPLORAZIONE COMPLETATA!")
        print("=" * 70)
        print()
        print("Prossimo passo: esegui 03_esercizi.py per praticare")
        print()
        
    except Exception as e:
        print(f"\n[ERRORE] {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

