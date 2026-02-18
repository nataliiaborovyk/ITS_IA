# ============================================================
# L’UNIONE FA LA FORZA: confronto tra
# 1) Decision Tree (singolo albero)
# 2) Bagging (Random Forest)
# 3) Boosting (Gradient Boosting)
# + Visualizzazione di un piccolo albero
# ============================================================

# ----------------------------
# 0. Import delle librerie
# ----------------------------

import numpy as np                         # Libreria per calcoli numerici (array, media, ecc.)
import matplotlib.pyplot as plt            # Libreria per disegnare grafici

from sklearn.datasets import load_breast_cancer              # Dataset di esempio (tumore al seno)
from sklearn.model_selection import train_test_split, cross_val_score  # Split e cross-validation
from sklearn.tree import DecisionTreeClassifier, plot_tree   # Albero di decisione + funzione per disegnarlo
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier  # Ensemble: bagging e boosting


# ----------------------------
# 1. Caricamento dati
# ----------------------------

data = load_breast_cancer()    # Carico il dataset (X = feature, y = target)

X = data.data                  # X contiene le caratteristiche (es. mean radius, worst perimeter, ecc.)
y = data.target                # y contiene le etichette: 0 = malignant, 1 = benign

# Divido i dati in train e test
# test_size=0.3 significa: 30% test, 70% train
# random_state=42 rende il risultato riproducibile (stessa divisione ogni volta)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)


# ----------------------------
# 2. Definizione dei modelli
# ----------------------------

# 2.1 Bagging (Random Forest)
# n_estimators=100 significa: uso 100 alberi
# random_state=42 per avere risultati ripetibili
bagging_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 2.2 Boosting (Gradient Boosting)
# n_estimators=100: numero di “stadi” (insieme di piccoli modelli in sequenza)
# learning_rate=0.1: quanto “forte” è ogni correzione (più piccolo = più prudente)
# random_state=42: riproducibilità
boosting_model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)

# 2.3 Modello base: Decision Tree singolo
tree_model = DecisionTreeClassifier(
    random_state=42
)


# ----------------------------
# 3. Valutazione con Cross Validation
# ----------------------------

# cross_val_score calcola l’accuracy usando k-fold cross validation
# cv=5 significa: 5 fold (divido il dataset in 5 parti e ruoto train/test)
# Nota: qui usiamo direttamente X e y (tutto il dataset) per stimare la performance media

bagging_scores = cross_val_score(bagging_model, X, y, cv=5)   # accuracy per ogni fold del Random Forest
boosting_scores = cross_val_score(boosting_model, X, y, cv=5) # accuracy per ogni fold del Gradient Boosting
tree_scores = cross_val_score(tree_model, X, y, cv=5)         # accuracy per ogni fold del Decision Tree

# Stampo la media delle accuracy (mean) con 4 cifre decimali
print(f"Accuratezza del modello Decision Tree: {tree_scores.mean():.4f}")
print(f"Accuratezza media Bagging (Random Forest): {bagging_scores.mean():.4f}")
print(f"Accuratezza media Boosting (Gradient Boosting): {boosting_scores.mean():.4f}")


# ----------------------------
# 4. Visualizzazione di un piccolo albero (per il plot)
# ----------------------------

# Creo un albero “piccolo” (più leggibile da disegnare)
# max_depth=3 limita la profondità: l’albero non cresce troppo
small_tree = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

# Addestro il piccolo albero su tutto il dataset (X, y)
# (Lo facciamo solo per visualizzare bene la struttura)
small_tree.fit(X, y)

# Creo la figura grande per vedere bene il disegno
plt.figure(figsize=(20, 10))

# Disegno l’albero
plot_tree(
    small_tree,                          # il modello da disegnare
    feature_names=data.feature_names,    # nomi delle feature nei nodi
    class_names=data.target_names,       # nomi delle classi (malignant, benign)
    filled=True,                         # colora i nodi in base alla classe prevalente
    rounded=True,                        # box con angoli arrotondati
    fontsize=12                          # dimensione del testo nei nodi
)

# Titolo del grafico
plt.title("Visualizzazione di un Decision Tree (Profondità=3)")

# Mostro il grafico
plt.show()
