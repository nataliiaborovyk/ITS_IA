import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

csv_clean_path: str = "../../dati/autos/auto_clean.csv"
df = pd.read_csv(csv_clean_path)
print(df.head())

# Esercizio 1: Connessione con SQLAlchemy
# Task: Write code to store the df DataFrame on a SQLite table named cars using SQLAlchemy. Handle errors gracefully (print a message if it fails).
# Soluzione:
print("***ESERCIZIO 1***")
table_name = "Cars"
url='fsfs'
engine = create_engine(url)
with engine.begin() as conn:
    df.to_sql(table_name, con=conn, if_exists='replace', index=True)
print("*****************"+"\n")
 
### Esercizio 2: Reading SQL Data 
### Task:  Query the cars table to load rows where fuel-type is "gas" into a new DataFrame df_gas 
### Soluzione:
print("***ESERCIZIO 2***")
engine=create_engine(url)
with engine.begin() as conn:
    df = pd.read_sql(text('jfsajhf'), conn)
print("*****************"+"\n")
 
### Esercizio 3: Replacing Missing Values
### Task: Replace missing values (NaN) in the price column with the column’s median
### Soluzione:
print("***ESERCIZIO 3***")
df2 = df[df['price'].fillna(df['price'].mean())]
print("*****************"+"\n")

## Esercizio 4: Most Frequent Value
## Task: Replace NaN values in num-of-doors with the most frequent door count
## Soluzione:
print("***ESERCIZIO 4***")
val = df['num-of-doors'].value_counts().idxmax()
f['num-of-doors']=df['num-of-doors'].fillna(val)
print("*****************"+"\n")
 
### Esercizio 5: Normalisation
### Task: Normalise the horsepower column (convert to numeric first) to a 0-1 range
### Soluzione:
print("***ESERCIZIO 5***")
df['horsepower']=df['horsepower'].astype('int')
min_hp = df['horsepower'].min()
max_hp = df['horsepower'].max()
df['horsepower_n'] = (df['horsepower']-min_hp)/(max_hp-min_hp)
print("*****************"+"\n")

### Esercizio 6: Clipping Outliers
### Task:  Clip values in city-mpg to the 10th and 90th percentiles
### Soluzione:
print("***ESERCIZIO 6***")
lower, upper = df['city-mpg'].quantile([0.1, 0.9])
df['city-mpg'].clip(lower, upper, inplace=True)
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
df.convert_dtypes()
df3 = pd.DataFrame({'make':['audi'],  "safety-rating": [8]})
df3.convert_dtypes()
dfm = pd.merge(df, df3, on='make', how='inner')
print("*****************"+"\n")

### Esercizio 9: Complex Cleaning
### Task: For normalized-losses:
###       Replace missing values (? or NaN) with np.nan.
###       Fill remaining NaN with the mean.
###       Convert to float64.
### Soluzione:
print("***ESERCIZIO 9***")

print("******************"+"\n")

