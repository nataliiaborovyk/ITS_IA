import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataPipeline:
    def __init__(self):
        self.csv_path = "../dati/raw_data.csv"
        self.clean_csv_path = "../dati/clean_data.csv"
        self.output_plot = "../visual/scatter_plot.png"
        

    def caricamento_dati(self) -> pd.DataFrame:
        #caricamento dati da file.csv locale
        df = pd.read_csv(self.csv_path)
        return df
    
    def salvataggio_dati(self, df:pd.DataFrame) -> None:
        # salvataggio dati  su un file csv locale
        df.to_csv(self.clean_csv_path)  # df.to_csv(...) scrive il DataFrame su file CSV.
    
    def preprocessamento_dati(self, df:pd.DataFrame) -> pd.DataFrame:
        # pulizia e preparazione dati
            # Creo una nuova colonna ("is_healthy") usando condizioni sulle altre colonne → tipico uso pandas.
        df["is_healthy"] = (df["screen_time_hours"] < 5) & (df["sleep_hours"] >= 8)
        self.salvataggio_dati(df)
        return  df

    def visualizzazione_dati(self, df:pd.DataFrame) -> None:
            # visualizzazione dati matplotlib
        plt.figure(figsize=(10, 6))
        true_data:pd.DataFrame = df[df["is_healthy"] == True]  # df[condizione] è il filtro di righe (subset) del DataFrame.
        false_data:pd.DataFrame = df[df["is_healthy"] == False]  # oppure df[~df["is_healthy"]]   ~ è Not
        plt.scatter(true_data["screen_time_hours"], true_data["math_score"], 
                    color="green", label="Vero")
        plt.scatter(false_data["screen_time_hours"], false_data["math_score"], 
                    color="red", label="Falso")
        plt.xlabel("Screen time hours")
        plt.ylabel("Math score")
        plt.title("Screen time hours & math score")
        plt.legend()
        plt.savefig(self.output_plot)
        plt.close()

            # visualizzazione dati seaborn
        # plt.figure(figsize=(10, 6))
        # plt.xlabel("Screen time hours")
        # plt.ylabel("Math score")
        # plt.title("Screen time hours & math score")
        # sns.scatterplot(data=df, x="screen_time_hours", y="math_score", hue="is_healthy")
        # # plt.legend()
        # plt.savefig(self.output_plot)
        # plt.close()

    def esegui_pipline(self) -> None:
        # passagio caricamento
        raw_df = self.caricamento_dati()
        print("  -letti dati da un file csv")
        # print(raw_df)
        # preprocessamento
        clean_df = self.preprocessamento_dati(raw_df)
        print("Pulizia dati comletato e file salvato")
        # print(clean_df.columns)
        self.visualizzazione_dati(clean_df)
        print("     -Visualizati e salvati risultati di analisi")



if __name__ == "__main__":

    pipeline = DataPipeline()
    print("Pipline avviata...")
    pipeline.esegui_pipline()
    print("Pipline completata con sucesso")
    

    