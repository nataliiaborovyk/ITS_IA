import pandas as pd
import matplotlib.pyplot as plt 
# import seaborn as sns 

class DataPipeline:
    def __init__(self):
        self.csv_path = "../dati/raw_data.csv"
        self.clean_csv_path = "../dati/clean_data.csv"
        self.output_plot = "../visual/scatter_plot.png"
        
    def caricamento_dati(self) -> pd.DataFrame:
        # Caricamento dati da un file .csv locale
        df = pd.read_csv(self.csv_path)
        return df
    
    def salvataggio_dati(self, df: pd.DataFrame) -> None:
        # Salvataggio dati su un file .csv locale
        df.to_csv(self.clean_csv_path)
    
    def preprocessamento_dati(self, df: pd.DataFrame) -> pd.DataFrame:
        # Pulizia e preparazione dati
        df["is_healthy"] = (df["screen_time_hours"] < 4) & (df["sleep_hours"] >= 8)
        self.salvataggio_dati(df)
        return df
    
    def visualizzazione_dati(self, df: pd.DataFrame) -> None:
        # Visualizzazione dati
        plt.figure(figsize=(10,6))
        true_data = df[df["is_healthy"] == True]
        false_data = df[df["is_healthy"] == False]
        plt.scatter(true_data['screen_time_hours'], true_data['math_score'], 
                    color='green', label='Vero')
        plt.scatter(false_data['screen_time_hours'], false_data['math_score'], 
                    color='red', label='Falso')
        plt.xlabel('Screen time hours')
        plt.ylabel('Math score')
        plt.title('Screen time hours vs. math score')
        plt.legend()
        plt.savefig(self.output_plot)
        plt.close()
        
        # plt.figure(figsize=(10,6))
        # plt.xlabel('Screen time hours')
        # plt.ylabel('Math score')
        # plt.title('Screen time hours vs. math score')
        # sns.scatterplot(data=df, x="screen_time_hours", y="math_score", hue="is_healthy")
        # # plt.legend()
        # plt.savefig(self.output_plot)
        # plt.close()
   
    def esegui_pipeline(self) -> None:
        # Caricamento
        raw_df = self.caricamento_dati()
        print("   -Letti dati da un file csv")
        # print(raw_df)
        # Preprocessamento
        clean_df = self.preprocessamento_dati(raw_df)
        print("   -Pulizia dati completata e file pulito salvato")
        # print(clean_df.columns)
        # Visualizzazione
        self.visualizzazione_dati(clean_df)
        print("   -Visualizzati e salvati risultati di analisi")
        
if __name__ == "__main__":
    pipeline = DataPipeline()
    print("Pipeline avviata...")
    pipeline.esegui_pipeline()
    print("Pipeline completata con successo")
