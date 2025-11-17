import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataPipeline:
    def __init__(self):
        self.csv_path = "../dati/raw_data.csv"
        self.clean_csv_path = "../dati/clean_data.csv"
        self.output_scaterplot = "../visual/scatter_plot.png"
        self.output_lineplot = "../visual/line_plot.png"
        self.output_histplot = "../visual/hist_plot.png"
        self.output_boxplot = "../visual/box_plot.png"
        self.output_heatmap = "../visual/heatmap.png"
        

    def caricamento_dati(self) -> pd.DataFrame:
        #caricamento dati da file.csv locale
        df = pd.read_csv(self.csv_path)
        return df
    
    def salvataggio_dati(self, df:pd.DataFrame) -> None:
        # salvataggio dati  su un file csv locale
        df.to_csv(self.clean_csv_path, index=False)  
                # df.to_csv(...) scrive il DataFrame su file CSV.
                # index=False -> evito la colonna extra dell’indice nel CSV.
    
    def preprocessamento_dati(self, df:pd.DataFrame) -> pd.DataFrame:
        # pulizia e preparazione dati
            # Creo una nuova colonna ("is_healthy") usando condizioni sulle altre colonne → tipico uso pandas.
        
        # df["is_healthy"] = (df["screen_time_hours"] < 5) & (df["sleep_hours"] >= 8)
        
        cond_basso_screen: pd.Series = df["screen_time_hours"] < 5
        cond_buon_sonno: pd.Series = df["sleep_hours"] >= 8

        mask_healthy: pd.Series = cond_basso_screen & cond_buon_sonno

        df["is_healthy"] = mask_healthy  # nuova colonna

        # Cos’è una mask? "filtro booleano"
        #     È una Series di valori True/False che “maschera” le righe di un DataFrame,
        #     cioè dice quali righe devono essere visibili o selezionate
        
        self.salvataggio_dati(df)
        return  df

    def visualizzazione_dati(self, df:pd.DataFrame) -> None:

# visualizzazione dati matplotlib

    #     plt.figure(figsize=(10, 6))  # creo la “tela”

    #     mask_Sani:pd.Series = df["is_healthy"] == True
    #     mask_nonSani:pd.Series = df["is_healthy"] == False  # ~df["is_healthy"]   # NOT logico

    # # creo sotto-DataFrame con mask booleana
    #     df_Sani:pd.DataFrame = df[mask_Sani]  # df[condizione] è il filtro di righe (subset) del DataFrame.
    #     df_nonSani:pd.DataFrame = df[mask_nonSani] 
        
    #     x_sani:pd.Series = df_Sani["screen_time_hours"]
    #     y_sani:pd.Series = df_Sani["math_score"]

    #     x_nonSani:pd.Series = df_nonSani["screen_time_hours"]
    #     y_nonSani:pd.Series = df_nonSani["math_score"]

    # # disegno punti (x,y)
    #     plt.scatter(
    #         x_sani, 
    #         y_sani, 
    #         color="green", 
    #         label="Vero"
    #         )
    #     plt.scatter(
    #         x_nonSani, 
    #         y_nonSani, 
    #         color="red", 
    #         label="Falso"
    #         )

    # # etichetta asse
    #     plt.xlabel("Screen time hours")
    #     plt.ylabel("Math score")

    #     plt.title("Screen time hours & math score")

    # # mostra la leggenda (tabella di riferimento dei colori)
    #     plt.legend()

    #     plt.savefig(self.output_plot)

    # # chiudi figura (libera memoria)
    #     plt.close()

# visualizzazione dati seaborn

        

        plt.xlabel("Screen time hours")
        plt.ylabel("Math score")

        plt.title("Screen time hours & math score")

    # Grafico a punti (relazione tra due variabili)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df, 
            x="screen_time_hours", 
            y="math_score", 
            hue="is_healthy" # hue="<colonna>" -> dividi i punti in base a questa colonna (True/False) — e colora automaticamente
            )
        plt.savefig(self.output_scaterplot)
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=df, 
            x="screen_time_hours", 
            y="math_score", 
            hue="is_healthy" 
            )        
        plt.savefig(self.output_lineplot)
        plt.close()

        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=df, 
            x="screen_time_hours", 
            y="math_score", 
            hue="is_healthy" 
            )
        plt.savefig(self.output_histplot)
        plt.close()
                
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            data=df, 
            x="screen_time_hours", 
            y="math_score", 
            hue="is_healthy" 
            )
        plt.savefig(self.output_boxplot)
        plt.close()
        
    # per il momento non capisco !!!!!!!!!
        # plt.figure(figsize=(10, 6))
        # sns.heatmap(
        #     data=df, 
        #     x="screen_time_hours", 
        #     y="math_score", 
        #     hue="is_healthy" 
        #     )
        # plt.savefig(self.output_heatmap)
        # plt.close()

        # plt.legend()  -> non c'è bisogno 



    def esegui_pipeline(self) -> None:
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
    pipeline.esegui_pipeline()
    print("Pipline completata con sucesso")
    

    