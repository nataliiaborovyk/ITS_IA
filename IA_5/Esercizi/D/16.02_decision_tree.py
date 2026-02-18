# Import librerie
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data = load_breast_cancer()

X = data.data


# =========================
# Target (label)
# =========================
y = data.target      # 0 = maligno, 1 = benigno

# =========================
# Stampa informazioni dataset
# =========================
print(f"Dimensione dataset: {X.shape}")

print(f"Classi: {data.target_names}")  
# es: ['malignant', 'benign']

print(f"Distribuzione classi: {pd.Series(y).value_counts().to_dict()}")
# Conta quanti campioni per classe

# =========================
# Split train / test
# 80% training – 20% test
# =========================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,     # 20% test
    random_state=42,   # riproducibilità
    stratify=y         # mantiene proporzione classi
)

# =========================
# Stampa dimensioni split
# =========================
print(f"Train: {X_train.shape[0]} campioni")
print(f"Test: {X_test.shape[0]} campioni")


# =========================
# Creazione del modello
# =========================
# max_depth controlla la complessità → trade-off Bias-Varianza
dt = DecisionTreeClassifier(
    max_depth=4,        # profondità massima dell'albero
    criterion='gini',  # misura di impurità (alternativa: 'entropy')
    min_samples_leaf=5, # almeno 5 campioni per foglia (regolarizzazione)
    random_state=42
)

# =========================
# Addestramento
# =========================
dt.fit(X_train, y_train)

# =========================
# Predizione classi
# =========================
y_pred = dt.predict(X_test)

# =========================
# Probabilità classe positiva
# =========================
# [:, 1] = probabilità della classe 1 (es. benigno)
y_proba = dt.predict_proba(X_test)[:, 1]

# =========================
# Stampa risultati
# =========================
print("Prime 5 predizioni:", y_pred[:5])
print("Prime 5 probabilità:", y_proba[:5].round(3))

# Tipo del modello
print(type(dt))

print(X_test.shape)
print(y_pred.shape)


# =========================
# Visualizzazione dell'Albero
# =========================

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Creo la figura
plt.figure(figsize=(20, 8))

# Disegno l'albero
plot_tree(
    dt,                           # modello addestrato
    feature_names=data.feature_names,  # nomi delle feature
    class_names=data.target_names,     # nomi delle classi
    filled=True,                  # colora i nodi per classe
    rounded=True,                 # bordi arrotondati
    fontsize=9                   # dimensione testo
)

# Titolo
plt.title("Decision Tree (max_depth=4)", fontsize=14)

# Ottimizza layout
plt.tight_layout()

# Mostra grafico
plt.show()




# ============================================================
# IMPORT LIBRERIE
# ============================================================

import numpy as np  
# Libreria per operazioni numeriche (array, medie, ecc.)

from sklearn.model_selection import train_test_split, cross_val_score
# train_test_split → divide dataset in train/test
# cross_val_score → esegue Cross Validation automatica

from sklearn.tree import DecisionTreeClassifier
# Modello: Albero di decisione singolo

from sklearn.ensemble import RandomForestClassifier
# Modello ensemble: tanti alberi (Bagging)

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
# Metriche di valutazione:
# accuracy → percentuale corretta
# ROC AUC → qualità separazione classi
# classification_report → precision, recall, f1


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

# Dividiamo il dataset originale in:
# 80% TRAIN → usato per addestramento + cross validation
# 20% TEST → usato solo alla fine (valutazione reale)

X_train, X_test, y_train, y_test = train_test_split(
    X,                 # Feature
    y,                 # Target
    test_size=0.2,     # 20% dati nel test
    stratify=y,        # Mantiene proporzione classi (molto importante)
    random_state=42    # Riproducibilità risultati
)


# ============================================================
# DEFINIZIONE MODELLI
# ============================================================

# ----- Decision Tree -----
tree_model = DecisionTreeClassifier(
    random_state=42    # Controlla casualità degli split
)

# ----- Random Forest -----
rf_model = RandomForestClassifier(
    n_estimators=100,  # Numero alberi nella foresta
    random_state=42,   # Riproducibilità
    n_jobs=-1          # Usa tutti i core CPU (più veloce)
)


# ============================================================
# CROSS VALIDATION SOLO SUL TRAIN
# ============================================================

# NOTA DIDATTICA IMPORTANTE:
# Facciamo CV solo su TRAIN per non "sporcare" il test finale

# ----- Decision Tree CV -----
tree_cv_scores = cross_val_score(
    tree_model,   # Modello
    X_train,      # Feature train
    y_train,      # Target train
    cv=5,         # 5 Fold Cross Validation
    scoring='roc_auc'  # Metri ca: Area sotto curva ROC
)

# ----- Random Forest CV -----
rf_cv_scores = cross_val_score(
    rf_model,
    X_train,
    y_train,
    cv=5,
    scoring='roc_auc'
)

# Stampa media performance CV
print("Decision Tree CV AUC:", tree_cv_scores.mean())
print("Random Forest CV AUC:", rf_cv_scores.mean())


# ============================================================
# FIT FINALE SUL TRAIN
# ============================================================

# Dopo la CV dobbiamo riaddestrare i modelli su tutto il TRAIN
# perché i modelli usati nei fold sono temporanei

tree_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)


# ============================================================
# VALUTAZIONE SU TEST SET
# ============================================================

# ----- Predizioni classi -----
tree_pred = tree_model.predict(X_test)
rf_pred = rf_model.predict(X_test)

# ----- Probabilità classe positiva (indice 1) -----
tree_proba = tree_model.predict_proba(X_test)[:, 1]
rf_proba = rf_model.predict_proba(X_test)[:, 1]


# ============================================================
# STAMPA PERFORMANCE TEST
# ============================================================

print("\n--- TEST PERFORMANCE ---")


# ======================
# Decision Tree
# ======================

print("\nDecision Tree")

# Accuracy → percentuale predizioni corrette
print("Accuracy:", accuracy_score(y_test, tree_pred))

# ROC AUC → qualità separazione classi
print("AUC:", roc_auc_score(y_test, tree_proba))

# Report completo classificazione
print(classification_report(y_test, tree_pred))


# ======================
# Random Forest
# ======================

print("\nRandom Forest")

print("Accuracy:", accuracy_score(y_test, rf_pred))

print("AUC:", roc_auc_score(y_test, rf_proba))

print(classification_report(y_test, rf_pred))
