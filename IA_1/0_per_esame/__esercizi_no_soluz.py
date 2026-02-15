import pandas as pd

## Esercizio 1: Carica il CSV in un DataFrame
## Task: Leggi i dati del file CSV fornito in un Pandas DataFrame e visualizza le prime 3 righe  
## Soluzione:
print("***ESERCIZIO 1***")
df = pd.read_csv('./some_music_albums.csv')
print(df.head(3))
print("*****************"+"\n")    
 
### Esercizio 2: Mostra informazioni di base sul DataFrame 
### Task: Mostra il numero di righe, colonne e tipi di dati per ogni colonna 
### Soluzione:
print("***ESERCIZIO 2***")
print(df.dtypes)
print("*****************"+"\n")
 
### Esercizio 3: Filtra gli album per genere
### Task: Crea un nuovo DataFrame contenente solo gli album con "rock" nella colonna 'Genre'
### Soluzione:
print("***ESERCIZIO 3***")
df_filt = df[df['Genre'].str.contains('rock', case=False)]
print(df_filt)
print("*****************"+"\n")

## Esercizio 4: Trova gli album pubblicati dopo il 1980
## Task: Filtra gli album pubblicati dopo il 1980 e visualizza solo le colonne 'Artist', 'Album' e 'Released'
## Soluzione:
print("***ESERCIZIO 4***")
cond = df['Released'] > 1980
df2 = df[cond].loc[1:, ['Artist', 'Album', 'Released']]
print(df2)
print("*****************"+"\n")

### Esercizio 5: Calcola la media delle valutazioni
### Task: Calcola la media della colonna 'Rating' per tutti gli album
### Soluzione:
print("***ESERCIZIO 5***")
avg = df['Rating'].mean()
print(avg)
print("*****************"+"\n")

### Esercizio 6: Trova l'album più lungo e il più breve
### Task: Identifica l'album con la durata massima e minima nella colonna 'Length' e visualizza i suoi dettagli
### Soluzione:
print("***ESERCIZIO 6***")
df['Length_int'] = pd.to_timedelta(df['Length'])
print(df.head(3))
max_ind = df['Length_int'].idxmax()
min_ind = df['Length_int'].idxmin()
print(df.loc[max_ind])
print(df.loc[min_ind])
print("*****************"+"\n")
 
### NON FARE
### Esercizio 7: Elenco generi unici
### Task: Estrai e stampa tutti i generi unici nel dataset (dividendo i generi combinati come "pop, rock")
### Soluzione:
print("***ESERCIZIO 7***")

print("*****************"+"\n")

### Esercizio 8: Confronta le vendite con vendite dichiarate
### Task: Aggiungi una nuova colonna 'Sales_Difference' che mostri la differenza tra 'Claimed Sales' e 'Music Recording Sales'
### Soluzione:
print("***ESERCIZIO 8***")
df['Sales_Difference'] = df['Claimed Sales'] - df['Music Recording Sales']
print(df.head())
print("*****************"+"\n")
  
### Esercizio 9: Trova gli album colonna sonora
### Task: Elenca tutti gli album contrassegnati come 'Soundtrack' (dove la colonna è "Y")
### Soluzione:
print("***ESERCIZIO 9***")
df4 = df[df['Soundtrack']=='Y'] 
print(df4)
print("*****************"+"\n")

### Esercizio 10: Salva i dati filtrati in un file CSV
### Task: Salva tutti gli album con una valutazione (Rating) ≥ 9 in un nuovo file CSV
### Soluzione:
print("***ESERCIZIO 10***")
cond2 = df['Rating'] >= 9
df5 = df[cond2]
df5.to_csv('./music_clean.csv', index=False)
print("******************"+"\n")

### NON FARE  
### Esercizio 11: Conta gli album per genere
### Task:Conta quanti album appartengono a ogni genere unico (dividendo generi combinati come "pop, rock")
### Soluzione:  
print("***ESERCIZIO 11***")

print("******************"+"\n")

### Esercizio 12: Trova l'album con la maggior differenza tra vendite e vendite dichiarate
### Task: Identifica l'album con la maggiore differenza tra 'Claimed Sales' e 'Music Recording Sales' e visualizza i suoi dettagli
### Soluzione:  
print("***ESERCIZIO 12***")
max_ind = df['Sales_Difference'].idxmax()
print(df.loc[max_ind])
print("******************"+"\n")
  
### Esercizio 13: Filtra gli album per generi multipli
### Task: Crea un nuovo DataFrame contenente gli album che includono entrambi "rock" e "pop" nella colonna 'Genre'
### Soluzione:**  
print("***ESERCIZIO 13***")
pop = df['Genre'].str.contains('pop', case=False)
rock = df['Genre'].str.contains('rock', case=False)
df6 = df[pop&rock]
print(df6)
print("******************"+"\n")

### NON FARE    
### Esercizio 14: Calcola la durata media per genere
### Task: Calcola la media della durata (in minuti) degli album per ogni genere (dividendo generi combinati)
### Soluzione:  
print("***ESERCIZIO 14***")

print("******************"+"\n")

### Esercizio 15: Trova l'album più venduto che non è una colonna sonora
### Task: Identifica l'album con le maggiori 'Music Recording Sales' che non è una colonna sonora
### Soluzione:  
print("***ESERCIZIO 15***")
df7 = df[df['Soundtrack'] != 'Y']
max_ind = df7['Music Recording Sales'].idxmax()
print(df.loc[max_ind])
print("******************"+"\n")