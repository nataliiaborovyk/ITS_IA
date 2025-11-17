import pandas as pd  # importiamo la libreria pandas e la chiamiamo 'pd'

# Percorso del file CSV con i dati degli album musicali
data_path = "../dati/SomeMusicAlbums.csv"

# =========================================================
# ESERCIZIO 1
# Carica il CSV in un DataFrame e mostra le prime 3 righe
# =========================================================
print("***ESERCIZIO 1***")

# pd.read_csv(path)
# - Legge un file CSV dal percorso indicato
# - Restituisce un oggetto DataFrame (una tabella: righe + colonne)
# ATTENZIONE: il percorso deve essere corretto rispetto alla posizione del file .py
df = pd.read_csv(data_path)

# df.head(3)
# - Restituisce le prime 3 righe del DataFrame
# - Utile per "dare un'occhiata" ai dati senza stamparli tutti
# Alternative:
#   - df.head()           → prime 5 righe (default)
#   - df.tail(3)          → ultime 3 righe
print(df.head(3))
print("\n")  # riga vuota per separare l'output


# =========================================================
# ESERCIZIO 2
# Mostra informazioni di base sul DataFrame
# =========================================================
print("***ESERCIZIO 2***")

# df.info()
# - Stampa:
#   * numero di righe
#   * numero di colonne
#   * nome di ogni colonna
#   * quanti valori NON null per ogni colonna
#   * tipo di dato (int64, float64, object, ecc.)
# È molto utile per capire la "struttura" del dataset.
info_result = df.info()
print(info_result)  # df.info() in realtà stampa già da solo, e ritorna None
print("\n")
# Alternative utili:
#   - df.shape    → tupla (num_righe, num_colonne)
#   - df.dtypes   → tipo di dato per ogni colonna
#   - df.describe() → statistiche per colonne numeriche


# =========================================================
# ESERCIZIO 3
# Filtra gli album per genere "rock"
# =========================================================
print("***ESERCIZIO 3***")

# Obiettivo: prendere solo le righe dove nella colonna 'Genre'
# compare la parola "rock" (anche se fa parte di una stringa più lunga, es. "pop, rock")
#
# df['Genre'] → Series con i valori della colonna 'Genre'
# .str.contains('rock', case=False)
#   - cerca la sottostringa "rock" dentro ogni stringa della colonna
#   - case=False → non fa differenza tra maiuscole/minuscole ("Rock", "ROCK", ecc.)
#   - restituisce una Series di True/False (maschera booleana)
#
# df[maschera] → DataFrame con solo le righe dove la maschera è True
rock_mask = df['Genre'].str.contains('rock', case=False)
rock_albums = df[rock_mask]
print(rock_albums)
print("\n")
# Alternative:
#   - df.query("Genre.str.contains('rock', case=False)", engine="python")
#     (un po' più avanzato, ma esiste)
#   - usare .apply(...) con una funzione personalizzata (di solito meno comodo)


# =========================================================
# ESERCIZIO 4
# Trova gli album pubblicati dopo il 1980
# e mostra solo 'Artist', 'Album', 'Released'
# =========================================================
print("***ESERCIZIO 4***")

# df['Released'] > 1980
# - crea una Series di True/False
# - True dove il valore della colonna Released è maggiore di 1980
condizione = df['Released'] > 1980

# df[condizione]
# - seleziona solo le righe dove condizione è True
df_nuovo = df[condizione]   # ho corretto il nome (prima era df_nuivo)

# df_nuovo.loc[:, 'Artist':'Released']
# - .loc[righe, colonne]
# - righe: ":" → tutte le righe
# - colonne: 'Artist':'Released' → da 'Artist' fino a 'Released' (estremi inclusi)
#   quindi ottieni le colonne: Artist, Album, Released (se sono in quell'ordine)
df_filtrato = df_nuovo.loc[:, 'Artist':'Released']
print(df_filtrato)
print("*****************" + "\n")

# Alternative:
#   - df_nuovo[['Artist', 'Album', 'Released']]
#     (se vuoi specificare le colonne una per una, senza usare intervallo)


