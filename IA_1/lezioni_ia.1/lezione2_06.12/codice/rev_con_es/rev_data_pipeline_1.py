import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataSourceConfig:
    """Configurazione sorgenti dati e destinazione output"""
    csv_path: str = "../../dati/rev/cl_company_intnl_revenues.csv"
    output_plot_line: str = "../../visual/rev/plot_line.png"
    output_plot_bar: str = "../../visual/rev/plot_bar.png"
    output_plot_pie: str = "../../visual/rev/plot_pie.png"
    output_plot_area: str = "../../visual/rev/plot_area.png"
    output_plot_hist: str = "../../visual/rev/plot_hist.png"
    output_plot_box: str = "../../visual/rev/plot_box.png"
    output_plot_scatter: str = "../../visual/rev/plot_scatter.png"
    output_plot_figure: str = "../../visual/rev/plot_figure.png"
    
class DataPipeline:
    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.years = list(map(str, range(1995, 2025)))
        self.first_decade = list(map(str, range(1995, 2005))) 
        self.second_decade = list(map(str, range(2005, 2015))) 
        self.third_decade = list(map(str, range(2015, 2025)))  
        self.data = None
        
    def load_from_csv(self) -> pd.DataFrame:
        """Carica dati da un file CSV"""
        return pd.read_csv(self.config.csv_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Operazioni varie di pulizia e pre-processamento dati"""
        # # ESERCIZI
        # Aggiungere al dataset una colonna 'Total" contenente il fatturato totale prodotto da ogni nazione in tutti i 30 anni 
        df['Total'] = df.select_dtypes(include=np.number).sum(axis=1)       
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

        # # # ESERCIZI
        # # Andamento fatturato solo da diverse nazioni (es. Italy, France, Germany)
        # big_eu =  df.loc[['Italy','France','Germany'] , self.years]
        # plt.subplots(figsize=(20, 12))
        # big_eu.transpose().plot()
        # # Andamento fatturato per decadi (es. 95-04, 05-14, 15-24)
        # df_first_dec = df.loc[:, self.first_decade]
        # # print(df_first_dec)
        # df_first_dec.rename(columns={'1995':'1', '1996':'2', '1997':'3', '1998':'4', '1999':'5', '2000':'6',
        #                    '2001':'7', '2002':'8', '2003':'9', '2004':'10'}, inplace=True)
        # rev_first_dec = df_first_dec.sum(axis=0)
        # # print(rev_first_dec)
        # df_second_dec = df.loc[:, self.second_decade]
        # df_second_dec.rename(columns={'2005':'1', '2006':'2', '2007':'3', '2008':'4', '2009':'5', '2010':'6',
        #                    '2011':'7', '2012':'8', '2013':'9', '2014':'10'}, inplace=True)
        # rev_second_dec = df_second_dec.sum(axis=0)
        # df_third_dec = df.loc[:, self.third_decade]   
        # df_third_dec.rename(columns={'2015':'1', '2016':'2', '2017':'3', '2018':'4', '2019':'5', '2020':'6',
        #                    '2021':'7', '2022':'8', '2023':'9', '2024':'10'}, inplace=True)
        # rev_third_dec = df_third_dec.sum(axis=0)
        # data = {"1995-2004":rev_first_dec, "2005-2014":rev_second_dec, "2015-2024":rev_third_dec} 
        # new_df = pd.concat(data, axis=1)
        # # print(new_df)
        # # rev_first_dec.plot(kind="line", color='green')
        # # rev_second_dec.plot(kind="line", color='orange')
        # # rev_third_dec.plot(kind="line", color='red')
        # new_df.plot(kind="line")
        # title = "Fatturato totale - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale - ds"
        # ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        # plt.title(title)
        # plt.ylabel(ylabel)
        # plt.xlabel('Anni')   

        plt.savefig(self.config.output_plot_line)
        plt.show()
        plt.close()         
        
        print("      -Line plot salvato e mostrato")

    def visualize_bar(self, df_in: pd.DataFrame) -> None:        
        """Crea e visualizza un Bar chart"""
        df = df_in.reset_index(drop=True).copy()   
        df.index = df['Country']

        # Andamento fatturato da diversi paesi       
        plt.subplots(figsize=(10, 6))  
        br = df.loc['Brazil', self.years]
        br.plot(kind='bar', color='red')
        china = df.loc['China', self.years]
        china.plot(kind='bar', color='blue')
        plt.title('Fatturato da Brasile e Cina - Anni: 1995-2024')
        plt.ylabel('Fatturato')
        plt.xlabel('Anni')

        # # # ESERCIZI
        # # Mostra andamento fatturato da Cina ordinato in senso decrescente
        # china = df.loc['China', self.years]
        # # print(china)
        # china.sort_values(ascending=False, axis=0, inplace=True)
        # # print(china)
        # china.plot(kind='bar', color='blue')
        # plt.title('Fatturato da Cina in senso decrescente')
        # plt.ylabel('Fatturato')
        # plt.xlabel('Anni')
        
        plt.savefig(self.config.output_plot_bar)        
        plt.show()
        plt.close() 
       
        print("      -Bar chart salvato e mostrato")        
        
    def visualize_pie(self, df_in: pd.DataFrame) -> None:        
        """Crea e visualizza un Pie chart"""
        df = df_in.reset_index(drop=True).copy()
        df_region_95 = df.groupby(['Region']).agg({'1995': 'sum'})
        # print(df_region_95.shape)
        # colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen'] # OCCHIO che sia  
        # print(len(colors_list))
        
        plt.figure(figsize=(20, 10))
        df_region_95['1995'].plot(kind='pie',
                            autopct='%1.1f%%',
                            startangle=90,
                            labels=None,
                            pctdistance=1.07,
                            shadow=False,
                            )
        plt.title('Percentuale fatturato per regione geografica (1995)')
        plt.ylabel("")
        plt.axis('equal')
        plt.legend(labels=df_region_95.index, loc='lower left') 
        
        # # # ESERCIZI
        # # Migliora l'aspetto della torta per renderla più leggibile (studia API)
        # if self.config.csv_path.__contains__("cl"):
        #     colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen']  
        #     explode_list = [0, 0, 0.05, 0.05, 0.05]       
        #     df_region_95['1995'].plot(kind='pie',
        #                                 autopct='%1.1f%%', 
        #                                 startangle=90,    
        #                                 shadow=True,       
        #                                 labels=None,        
        #                                 pctdistance=1.07, 
        #                                 colors=colors_list,
        #                                 explode=explode_list 
        #                                 )
        #     plt.title('Percentuale fatturato per regione geografica (1995) - cl')
        #     plt.ylabel("")
        #     plt.axis('equal')
        #     plt.legend(labels=df_region_95.index, loc='lower left') 
        # else:
        #     colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'tan']  
        #     explode_list = [0.05, 0, 0, 0, 0.05, 0.05]       
        #     df_region_95['1995'].plot(kind='pie',
        #                                 autopct='%1.1f%%', 
        #                                 startangle=90,    
        #                                 shadow=True,       
        #                                 labels=None,        
        #                                 pctdistance=1.07, 
        #                                 colors=colors_list,
        #                                 explode=explode_list 
        #                                 )
        #     plt.title('Percentuale fatturato per regione geografica (1995) - ds')
        #     plt.ylabel("")
        #     plt.axis('equal')
        #     plt.legend(labels=df_region_95.index, loc='lower left') 
        # # Inserisci in una stessa figura la torta per il 1995 e quella per il 2024 per osservare agevolmente le differenze 
        # plt.figure(figsize=(26, 13))
        # df_region_24 = df.groupby(['Region']).agg({'2024': 'sum'})
        # plt.subplot(1, 2, 1)
        # df_region_95['1995'].plot(kind='pie',
        #                     autopct='%1.1f%%',
        #                     startangle=90,
        #                     labels=None,
        #                     pctdistance=1.10,
        #                     shadow=False,
        #                     )
        # plt.title('Percentuale fatturato per regione geografica (1995)')
        # plt.ylabel("")
        # plt.axis('equal')
        # plt.legend(labels=df_region_95.index, loc='lower left') 
        
        # plt.subplot(1, 2, 2)
        # df_region_24['2024'].plot(kind='pie',
        #                     autopct='%1.1f%%', 
        #                     startangle=90,     
        #                     labels=None,
        #                     pctdistance=1.07,
        #                     shadow=False,
        #                     )
        # plt.title('Percentuale fatturato per regione geografica (2024)')
        # plt.ylabel("")
        # plt.axis('equal')
        # plt.legend(labels=df_region_24.index, loc='lower left') 
        
        plt.savefig(self.config.output_plot_pie)        
        plt.show()
        plt.close()
        
        print("      -Pie chart salvato e mostrato") 

    def visualize_area(self, df_in: pd.DataFrame) -> None:
        """Crea e visualizza un Area plot"""
        df = df_in.reset_index(drop=True).copy()
        
        df.sort_values(['Total'], ascending=False, axis=0, inplace=True)
        df.index = df['Country']
        df_top5 = df.head(5)
        print(df_top5)
        df_top5 = df_top5[self.years].transpose() 
        # print(df_top5.head())
        
        # SOLUZIONE "pandas only"
        df_top5.plot(kind="area", figsize=(14, 8)).get_figure().savefig(self.config.output_plot_area)
        
        # # SOLUZIONE "pandas+Artist"
        # # ax = df_top5.plot(kind='area', alpha=0.35, figsize=(20, 9))
        # # ax = df_top5.plot(kind='area', alpha=0.10, stacked=False, figsize=(20, 9))
        # ax = df_top5.plot(kind='line', figsize=(20, 9))
        # # Notazione compatta if-then-else: value_if_true if condition else value_if_false        
        # title = "Fatturato: primi 5 paesi per importo totale - cl" if self.config.csv_path.__contains__("cl") else "Fatturato: primi 5 paesi per importo totale - ds"
        # ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        # ax.set_title(title)
        # ax.set_ylabel(ylabel)
        # ax.set_xlabel('Anni')
        # ax.figure.savefig(self.config.output_plot_area) 
        
        # # ESERCIZI
        # 1) Mostra il fatturato cumulativo anno per anno nei 30 anni coi diversi contributi SOLO delle prime 
        #    5 sottoregioni per fatturato totale dei tre anni 1999, 2000, 2001
        # 2) Confronta il fatturato cumulativo calcolato come al punto uno per il triennio 1995, 1996, 1997 ed 
        #    il triennio 2022, 2023, 2024. Cosa osservi?

        print("      -Area plot salvato e mostrato") 
        
    def visualize_hist(self, df_in: pd.DataFrame) -> None:      
        """Crea e visualizza un Istogramma"""
        df = df_in.reset_index(drop=True).copy()
        
        # print(df.sort_values(['2024'], ascending=False)[['Country', '2024']])
        # count, bin_edges = np.histogram(df['2024'], bins=5)        
        # print(count) # conteggio frequenze, mumero paesi in ogni intervallo 
        # print(bin_edges) # intervalli (bins), default = 10, 
        # #                  # dim di ogni bin = (df['2024'].max() - df['2024'].min()) / numero intervalli (bins)
        # # df['2024'].plot(kind='hist', figsize=(8, 5))
        # df['2024'].plot(kind='hist', figsize=(8, 5), xticks=bin_edges, color='green')
              
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.hist(df['2024'], bins=10, color='green', edgecolor='white')
        # print(type(bars))
        # print(bars)
        print(bars[1])
        print(bars[2])
        plt.bar_label(bars[2], fontsize=10, color='navy')
        # plt.xticks(bars[1])
        plt.xticks(bars[1], rotation=45)
        
        # # ESERCIZI
        # 1) Scrivere il codice per generare gli istogrammi delle slide 13, 14, 15 in IA.1_Lezione2.3.pdf 
        # 2) Cambiare paesi, osservare i diversi trend e rifletterci un po' su 

        title = "Fatturato da tutti i paesi nel 2024 - cl" if self.config.csv_path.__contains__("cl") else "Fatturato da tutti i paesi nel 2024 - ds"
        xlabel = "Fatturato (milioni di USD)" if self.config.csv_path.__contains__("cl") else "Fatturato (USD)" 
        plt.title(title)
        plt.ylabel('Numero di Paesi') 
        plt.xlabel(xlabel)  
        plt.tight_layout()       

        plt.savefig(self.config.output_plot_hist)        
        plt.show()
        plt.close()

        print("      -Istogramma mostrato e salvato")
        
    def visualize_boxplot(self, df_in: pd.DataFrame) -> None:
        """Crea e visualizza un Box plot"""
        df = df_in.reset_index(drop=True).copy() 

        df.set_index('Country', inplace=True)
        country_name = "India"
        country = df.loc[country_name, self.years]
        print(country)
        country = pd.DataFrame(df.loc[country_name, self.years])
        country[[country_name]] = country[[country_name]].astype("float")       
        # print(country)
        print()
        print(country.describe())
        country = country.reset_index()
        country_outlier_up_value = country.describe().loc['75%'][country_name] + 1.5 * (country.describe().loc['75%'][country_name] - country.describe().loc['25%'][country_name])
        print()
        print("Q3 + 1.5*IQR = " + str(country_outlier_up_value))
        print()
        print("Upper whisker (baffo superiore): " + str(country[country[country_name] < country_outlier_up_value][country_name].max()))
        print()
        country.plot(kind='box', figsize=(10, 6))
        title = "Fatturato " + str(country_name) + " - cl" if self.config.csv_path.__contains__("cl") else "Fatturato " + str(country_name) + " - ds"
        plt.title(title)
        
        # df_top = df.sort_values(['Total'], ascending=False, axis=0).head(15)
        # print(df_top["Country"])
        # df_first_dec = df_top.loc[:, self.first_decade].sum(axis=1) 
        # df_second_dec = df_top.loc[:, self.second_decade].sum(axis=1) 
        # df_third_dec = df_top.loc[:, self.third_decade].sum(axis=1)         
        # new_df = pd.DataFrame({'95-04': df_first_dec, '05-14': df_second_dec, '15-24':df_third_dec}) 
        # print(new_df)
        # print(new_df.describe())
        # # # print(new_df.head())
        # outlier_up_value_first_dec = new_df.describe().loc['75%']['95-04'] + 1.5 * (new_df.describe().loc['75%']['95-04'] - new_df.describe().loc['25%']['95-04'])
        # # print(outlier_up_value_first_dec)
        # outlier_up_value_second_dec = new_df.describe().loc['75%']['05-14'] + 1.5 * (new_df.describe().loc['75%']['05-14'] - new_df.describe().loc['25%']['05-14'])
        # # print(outlier_up_value_second_dec)  
        # outlier_up_value_third_dec = new_df.describe().loc['75%']['15-24'] + 1.5 * (new_df.describe().loc['75%']['15-24'] - new_df.describe().loc['25%']['15-24'])
        # # print(outlier_up_value_third_dec)
        # print()
        # print("Q3 + 1.5*IQR") 
        # print("       " + str(outlier_up_value_first_dec.round(3)))
        # print("                    " + str(outlier_up_value_second_dec.round(3)))
        # print("                                 " + str(outlier_up_value_third_dec.round(3)))

 
        # new_df.plot(kind='box', figsize=(10, 6))
        # title = "Fatturato dalle prime 15 nazioni nei decenni 95-04, 05-14 e 15-24 - cl" if self.config.csv_path.__contains__("cl") else "Fatturato dalle prime 15 nazioni nei decenni 95-04, 05-14 e 15-24 - ds"
        # plt.title(title)
       
        # new_df = new_df.reset_index()
        # print(new_df)
        # filter_series_95_04 = new_df[new_df['95-04'] > outlier_up_value_first_dec]["index"]
        # filtered_df_95_04 = df_top.loc[df_top.index.isin(filter_series_95_04.values)][["Country"]]
        # print(filtered_df_95_04)
        # filter_series_05_14 = new_df[new_df['05-14'] > outlier_up_value_second_dec]["index"]
        # filtered_df_05_14 = df_top.loc[df_top.index.isin(filter_series_05_14.values)][["Country"]]
        # print(filtered_df_05_14)        
        # filter_series_15_24 = new_df[new_df['15-24'] > outlier_up_value_third_dec]["index"]
        # filtered_df_15_24 = df_top.loc[df_top.index.isin(filter_series_15_24.values)][["Country"]]
        # print(filtered_df_15_24)      
        
        plt.savefig(self.config.output_plot_box)
        plt.show()
        plt.close()        
        
        print("      -Box plot mostrato e salvato")  
        
    def visualize_scatter(self, df_in: pd.DataFrame) -> None:
        
        def compute_equation(c: np.ndarray) -> str:
            output = "y = "
            for i in range(0, c.shape[0]):
                if (i < c.shape[0] - 1):
                    if (c.shape[0] - i - 1 > 1):
                        output += str(c[i]) + "$x^{" + str(c.shape[0] - i - 1) + "}$ + "
                    else:
                        output += str(c[i]) + "x + "
                else:
                    output += str(c[i])                   
            return output

        def add_columns(df: pd.DataFrame) -> pd.DataFrame:
            df["employees"]  = np.random.uniform(10, 100, 30).round(0)
            df["employees"]  = df["employees"].astype(int)
            shifts = np.array(['all_day', 'morning', 'night'])
            df["shift"]  = np.nan
            df["shift"] = df["shift"].apply(
                lambda x: np.random.choice(shifts) if pd.isna(x) else x
            )
            return df
                     
        """Crea e visualizza uno Scatter plot"""
        df = df_in.reset_index(drop=True).copy()
        
        df_tot = pd.DataFrame(df[self.years].sum(axis=0))
        df_tot.index = map(int, df_tot.index)
        df_tot.reset_index(inplace = True)
        df_tot.columns = ['year', 'total']
        # print(df_tot)

        plt.figure(figsize=(10, 6))
        # df_tot.plot(kind='scatter', x='year', y='total', color='darkblue')
        plt.scatter(df_tot['year'], df_tot['total'], color='darkblue')
        title = "Fatturato totale per anno [1995 - 2024] - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale per anno [1995 - 2024] - ds"        
        ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        plt.title(title) 
        plt.xlabel('Anno')
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)

        # fig, ax = plt.subplots()
        # # ax = df_tot.plot(kind='scatter', x='year', y='total', color='darkblue')
        # ax.scatter(df_tot['year'], df_tot['total'], color='darkblue')
        # title = "Fatturato totale per anno [1995 - 2024] - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale per anno [1995 - 2024] - ds"        
        # ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        # ax.set_title(title)
        # ax.set_xlabel('Anno')
        # ax.set_ylabel(ylabel)  
        # plt.xticks(rotation=45)

        # df_tot = add_columns(df_tot)   
        # # print(df_tot) 
        # plt.figure(figsize=(10, 6))
        # sns.scatterplot(data=df_tot, x="year", y="total", hue="shift", size="employees")        
        # title = "Fatturato totale per anno [1995 - 2024] - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale per anno [1995 - 2024] - ds"        
        # ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
        # plt.title(title) 
        # plt.xlabel('Anno')
        # plt.ylabel(ylabel)
        # plt.xticks(rotation=45)
        
        # # Fit linear regressions 
        # x = df_tot['year']
        # y = df_tot['total']   
        # coefficients = np.polyfit(x, y, 1)
        # p = np.poly1d(coefficients)
        # plt.plot(x, p(x), color='red')        
        # plt.rcParams['text.usetex'] = False
        # equation = compute_equation(coefficients)
        # plt.annotate(equation, xy=(0.02, 0.95), xycoords='axes fraction', fontsize=6)
        # # ax.annotate(equation, xy=(0.05, 0.95), fontsize=14)          
            
        plt.savefig(self.config.output_plot_scatter)
        plt.show()
        plt.close()               
                
        print("      -Scatter plot mostrato e salvato")          

    # # # ESERCIZI
    # # Aggiungi alla run_pipeline la chiamata ad una funzione "visualize_data" che generi un'unica immagine con plot line, bar chart e pie chart(s) 
    # def visualize_data(self, df_in: pd.DataFrame) -> None:
    #    """Crea e salva visualizzazioni"""
    #    df = df_in.reset_index(drop=True).copy()
       
    #    plt.figure(figsize=(30, 15))
         
    #    plt.subplot(1, 3, 1)
    #    df.index = df['Country']  
    #    # Andamento fatturato totale sui trent'anni
    #    rev_tot = df.loc[:, self.years].sum(axis=0)
    #    rev_tot.plot(kind="line")       
    #    title = "Fatturato totale - cl" if self.config.csv_path.__contains__("cl") else "Fatturato totale - ds"
    #    ylabel = "milioni di USD" if self.config.csv_path.__contains__("cl") else "USD"
    #    plt.title(title)
    #    plt.ylabel(ylabel)
    #    plt.xlabel('Anni')      
           
    #    plt.subplot(1, 3, 2)
    #    df.index = df['Country']  
    #    china = df.loc['China', self.years]
    #    china.plot(kind='bar', color='blue')
    #    br = df.loc['Brazil', self.years]
    #    br.plot(kind='bar', color='red')
    #    plt.title('Fatturato da Brasile e Cina - Anni: 1995-2024')
    #    plt.ylabel('Fatturato')
    #    plt.xlabel('Anni')
           
    #    plt.subplot(1, 3, 3)
    #    df_region_95 = df.groupby(['Region']).agg({'1995': 'sum'})
    #    df_region_95['1995'].plot(kind='pie',
    #                   autopct='%1.1f%%',
    #                   startangle=90,
    #                   labels=None,
    #                   pctdistance=1.07,
    #                   shadow=False,
    #                   )
    #    plt.title('Percentuale fatturato per regione geografica (1995)')
    #    plt.ylabel("")
    #    plt.axis('equal')
    #    plt.legend(labels=df_region_95.index, loc='lower left') 
                
    #    plt.tight_layout()           
    #    plt.savefig(self.config.output_plot_figure)
    #    plt.show()
    #    plt.close()
               
    def run_pipeline(self) -> pd.DataFrame:
        """Esegue la pipeline completa"""
        # Carica dati da locale
        df_rev = self.load_from_csv()
        print("   -Letto file locale")
        # Pulizia e pre-processamento dati
        df_rev = self.clean_data(df_rev)
        # Visualizzazione dati
        # self.visualize_plot(df_rev)
        # self.visualize_bar(df_rev)
        # self.visualize_pie(df_rev)
        self.visualize_area(df_rev)
        self.visualize_hist(df_rev)
        # self.visualize_boxplot(df_rev)
        # self.visualize_scatter(df_rev) 
        # self.visualize_data(df_rev)        
        print("   -Terminata visualizzazione risultati di analisi")        
        self.data = df_rev
        return df_rev    
        
if __name__ == "__main__":
    config = DataSourceConfig()
    pipeline = DataPipeline(config)
    print("Pipeline avviata...")
    final_df = pipeline.run_pipeline()
    print("Pipeline completata con successo!")
    # print(final_df.head())
