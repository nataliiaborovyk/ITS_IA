import pandas as pd          # Importo la libreria pandas e le do il nome abbreviato "pd".
                             # Userò "pd" ogni volta che creo/leggo/salvo DataFrame.

import numpy as np           # Importo numpy come "np", lo userò per gestire valori speciali come np.nan.

from sqlalchemy import create_engine, text   # Importo da SQLAlchemy:
                                             # - create_engine: per creare il collegamento al DB
                                             # - text: per avvolgere stringhe SQL in oggetti "sicuri" per SQLAlchemy

from sqlalchemy.exc import SQLAlchemyError   # Importo il tipo di eccezione usata da SQLAlchemy
                                             # per intercettare errori di lettura/scrittura sul database.


class DataSourceConfig:
    """Configurazione sorgenti dati e destinazione output"""
    remote_url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
    db_uri: str = "postgresql+psycopg://postgres:postgres@postgresql:5432/auto_db"
    csv_path: str = "../../dati/autos/auto.csv"
    csv_clean_path: str = "../../dati/autos/auto_clean.csv"
    output_plot: str = "../../visual/autos/plot.png"

# postgresql + psycopg:// postgres : postgres @ postgresql : 5432 / auto_db
#       |         |             |         |           |         |
#   dialetto     driver       utente    password     host     porta   database

dialect = "postgresql"
driver = "psycopg"
username = "postgres"
password = "postgres"
host = "postgresql"
port = 5432
database = "auto_db"

db_uri_es = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"



