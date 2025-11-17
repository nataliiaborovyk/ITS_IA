# ---------------------------------------------------------
# IMPORT DELLE LIBRERIE
# ---------------------------------------------------------

import os              # modulo 'os' serve per lavorare con i percorsi dei file (path)
import pandas as pd    # importiamo la libreria pandas e la chiamiamo 'pd'
                       # pandas serve per lavorare con tabelle (DataFrame)


# ---------------------------------------------------------
# 1) CREARE UN DATAFRAME DA UN DIZIONARIO PYTHON
# ---------------------------------------------------------

# ATTENZIONE: evitare di usare il nome 'dict', perché è anche il nome del tipo built-in di Python
# Meglio usare un nome diverso, per esempio 'people_dict'

people_dict = {
    "Name": [
        "Braund, Mr. Owen Harris",
        "Allen, Mr. William Henry",
        "Bonnell, Miss. Elizabeth",
        "Taylor, Miss. Jane",
    ],
    "Age": [22, 35, 58, 55],
    "Sex": ["male", "male", "female", "female"],
    "Location": ["Rome", "London", "Berlin", "New York"],
}

# pd.DataFrame(...) crea un DataFrame a partire da un dizionario
# - chiavi del dizionario = nomi delle colonne
# - liste = valori nelle righe
df = pd.DataFrame(people_dict)

print("Un DataFrame creato da un dizionario Python:")
print(df)        # stampa l'intera tabella
print("\n")      # stampa una riga vuota per separare l'output


# ---------------------------------------------------------
# 2) CREARE UN DATAFRAME DA UN FILE CSV (ESEMPIO)
# ---------------------------------------------------------
# Questo blocco è COMMENTATO, ma ti spiego cosa fa.
# Lo puoi usare quando hai un file CSV sul disco.

# script_dir = os.path.dirname(os.path.abspath(__file__))
# # script_dir = cartella dove si trova il file .py corrente
#
# # os.path.join mette insieme cartella + nome file, in modo portabile
# csv_path = os.path.join(script_dir, "../dati/clean_data.csv")
#
# # pd.read_csv legge un file CSV e lo trasforma in un DataFrame
# df = pd.read_csv(csv_path)
#
# print("Un DataFrame creato da un file csv")
# print(df.head())     # .head() mostra le prime 5 righe (default)
# print("\n")
#
# # In alternativa, se sei già nella cartella giusta, puoi fare:
# # df = pd.read_csv("../dati/titanic.csv")


# ---------------------------------------------------------
# 3) MODI DIVERSI DI SELEZIONARE COLONNE
# ---------------------------------------------------------

# df.Age   → usa la notazione "a punto", funziona solo se il nome della colonna è un identificatore valido
print(df.Age)
print("\n")

# df['Age'] → modo più generale, funziona sempre (finché la colonna si chiama 'Age')
print(df['Age'])
print("\n")

# df[['Age']] → ritorna un DataFrame con UNA colonna (non una Series)
print(df[['Age']])
print("\n")

# df[['Age', 'Location']] → DataFrame con DUE colonne
# Nel tuo codice c'era df['Age', 'Location'], che non è corretto per due colonne
print(df[['Age', 'Location']])
print("\n")


# ---------------------------------------------------------
# 4) SELEZIONARE RIGHE CON .iloc (posizione) E .loc (etichetta)
# ---------------------------------------------------------

# .iloc usa INDICI POSIZIONALI (0,1,2,3, ...)
# df.iloc[2] → terza riga (indice 2), come Series
print(df.iloc[2])
print(type(df.iloc[2]))   # <class 'pandas.core.series.Series'>
print("\n")

# df.iloc[[2]] → ancora la terza riga, ma come DataFrame
print(df.iloc[[2]])
print(type(df.iloc[[2]]))  # <class 'pandas.core.frame.DataFrame'>
print("\n")

# df.iloc[0:2, 0:3]
# - righe: da 0 incluso a 2 escluso (quindi 0 e 1)
# - colonne: da 0 incluso a 3 escluso (quindi le prime 3 colonne)
print(df.iloc[0:2, 0:3])
print("\n")


# ---------------------------------------------------------
# 5) USO DI set_index E loc SUL NUOVO INDICE
# ---------------------------------------------------------

# set_index('Name', inplace=True)
# - imposta la colonna 'Name' come INDICE del DataFrame
# - inplace=True → modifica df direttamente, senza creare una copia
df.set_index("Name", inplace=True)

# .loc con etichetta (label) dell'indice
print(df.loc["Taylor, Miss. Jane"])   # seleziona la riga con indice "Taylor, Miss. Jane"
print("\n")

# reset_index(inplace=True) ripristina un indice numerico 0..n-1
df.reset_index(inplace=True)

print("DataFrame dopo reset_index:")
print(df)
print("\n")


# ---------------------------------------------------------
# 6) METODI DI RIEPILOGO: head, tail, describe, dtypes, info, columns, index, shape
# ---------------------------------------------------------

# .head(n) → prime n righe (default n=5)
print("Prime 2 righe:")
print(df.head(2))
print("\n")

