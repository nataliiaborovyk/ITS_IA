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
