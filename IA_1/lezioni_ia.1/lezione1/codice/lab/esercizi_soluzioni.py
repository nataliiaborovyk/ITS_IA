import pandas as pd

# Esercizio 1: Lettura da file locale
# Task: Leggi i dati del file CSV fornito in un Pandas DataFrame e visualizza le prime 3 righe  
# Soluzione:
print("***ESERCIZIO 1***")
df = pd.read_csv('../../dati/lab/some_music_albums.csv')
print(df.head(3))
print("*****************"+"\n")
 
### Esercizio 2: Mostra informazioni di base sul DataFrame 
### Task: Mostra il numero di righe, colonne e tipi di dati per ogni colonna 
### Soluzione:
print("***ESERCIZIO 2***")
print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("*****************"+"\n")
 
### Esercizio 3: Filtra gli album per genere
### Task: Crea un nuovo DataFrame contenente solo gli album con "rock" nella colonna 'Genre'
### Soluzione:
print("***ESERCIZIO 3***")
rock_albums = df[df['Genre'].str.contains('rock', case=False)]
print(rock_albums)
print("*****************"+"\n")

## Esercizio 4: Trova gli album pubblicati dopo il 1980
## Task: Filtra gli album pubblicati dopo il 1980 e visualizza solo le colonne 'Artist', 'Album' e 'Released'
## Soluzione:
print("***ESERCIZIO 4***")
condition_1 = df['Released'] > 1980
# print(type(condition_1))
condition_2 = df['Artist'].str.contains('Whitney', case=False) 
# print(type(condition_2))
recent_albums_full = df[condition_1 & condition_2]
# print(type(recent_albums_full))
recent_albums = recent_albums_full[['Artist', 'Album', 'Released']]
# print(type(recent_albums))
# recent_albums = df[df['Released'] > 1980][['Artist', 'Album', 'Released']]
print(recent_albums)
print("*****************"+"\n")
 
### Esercizio 5: Calcola la media delle valutazioni
### Task: Calcola la media della colonna 'Rating' per tutti gli album
### Soluzione:
print("***ESERCIZIO 5***")
avg_rating = df['Rating'].mean()
print("Average Rating:", avg_rating)
print("*****************"+"\n")

### Esercizio 6: Trova l'album più lungo e il più breve
### Task: Identifica l'album con la durata massima e minima nella colonna 'Length' e visualizza i suoi dettagli
### Soluzione:
print("***ESERCIZIO 6***")
df['Length_timedelta'] = pd.to_timedelta(df['Length'])
# print(df[['Length','Length_timedelta']])
# print(type(df['Length'][0]))
# print(type(df['Length_timedelta'][0]))
longest_album = df.loc[[df['Length_timedelta'].idxmax()]]
print(longest_album)
print(f"Artist: {longest_album['Artist']}, Title: {longest_album['Album']}, Length: {longest_album['Length']}")
shortest_album = df.loc[df['Length_timedelta'].idxmin()]
print(f"Artist: {shortest_album['Artist']}, Title: {shortest_album['Album']}, Length: {shortest_album['Length']}")
print("*****************"+"\n")
 
### Esercizio 7: Elenco generi unici
### Task: Estrai e stampa tutti i generi unici nel dataset (dividendo i generi combinati come "pop, rock")
### Soluzione:
print("***ESERCIZIO 7***")
unique_genres = set()
for genres in df['Genre'].str.split(','):
    unique_genres.update([g.strip() for g in genres])
print(unique_genres)
print("*****************"+"\n")

### Esercizio 8: Confronta le vendite con vendite dichiarate
### Task: Aggiungi una nuova colonna 'Sales_Difference' che mostri la differenza tra 'Claimed Sales' e 'Music Recording Sales'
### Soluzione:
print("***ESERCIZIO 8***")
df['Sales_Difference'] = df['Claimed Sales (millions)'] - df['Music Recording Sales (millions)']
print(df[['Artist', 'Album', 'Sales_Difference']])
print("*****************"+"\n")
  