# .tail(n) → ultime n righe (default n=5)
print("Ultime 2 righe:")
print(df.tail(2))
print("\n")

# .describe() → statistiche descrittive per le colonne numeriche
print("Statistiche descrittive per tutte le colonne numeriche:")
print(df.describe())
print("\n")

# df["Age"].describe() → statistiche solo per la colonna Age (Series)
print("Statistiche descrittive per la colonna 'Age':")
print(df["Age"].describe())
print("\n")

# df.dtypes → tipo di dato di ogni colonna (int64, object, float64, ecc.)
print("Tipi di dato delle colonne:")
print(df.dtypes)
print("\n")

# df.info() → info generali: numero di righe, colonne, null, tipi, memoria
print("Informazioni generali sul DataFrame:")
print(df.info())
print("\n")

# df.columns → Index con i nomi delle colonne
print("Nomi delle colonne:")
print(df.columns)
print("\n")

# df.index → Index con gli indici delle righe
print("Indici delle righe:")
print(df.index)
print("\n")

# df.shape → tupla (numero_righe, numero_colonne)
print("Forma del DataFrame (righe, colonne):")
print(df.shape)
print("\n")


# ---------------------------------------------------------
# 7) CREARE UN NUOVO DATAFRAME CON INDICE PERSONALIZZATO
# ---------------------------------------------------------

df = pd.DataFrame(
    {
        'Name': ['Alice', 'Bob', 'Aritra'],
        'Age': [25, 30, 35],
        'Location': ['Seattle', 'New York', 'Kona'],
    },
    index=[10, 20, 30]   # qui l'indice non è 0,1,2 ma 10,20,30
)

print("Un DataFrame creato da un dizionario Python con indici personalizzati:")
print(df)
print("\n")
print("Tipo di df:", type(df))
print("\n")


# ---------------------------------------------------------
# 8) MODI DIVERSI PER ACCEDERE A UNA COLONNA E TIPI RESTITUITI
# ---------------------------------------------------------

print(df.Location)        # Series
print(df['Location'])     # stesso risultato, Series
print(df[['Location']])   # DataFrame con una colonna
print("\n")

print("Tipi restituiti:")
print(type(df.Location))      # Series
print(type(df['Location']))   # Series
print(type(df[['Location']])) # DataFrame
print("\n")


# ---------------------------------------------------------
# 9) TIPO DELLA COLONNA NEL DIZIONARIO ORIGINALE VS. NEL DATAFRAME
# ---------------------------------------------------------

# people_dict.get("Age") → lista Python
print("Tipo di people_dict.get('Age'):", type(people_dict.get("Age")))
print("\n")

print(df)
print("\n")

# df["Age"] → pandas.Series (colonna del DataFrame)
print("Tipo di df['Age']:", type(df["Age"]))
print("\n")

# pd.Series([...], name="Age") crea una Series direttamente
ages = pd.Series([22, 35, 58], name="Age")
print("Tipo di 'ages':", type(ages))
print("\n")


# ---------------------------------------------------------
# 10) ALCUNE OPERAZIONI SULLE COLONNE
# ---------------------------------------------------------

# df["Location"].max() → massimo "lessicografico" (ordine alfabetico) sulla colonna Location
print("Valore massimo (alfabetico) in Location:", df["Location"].max())
print("\n")

print("Colonna Location:")
print(df.Location)
print("\n")

print("DataFrame con colonne Age e Sex (se esistessero):")
# In questo DataFrame df attuale non c'è 'Sex', quindi questa riga darebbe errore.
# Nel tuo esempio originale c'era un altro DataFrame con 'Sex'.
# Scrivo la sintassi corretta, ma la commento per non avere errore:
# print(df[['Age', 'Sex']])
print("ESEMPIO (commentato): df[['Age', 'Sex']] → DataFrame con due colonne")
print("\n")


# ---------------------------------------------------------
# 11) SELEZIONI CON loc E FILTRI SULLE RIGHE
# ---------------------------------------------------------

# Esempio 1: selezionare prime 2 righe e colonne 'Name' e 'Location' (se esistono)
# df_1 = df.loc[:, ['Name', 'Location']].head(2)
# Stessa cosa
# df_2 = df[['Name', 'Location']].head(2)

# Esempio 2: filtrare sulle righe con una condizione sulla colonna Age
# df_1 = df[df['Age'] > 30]     # tutte le righe con Age > 30
# df_2 = df.loc[df['Age'] < 30] # tutte le righe con Age < 30

# print(df_1)
# print(df_2)


# ---------------------------------------------------------
# 12) DIFFERENZA TRA iloc E loc (RIASSUNTO)
# ---------------------------------------------------------

# iloc → usa POSIZIONI intere (0,1,2,...)
# loc  → usa ETICHETTE (nomi di indice o nomi di colonne)

# Row Selection (righe):
#   iloc[0:2] → righe con posizione 0 e 1 (2 escluso)
#   loc[0:2]  → se l'indice è numerico, righe con etichette 0,1,2 (2 incluso)

# Column Selection (colonne):
#   iloc[0:3]          → colonne di posizione 0,1,2
#   loc['Name':'Age']  → colonne da 'Name' fino a 'Age' (estremi inclusi)


