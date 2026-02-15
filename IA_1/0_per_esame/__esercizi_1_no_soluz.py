import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError 

# csv_clean_path: str = "../../dati/autos/auto_clean.csv"
# # df = pd.read_csv(csv_clean_path)
# print(df9.head())

# Esercizio 1: Connessione con SQLAlchemy
# Task: Write code to store the df DataFrame on a SQLite table named cars using SQLAlchemy. Handle errors gracefully (print a message if it fails).
# Soluzione:
print("***ESERCIZIO 1***")
df = pd.read_csv('./auto_clean.csv')
print(df.head())
url_db = "sqlite:///cars.db"
table_name = "Cars"
engine = create_engine("sqlite:///cars.db")
try:
    with engine.begin() as conn:
        df.to_sql(table_name, con=conn, if_exists='replace', index=True)
except SQLAlchemyError as e:
    print(' ups')
finally:
    engine.dispose()
print("*****************"+"\n")
 
### Esercizio 2: Reading SQL Data 
### Task:  Query the cars table to load rows where fuel-type is "gas" into a new DataFrame df_gas 
### Soluzione:
print("***ESERCIZIO 2***")
query = "SELECT * FROM cars WHERE `fuel-type` = 'gas'"
try:
    with engine.begin() as conn:
        df = pd.read_sql(text(query), conn)
except SQLAlchemyError as e:
    print('ups')
finally:
    engine.dispose()

print("*****************"+"\n")
 
### Esercizio 3: Replacing Missing Values
### Task: Replace missing values (NaN) in the price column with the column’s median
### Soluzione:
print("***ESERCIZIO 3***")
avg = df['price'].mean()
df['price'] = df['price'].fillna(avg)
print("*****************"+"\n")

## Esercizio 4: Most Frequent Value
## Task: Replace NaN values in num-of-doors with the most frequent door count
## Soluzione:
print("***ESERCIZIO 4***")
fr = df['num-of-doors'].value_counts().idxmax()
df['num-of-doors'] = df['num-of-doors'].fillna(fr)
print("*****************"+"\n")
 
### Esercizio 5: Normalisation
### Task: Normalise the horsepower column (convert to numeric first) to a 0-1 range
### Soluzione:
print("***ESERCIZIO 5***")
df['horsepower'] = pd.to_numeric(df['horsepower'])
print("*****************"+"\n")

### Esercizio 6: Clipping Outliers
### Task:  Clip values in city-mpg to the 10th and 90th percentiles
### Soluzione:
print("***ESERCIZIO 6***")
lower, upper = df['city-mpg'].quantile([0.1, 0.9])
df['city-mpg'] = df['city-mpg'].clip(lower, upper)
print("*****************"+"\n")
 
### Esercizio 7: Dropping Rows
### Task:  Drop all rows where both price and horsepower are NaN
### Soluzione:
print("***ESERCIZIO 7***")
df.dropna(subset=['price', 'horsepower'], how='all', inplace=True)
print("*****************"+"\n")
  
### Esercizio 8: Merging DataFrames
### Task: Merge df with a new DataFrame df_extra (columns: make, safety-rating) on the make column. Keep only matching rows
### Soluzione:
print("***ESERCIZIO 8***")
print(df.dtypes)
df = df.convert_dtypes()
print(df.dtypes)
df_3 = pd.DataFrame({'make':['audi'],  "safety-rating": [8]})

df_3 = df_3.convert_dtypes()
print(df_3.dtypes)

df_merdge = pd.merge(df, df_3, on='make', how='inner')
print(df_merdge.head(3))
print("*****************"+"\n")

### Esercizio 9: Complex Cleaning
### Task: For normalized-losses:
###       Replace missing values (? or NaN) with np.nan.
###       Fill remaining NaN with the mean.
###       Convert to float64.
### Soluzione:
print("***ESERCIZIO 9***")
df['normalized-losses']=df['normalized-losses'].replace('?', np.nan)
avg = df['normalized-losses'].mean()
df['normalized-losses'] = df['normalized-losses'].fillna(avg)
df['normalized-losses'] = df['normalized-losses'].astype('float64')
print("******************"+"\n")

