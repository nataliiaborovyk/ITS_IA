# ============================================================
# RETE NEURALE (Keras) usando dataset UCI (fetch_ucirepo)
# Pipeline completo: caricamento → pulizia → preprocessing →
# train/test split → modello → training → valutazione
# ============================================================

import pandas as pd
import numpy as np

from ucimlrepo import fetch_ucirepo

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# ------------------------------------------------------------
# 0) Per rendere i risultati più "ripetibili" (non perfetti, ma meglio)
# ------------------------------------------------------------
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)


# ------------------------------------------------------------
# 1) Carico dataset direttamente da UCI
# ------------------------------------------------------------
dataset = fetch_ucirepo(id=300)

X = dataset.data.features          # DataFrame con feature
y = dataset.data.targets           # DataFrame (di solito 1 colonna target)

# Unisco per comodità (solo per ispezione)
df = pd.concat([X, y], axis=1)

print("Shape totale (X + y):", df.shape)
print("\nPrime righe del dataset completo:")
print(df.head())

print("\nInfo su X:")
print(X.info())

print("\nInfo su y:")
print(y.info())


# ------------------------------------------------------------
# 2) Sistemo y (target) in un formato facile da usare
#    - A volte y è un DataFrame con 1 colonna: lo trasformo in Series
#    - Se per caso ha più colonne, prendo la prima (caso raro)
# ------------------------------------------------------------
if isinstance(y, pd.DataFrame):
    if y.shape[1] == 1:
        y_series = y.iloc[:, 0]          # prendo l'unica colonna
    else:
        # Se ci sono più target, qui semplifico prendendo il primo
        # (in un progetto reale dovresti decidere come gestirli)
        print("\n[ATTENZIONE] y ha più colonne. Uso la prima colonna come target.")
        y_series = y.iloc[:, 0]
else:
    # Se per caso è già una Series
    y_series = y

print("\nTarget (y) - prime righe:")
print(y_series.head())


# ------------------------------------------------------------
# 3) Capisco che tipo di problema è:
#    - Se y ha pochi valori distinti → probabile classificazione
#    - Se y ha tantissimi valori diversi e sembra continua → probabile regressione
#    Per essere didattici facciamo una stima semplice:
# ------------------------------------------------------------
n_unique = y_series.nunique(dropna=True)
print("\nNumero di valori unici in y:", n_unique)

# Heuristica semplice:
# - se <= 20 valori unici → classificazione (binaria o multiclasse)
# - altrimenti → regressione
is_classification = (n_unique <= 20)

print("Tipo problema stimato:", "CLASSIFICAZIONE" if is_classification else "REGRESSIONE")


# ------------------------------------------------------------
# 4) Split Train/Test (come hai scritto tu)
#    Se è classificazione, uso stratify=y per mantenere proporzioni classi
# ------------------------------------------------------------
if is_classification:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_series,
        test_size=0.2,
        random_state=SEED,
        stratify=y_series
    )
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_series,
        test_size=0.2,
        random_state=SEED
    )

print("\nShape X_train:", X_train.shape)
print("Shape X_test :", X_test.shape)


# ------------------------------------------------------------
# 5) Preprocessing (pulizia + trasformazioni) su X
#    Idea:
#    - colonne numeriche: imputazione (mediana) + standardizzazione
#    - colonne categoriche: imputazione (moda) + one-hot encoding
#
#    Questo è importante perché le reti neurali lavorano meglio con:
#    - numeri senza NaN
#    - scale simili (standardizzazione)
#    - categorie trasformate in numeri (one-hot)
# ------------------------------------------------------------

# Trovo automaticamente colonne numeriche e categoriche
numeric_cols = X_train.select_dtypes(include=["number"]).columns.tolist()
categorical_cols = X_train.select_dtypes(exclude=["number"]).columns.tolist()

print("\nColonne numeriche:", numeric_cols)
print("Colonne categoriche:", categorical_cols)

# Pipeline per NUMERICHE:
# 1) SimpleImputer: sostituisce i valori mancanti (NaN) con la mediana
# 2) StandardScaler: porta le feature su scala simile (media 0, dev std 1)
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Pipeline per CATEGORICHE:
# 1) SimpleImputer: riempie NaN con il valore più frequente
# 2) OneHotEncoder: trasforma categorie in colonne 0/1
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# ColumnTransformer: applica trasformazioni diverse a colonne diverse
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ],
    remainder="drop"  # ignora colonne non incluse (qui non ce ne dovrebbero essere)
)

# "Fitting" del preprocessing SOLO sul training:
# - impariamo mediana, media/devstd, categorie...
preprocessor.fit(X_train)

# Trasformo train e test in matrici numeriche pronte per la rete
X_train_p = preprocessor.transform(X_train)
X_test_p = preprocessor.transform(X_test)

# Se esce una matrice "sparse", la converto in array denso
# (Keras può lavorare con dense facilmente)
try:
    X_train_p = X_train_p.toarray()
    X_test_p = X_test_p.toarray()
except Exception:
    pass

print("\nShape dopo preprocessing:")
print("X_train_p:", X_train_p.shape)
print("X_test_p :", X_test_p.shape)


