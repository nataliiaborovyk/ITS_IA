import pandas as pd
import numpy as np

csv_clean_path: str = "../../dati/autos/auto_clean.csv"
df = pd.read_csv(csv_clean_path)
print(df.make.head())
print(df.dtypes)

# Esercizio 1: Connessione con SQLAlchemy
# Task: Write code to store the df DataFrame on a SQLite table named cars using SQLAlchemy. Handle errors gracefully (print a message if it fails).
# Soluzione:
print("***ESERCIZIO 1***")
from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///cars.db")  # Or use your config.db_uri
try:
    with engine.begin() as conn:
        df.to_sql("cars", conn, if_exists="replace", index=False)
except Exception as e:
    print(f"Error: {e}")
finally:
    engine.dispose()
print("*****************"+"\n")
 
### Esercizio 2: Reading SQL Data 
### Task:  Query the cars table to load rows where fuel-type is "gas" into a new DataFrame df_gas 
### Soluzione:
print("***ESERCIZIO 2***")
query = "SELECT * FROM cars WHERE `fuel-type` = 'gas'"
with engine.begin() as conn:
    df_gas = pd.read_sql(text(query), conn)
print("*****************"+"\n")
 
### Esercizio 3: Replacing Missing Values
### Task: Replace missing values (NaN) in the price column with the column’s median
### Soluzione:
print("***ESERCIZIO 3***")
median_price = df["price"].median()
df["price"] = df["price"].fillna(median_price)
print("*****************"+"\n")

## Esercizio 4: Most Frequent Value
## Task: Replace NaN values in num-of-doors with the most frequent door count
## Soluzione:
print("***ESERCIZIO 4***")
most_frequent_doors = df["num-of-doors"].value_counts().idxmax()
df["num-of-doors"] = df["num-of-doors"].fillna(most_frequent_doors)
print("*****************"+"\n")
 
### Esercizio 5: Normalisation
### Task: Normalise the horsepower column (convert to numeric first) to a 0-1 range
### Soluzione:
print("***ESERCIZIO 5***")
df["horsepower"] = pd.to_numeric(df["horsepower"])
df["horsepower"] = (df["horsepower"] - df["horsepower"].min()) / (df["horsepower"].max() - df["horsepower"].min())
print("*****************"+"\n")

### Esercizio 6: Clipping Outliers
### Task:  Clip values in city-mpg to the 10th and 90th percentiles
### Soluzione:
print("***ESERCIZIO 6***")
lower, upper = df["city-mpg"].quantile([0.1, 0.9])
df["city-mpg"] = df["city-mpg"].clip(lower, upper)
print("*****************"+"\n")
 
### Esercizio 7: Dropping Rows
### Task:  Drop all rows where both price and horsepower are NaN
### Soluzione:
print("***ESERCIZIO 7***")
df.dropna(subset=["price", "horsepower"], how="all", inplace=True)
print("*****************"+"\n")
  
### Esercizio 8: Merging DataFrames
### Task: Merge df with a new DataFrame df_extra (columns: make, safety-rating) on the make column. Keep only matching rows
### Soluzione:
print("***ESERCIZIO 8***")
df = df.convert_dtypes()
print(df.dtypes)
df_extra = pd.DataFrame({"make": ["audi"], "safety-rating": [8]})
print(df_extra.dtypes)
df_merged = pd.merge(df, df_extra, on="make", how="inner")
print(df_merged.head(3))
print("*****************"+"\n")

### Esercizio 9: Complex Cleaning
### Task: For normalized-losses:
###       Replace missing values (? or NaN) with np.nan.
###       Fill remaining NaN with the mean.
###       Convert to float64.
### Soluzione:
print("***ESERCIZIO 9***")
df["normalized-losses"] = df["normalized-losses"].replace("?", np.nan)
df["normalized-losses"] = df["normalized-losses"].fillna(df["normalized-losses"].mean())
df["normalized-losses"] = df["normalized-losses"].astype("float64")
print("******************"+"\n")

