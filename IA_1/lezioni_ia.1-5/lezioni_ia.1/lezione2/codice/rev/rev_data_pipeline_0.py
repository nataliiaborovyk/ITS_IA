import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataSourceConfig:
    """Configurazione sorgenti dati e destinazione output"""
    csv_path: str = "../../dati/rev/cl_company_intnl_revenues.csv"
    output_plot_line: str = "../../visual/rev/plot_line.png"
    output_plot_bar: str = "../../visual/rev/plot_bar.png"
    output_plot_pie: str = "../../visual/rev/plot_pie.png"
    
class DataPipeline:
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.years = list(map(str, range(1995, 2025)))
        self.data = None
        
    def load_from_csv(self) -> pd.DataFrame:
        """Carica dati da un file CSV"""
        return pd.read_csv(self.config.csv_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Operazioni varie di pulizia e pre-processamento dati"""
        # # # ESERCIZI
        # # Aggiungere al dataset una colonna 'Total" contenente il fatturato totale prodotto da ogni nazione in tutti i 30 anni 
        return df

    def visualize_plot(self, df_in: pd.DataFrame) -> None:        
        """Crea e visualizza un Line plot"""
        df = df_in.reset_index(drop=True).copy()
        df.index = df['Country']  
        
        # Andamento fatturato totale sui trent'anni
        rev_tot = df.loc[:, self.years].sum(axis=0)
        rev_tot.plot(kind="line")       
        title = "Fatturato totale - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale - ds"
        ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel('Anni')
        plt.savefig(self.config.output_plot_line)
        plt.show()
        plt.close()    

        # # # ESERCIZI
        # # Andamento fatturato solo da diverse nazioni (es. Italy, France, Germany)
        # # Andamento fatturato per decadi (es. 95-04, 05-14, 15-24)           
        
        print("      -Line plot salvato e mostrato")

    def visualize_bar(self, df_in: pd.DataFrame) -> None:        
        """Crea e visualizza un Bar chart"""
        df = df_in.reset_index(drop=True).copy()   
        df.index = df['Country']

        # Andamento fatturato da diversi paesi       
        plt.subplots(figsize=(10, 6))         
        china = df.loc['China', self.years]
        china.plot(kind='bar', color='blue')
        br = df.loc['Brazil', self.years]
        br.plot(kind='bar', color='red')
        plt.title('Fatturato da Brasile e Cina - Anni: 1995-2024')
        plt.ylabel('Fatturato')
        plt.xlabel('Anni')
        plt.savefig(self.config.output_plot_bar)        
        plt.show()
        plt.close() 

        # # # ESERCIZI
        # # Mostra andamento fatturato da Cina ordinato in senso decrescente       
       
        print("      -Bar chart salvato e mostrato")        
        
    def visualize_pie(self, df_in: pd.DataFrame) -> None:        
        """Crea e visualizza un Pie chart"""
        df = df_in.reset_index(drop=True).copy()
        df_region_95 = df.groupby(['Region']).agg({'1995': 'sum'})
        
        plt.figure(figsize=(20, 10))
        df_region_95['1995'].plot(kind='pie',
                            autopct='%1.1f%%',
                            startangle=90,
                            labels=None,
                            pctdistance=1.07,
                            shadow=True,
                            )
        plt.title('Percentuale fatturato per regione geografica (1995)')
        plt.ylabel("")
        plt.axis('equal')
        plt.legend(labels=df_region_95.index, loc='lower right') 
        plt.savefig(self.config.output_plot_pie)        
        plt.show()
        plt.close()  
        
        # # # ESERCIZI
        # # Migliora l'aspetto della torta per renderla più leggibile (studia API)
        # # Inserisci in una stessa figura la torta per il 1995 e quella per il 2024 per osservare agevolmente le differenze 
        
        print("      -Pie chart salvato e mostrato")          
               
    def run_pipeline(self) -> pd.DataFrame:
        """Esegue la pipeline completa"""
        # Carica dati da locale
        df_rev = self.load_from_csv()
        print("   -Letto file locale")
        # Pulizia e pre-processamento dati
        df_rev = self.clean_data(df_rev)
        # Visualizzazione dati
        self.visualize_plot(df_rev)
        self.visualize_bar(df_rev)
        self.visualize_pie(df_rev)
        print("   -Terminata visualizzazione risultati di analisi")        
        self.data = df_rev
        return df_rev

        # # # ESERCIZI
        # # Aggiungi alla run_pipeline la chiamata ad una funzione "visualize_data" che generi un'unica immagine con plot line, bar chart e pie chart(s) 
        
if __name__ == "__main__":
    config = DataSourceConfig()
    pipeline = DataPipeline(config)
    print("Pipeline avviata...")
    final_df = pipeline.run_pipeline()
    print("Pipeline completata con successo!")
    # print(final_df.head())