# ---------------------------------------------------------
# 13) FILTRI CONDIZIONALI E .query, .str.contains
# ---------------------------------------------------------

# Per mostrare gli esempi, ricreiamo il DataFrame "originale" con Name, Age, Sex, Location
df = pd.DataFrame({
    "Name": [
        "Braund, Mr. Owen Harris",
        "Allen, Mr. William Henry",
        "Bonnell, Miss. Elizabeth",
        "Taylor, Miss. Jane",
    ],
    "Age": [22, 35, 58, 55],
    "Sex": ["male", "male", "female", "female"],
    "Location": ["Rome", "London", "Berlin", "New York"],
})

print("DataFrame di esempio per i filtri:")
print(df)
print("\n")

# Condizione semplice: Age >= 40
simple_condition_1 = df['Age'] >= 40
print("simple_condition_1 (Age >= 40):")
print(simple_condition_1)        # Series di True/False
print("\n")

# df[condizione] → restituisce solo le righe dove la condizione è True
print("Righe con Age >= 40:")
print(df[df['Age'] >= 40])
print("\n")

# Stessa cosa con .query (stringa tipo SQL)
print("Righe con Age >= 40 (usando query):")
print(df.query('Age >= 40'))
print("\n")

# Altra condizione: Age > 40
simple_condition_1 = df['Age'] > 40
print("simple_condition_1 (Age > 40):")
print(simple_condition_1)
print(type(simple_condition_1))   # Series di bool
print("\n")

print("Righe con Age > 40:")
print(df[simple_condition_1])
print("\n")

# Condizione sulle stringhe: Location contiene 'ne' (case=False → non sensibile a maiuscole/minuscole)
simple_condition_2 = df['Location'].str.contains('ne', case=False)
print("simple_condition_2 (Location contiene 'ne'):")
print(simple_condition_2)
print("\n")

print("Righe con Location che contiene 'ne':")
print(df[simple_condition_2])
print("\n")

# Condizione combinata con & (AND logico):
print("Righe con Age > 40 E Location che contiene 'ne':")
print(df[simple_condition_1 & simple_condition_2])
print("\n")

# Modificare valori con .loc + condizione:
# df.loc[condizione, 'Colonna'] = nuovo_valore
df.loc[df['Location'].str.contains('r', case=False), 'Location'] = '?'
print("DataFrame dopo aver sostituito Location con '?' dove c'è una 'r':")
print(df)
print("\n")


# ---------------------------------------------------------
# 14) CAMBIARE COMPLETAMENTE L'INDICE
# ---------------------------------------------------------

print("Indici attuali:")
print(df.index)
print("\n")

print("Forma del DataFrame (righe, colonne):")
print(df.shape)
print("\n")

# Cambiamo l'indice con una lista di etichette personalizzate
new_index = ['a', 'b', 'c', 'd']
df.index = new_index

print("Indici dopo la modifica:")
print(df.index)
print("\n")

print("DataFrame con nuovi indici:")
print(df)
print("\n")

# Affettare con loc su nuovi indici
print("df.loc['a':'c', 'Name'] → righe da 'a' a 'c', colonna Name:")
print(df.loc['a':'c', 'Name'])
print(type(df.loc['a':'c', 'Name']))   # Series
print("\n")

print("df.loc['a':'c', 'Name':'Age'] → righe da 'a' a 'c', colonne da Name a Age:")
print(df.loc['a':'c', 'Name':'Age'])
print(type(df.loc['a':'c', 'Name':'Age']))  # DataFrame
print("\n")

print("df.loc['b':'d'][['Age','Location']] → righe b..d, solo colonne Age e Location:")
print(df.loc['b':'d'][['Age', 'Location']])
print(type(df.loc['b':'d'][['Age', 'Location']]))
print("\n")


# ---------------------------------------------------------
# 15) ORDINARE IL DATAFRAME CON sort_values
# ---------------------------------------------------------

# df.sort_values('Age', ascending=False)
# - ordina le righe in base alla colonna Age
# - ascending=False → dal più grande al più piccolo
print("DataFrame ordinato per Age (decrescente):")
print(df.sort_values('Age', ascending=False))
print("\n")


# ---------------------------------------------------------
# 16) ESEMPIO FINALE CON UN ALTRO CSV (MUSIC ALBUMS)
# ---------------------------------------------------------
# Anche questo blocco nel tuo codice era commentato. Ti spiego cosa fa.

# df = pd.read_csv("../dati/SomeMusicAlbums.csv")
#
# print(df.iloc[3:6, 0:3])
# - righe dalla posizione 3 alla 5 (6 escluso)
# - colonne dalla posizione 0 alla 2 (3 escluso)
#
# print(df.loc[3:5, 'Artist':'Released'])
# - righe con etichette 3, 4, 5
# - colonne da 'Artist' a 'Released' (estremi inclusi)
#
# df_new = df[['Artist', 'Soundtrack']]
# print(df_new.loc[3:5])   # usa loc con indici di riga 3..5
# print(df_new.iloc[3:6])  # usa iloc con posizioni 3..5
