import pandas as pd

data_path = "../dati/SomeMusicAlbums.csv"
output_path = "../dati/RatingMaggiore9.csv"

## Esercizio 1: Carica il CSV in un DataFrame
## Task: Leggi i dati del file CSV fornito in un Pandas DataFrame e visualizza le prime 3 righe  
## Soluzione:
print("***ESERCIZIO 1***")
df = pd.read_csv(data_path)
print(df.head(3))    
print("*****************"+"\n")
 
### Esercizio 2: Mostra informazioni di base sul DataFrame 
### Task: Mostra il numero di righe, colonne e tipi di dati per ogni colonna 
### Soluzione:
print("***ESERCIZIO 2***")
print(df.info())   
print("*****************"+"\n")

 
### Esercizio 3: Filtra gli album per genere
### Task: Crea un nuovo DataFrame contenente solo gli album con "rock" nella colonna 'Genre'
### Soluzione:
print("***ESERCIZIO 3***")
print(df[df['Genre'].str.contains('rock', case=False)])
print("*****************"+"\n")

## Esercizio 4: Trova gli album pubblicati dopo il 1980
## Task: Filtra gli album pubblicati dopo il 1980 e visualizza solo le colonne 'Artist', 'Album' e 'Released'
## Soluzione:
print("***ESERCIZIO 4***")
condizione = df['Released'] > 1980
df_nuivo = df[condizione]
print(df_nuivo.loc[:,'Artist':'Released'])
print("*****************"+"\n")

### Esercizio 5: Calcola la media delle valutazioni
### Task: Calcola la media della colonna 'Rating' per tutti gli album
### Soluzione:
print("***ESERCIZIO 5***")
media = df['Rating'].mean()
print(media)
print("*****************"+"\n")

### Esercizio 6: Trova l'album più lungo e il più breve
### Task: Identifica l'album con la durata massima e minima nella colonna 'Length' e visualizza i suoi dettagli
### Soluzione:
print("***ESERCIZIO 6***")

durate = pd.to_timedelta(df['Length'])
index_max = durate.idxmax()
index_min = durate.idxmin()
print("Album piu lungo: ")
print(df.loc[index_max])
print()
print("Album piu bleve: ")
print(df.loc[index_min])
print()
# oppure

durate = pd.to_timedelta(df['Length'])
max = df['Length'].max()
condiz_max = df['Length'] == max
min = df['Length'].min()
condiz_min = df['Length'] == min
print("Album piu lungo: ")
print(df[condiz_max])
print()
print("Album piu bleve: ")
print(df[condiz_min])

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
df['Sales_Difference'] = df['Claimed Sales (millions)'] - df['Music Recording Sales (millions)']
print(df.head(3))
print("*****************"+"\n")
  
### Esercizio 9: Trova gli album colonna sonora
### Task: Elenca tutti gli album contrassegnati come 'Soundtrack' (dove la colonna è "Y")
### Soluzione:
print("***ESERCIZIO 9***")
condiz1 = df['Soundtrack'] == 'Y'
print(df[condiz1])
print("*****************"+"\n")

### Esercizio 10: Salva i dati filtrati in un file CSV
### Task: Salva tutti gli album con una valutazione (Rating) ≥ 9 in un nuovo file CSV
### Soluzione:
print("***ESERCIZIO 10***")
condiz2 = df['Rating'] >= 9
nuovo = df[condiz2]
nuovo.to_csv(output_path, index=False)
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
print(df.describe())
condiz3 = df['Sales_Difference'] == 23.900000
print(df[condiz3])

# oppure
max = df['Sales_Difference'].max()
condiz4 = df['Sales_Difference'] == max
print(df[condiz4])

print("******************"+"\n")
  
### Esercizio 13: Filtra gli album per generi multipli
### Task: Crea un nuovo DataFrame contenente gli album che includono entrambi "rock" e "pop" nella colonna 'Genre'
### Soluzione:**  
print("***ESERCIZIO 13***")
rock = df['Genre'].str.contains('rock', case=True)
pop = df['Genre'].str.contains('pop', case=True)
print(df[(rock)&(pop)])
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
max = df['Music Recording Sales (millions)'].max()
condiz5 = (df['Music Recording Sales (millions)'] == max) & (df['Soundtrack'].isna())
print(df[condiz5])
print("******************"+"\n")