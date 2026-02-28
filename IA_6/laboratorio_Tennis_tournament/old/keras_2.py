import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) Dataset UCI
# pip install ucimlrepo
from ucimlrepo import fetch_ucirepo

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve,
    roc_auc_score
)

from keras.models import Sequential, load_model
from keras.layers import Dense, Input
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint


# ----------------------------
# A) CARICAMENTO DATASET
# ----------------------------
tennis = fetch_ucirepo(id=300)

X_raw = tennis.data.features
y_raw = tennis.data.targets

df = pd.concat([X_raw, y_raw], axis=1)

print("Shape df:", df.shape)
print("Colonne totali:", len(df.columns))


# ----------------------------
# B) SEPARO X e y
# ----------------------------
# Target
# Se "Result" è già 0/1 va bene.
# Se è testo (tipo 'W'/'L' o simile), lo trasformiamo in 0/1 con factorize.
y_col_name = "Result"
y_series = df[y_col_name]

if not np.issubdtype(y_series.dtype, np.number):
    # Trasforma qualsiasi etichetta in numeri 0/1/2...
    y, classes_ = pd.factorize(y_series)
    print("Classi originali in Result:", list(classes_))
else:
    y = y_series.to_numpy()

# Features
X = df.drop(columns=[y_col_name])


# ----------------------------
# C) RIMOZIONE COLONNE CATEGORICHE (come hai fatto tu)
# ----------------------------
categorical_cols = X.select_dtypes(include="object").columns
print("Colonne categoriche trovate:", list(categorical_cols))

# scelta didattica: le togliamo
X = X.drop(columns=categorical_cols)


# ----------------------------
# D) RIMOZIONE COLONNE DI LEAKAGE (come hai fatto tu)
# ----------------------------
colonne_da_eliminare = [
    'ST1.1', 'ST1.2',
    'ST2.1', 'ST2.2',
    'ST3.1', 'ST3.2',
    'ST4.1', 'ST4.2',
    'ST5.1', 'ST5.2',
    'TPW.1', 'TPW.2',
    'FNL1',  'FNL2'
]

presenti = [c for c in colonne_da_eliminare if c in X.columns]
X = X.drop(columns=presenti)

print("Nuova shape X dopo drop leakage:", X.shape)


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
    test_size=0.25,
    random_state=42,
    stratify=y_temp
)

print("Train:", X_train.shape, "Val:", X_val.shape, "Test:", X_test.shape)


# ----------------------------
# F) PREPROCESSING: imputazione + scaling
# ----------------------------
# 1) Imputazione: media per tutte le colonne numeriche
imputer = SimpleImputer(strategy="mean")

# FIT solo su train
X_train_imp = imputer.fit_transform(X_train)
X_val_imp   = imputer.transform(X_val)
X_test_imp  = imputer.transform(X_test)

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
print("Numero feature finali:", n_features)


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
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath="best_tennis_model.keras",
    monitor="val_loss",
    save_best_only=True
)

# ----------------------------
# H) FIT
# ----------------------------
history = model.fit(
    X_train_scaled, y_train,
    epochs=200,
    batch_size=32,
    validation_data=(X_val_scaled, y_val),
    callbacks=[early_stop, checkpoint],
    verbose=1
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
best_model = load_model("best_tennis_model.keras")
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
print("AUC =", auc_score)

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