### Esercizio 9: Trova gli album colonna sonora
### Task: Elenca tutti gli album contrassegnati come 'Soundtrack' (dove la colonna è "Y")
### Soluzione:
print("***ESERCIZIO 9***")
soundtracks = df[df['Soundtrack'] == 'Y']
print(soundtracks[['Artist', 'Album']])
print("*****************"+"\n")

### Esercizio 10: Salva i dati filtrati in un file CSV
### Task: Salva tutti gli album con una valutazione (Rating) ≥ 9 in un nuovo file CSV
### Soluzione:
print("***ESERCIZIO 10***")
top_albums = df[df['Rating'] >= 9]
print(top_albums)
top_albums.to_csv('../../dati/lab/top_rated_albums.csv', index=False)
print("Writing done!")
print("******************"+"\n")
  
### Esercizio 11: Conta gli album per genere
### Task:Conta quanti album appartengono a ogni genere unico (dividendo generi combinati come "pop, rock")
### Soluzione:  
print("***ESERCIZIO 11***")
genre_counts = {}
for genres in df['Genre'].str.split(','):
    for g in genres:
        genre = g.strip()
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
print(genre_counts)
print("******************"+"\n")

### Esercizio 12: Trova l'album con la maggior differenza tra vendite e vendite dichiarate
### Task: Identifica l'album con la maggiore differenza tra 'Claimed Sales' e 'Music Recording Sales' e visualizza i suoi dettagli
### Soluzione:  
print("***ESERCIZIO 12***")
df['Sales_Difference'] = df['Claimed Sales (millions)'] - df['Music Recording Sales (millions)']
max_diff_album = df.loc[df['Sales_Difference'].idxmax()]
print(f"Artist: {max_diff_album['Artist']}, Album: {max_diff_album['Album']}, Sales Difference: {max_diff_album['Sales_Difference']}M")
print("******************"+"\n")
  
### Esercizio 13: Filtra gli album per generi multipli
### Task: Crea un nuovo DataFrame contenente gli album che includono entrambi "rock" e "pop" nella colonna Genre
### Soluzione:**  
print("***ESERCIZIO 13***")
rock_pop_albums = df[df['Genre'].str.contains('rock', case=False) & df['Genre'].str.contains('pop', case=False)]
print(rock_pop_albums[['Artist', 'Album', 'Genre']])
print("******************"+"\n")
    
## Esercizio 14: Calcola la durata media per genere
## Task: Calcola la media della durata (in minuti) degli album per ogni genere (dividendo generi combinati)
## Soluzione:  
print("***ESERCIZIO 14***")
df['Length_min'] = pd.to_timedelta(df['Length']).dt.total_seconds() / 60
genre_lengths = {}
for idx, row in df.iterrows():
    # print(idx)
    # print(type(row))
    # print("\n")
    for g in row['Genre'].split(','):
        genre = g.strip()
        if genre not in genre_lengths:
            genre_lengths[genre] = []
        genre_lengths[genre].append(row['Length_min'])
# print(type(genre_lengths))
for k, v in genre_lengths.items():
    print(k)
    print(v)
avg_length = {k: sum(v)/len(v) for k, v in genre_lengths.items()}
print(avg_length)
print("******************"+"\n")

### Esercizio 15: Trova l'album più venduto che non è una colonna sonora
### Task: Identifica l'album con le maggiori 'Music Recording Sales' che non è una colonna sonora
### Soluzione:  
print("***ESERCIZIO 15***")
non_soundtrack = df[df['Soundtrack'] != 'Y']
best_seller = non_soundtrack.loc[non_soundtrack['Music Recording Sales (millions)'].idxmax()]
print(f"Artist: {best_seller['Artist']}, Album: {best_seller['Album']}, Sales: {best_seller['Music Recording Sales (millions)']}M")
print("******************"+"\n")