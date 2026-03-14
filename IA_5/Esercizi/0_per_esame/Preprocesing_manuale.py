import pandas as pd

# preprocessing
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# split
from sklearn.model_selection import train_test_split

# esempio dati
df = pd.DataFrame({
    "eta": [25, 30, None, 40, 35],
    "salario": [1200, 1500, 1800, None, 2000],
    "citta": ["Roma", "Milano", "Roma", "Napoli", None],
    "target": [0, 1, 0, 1, 1]
})

# separo X e y
X = df.drop(columns="target")
y = df["target"]

# split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# scelgo le colonne
col_num = ["eta", "salario"]
col_cat = ["citta"]

# -------------------------
# PARTE NUMERICA
# -------------------------

# creo imputatore per colonne numeriche
imputer_num = SimpleImputer(strategy="mean")

# fit sul train numerico: impara le medie
imputer_num.fit(X_train[col_num])

# transform su train e test: riempie i null usando le medie del train
X_train_num = imputer_num.transform(X_train[col_num])
X_test_num = imputer_num.transform(X_test[col_num])

# creo scaler
scaler = StandardScaler()

# fit sul train numerico già imputato: impara media e deviazione standard
scaler.fit(X_train_num)

# transform su train e test
X_train_num_scaled = scaler.transform(X_train_num)
X_test_num_scaled = scaler.transform(X_test_num)

# -------------------------
# PARTE CATEGORICA
# -------------------------

# creo imputatore categorico
imputer_cat = SimpleImputer(strategy="most_frequent")

# fit sul train categorico
imputer_cat.fit(X_train[col_cat])

# transform su train e test
X_train_cat = imputer_cat.transform(X_train[col_cat])
X_test_cat = imputer_cat.transform(X_test[col_cat])

# creo encoder
encoder = OneHotEncoder(handle_unknown="ignore")

# fit sul train categorico imputato
encoder.fit(X_train_cat)

# transform su train e test
X_train_cat_encoded = encoder.transform(X_train_cat)
X_test_cat_encoded = encoder.transform(X_test_cat)

# A questo punto dovresti unire:
# - parte numerica scalata
# - parte categorica codificata