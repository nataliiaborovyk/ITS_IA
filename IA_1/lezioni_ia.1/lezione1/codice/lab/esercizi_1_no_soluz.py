import pandas as pd
import numpy as np

csv_clean_path: str = "../../dati/autos/auto_clean.csv"
df = pd.read_csv(csv_clean_path)
print(df.head())

# Esercizio 1: Connessione con SQLAlchemy
# Task: Write code to store the df DataFrame on a SQLite table named cars using SQLAlchemy. Handle errors gracefully (print a message if it fails).
# Soluzione:
print("***ESERCIZIO 1***")

print("*****************"+"\n")
 
### Esercizio 2: Reading SQL Data 
### Task:  Query the cars table to load rows where fuel-type is "gas" into a new DataFrame df_gas 
### Soluzione:
print("***ESERCIZIO 2***")

print("*****************"+"\n")
 
### Esercizio 3: Replacing Missing Values
### Task: Replace missing values (NaN) in the price column with the column’s median
### Soluzione:
print("***ESERCIZIO 3***")

print("*****************"+"\n")

## Esercizio 4: Most Frequent Value
## Task: Replace NaN values in num-of-doors with the most frequent door count
## Soluzione:
print("***ESERCIZIO 4***")

print("*****************"+"\n")
 
### Esercizio 5: Normalisation
### Task: Normalise the horsepower column (convert to numeric first) to a 0-1 range
### Soluzione:
print("***ESERCIZIO 5***")

print("*****************"+"\n")

### Esercizio 6: Clipping Outliers
### Task:  Clip values in city-mpg to the 10th and 90th percentiles
### Soluzione:
print("***ESERCIZIO 6***")

print("*****************"+"\n")
 
### Esercizio 7: Dropping Rows
### Task:  Drop all rows where both price and horsepower are NaN
### Soluzione:
print("***ESERCIZIO 7***")

print("*****************"+"\n")
  
### Esercizio 8: Merging DataFrames
### Task: Merge df with a new DataFrame df_extra (columns: make, safety-rating) on the make column. Keep only matching rows
### Soluzione:
print("***ESERCIZIO 8***")

print("*****************"+"\n")

### Esercizio 9: Complex Cleaning
### Task: For normalized-losses:
###       Replace missing values (? or NaN) with np.nan.
###       Fill remaining NaN with the mean.
###       Convert to float64.
### Soluzione:
print("***ESERCIZIO 9***")

print("******************"+"\n")

