import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"     # forza CPU
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"      # riduce log (0=all, 1=INFO-, 2=WARNING-, 3=ERROR-)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) Dataset UCI
# pip install ucimlrepo
from ucimlrepo import fetch_ucirepo

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve,
    roc_auc_score
)

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


# ----------------------------
# A) CARICAMENTO DATASET
# ----------------------------
tennis = fetch_ucirepo(id=300)

X_raw = tennis.data.features
y_raw = tennis.data.targets

df = pd.concat([X_raw, y_raw], axis=1)

# print("\nShape df:", df.shape)
# print("\nColonne totali:", len(df.columns))


# ----------------------------
# B) SEPARO X e y
# ----------------------------
# Target
y = df["Result"] 

# Features
X = df.drop("Result", axis=1)


# ----------------------------
# C) RIMOZIONE COLONNE CATEGORICHE 
# ----------------------------
categorical_cols = X.select_dtypes(include=["object", "string"]).columns
print("\nColonne categoriche trovate:", list(categorical_cols))


# decisione didattica eliminiamo le colonne categoriche
    # eliminiamo Player1 / Player2 perche cosi evitiamo il bias da identita. 
    # Voliamo che il modello impara statistiche e non che Federer = vittoria
    # eliminiamo Tournament perche voliamo modello basato su statistiche match
    #  e non su dove si è svolto. È una semplificazione didattica.
X = X.drop(categorical_cols, axis=1)


# ----------------------------
# D) RIMOZIONE COLONNE DI LEAKAGE 
# ----------------------------
colonne_da_eliminare = [
    'ST1.1', 'ST1.2',         # Game set 1
    'ST2.1', 'ST2.2',         # Game set 2
    'ST3.1', 'ST3.2',         # Game set 3
    'ST4.1', 'ST4.2',         # Game set 4 
    'ST5.1', 'ST5.2',         # Game set 5                             
    'TPW.1', 'TPW.2',         # Punti totali (troppo vicini al risultato)  leakage!!
    'FNL1',  'FNL2'           # Risultato finale set                       leakage!!
]

X = X.drop(colonne_da_eliminare, axis=1)

print("\nNuova shape X dopo drop leakage:", X.shape)


# ----------------------------
# E) SPLIT train/val/test
# ----------------------------
# 20% test
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 20% di (train+val) diventa val -> 0.25 del temp = 0.2 totale
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.15,
    random_state=42,
    stratify=y_temp
)

print("\nTrain:", X_train.shape, "Val:", X_val.shape, "Test:", X_test.shape)


# ----------------------------
# F) PREPROCESSING: imputazione + scaling
# ----------------------------

zero_cols = ["ACE.1","ACE.2","DBF.1","DBF.2"]

mean_cols = [col for col in X.columns if col not in zero_cols]

# VERSIONE 1

# 1) Imputazione: media 
mean_imputer = SimpleImputer(strategy="mean")

# FIT solo su train
X_train_mean = mean_imputer.fit_transform(X_train[mean_cols])
X_val_mean   = mean_imputer.transform(X_val[mean_cols])
X_test_mean  = mean_imputer.transform(X_test[mean_cols])

# Per le colonne zero
X_train_zero = X_train[zero_cols].fillna(0).values
X_val_zero   = X_val[zero_cols].fillna(0).values
X_test_zero  = X_test[zero_cols].fillna(0).values

# Ricompongo il dataset
X_train_imp = np.hstack([X_train_mean, X_train_zero])
X_val_imp   = np.hstack([X_val_mean,   X_val_zero])
X_test_imp  = np.hstack([X_test_mean,  X_test_zero])

# 2) Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_imp)
X_val_scaled   = scaler.transform(X_val_imp)
X_test_scaled  = scaler.transform(X_test_imp)

# Keras vuole numpy array
y_train = np.array(y_train)
y_val   = np.array(y_val)
y_test  = np.array(y_test)

n_features = X_train_scaled.shape[1]
print("\nNumero feature finali:", n_features)


# VERSIONE 2

preprocessor = ColumnTransformer(
    transformers=[
        ("mean_imp", SimpleImputer(strategy="mean"), mean_cols),
        ("zero_imp", SimpleImputer(strategy="constant", fill_value=0), zero_cols)
    ]
)

pipeline = Pipeline([
    ("imputer", preprocessor),
    ("scaler", StandardScaler())
])

# Fit solo su train
X_train_final = pipeline.fit_transform(X_train)
X_val_final   = pipeline.transform(X_val)
X_test_final  = pipeline.transform(X_test)


# ----------------------------
# G) MODELLO KERAS (Sequential)
# ----------------------------
model = Sequential([
    Input(shape=(n_features,)),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=SGD(learning_rate=0.05),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Callbacks
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath="./IA_6/laboratorio_Tennis_tournament/best_tennis_model.keras",
    monitor="val_loss",
    save_best_only=True
)

# ----------------------------
# H) FIT
# ----------------------------
history = model.fit(
    X_train_scaled, y_train,
    epochs=80,
    batch_size=20,
    validation_data=(X_val_scaled, y_val),
    callbacks=[early_stop, checkpoint],
    verbose=0
)

print("\nChiavi history:", history.history.keys())


# ----------------------------
# I) EVALUATE SU TEST (modello in RAM)
# ----------------------------
test_loss, test_acc = model.evaluate(X_test_scaled, y_test, verbose=0)
print("\nTEST (model in RAM):")
print("test_loss =", test_loss)
print("test_acc  =", test_acc)

# Carico best model dal checkpoint (su disco)
best_model = load_model("./IA_6/laboratorio_Tennis_tournament/best_tennis_model.keras")
best_test_loss, best_test_acc = best_model.evaluate(X_test_scaled, y_test, verbose=0)

print("\nTEST (BEST model da file):")
print("best_test_loss =", best_test_loss)
print("best_test_acc  =", best_test_acc)


# ----------------------------
# J) PREDICT + METRICHE SKLEARN
# ----------------------------
y_prob = best_model.predict(X_test_scaled, verbose=0).reshape(-1)  # probabilità
y_pred = (y_prob > 0.5).astype(int)  # classi 0/1

print("\nAccuracy (sklearn) =", accuracy_score(y_test, y_pred))
print("\nClassification report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Neural Network - Confusion Matrix")
plt.show()


# ----------------------------
# K) ROC CURVE + AUC
# ----------------------------
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
auc_score = roc_auc_score(y_test, y_prob)
print("\nAUC =", auc_score)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
plt.plot([0, 1], [0, 1], "--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Neural Network")
plt.legend()
plt.show()


# ----------------------------
# L) GRAFICI TRAINING (LOSS / ACC)
# ----------------------------
plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("Loss durante training")
plt.xlabel("Epoche")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])
plt.show()

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Accuracy durante training")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])
plt.show()

print("\nFile salvato:", "best_tennis_model.keras")