# =========================================================
# ESERCIZIO 5
# Calcola la media delle valutazioni (colonna 'Rating')
# =========================================================
print("***ESERCIZIO 5***")

# df['Rating'] → colonna 'Rating' come Series
# .mean()      → media aritmetica dei valori numerici
media_rating = df['Rating'].mean()
print("La media della colonna 'Rating' è:", media_rating)
print("*****************" + "\n")

# Alternative:
#   - df['Rating'].describe() → ti dà anche media, min, max, quartili, ecc.
#   - df['Rating'].agg('mean') → altro modo per fare la media


# =========================================================
# ESERCIZIO 6
# Trova l'album più lungo e il più breve (colonna 'Length')
# =========================================================
print("***ESERCIZIO 6***")

# Molto spesso la colonna 'Length' è in formato stringa "mm:ss"
# Per confrontare le durate in modo corretto, convertiamo in SECONDI.

# 1) Spezziamo la stringa "mm:ss" in due colonne: minuti e secondi
# df['Length'].str.split(':', expand=True)
#   - 'str.split' divide ogni stringa alla presenza di ':'
#   - expand=True → restituisce un DataFrame con 2 colonne (es. 43:59 → ["43","59"])
length_split = df['Length'].str.split(':', expand=True)

# 2) Convertiamo le due colonne in interi (int)
#   - astype(int) → cambia il tipo da stringa a intero
minutes = length_split[0].astype(int)
seconds = length_split[1].astype(int)

# 3) Calcoliamo la durata totale in secondi: minuti * 60 + secondi
total_seconds = minutes * 60 + seconds

# 4) Troviamo gli indici (riga) della durata massima e minima
#   - idxmax() → indice del valore massimo
#   - idxmin() → indice del valore minimo
idx_max = total_seconds.idxmax()
idx_min = total_seconds.idxmin()

# 5) Usiamo .loc per prendere le righe corrispondenti
album_piu_lungo = df.loc[idx_max]
album_piu_breve = df.loc[idx_min]

print("Album più lungo:")
print(album_piu_lungo)
print("\nAlbum più breve:")
print(album_piu_breve)
print("*****************" + "\n")

# Alternative (meno precise se 'Length' è stringa):
#   - df.loc[df['Length'].idxmax()]  → confronto sulle stringhe (non consigliato)
#   - convertire la colonna 'Length' a timedelta (più avanzato)


# =========================================================
# ESERCIZIO 7 - NON FARE (solo struttura)
# =========================================================
print("***ESERCIZIO 7***")
print("Esercizio 7: da NON fare (lo saltiamo).")
print("*****************" + "\n")


# =========================================================
# ESERCIZIO 8
# Aggiungi colonna 'Sales_Difference' = Claimed Sales - Music Recording Sales
# =========================================================
print("***ESERCIZIO 8***")

# df['Claimed Sales'] e df['Music Recording Sales']
# - sono due colonne numeriche (speriamo nel CSV)
# Quando fai una sottrazione tra due Series di pandas
# - il calcolo avviene elemento per elemento (riga per riga)
df['Sales_Difference'] = df['Claimed Sales'] - df['Music Recording Sales']

print("Prime righe con la nuova colonna 'Sales_Difference':")
print(df[['Artist', 'Album', 'Claimed Sales', 'Music Recording Sales', 'Sales_Difference']].head())
print("*****************" + "\n")

# Alternative:
#   - df.assign(Sales_Difference=lambda x: x['Claimed Sales'] - x['Music Recording Sales'])
#     (crea una copia con la colonna aggiunta, invece di modificare df in place)


# =========================================================
# ESERCIZIO 9
# Trova gli album colonna sonora (Soundtrack = 'Y')
# =========================================================
print("***ESERCIZIO 9***")

# df['Soundtrack'] == 'Y'
# - crea una maschera booleana True/False
soundtrack_mask = df['Soundtrack'] == 'Y'

# df[maschera] → solo le righe dove soundtrack_mask è True
soundtrack_albums = df[soundtrack_mask]
print("Album che sono colonna sonora (Soundtrack = 'Y'):")
print(soundtrack_albums)
print("*****************" + "\n")

