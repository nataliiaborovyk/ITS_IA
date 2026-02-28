# ============================================================
# RETE NEURALE usando dataset UCI (fetch_ucirepo)
# Esempio didattico completo: train / validation / test
# ============================================================

import pandas as pd                         # per DataFrame (tabelle)
import numpy as np                          # per array numerici

from ucimlrepo import fetch_ucirepo         # per scaricare dataset UCI

# Strumenti sklearn per preparare i dati
from sklearn.model_selection import train_test_split  # per dividere il dataset
from sklearn.preprocessing import StandardScaler       # per standardizzare feature
from sklearn.impute import SimpleImputer               # per riempire i NaN (valori mancanti)
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# TensorFlow / Keras per la rete neurale
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ------------------------------------------------------------
# 1) Carico dataset direttamente da UCI
# ------------------------------------------------------------

dataset = fetch_ucirepo(id=300)             # scarica dataset con id=300 da UCI

X = dataset.data.features                   # tutte le feature (input) come DataFrame
y = dataset.data.targets                    # target (output) come DataFrame

# Unisco per comodità in un unico DataFrame (utile per controlli/EDA)
df = pd.concat([X, y], axis=1)

print("Shape totale (righe, colonne):", df.shape)
print("\nColonne disponibili:\n", df.columns)

# ------------------------------------------------------------
# 2) Definisco target y e matrice feature X
# ------------------------------------------------------------

# Target: nel dataset tennis di solito 'Result' è 0/1 (vittoria/sconfitta)
# Se fosse stringa, la convertiamo a intero.
y = df["Result"].astype(int)

# Rimuovo dal DataFrame le colonne non utilizzabili come input numerico:
# - Result: è il target, non deve stare dentro X
# - Player1/Player2: sono nomi (categoriche) -> se le usi "bene" servirebbe encoding, ma qui le togliamo
X = df.drop(columns=["Result", "Player1", "Player2"], errors="ignore")

# Se ci sono altre colonne di tipo object (stringhe), le togliamo per evitare problemi
# (se un giorno vuoi usarle, bisogna fare encoding con OneHotEncoder)
obj_cols = X.select_dtypes(include="object").columns
if len(obj_cols) > 0:
    print("\nColonne categoriche (tolte):", list(obj_cols))
    X = X.drop(columns=obj_cols)

print("\nShape X (solo feature numeriche):", X.shape)
print("Distribuzione classi (y):\n", y.value_counts())

# ------------------------------------------------------------
# 3) Split: Train / Validation / Test
# ------------------------------------------------------------
# Obiettivo:
# - Test: 20% (mai toccato durante training e scelta modello)
# - Dal restante 80%: prendiamo 20% come validation (cioè 0.2 * 0.8 = 16% del totale)
#
# Quindi:
# - Train ~ 64%
# - Validation ~ 16%
# - Test ~ 20%

# 3A) Prima split: train_val vs test
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y,
    test_size=0.20,                         # 20% test
    random_state=42,                        # seed per avere risultati riproducibili
    stratify=y                              # mantiene proporzione classi 0/1 in ogni split
)

# 3B) Seconda split: train vs validation (dentro train_val)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval,
    test_size=0.20,                         # 20% di (train_val) diventa validation
    random_state=42,
    stratify=y_trainval
)

print("\nDimensioni finali:")
print("Train:", X_train.shape, y_train.shape)
print("Val  :", X_val.shape, y_val.shape)
print("Test :", X_test.shape, y_test.shape)

# ------------------------------------------------------------
# 4) Preprocessing numerico: imputazione NaN + standardizzazione
# ------------------------------------------------------------
# 4A) Imputer: riempie valori mancanti con la media della colonna (calcolata sul TRAIN)
imputer = SimpleImputer(strategy="mean")

# 4B) Scaler: standardizza (media=0, dev.std=1) -> utile per reti Dense
scaler = StandardScaler()

# IMPORTANTISSIMO:
# - fit SOLO su TRAIN
# - transform su VAL e TEST
#
# Per evitare "data leakage" (cioè usare info del test/val nel training).

# Imputazione
X_train_imp = imputer.fit_transform(X_train)     # impara le medie dal train
X_val_imp   = imputer.transform(X_val)           # applica le medie del train
X_test_imp  = imputer.transform(X_test)

# Scaling
X_train_sc = scaler.fit_transform(X_train_imp)   # impara media/devstd dal train
X_val_sc   = scaler.transform(X_val_imp)         # applica scaling del train
X_test_sc  = scaler.transform(X_test_imp)

# ------------------------------------------------------------
# 5) Costruisco una rete neurale "piccola" (adatta a ~943 righe)
# ------------------------------------------------------------
# Perché piccola?
# - dataset piccolo -> rischio overfitting se metti troppi neuroni/strati
#
# Architettura consigliata base:
# Input -> Dense(32, relu) -> Dropout(0.2) -> Dense(1, sigmoid)

n_features = X_train_sc.shape[1]                 # numero di feature finali

model = keras.Sequential([
    layers.Input(shape=(n_features,)),           # input = vettore di lunghezza n_features

    layers.Dense(32, activation="relu"),         # hidden layer con 32 neuroni
    layers.Dropout(0.2),                         # spegne casualmente il 20% neuroni in training (anti-overfitting)

    layers.Dense(1, activation="sigmoid")        # output binario (probabilità classe 1)
])

# ------------------------------------------------------------
# 6) Compile: scelgo ottimizzatore + loss + metriche
# ------------------------------------------------------------
# optimizer='adam' = aggiornamento pesi moderno e stabile
# loss='binary_crossentropy' = loss standard per classificazione binaria
# metrics = cosa vogliamo monitorare

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        keras.metrics.AUC(name="auc")            # AUC è spesso più informativa dell'accuracy
    ]
)

print("\nMODEL SUMMARY:")
model.summary()

# ------------------------------------------------------------
# 7) Callbacks: EarlyStopping
# ------------------------------------------------------------
# EarlyStopping controlla la validation loss:
# se per N epoche non migliora, ferma il training e ripristina i pesi migliori.

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",                          # guardo la loss su validation
    patience=10,                                 # aspetta 10 epoche senza miglioramento
    restore_best_weights=True                    # torna ai pesi migliori (non ultimi)
)

# ------------------------------------------------------------
# 8) Training (fit) usando validation esplicita
# ------------------------------------------------------------
# Qui NON uso validation_split, perché ho già X_val e y_val separati.

history = model.fit(
    X_train_sc, y_train,
    validation_data=(X_val_sc, y_val),           # validation esplicita
    epochs=200,                                  # alto: early stopping fermerà prima
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

# ------------------------------------------------------------
# 9) Valutazione finale sul test set (mai visto prima)
# ------------------------------------------------------------

test_loss, test_acc, test_auc = model.evaluate(X_test_sc, y_test, verbose=0)

print("\nRISULTATI SU TEST:")
print(f"Loss     : {test_loss:.4f}")
print(f"Accuracy : {test_acc:.4f}")
print(f"AUC      : {test_auc:.4f}")

# ------------------------------------------------------------
# 10) Predizioni + metriche più dettagliate
# ------------------------------------------------------------
# predict() restituisce probabilità (0..1)
y_prob = model.predict(X_test_sc, verbose=0).ravel()

# trasformo probabilità in classi (0/1) con soglia 0.5
y_pred = (y_prob >= 0.5).astype(int)

print("\nROC AUC (sklearn):", roc_auc_score(y_test, y_prob))
print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification report:\n", classification_report(y_test, y_pred))