class DataPipeline:
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.data = None
        
    def load_from_csv(self) -> pd.DataFrame:
        """Carica dati da un file CSV"""
        # pd.read_csv(...)
        # - "pd" è pandas
        # - "read_csv" legge un file CSV e restituisce un DataFrame
        # - self.config.csv_path è il percorso del file da leggere
        return pd.read_csv(self.config.csv_path)

    def load_from_remote(self) -> pd.DataFrame:
        """Carica dati da un file remoto identificato da un URL aggiungendo intestazioni"""
        # Qui preparo una lista di nomi di colonne per il dataset auto:
        headers = [
            "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
            "num-of-doors", "body-style", "drive-wheels", "engine-location",
            "wheel-base", "length", "width", "height", "curb-weight", "engine-type",
            "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke",
            "compression-ratio", "horsepower", "peak-rpm", "city-mpg",
            "highway-mpg", "price"
        ]
        # pd.read_csv(self.config.remote_url, names=headers)
        # - Legge un CSV direttamente da un URL (quindi da remoto).
        # - "names=headers" dice a pandas: usa questa lista come intestazioni di colonna
        #   invece di cercarle nel file.
        return pd.read_csv(self.config.remote_url, names=headers)
    
    def save_on_csv(self, df: pd.DataFrame) -> None:
        """Salva dati in un file CSV"""
        # df.to_csv(self.config.csv_path)
        # - "df" è un DataFrame di pandas.
        # - "to_csv" salva il DataFrame in formato CSV.
        # - self.config.csv_path è il percorso dove salvare il file.
        # - di default salva anche l'indice come prima colonna (index=True di default).
        df.to_csv(self.config.csv_path)
        
    def save_clean_on_csv(self, df: pd.DataFrame) -> None:
        """Salva dati puliti in un file CSV"""
        # Stesso discorso di sopra, ma salviamo nella versione "pulita":
        df.to_csv(self.config.csv_clean_path)
    
    def store_on_database(self, df: pd.DataFrame) -> None:
        """Scrive dati in un database PostgreSQL"""
        table_name = "auto_info"

        # create_engine(self.config.db_uri)
        # - Crea un "motore" SQLAlchemy, cioè l'oggetto che rappresenta
        #   la connessione (parametri, driver, host, porta, DB, utente, password).
        # - self.config.db_uri è una stringa con tutte le info di connessione.
        engine = create_engine(self.config.db_uri)

        try:
            # with engine.begin() as conn:
            # - Apre una connessione al database con gestione automatica della transazione.
            # - "begin()" ci dà:
            #     * COMMIT automatico se tutto va bene
            #     * ROLLBACK automatico se viene sollevata un'eccezione.
            # - "conn" è l'oggetto connessione che passeremo a pandas.
            with engine.begin() as conn:
                # df.to_sql(...)
                # - Scrive il DataFrame "df" come tabella in un database.
                # - table_name: nome della tabella da creare/sovrascrivere.
                # - con=conn: uso la connessione SQLAlchemy creata sopra.
                # - if_exists='replace': se la tabella esiste già, viene cancellata e ricreata.
                # - index=False: non salvare la colonna di indice del DataFrame.
                df.to_sql(table_name, con=conn, if_exists='replace', index=False)
        except SQLAlchemyError as e:
            # Se succede un errore SQLAlchemy (es. connessione rifiutata, tabella bloccata, ecc.)
            # lo intercetto e stampo un messaggio.
            print(f"Error di scrittura in database: {e}")
        finally:
            # engine.dispose()
            # - Chiude tutte le connessioni collegate a questo engine.
            # - Libera risorse (pool di connessioni, ecc.).
            engine.dispose()
        
    def load_from_database(self) -> pd.DataFrame:
        """Carica dati da un database PostgreSQL"""
        # Stringa con la query SQL che vogliamo eseguire.
        query_def = "SELECT * FROM public.auto_info"

        # Creo il "motore" del database, come sopra.
        engine = create_engine(self.config.db_uri)

        try:
            # with engine.connect() as conn:
            # - Apro una semplice connessione (solo lettura in questo caso).
            with engine.connect() as conn:
                # pd.read_sql_query(text(query_def), con=conn)
                # - text(query_def): trasforma la stringa SQL in un oggetto TextClause
                #   che SQLAlchemy gestisce in modo sicuro.
                # - con=conn: specifica la connessione da usare.
                # - read_sql_query esegue la query sul DB e restituisce un DataFrame pandas
                #   con i risultati (colonne = colonne SQL, righe = record).
                df = pd.read_sql_query(text(query_def), con=conn)
                # pd.read_sql_query(sql, con)
        except SQLAlchemyError as e:
            print(f"Errore di lettura da database: {e}")
            # Se succede un errore, restituisco un DataFrame vuoto, così il resto del codice
            # non va in crash ma può verificare che df è vuoto.
            df = pd.DataFrame()
        finally:
            # Chiudo e rilascio tutte le risorse legate all'engine.
            engine.dispose()
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Operazioni varie di pulizia dati"""

        # - Sostituisce tutti i valori "?" nel DataFrame con np.nan (valore mancante di numpy).
        # - inplace=True: modifica direttamente df, non restituisce una copia.
        df.replace("?", np.nan, inplace=True)

        # - df["normalized-losses"]: seleziona la colonna come Series.
        # - astype("float"): converte i valori della colonna a float (numeri con la virgola).
        # - mean(axis=0): calcola la media dei valori lungo l'asse 0 (lungo le righe).
        avg = df["normalized-losses"].astype("float").mean(axis=0)

        # - Nella colonna "normalized-losses" sostituisco i valori NaN con la media appena calcolata.
        df["normalized-losses"] = df["normalized-losses"].replace(np.nan, avg)

        # - value_counts(): conta quante volte compare ciascun valore nella colonna.
        # - idxmax(): restituisce il valore con la frequenza massima (moda).
        # Poi uso questo valore per rimpiazzare i NaN nella colonna 'num-of-doors'.
        df["num-of-doors"] = df["num-of-doors"].replace(
            np.nan,
            df['num-of-doors'].value_counts().idxmax()
        )

        # - Elimino tutte le righe dove la colonna "price" è NaN.
        # - subset=["price"]: considera i NaN solo in questa/e colonna/e.
        # - axis=0: cancella righe (non colonne).
        # - inplace=True: modifica df direttamente.
        df.dropna(subset=["price"], axis=0, inplace=True)

        # - Dopo aver eliminato righe, l'indice può avere "buchi".
        # - reset_index(drop=True) ricrea un indice da 0 a n-1 e NON salva l'indice vecchio come colonna.
        df.reset_index(drop=True, inplace=True)

        # - Tenta di indovinare il tipo "migliore" per ogni colonna (es. int, string, boolean, ecc.)
        #   sulla base dei valori presenti. Restituisce un DataFrame nuovo.
        df = df.convert_dtypes()

        # - Seleziono la colonna "normalized-losses" come DataFrame (doppie parentesi) e
        #   la converto esplicitamente a interi.
        df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")

        # Stessa cosa per "price", ma la converto a float.
        df[["price"]] = df[["price"]].astype("float")

        # Stessa cosa per "peak-rpm".
        df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")

        # df['make'].replace({...})
        # - Nella colonna 'make' correggo refusi nei nomi delle marche:
        #   'alfa-romero' → 'alfa-romeo', 'peugot' → 'peugeot'.
        df['make'] = df['make'].replace({
            'alfa-romero': 'alfa-romeo',
            'peugot': 'peugeot'
        })

        # Salvo il DataFrame pulito su CSV, usando la funzione definita prima.
        self.save_clean_on_csv(df)

        # Restituisco il DataFrame pulito.
        return df

    def visualize(self, df: pd.DataFrame) -> None:
        """Crea e salva visualizzazioni"""
        # Qui più avanti userai Matplotlib / pandas.plot per creare grafici a partire da df.
        # Per ora il metodo è vuoto.
        pass
        
    def run_pipeline(self) -> pd.DataFrame:
        """Esegue la pipeline completa"""
        # Carica dati da remoto (pandas legge l'URL e crea un DataFrame).
        remote_df = self.load_from_remote()
        print("   -Letto file remoto")

        # Salva dati in locale su CSV.
        self.save_on_csv(remote_df)
        print("   -Salvato file remoto in locale")

        # Scrive dati nel database (pandas + SQLAlchemy).
        self.store_on_database(remote_df)
        print("   -Scritto file remoto in una tabella su db")

        # Legge i dati dal database (SQLAlchemy + pandas.read_sql_query).
        db_df = self.load_from_database()
        print("   -Letti dati da una tabella su db")

        # Pulizia dati (solo pandas).
        clean_df = self.clean_data(db_df)
        print("   -Pulizia dati completata e file pulito salvato")

        # Visualizzazione risultati (Matplotlib + pandas.plot, quando lo implementerai).
        self.visualize(clean_df)
        print("   -Analisi e visualizzazione dati terminate")

        # Salvo il DataFrame pulito come attributo dell'oggetto pipeline.
        self.data = clean_df
        return clean_df
        
if __name__ == "__main__":
    config = DataSourceConfig()
    pipeline = DataPipeline(config)


    df_remote = pipeline.load_from_database()

    print("\n--- COLONNE DATI GREZZI ---")
    print(df_remote.columns.tolist())

    print("\n--- PRIME RIGHE DATI GREZZI ---")
    print(df_remote.head())

    print("\n--- INFO SUI TIPI ---")
    print(df_remote.dtypes)

    print("\n--- NUMERO DI RIGHE E COLONNE ---")
    print(df_remote.shape)

    print("     Mostra i nomi delle colonne")
    print(df_remote.columns.tolist())

    print("     Numero di valori mancanti per ogni colonna")
    print(df_remote.isna().sum())

    print("     Numero totale di valori mancanti nel DataFrame")
    print(df_remote.isna().sum().sum())

    print("     Statistiche delle colonne numeriche")
    print(df_remote.describe(include="all"))




    # print("Pipeline avviata...")
    # final_df = pipeline.run_pipeline()
    # print("Pipeline completata con successo!")

    # # final_df.head()
    # # - head() è un metodo pandas che mostra le prime 5 righe del DataFrame.
    # #   Utile per "dare un'occhiata" al risultato finale.
    # print(final_df.head())