# Alternative:
#   - df.query("Soundtrack == 'Y'")
#   - df.loc[df['Soundtrack'] == 'Y']


# =========================================================
# ESERCIZIO 10
# Salva in un nuovo CSV gli album con Rating ≥ 9
# =========================================================
print("***ESERCIZIO 10***")

# Creiamo un DataFrame filtrato con solo gli album con Rating >= 9
high_rating_mask = df['Rating'] >= 9
df_rating_9_plus = df[high_rating_mask]

# Percorso del nuovo file CSV
output_path = "../dati/SomeMusicAlbums_Rating_ge_9.csv"

# df.to_csv(path, index=False)
# - salva il DataFrame in un file CSV
# - index=False → non scrive la colonna degli indici nel file (più pulito)
df_rating_9_plus.to_csv(output_path, index=False)

print(f"Salvati {df_rating_9_plus.shape[0]} album con Rating >= 9 in: {output_path}")
print("******************" + "\n")


# =========================================================
# ESERCIZIO 11 - NON FARE (solo struttura)
# =========================================================
print("***ESERCIZIO 11***")
print("Esercizio 11: da NON fare (lo saltiamo).")
print("******************" + "\n")


# =========================================================
# ESERCIZIO 12
# Album con la maggiore differenza tra vendite dichiarate e registrate
# (usiamo 'Sales_Difference' creata nell'esercizio 8)
# =========================================================
print("***ESERCIZIO 12***")

# Controlliamo che la colonna 'Sales_Difference' esista
# (se il codice è eseguito tutto di fila, esiste di sicuro)
if 'Sales_Difference' in df.columns:
    # idxmax() → indice della riga con valore massimo nella colonna
    idx_max_diff = df['Sales_Difference'].idxmax()
    album_max_diff = df.loc[idx_max_diff]

    print("Album con la maggiore differenza tra 'Claimed Sales' e 'Music Recording Sales':")
    print(album_max_diff)
else:
    print("Attenzione: la colonna 'Sales_Difference' non esiste. Esegui prima l'esercizio 8.")
print("******************" + "\n")


# =========================================================
# ESERCIZIO 13
# Filtra gli album che hanno sia 'rock' che 'pop' nel Genre
# =========================================================
print("***ESERCIZIO 13***")

# Vogliamo le righe dove 'Genre' contiene 'rock' E contiene 'pop'
# - str.contains('rock', case=False) → True se c'è "rock"
# - str.contains('pop', case=False)  → True se c'è "pop"
mask_rock = df['Genre'].str.contains('rock', case=False)
mask_pop = df['Genre'].str.contains('pop', case=False)

# & = AND logico elemento per elemento
both_rock_pop_mask = mask_rock & mask_pop

df_rock_pop = df[both_rock_pop_mask]
print("Album che hanno sia 'rock' che 'pop' nel Genre:")
print(df_rock_pop)
print("******************" + "\n")

# Alternative:
#   - usare .query con espressioni più complesse (ma è più avanzato)


# =========================================================
# ESERCIZIO 14 - NON FARE (solo struttura)
# =========================================================
print("***ESERCIZIO 14***")
print("Esercizio 14: da NON fare (lo saltiamo).")
print("******************" + "\n")


# =========================================================
# ESERCIZIO 15
# Trova l'album più venduto che NON è una colonna sonora
# (massime 'Music Recording Sales' con Soundtrack != 'Y')
# =========================================================
print("***ESERCIZIO 15***")

# 1) Filtriamo gli album che NON sono colonna sonora
#    (Soundtrack diverso da 'Y')
non_soundtrack_mask = df['Soundtrack'] != 'Y'
df_non_soundtrack = df[non_soundtrack_mask]

# 2) Troviamo l'indice dell'album con 'Music Recording Sales' massimo
idx_max_sales = df_non_soundtrack['Music Recording Sales'].idxmax()

# 3) Selezioniamo la riga corrispondente
album_piu_venduto_non_soundtrack = df_non_soundtrack.loc[idx_max_sales]

print("Album più venduto che NON è una colonna sonora:")
print(album_piu_venduto_non_soundtrack)
print("******************" + "\n")
