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
        # # # ESERCIZIO 1
        # # Aggiungere al dataset una colonna 'Total" contenente il fatturato totale prodotto da ogni nazione in tutti i 30 anni 
        df['Total'] = df[self.years].sum(axis=1)
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
        plt.savefig("../../visual/rev/plot_line_1.png")
        plt.show()
        plt.close()    


        # # # ESERCIZIO 2
        # # Andamento fatturato solo da diverse nazioni (es. Italy, France, Germany)
        df.index = df["Country"]
        rev_parz = df.loc[['Italy','France','Germany'], self.years]
        rev_new = rev_parz.transpose().plot(kind='line')
        title ="Andamento faturato per Italia, France, Germany"
        plt.title(title)
        plt.ylabel("anni")
        plt.ylabel("fatturato")
        plt.savefig("../../visual/rev/es_2_plot_line_1.png")
        plt.show()
        plt.close()
        
        # # Andamento fatturato per decadi (es. 95-04, 05-14, 15-24)     
        dec_95_04 = [str(x) for x in range(1995, 2005)]  
        dec_05_14 = [str(x) for x in range(2005, 2015)]  
        dec_15_24 = [str(x) for x in range(2015, 2025)]  
        rev_d1 = df.loc[:,dec_95_04].sum(axis=0).sum()
        rev_d2 = df.loc[:,dec_05_14].sum(axis=0).sum()
        rev_d3 = df.loc[:,dec_15_24].sum(axis=0).sum()
        valori = [rev_d1, rev_d2, rev_d3]
        decadi = ["1995-2004", "2005-2014", "2015-2024"]
        plt.figure(figsize=(10,5))
        plt.bar(decadi, valori, color=['red','blue', 'green'])
        plt.title('Fatturato per decade')
        plt.xlabel('Decadi')
        plt.ylabel('Fatturato')
        plt.savefig("../../visual/rev/es_2_plot_line_2.png")
        plt.show()
        plt.close()

        
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

        # # # ESERCIZIO 3
        # # Mostra andamento fatturato da Cina ordinato in senso decrescente       
        china2 = china.sort_values(ascending= False)
        plt.figure(figsize=(10,5))
        china2.plot(kind='bar', color='green')
        plt.title('Andamento per Cina')
        plt.xlabel('Anno')
        plt.ylabel('Fatturato')
        plt.savefig("../../visual/rev/es_3_bar.png")
        plt.show()
        plt.close()


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
        
        # # # ESERCIZIO 4
        # # Migliora l'aspetto della torta per renderla più leggibile (studia API)
        # # Inserisci in una stessa figura la torta per il 1995 e quella per il 2024 per osservare agevolmente le differenze 
        df_region_24 = df.groupby(['Region']).agg({'2024': 'sum'})
        fig, (ax1, ax2) =plt.subplots(2,1)
        ax1.pie(
            df_region_95['1995'],
            labels = df_region_95.index,
            autopct='%1.1f%%',
            startangle=90
        )
        ax1.set_title("1995")
        ax2.pie(
            df_region_24['2024'],
            labels = df_region_24.index,
            autopct='%1.1f%%',
            startangle=90
        )
        ax2.set_title("2024")
        plt.tight_layout() # per non sovraporrere
        plt.savefig("../../visual/rev/es_4_doppio_pie.png")
        plt.show()
        plt.close()      


        print("      -Pie chart salvato e mostrato")          

    def visualize_data(self, df:pd.DataFrame) -> None:
        df.index = df["Country"]
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))
        # plot line
        rev_tot = df.loc[:, self.years].sum(axis=0)
        ax1.plot(self.years, rev_tot)
        ax1.set_title('Andatento totale')
        ax1.set_xlabel('Anni')
        ax1.set_ylabel('Fatturato')
        # bar
        china = df.loc["China", self.years]
        ax2.bar(self.years, china)
        ax2.set_title("Fatturato Cina")
        ax2.set_xlabel("Anni")
        ax2.set_ylabel("Valori")
        # pie
        df_region_95 = df.groupby("Region").agg({"1995": "sum"})
        ax3.pie(
        df_region_95["1995"],
        labels=df_region_95.index,
        autopct='%1.1f%%',
        startangle=90
        )
        ax3.set_title("Percentuale regioni (1995)")

        plt.tight_layout()
        plt.savefig("../../visual/rev/es_5_tripla_ax.png")
        plt.show()
        plt.close()


               
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
        self.visualize_data(df_rev)
        print("   -Terminata visualizzazione risultati di analisi")        
        self.data = df_rev
        return df_rev

        # # # ESERCIZIO 5
        # # Aggiungi alla run_pipeline la chiamata ad una funzione "visualize_data" che generi un'unica immagine con plot line, bar chart e pie chart(s) 
        
if __name__ == "__main__":
    config = DataSourceConfig()
    pipeline = DataPipeline(config)

    # # carico
    # df1 = pipeline.load_from_csv()
    # # print(df1.dtypes)
    # print(df1.head())
    
    # # pulizia
    # df_clean = pipeline.clean_data(df1)
    # print(df_clean.head())

    # pipeline.visualize_plot(df1)
    # pipeline.visualize_bar(df1)
    # pipeline.visualize_pie(df1)


    print("Pipeline avviata...")
    final_df = pipeline.run_pipeline()
    print("Pipeline completata con successo!")
    # print(final_df.head())