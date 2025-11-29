import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json
import matplotlib.pyplot as plt
from typing import Tuple

class DataSourceConfig:
    """Configurazione sorgenti dati e destinazione output"""
    # db_uri: str = "postgresql+psycopg://postgres:postgres@postgresql:5432/titanic_db"
    db_uri: str = "postgresql+psycopg://postgres:postgres@localhost:5432/titanic_db"
    json_path: str = "../../dati/titanic/titanic_prefs_small.json"
    output_plot: str = "../../visual/titanic/plot.png"

class DataPipeline:
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.data = None
    
    def load_from_database(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Carica dati da un database PostgreSQL"""
        queries = {
            'passenger': "SELECT * FROM public.passenger_info_small",
            'ticket': "SELECT * FROM public.ticket_info_small"
        }
        
        engine = create_engine(self.config.db_uri)
        try:
            with engine.connect() as conn:
                df1 = pd.read_sql_query(text(queries['passenger']), conn)
                df2 = pd.read_sql_query(text(queries['ticket']), conn)
        except SQLAlchemyError as e:
            print(f"Errore di lettura da database: {e}")
            df1 = pd.DataFrame()
            df2 = pd.DataFrame() 
        finally:
            engine.dispose()
        return df1, df2 
    
    def load_from_json(self) -> pd.DataFrame:
        """Carica dati da un file JSON"""
        return pd.read_json(self.config.json_path)
        
    def merge_data(self, db_df1: pd.DataFrame, db_df2: pd.DataFrame, json_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregazione dati di diverse sorgenti"""
        db_merged = pd.merge(db_df1, db_df2, on='PassengerId')
        return pd.merge(db_merged, json_df, on='PassengerId')
    
    def expand_json_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parsing ed espansione della colonna JSON di preferenze"""
        df['preferences'] = df['preferences'].apply(json.loads)
        prefs_expanded = pd.json_normalize(df['preferences'])
        return pd.concat([df.drop('preferences', axis=1), prefs_expanded], axis=1)
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Operazioni varie di pulizia dati"""
        # print(df.dtypes)
        # print(df[['Age' ,'Fare', 'preferred_deck', 'dining_time', 'activity', 'Sex']].head(10))
        # print(df[['Age' ,'Fare', 'preferred_deck', 'dining_time', 'activity', 'Sex']].tail())

        # Sostituisce valori nulli/assenti con NaN
        df.replace("?", np.nan, inplace=True)
        
        # # Quanti NaNs per colonna
        # missing_data = df.isnull()
        # for column in missing_data.columns.values.tolist():
        #     # print(column)
        #     print (missing_data[column].value_counts())
        
        # Limita gli outliers
        df['Age'] = df['Age'].clip(upper=80)
        
        # Sostituisce NaNs con il valor medio
        avg = df["Age"].astype("float").mean(axis=0)
        df["Age"] = df["Age"].replace(np.nan, avg)
        avg = df["Fare"].astype("float").mean(axis = 0)
        df["Fare"] = df["Fare"].replace(np.nan, avg)
        
        # Sositutisce NaNs con valori random di colonne categoriche
        decks = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
        df["preferred_deck"] = df["preferred_deck"].apply(
            lambda x: np.random.choice(decks) if pd.isna(x) else x
        )
        times = np.array(['early', 'flexible', 'late'])
        df["dining_time"] = df["dining_time"].apply(
            lambda x: np.random.choice(times) if pd.isna(x) else x
        )
        
        # Sositutisce NaNs con il valore più frequente 
        df["activity"] = df["activity"].replace(
            np.nan, df['activity'].value_counts().idxmax()        
        )
        
        # Correzione di errori per contenuti standard
        df['Sex'] = df['Sex'].replace({'mael': 'male', 'femael': 'female'})
        
        # Conversione dei tipi di dato
        df = df.convert_dtypes()
        df[["Age"]] = df[["Age"]].astype("float")
        
        # print(df.dtypes)
        # print(df[['Age' ,'Fare', 'preferred_deck', 'dining_time', 'activity', 'Sex']].head(10))
        # print(df[['Age' ,'Fare', 'preferred_deck', 'dining_time', 'activity', 'Sex']].tail())
        
        return df
    
    def visualize(self, df: pd.DataFrame) -> None:
        """Crea e salva visualizzazioni"""
        plt.figure(figsize=(24, 12))
        df_agg_1 = df.groupby('preferred_deck').agg(deck_count=('PassengerId', 'count'))
        df_agg_2 = df.groupby('dining_time').agg(mean_fare=('Fare', 'mean'))
        df_agg_3 = df.groupby('activity').agg(min_age=('Age', 'min'))
        # print(type(df_agg_1))
        # print(df_agg_1)
        # print(df_agg_2)
        # print(df_agg_3)

        plt.subplot(1, 3, 1)
        # plt.barh(y=df_agg_3.index.astype(str), width=df_agg_3['min_age'])
        plt.bar(x=df_agg_3.index.astype(str), height=df_agg_3['min_age'])
        plt.title('Età Minima per Attività')
        plt.ylabel('Età')
        plt.xlabel('Attività')        
        
        plt.subplot(1, 3, 2)
        colors_list = ['gold', 'yellowgreen', 'lightcoral']
        plt.bar(x=df_agg_2.index.astype(str), height=df_agg_2['mean_fare'], color=colors_list)
        plt.title('Tariffa Media vs. Orario di Pasto')
        plt.ylabel('Tariffa')
        plt.xlabel('Orario di Pasto')
        
        plt.subplot(1, 3, 3)
        # plt.bar(x=df_agg_1.index.astype(str), height=df_agg_1['deck_count'])       
        # plt.title('Preferenze Ponte')
        # plt.ylabel('Numero di Passeggeri')
        # plt.xlabel('Ponte Preferito')
        df_agg_1['deck_count'].plot(kind='pie',
                            autopct='%1.1f%%', # aggiungi le percentuali
                            startangle=90,     # Angolo iniziale a 90°     
                            ) 
        plt.title('Preferenze Ponte')
        plt.ylabel('')
        plt.axis('equal') # rende il pie chart un cerchio        
        
        plt.savefig(self.config.output_plot)
        plt.show()
        plt.close()
    
    def run_pipeline(self) -> pd.DataFrame:
        """Esegue la pipeline completa"""
        # Carica dati
        db_df1, db_df2 = self.load_from_database()
        print("   -Letti dati da due tabelle su db")
        json_df = self.load_from_json()
        print("   -Letti dati da un file JSON")        
        # Preprocessa dati
        merged_df = self.merge_data(db_df1, db_df2, json_df)
        expanded_df = self.expand_json_data(merged_df)
        print("   -Aggregazione ed espansione dati effettuate")
        cleaned_df = self.clean_data(expanded_df)
        print("   -Pre-processamento e pulizia dati completati")        
        # Visualizza risultati
        self.visualize(cleaned_df)
        print("   -Analisi e visualizzazione dati terminate")          
        self.data = cleaned_df
        return cleaned_df
        
# Uso delle classi
if __name__ == "__main__":
    config = DataSourceConfig() 
    # Esegui la pipeline
    pipeline = DataPipeline(config)
    print("Pipeline avviata...")
    final_df = pipeline.run_pipeline()
    print("Pipeline completata con successo!")
    # print(final_df.head())