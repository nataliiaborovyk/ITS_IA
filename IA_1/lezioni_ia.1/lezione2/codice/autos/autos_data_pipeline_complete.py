import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.pyplot as plt

class DataSourceConfig:
    """Configurazione sorgenti dati e destinazione output"""
    remote_url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
    db_uri: str = "postgresql+psycopg://postgres:postgres@postgresql:5432/auto_db"
    csv_path: str = "../../dati/autos/auto.csv"
    csv_clean_path: str = "../../dati/autos/auto_clean.csv"
    output_plot: str = "../../visual/autos/plot.png"

class DataPipeline:
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.data = None
        
    def load_from_csv(self) -> pd.DataFrame:
        """Carica dati da un file CSV"""
        return pd.read_csv(self.config.csv_path)        

    def load_from_remote(self) -> pd.DataFrame:
        """Carica dati da un file remoto identificato da un URL aggiungendo intestazioni"""
        headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
                  "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
                  "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
                  "peak-rpm","city-mpg","highway-mpg","price"]
        return pd.read_csv(self.config.remote_url, names = headers)
    
    def save_on_csv(self, df: pd.DataFrame) -> None:
        """Salva dati in un file CSV"""
        df.to_csv(self.config.csv_path)    
        
    def save_clean_on_csv(self, df: pd.DataFrame) -> None:
        """Salva dati puliti in un file CSV"""
        df.to_csv(self.config.csv_clean_path)    
    
    def store_on_database(self, df: pd.DataFrame) -> None:
        """Scrive dati in un database PostgreSQL"""      
        table_name = "auto_info"
        engine = create_engine(self.config.db_uri)
        try:
            with engine.begin() as conn:  # begin() per gestione automatica di commit/rollback
                df.to_sql(table_name, con=conn, if_exists='replace', index=False)
        except SQLAlchemyError as e:
            print(f"Error di scrittura in database: {e}")
        finally:
            engine.dispose()  # Chiusura pulita e rilascio risorse
        
    def load_from_database(self) -> pd.DataFrame:
        """Carica dati da un database PostgreSQL"""
        query_def = "SELECT * FROM public.auto_info"        
        engine = create_engine(self.config.db_uri)
        try:
            with engine.connect() as conn:
                df = pd.read_sql_query(text(query_def), con=conn)
        except SQLAlchemyError as e:
            print(f"Errore di lettura da database: {e}")
            df = pd.DataFrame() 
        finally:
            engine.dispose()  # Chiusura pulita e rilascio risorse
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Operazioni varie di pulizia dati"""
        df.replace("?", np.nan, inplace=True)
        avg = df["normalized-losses"].astype("float").mean(axis = 0)
        df["normalized-losses"] = df["normalized-losses"].replace(np.nan, avg)
        df["num-of-doors"] = df["num-of-doors"].replace(np.nan, df['num-of-doors'].value_counts().idxmax())
        df.dropna(subset=["price"], axis=0, inplace = True)
        df.reset_index(drop = True, inplace = True)
        df = df.convert_dtypes()
        df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
        df[["price"]] = df[["price"]].astype("float")
        df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")
        df['make'] = df['make'].replace({'alfa-romero': 'alfa-romeo', 'peugot': 'peugeot'})
        self.save_clean_on_csv(df)
        return df

    def visualize(self, df: pd.DataFrame) -> None:
        """Crea e salva visualizzazioni"""         
        plt.figure(figsize=(20, 9))
        
        # ESEMPIO 1 - Prezzo Medio
        # df_agg = df.groupby('make').agg(mean_price=('price', 'mean'))
        # # df.groupby("make").agg(
        # #     mean_price=("price", "mean"),
        # #     max_price=("price", "max"),
        # #     min_price=("price", "min"),
        # #     count_auto=("price", "count"),
        # # )

        # # plt.bar(x=df_agg.index.astype(str), height=df_agg['mean_price'], color='green')
        # x = df_agg.index.astype(str) # dopo groupby indice diventa il valore di colonna 'make', es. "audi" ma di tipo object
        # y = df_agg['mean_price']
        # plt.bar(x, y)

        # # ESEMPIO 2 - Prezzo Medio Decrescente
        # df_agg = df.groupby('make').agg(mean_price=('price', 'mean'))
        # df_agg_mean_down = df_agg.sort_values(by='mean_price', ascending=False).head()
        # # plt.bar(x=df_agg_mean_down.index.astype(str), height=df_agg_mean_down['mean_price'], color='orange')
        # X = df_agg_mean_down.index.astype(str)     # nomi delle marche (Top 5)
        # Y = df_agg_mean_down['mean_price']         # prezzi medi delle top 5 marche
        # plt.bar(X, Y, color='orange')

        
        # # ESEMPIO 3 - Prezzo Medio Colorato
        # df_agg = df.groupby('make').agg(mean_price=('price', 'mean'))
        # bar_colors = ['tab:blue', 'tab:red', 'tab:orange', 'tab:green', 'tab:purple']
        # # plt.bar(x=df_agg.index.astype(str), height=df_agg['mean_price'], color=bar_colors)
        # x = df_agg.index.astype(str)
        # y = height=df_agg['mean_price']
        # plt.bar(x,y,color=bar_colors)


        # # ESEMPIO 4 - Prezzo Medio Colorato Decrescente Top 5
        df_agg = df.groupby('make').agg(mean_price=('price', 'mean'))
        df_agg_mean_down = df_agg.sort_values(by='mean_price', ascending=False).head()
        bar_colors = ['tab:blue', 'tab:red', 'tab:orange', 'tab:green', 'tab:purple']
        # plt.bar(x=df_agg_mean_down.head().index.astype(str), height=df_agg_mean_down.head()['mean_price'], color=bar_colors)
        x = df_agg_mean_down.index.astype(str)
        y = df_agg_mean_down['mean_price']
        plt.bar(x,y, color=bar_colors)

        plt.title('Prezzo Medio Auto per Marca')
        plt.ylabel('Prezzo Medio')
        plt.xlabel('Marca')
        plt.xticks(rotation=30)
        plt.yticks(rotation=30)
        plt.savefig(self.config.output_plot)
        plt.show()        
        plt.close()        
        
    def run_pipeline(self) -> pd.DataFrame:
        """Esegue la pipeline completa"""
        # # Carica dati da remoto
        # remote_df = self.load_from_remote()
        # print("   -Letto file remoto")
        # # Salva dati in locale
        # self.save_on_csv(remote_df)
        # print("   -Salvato file remoto in locale")
        # # Scrive dati in database
        # self.store_on_database(remote_df)
        # print("   -Scritto file remoto in una tabella su db")
        # Legge dati da database
        db_df = self.load_from_database()
        print("   -Letti dati da una tabella su db")
        # Pulizia dati
        cleaned_df = self.clean_data(db_df)
        print("   -Pulizia dati completata e salvata")
        # Visualizza risultati
        self.visualize(cleaned_df)
        print("   -Analisi e visualizzazione dati terminate")
        self.data = cleaned_df
        return cleaned_df
        
if __name__ == "__main__":
    config = DataSourceConfig() # Usa default DataSourceConfig
    pipeline = DataPipeline(config) # Esegui la pipeline
    print("Pipeline avviata...")
    final_df = pipeline.run_pipeline()
    print("Pipeline completata con successo!")
    # print(final_df.head())