# ------------------------------------------------------------
# 6) Preprocessing su y (target)
#    Se classificazione:
#      - se target è stringa/categoria → LabelEncoder (0..K-1)
#      - poi scelgo:
#          * binary: 1 output sigmoid + binary_crossentropy
#          * multiclass: K output softmax + sparse_categorical_crossentropy
#    Se regressione:
#      - y deve essere float (numerico)
# ------------------------------------------------------------
if is_classification:
    # Se y non è numerica, la converto in etichette numeriche
    if y_train.dtype == "object" or str(y_train.dtype).startswith("category"):
        le = LabelEncoder()
        y_train_enc = le.fit_transform(y_train.astype(str))
        y_test_enc = le.transform(y_test.astype(str))
        class_names = le.classes_
        print("\nClassi (LabelEncoder):", class_names)
    else:
        # Già numerica: la uso così com'è
        y_train_enc = y_train.to_numpy()
        y_test_enc = y_test.to_numpy()
        class_names = np.unique(y_train_enc)

    n_classes = len(np.unique(y_train_enc))
    print("Numero classi:", n_classes)

else:
    # REGRESSIONE: target numerico float
    y_train_enc = pd.to_numeric(y_train, errors="coerce").to_numpy(dtype=np.float32)
    y_test_enc = pd.to_numeric(y_test, errors="coerce").to_numpy(dtype=np.float32)


# ------------------------------------------------------------
# 7) Costruzione del modello Keras
#    Struttura base:
#    - input: numero feature = X_train_p.shape[1]
#    - 2 strati densi con ReLU (tipico punto di partenza)
#    - output:
#        * binary: 1 neurone sigmoid
#        * multiclass: K neuroni softmax
#        * regressione: 1 neurone lineare
# ------------------------------------------------------------
input_dim = X_train_p.shape[1]

model = keras.Sequential()

# "Input layer" (in Keras spesso si mette così)
model.add(layers.Input(shape=(input_dim,)))

# Strato denso 1: 64 neuroni
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dropout(0.2))  # Dropout: riduce overfitting

# Strato denso 2: 32 neuroni
model.add(layers.Dense(32, activation="relu"))
model.add(layers.Dropout(0.2))

# Output layer dipende dal tipo di problema
if is_classification:
    if n_classes == 2:
        # Classificazione binaria
        model.add(layers.Dense(1, activation="sigmoid"))
        loss_fn = "binary_crossentropy"
        metrics_list = ["accuracy"]
    else:
        # Classificazione multiclasse
        model.add(layers.Dense(n_classes, activation="softmax"))
        loss_fn = "sparse_categorical_crossentropy"
        metrics_list = ["accuracy"]
else:
    # Regressione
    model.add(layers.Dense(1, activation="linear"))
    loss_fn = "mse"
    metrics_list = ["mae"]  # Mean Absolute Error


# ------------------------------------------------------------
# 8) Compilazione del modello
#    Qui scelgo:
#    - optimizer: Adam (ottimo default)
#    - loss: dipende dal problema
#    - metrics: accuracy o mae
# ------------------------------------------------------------
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=loss_fn,
    metrics=metrics_list
)

print("\nRiepilogo modello:")
model.summary()


# ------------------------------------------------------------
# 9) Training (fit)
#    - validation_split: prende una parte del TRAIN per validazione
#    - EarlyStopping: ferma quando non migliora più (molto utile)
# ------------------------------------------------------------
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",          # guarda la loss di validazione
    patience=10,                 # aspetta 10 epoche senza miglioramento
    restore_best_weights=True    # torna automaticamente ai pesi migliori
)

history = model.fit(
    X_train_p, y_train_enc,
    epochs=100,
    batch_size=32,
    validation_split=0.2,        # 20% del TRAIN usato come validation
    callbacks=[early_stop],
    verbose=1
)


# ------------------------------------------------------------
# 10) Valutazione finale su TEST (questo è il test vero)
# ------------------------------------------------------------
print("\nValutazione su TEST:")
test_metrics = model.evaluate(X_test_p, y_test_enc, verbose=0)
print("Metriche:", dict(zip(model.metrics_names, test_metrics)))


# ------------------------------------------------------------
# 11) Report finale (solo classificazione)
#     - Predizioni
#     - Confusion matrix
#     - Classification report (precision/recall/f1)
# ------------------------------------------------------------
if is_classification:
    if n_classes == 2:
        # output sigmoid: probabilità tra 0 e 1
        y_prob = model.predict(X_test_p, verbose=0).ravel()
        # soglia 0.5: sopra → classe 1, sotto → classe 0
        y_pred = (y_prob >= 0.5).astype(int)
    else:
        # output softmax: array di probabilità (N, K)
        y_prob = model.predict(X_test_p, verbose=0)
        # classe predetta = argmax
        y_pred = np.argmax(y_prob, axis=1)

    print("\nAccuracy (calcolata a mano):", accuracy_score(y_test_enc, y_pred))

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test_enc, y_pred))

    print("\nClassification report:")
    print(classification_report(y_test_enc, y_pred))


# ------------------------------------------------------------
# 12) Nota didattica importante
#     - Se il risultato è scarso, non significa "Keras non funziona".
#       Può dipendere da:
#       * qualità del dataset
#       * feature non informative
#       * modello troppo semplice
#       * classi sbilanciate
#       * iperparametri (lr, batch_size, layer, ecc.)
# ------------------------------------------------------------
print("\nFINE. Se vuoi, nel prossimo passo miglioriamo il modello (e vediamo le curve di training).")