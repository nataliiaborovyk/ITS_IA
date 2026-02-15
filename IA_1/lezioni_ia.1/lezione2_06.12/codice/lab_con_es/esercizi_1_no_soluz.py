import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError 

csv_clean_path: str = "../../dati/autos/auto_clean.csv"
df = pd.read_csv(csv_clean_path)
print(df.head())

# Esercizio 1: Connessione con SQLAlchemy
# Task: Write code to store the df DataFrame on a SQLite table named cars using SQLAlchemy. Handle errors gracefully (print a message if it fails).
# Soluzione:
print("***ESERCIZIO 1***")

url_db = "sqlite:///../../dati/lab/cars.db"
table_name = "Cars"
engine = create_engine(url_db)
try:
    with engine.begin() as conn:
        df.to_sql(table_name, con=conn, if_exists='replace', index=False)
except SQLAlchemyError as e:
    print(f"...ups, qualcosa non ha funzionato {e}")
finally:
    engine.dispose()
print("*****************"+"\n")


### Esercizio 2: Reading SQL Data 
### Task:  Query the cars table to load rows where fuel-type is "gas" into a new DataFrame df_gas 
### Soluzione:
print("***ESERCIZIO 2***")
query = "select * from cars where 'fuel-type'='gas' "
try:
    with engine.begin() as conn:
        df_n = pd.read_sql(text(query),conn)
except SQLAlchemyError as e:
    print(f"...ups, errore {e}")
finally:
    engine.dispose()

print("*****************"+"\n")
 
### Esercizio 3: Replacing Missing Values
### Task: Replace missing values (NaN) in the price column with the column’s median
### Soluzione:
print("***ESERCIZIO 3***")
median = df['price'].median()
df['price'] = df['price'].fillna(median)

print("*****************"+"\n")

## Esercizio 4: Most Frequent Value
## Task: Replace NaN values in num-of-doors with the most frequent door count
## Soluzione:
print("***ESERCIZIO 4***")
frequent = df['num-of-doors'].value_counts().idxmax()
df['num-of-doors'] =  df['num-of-doors'].fillna(frequent)
print("*****************"+"\n")
 
### Esercizio 5: Normalisation
### Task: Normalise the horsepower column (convert to numeric first) to a 0-1 range
### Soluzione:
print("***ESERCIZIO 5***")
print(df.dtypes)
df["horsepower"] = pd.to_numeric(df["horsepower"])
print(df.dtypes)
def normalize(s):
    return (s - s.min()) / (s.max() - s.min())
df["horsepower"] = normalize(df["horsepower"])
print("*****************"+"\n")

### Esercizio 6: Clipping Outliers
### Task:  Clip values in city-mpg to the 10th and 90th percentiles
### Soluzione:
print("***ESERCIZIO 6***")

val_10 = df["city-mpg"].quantile(0.10)
val_90 = df["city-mpg"].quantile(0.90)
df["city-mpg"] = df["city-mpg"].clip(lower=val_10, upper=val_90)

print("*****************"+"\n")
 
### Esercizio 7: Dropping Rows
### Task:  Drop all rows where both price and horsepower are NaN
### Soluzione:
print("***ESERCIZIO 7***")
df.dropna(subset=['price', 'horsepower'], how='all', inplace=True )

print("*****************"+"\n")
  
### Esercizio 8: Merging DataFrames
### Task: Merge df with a new DataFrame df_extra (columns: make, safety-rating) on the make column. Keep only matching rows
### Soluzione:
print("***ESERCIZIO 8***")
df_extra = pd.DataFrame({
    'make' : ['audi', 'bmw', 'subaru'],
    'safety-rating' : [3,4,5]
})
print(df_extra.dtypes)
df_new = pd.merge(df, df_extra, on='make', how='inner')
print(df_new.dtypes)
print("*****************"+"\n")

### Esercizio 9: Complex Cleaning
### Task: For normalized-losses:
###       Replace missing values (? or NaN) with np.nan.
###       Fill remaining NaN with the mean.
###       Convert to float64.
### Soluzione:
print("***ESERCIZIO 9***")
df['normalized-losses'] = df['normalized-losses'].replace('?', np.nan)
df['normalized-losses'] = pd.to_numeric(df['normalized-losses'])
avg2 = df['normalized-losses'].mean()
df['normalized-losses'] = df['normalized-losses'].fillna(avg2)
df['normalized-losses'] = df['normalized-losses'].astype('float64')
print("******************"+"\n")

