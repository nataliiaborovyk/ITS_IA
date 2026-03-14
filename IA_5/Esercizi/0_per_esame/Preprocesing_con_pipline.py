import pandas as pd

# preprocessing
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# modello
from sklearn.linear_model import LogisticRegression

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

# definisco colonne
col_num = ["eta", "salario"]
col_cat = ["citta"]

# pipeline per colonne numeriche
pipeline_num = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

# pipeline per colonne categoriche
pipeline_cat = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# column transformer: applica pipeline diverse a colonne diverse
preprocessor = ColumnTransformer([
    ("num", pipeline_num, col_num),
    ("cat", pipeline_cat, col_cat)
])

# pipeline finale: preprocessing + modello
pipeline_finale = Pipeline([
    ("preprocessing", preprocessor),
    ("modello", LogisticRegression())
])

# fit: fa tutto automaticamente
pipeline_finale.fit(X_train, y_train)

# predict: fa preprocessing del test e poi predizione
y_pred = pipeline_finale.predict(X_test)