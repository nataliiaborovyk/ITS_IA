import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. INGESTION (Caricamento)
# ==========================================
# Obiettivo: Caricare il file, ma dire subito a Pandas che "n.a." e "?" sono valori nulli
lista_valori_nulli = ["n.a.", "?", "nan"]
df = pd.read_csv("vendite_raw.csv", na_values=___)


# ==========================================
# 2. CLEANING (Pulizia)
# ==========================================

# A. Rinomina le colonne per averle pulite (snake_case)
# Mappa: 'Order ID' -> 'order_id', 'PRICE (eu)' -> 'price', 'Date_Order' -> 'date'
df.rename(columns={
    'Order ID': 'order_id', 
    'PRICE (eu)': '___', 
    'Date_Order': 'date',
    'Product Name': 'product'
}, inplace=True)

# B. Pulizia Prezzo (Price)
# Il prezzo è tipo "1.200,00 €". Dobbiamo togliere '€' e '.', e cambiare ',' in '.'
# Nota: Prima lo trattiamo come stringa (.str)
df['price'] = df['price'].str.replace(' €', '').str.replace('.', '').str.replace(',', '.')

# Ora convertiamo in numero (float). 
# Attenzione: se ci sono ancora NaN, astype(float) gestisce bene i NaN? Sì.
df['price'] = df['price'].astype(___)

# Riempiamo i prezzi mancanti con la MEDIA della colonna
prezzo_medio = df['price'].mean()
df['price'].fillna(___, inplace=True)

# C. Pulizia Data
# Converti la colonna 'date' in oggetti datetime
df['date'] = pd.to_datetime(df['date'])

# D. Pulizia Logica
# Elimina le righe dove 'Quantity' è minore o uguale a 0
df = df[df['Quantity'] > ___]


# ==========================================
# 3. ANALYSIS (Aggregazione)
# ==========================================
# Obiettivo: Calcolare il Fatturato Totale (Price * Quantity) per ogni Categoria

# Creiamo prima la colonna Fatturato
df['total_revenue'] = df['price'] * df['Quantity']

# Raggruppa per 'Category' e somma il 'total_revenue'
# Vogliamo un DataFrame alla fine, non una Series (ricorda le parentesi!)
df_agg = df.groupby('Category')[[___]].sum()

# Ordiniamo dal più ricco al più povero
df_agg = df_agg.sort_values(by='total_revenue', ascending=___)


# ==========================================
# 4. VISUALIZATION (Artist Layer)
# ==========================================
# Obiettivo: Bar Chart del fatturato

# Crea la figura e gli assi
fig, ax = plt.subplots(figsize=(10, 6))

# Disegna le barre
# x = l'indice del df_agg (le categorie), y = la colonna total_revenue
ax.bar(x=df_agg.___, height=df_agg['total_revenue'], color='royalblue')

# Personalizza
ax.set_title("Fatturato per Categoria")
ax.set_xlabel("Categoria")
ax.set_ylabel("Euro (€)")
ax.grid(axis='y', linestyle='--') # Griglia orizzontale tratteggiata

plt.show()