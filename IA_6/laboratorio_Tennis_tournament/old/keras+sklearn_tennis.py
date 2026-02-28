

"""# **FASE 1   -  CARICAMENTO DATI**"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import math
import seaborn as sns

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

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

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

df_raw = pd.concat([X_raw, y_raw], axis=1)

# Controlli base
print("Shape df:", df_raw.shape)
print("\nInfo:")
print(df_raw.info())
df_raw.head()

"""# **FASE 2  - Ramo EDA su copia (analisi esplorativa)**"""

# ----------------------------
#  CREO COPIA PER EDA
# ----------------------------

df_eda = df_raw.copy()

# ----------------------------
#  SEPARO X e y
# ----------------------------

# Target
y_eda = df_eda["Result"]

# Features
X_eda = df_eda.drop(columns=["Result"])

# ----------------------------
#  Controllo missing values
# ----------------------------

# Missing values (top 20)
missing = X_eda.isnull().sum().sort_values(ascending=False)
print("\nTotale null: ", X_eda.isnull().sum().sum())
print("\nTop 20 colonne con più NaN:")
print(missing.head(20))

# ----------------------------
#  Colonne categoriche (stringhe)
# ----------------------------

cat_cols = X_eda.select_dtypes(include=["object", "string"]).columns
num_cols = X_eda.select_dtypes(include=np.number).columns

print("Colonne categoriche:", list(cat_cols))
print("\nNumero colonne numeriche:", len(num_cols))
print("\nVecchia shape:", X_eda.shape)

# decisione didattica elimino le colonne categoriche
    # elimino Player1 / Player2 perche cosi evito il bias da identita.
    # Voglio che il modello impara statistiche e non che Federer = vittoria
    # elimino Tournament perche voglio modello basato su statistiche match
    # e non su dove si è svolto. È una semplificazione didattica.

X_eda = X_eda.drop(cat_cols, axis=1)
print("\nNuova shape:", X_eda.shape)

"""   Elimino le colonne

Colonna	Significato
ST1	    Set 1
ST2	    Set 2
ST3	    Set 3
ST4	    Set 4
ST5	    Set 5

--> Sono statistiche dei set  quindi  Null ≠ dato mancante ma Null = set non giocato
Decisione didattica: Eliminiamo tutte le colonne dei set perche troppi null e informazione già indiretta nel risultato

TPW (Total Points Won)

--> Totale punti vinti. È quasi il risultato della partita. Data leakage forte!
Eliminiamo anche TPW.

FNL1 / FNL2    Final score

--> data leakage. Contiene risultato match. Eliminiamo.
"""

# Definisco le colonne da eliminare (Data Leakage + Target)
colonne_da_eliminare = [
    'ST1.1', 'ST1.2',         # Game set 1
    'ST2.1', 'ST2.2',         # Game set 2
    'ST3.1', 'ST3.2',         # Game set 3
    'ST4.1', 'ST4.2',         # Game set 4
    'ST5.1', 'ST5.2',         # Game set 5
    'TPW.1', 'TPW.2',         # Punti totali (troppo vicini al risultato)  leakage!!
    'FNL1',  'FNL2'           # Risultato finale set                       leakage!!
]
print("Vecchia shape:", X_eda.shape)

X_eda = X_eda.drop(colonne_da_eliminare, axis=1)

print("Features rimaste in X:")
print(X_eda.columns.tolist())
print("Nuova shape:", X_eda.shape)

# ---------------------------------
#  Controllo missing values rimasti
# ---------------------------------

# Missing values (top 20)
missing = X_eda.isnull().sum().sort_values(ascending=False)
print("\nTotale null: ", X_eda.isnull().sum().sum())
print("\nTop 20 colonne con più NaN:")
print(missing.head(20))

"""   Gestisco i valori null

UFE - Unforced Errors
WNR

--> Winners
Null pochi (126 su dataset grande). Qui ha senso imputare.
Strategia: Media.

NPA / NPW  

--> Net Points Attempted / Won
Null pochi - imputazione media.

ACE / DBF

--> Ace e Doppi falli.
Null pochissimi - logico usare 0. Se non registrato - probabilmente 0

BPC	- Break Points Created

BPW	- Break Points Won

-->
Strategia: Media imputazione perché dataset grande, pochi null e variabile continua

"""

# Media imputazione
for col in ["UFE.1","UFE.2","WNR.1","WNR.2",
            "NPA.1","NPA.2","NPW.1","NPW.2",
            "BPC.1","BPW.1","BPC.2","BPW.2"]:
    X_eda[col] = X_eda[col].fillna(X_eda[col].mean())

# Zero imputazione
for col in ["ACE.1","ACE.2","DBF.1","DBF.2"]:
        X_eda[col] = X_eda[col].fillna(0)

print("\nTotale null: ", X_eda.isnull().sum().sum())

"""#   Grafici EDA

Boxplot per classe (Result=0 vs Result=1)
                    
Serve per verificare se:
    La mediana (linea nel box) è diversa tra 0 e 1?
    I box sono separati o sovrapposti?
    Una classe ha valori molto più alti?

Se sì → quella feature distingue bene le classi e quindi aiuta a prevedere Result
"""

# unisco per i boxplot

df_plot = X_eda.copy()
df_plot["Result"] = y_eda

cols = [c for c in df_plot.columns if c != "Result"]

per_fig = 6
n_fig = math.ceil(len(cols) / per_fig)

for f in range(n_fig):
    subset = cols[f*per_fig:(f+1)*per_fig]
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    axes = axes.ravel()

    for ax, col in zip(axes, subset):
        sns.boxplot(data=df_plot, x="Result", y=col, ax=ax)
        ax.set_title(col)
        ax.set_xlabel("Result")
        ax.set_ylabel("")

    for ax in axes[len(subset):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()

plt.figure(figsize=(20,10))
X_eda.boxplot()
plt.xticks(rotation=90)
plt.show()

X_eda.hist(figsize=(20,15))
plt.show()

# ----------------------------
# correlazioni featurs e target
# ----------------------------

df_numeric = df_plot.select_dtypes(include=np.number)

corr_target = df_numeric.corr()['Result'].sort_values(ascending=False)

print("\nCorrelazione (imputazione globale SOLO EDA) ", corr_target)

"""

# **FASE 3 — Decisioni di preprocessing**
##  RAMO TRAINING (pipeline corretta)
Qui faccio:
1) decido cosa togliere (categoriche + leakage)
2) split train/val/test
3) preprocessing con ColumnTransformer (mean + zero) + StandardScaler, fit solo su train
4) modelli classici + rete neurale"""

# ----------------------------
#  CREO COPIA PER TRAINING
# ----------------------------

#  Parto dal RAW (non dalla copia imputata EDA)
df = df_raw.copy()

y = df["Result"]
X = df.drop(columns=["Result"])

# ----------------------------
#  RIMOZIONE COLONNE CATEGORICHE
# ----------------------------

# 1) Drop categoriche (scelta didattica)
cat_cols = X.select_dtypes(include=["object", "string"]).columns
X = X.drop(columns=cat_cols)

# 2) Drop leakage (se colonne presenti)
leak_cols = [
    'ST1.1', 'ST1.2',
    'ST2.1', 'ST2.2',
    'ST3.1', 'ST3.2',
    'ST4.1', 'ST4.2',
    'ST5.1', 'ST5.2',
    'TPW.1', 'TPW.2',
    'FNL1',  'FNL2'
]
leak_present = [c for c in leak_cols if c in X.columns]
X = X.drop(columns=leak_present)

print("Shape X dopo drop:", X.shape)

"""# **FASE 4 — Split**"""

# ----------------------------
#  SPLIT train/val/test
# ----------------------------

# 20% test
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 20% di (train+val) diventa val -> 0.15 del temp = 0.2 totale
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.15,
    random_state=42,
    stratify=y_temp
)

print("\nTrain:", X_train.shape, "Val:", X_val.shape, "Test:", X_test.shape)

"""# **FASE 5 — Preprocessing statistico**  (imputazione mista + scaling)"""

# Controllo missing values

# print(X.isnull().sum().sort_values(ascending=False))
print("\nTotale null: ", X.isnull().sum().sum())

# ----------------------------
#  PREPROCESSING: imputazione + scaling
# ----------------------------

zero_cols = ["ACE.1","ACE.2","DBF.1","DBF.2"]

mean_cols = [col for col in X.columns if col not in zero_cols]

"""  VERSIONE 1"""

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

n_features = X_train_scaled.shape[1]
print("\nNumero feature finali:", n_features)
print("Shape dopo preprocessing:", X_train_scaled.shape, X_val_scaled.shape, X_test_scaled.shape)

"""VERSIONE 2"""

preprocessor = ColumnTransformer(
    transformers=[
        ("mean_imp", SimpleImputer(strategy="mean"), mean_cols),
        ("zero_imp", SimpleImputer(strategy="constant", fill_value=0), zero_cols)
    ]
)

# Preprocessing per alberi

pipeline_tree = Pipeline([
    ("imputer", preprocessor)   # senza scaler
])

# Preprocessing per modelli lineari e NN

pipeline_scaled = Pipeline([
    ("imputer", preprocessor),
    ("scaler", StandardScaler())
])

# Fit solo su train
X_train_tree = pipeline_tree.fit_transform(X_train)
X_val_tree   = pipeline_tree.transform(X_val)
X_test_tree  = pipeline_tree.transform(X_test)

# Fit solo su train
X_train_scaled = pipeline_scaled.fit_transform(X_train)
X_val_scaled   = pipeline_scaled.transform(X_val)
X_test_scaled  = pipeline_scaled.transform(X_test)

print("Shape dopo preprocessing:", X_train_tree.shape, X_val_tree.shape, X_test_tree.shape)



"""# **FASE 6 — Modelli classici**  (sklearn)"""

from sklearn.metrics import precision_recall_curve, auc

# Decision Tree
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train_tree, y_train)
tree_proba = tree.predict_proba(X_test_tree)[:, 1]
tree_pred = (tree_proba > 0.5).astype(int)

cm_tree = confusion_matrix(y_test, tree_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm_tree)
disp.plot()
plt.title("Decision Tree - Confusion Matrix")
plt.show()

# Random Forest
rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf.fit(X_train_tree, y_train)
rf_proba = rf.predict_proba(X_test_tree)[:, 1]
rf_pred = (rf_proba > 0.5).astype(int)

cm_rf = confusion_matrix(y_test, rf_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm_rf)
disp.plot()
plt.title("Random Forest - Confusion Matrix")
plt.show()

# Gradient Boosting
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
gb.fit(X_train_tree, y_train)
gb_proba = gb.predict_proba(X_test_tree)[:, 1]
gb_pred = (gb_proba > 0.5).astype(int)

cm_gb = confusion_matrix(y_test, gb_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm_gb)
disp.plot()
plt.title("Gradient Boosting - Confusion Matrix")
plt.show()

# Logistic Regression
log = LogisticRegression(max_iter=2000)
log.fit(X_train_scaled, y_train)
log_proba = log.predict_proba(X_test_scaled)[:, 1]
log_pred = (log_proba > 0.5).astype(int)

cm_log = confusion_matrix(y_test, log_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm_log)
disp.plot()
plt.title("Logistic Regression - Confusion Matrix")
plt.show()

def metrics_binary(name, y_true, y_pred, y_proba):
    acc = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_proba)
    return {"model": name, "accuracy": acc, "auc": auc}

results = []
results.append(metrics_binary("DecisionTree", y_test, tree_pred, tree_proba))
results.append(metrics_binary("RandomForest", y_test, rf_pred, rf_proba))
results.append(metrics_binary("GradientBoosting", y_test, gb_pred, gb_proba))
results.append(metrics_binary("LogisticRegression", y_test, log_pred, log_proba))

pd.DataFrame(results).sort_values(by="auc", ascending=False)

"""# Feature Importance - Random Forest"""

#    Estrazione Feature Importance

importances = rf.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
})

feature_importance_df = feature_importance_df.sort_values(
    by="Importance",
    ascending=False
)

# Grafico Feature Importance

plt.figure(figsize=(10, 8))
plt.barh(
    feature_importance_df["Feature"],
    feature_importance_df["Importance"]
)
plt.gca().invert_yaxis()
plt.title("Feature Importance - Random Forest")
plt.xlabel("Importanza")
plt.ylabel("Feature")
plt.show()

"""# Feature Importance — Logistic Regression"""

from matplotlib.patches import Patch

coefs = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': log.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

colors = ['firebrick' if x > 0 else 'steelblue'
          for x in coefs['Coefficient']]

plt.figure(figsize=(10, 6))
plt.barh(coefs['Feature'], coefs['Coefficient'], color=colors)
plt.axvline(0, color='black', linewidth=1)
plt.title("Feature Importance (Coefficienti della Regressione)")
plt.xlabel("Impatto sulla probabilità di vittoria")
plt.gca().invert_yaxis()
legend_elements = [
    Patch(facecolor='firebrick', label='Favorisce Player 1'),
    Patch(facecolor='steelblue', label='Favorisce Player 2')
]
plt.legend(handles=legend_elements)
plt.show()

"""# **FASE 7 — Rete neurale (Keras)**
Usa gli stessi dati preprocessati (X_train_slaled, X_val_scaled, X_test_scaled).

Keras vuole numpy array
"""

y_train_np = np.array(y_train)
y_val_np   = np.array(y_val)
y_test_np  = np.array(y_test)

n_features = X_train_scaled.shape[1]

nn = Sequential([
    Input(shape=(n_features,)),
    Dense(8, activation="relu"),
    # Dense(2, activation="relu"),
    Dense(1, activation="sigmoid")
])

nn.compile(
    optimizer=SGD(learning_rate=0.05),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath="best_tennis_nn.keras",
    monitor="val_loss",
    save_best_only=True
)

history = nn.fit(
    X_train_scaled, y_train_np,
    validation_data=(X_val_scaled, y_val_np),
    epochs=200,
    batch_size=15,
    callbacks=[early_stop, checkpoint],
    verbose=1
)

test_loss, test_acc = nn.evaluate(X_test_scaled, y_test_np, verbose=0)
print("NN test_loss:", test_loss)
print("NN test_acc :", test_acc)

best_nn = load_model("best_tennis_nn.keras")
nn_proba = best_nn.predict(X_test_scaled, verbose=0).reshape(-1)   # un vettore 1D di probabilità
nn_pred = (nn_proba > 0.5).astype(int)

nn_auc = roc_auc_score(y_test_np, nn_proba)
print("NN AUC:", nn_auc)

# Aggiungo NN alla tabella risultati
results.append(metrics_binary("NeuralNetwork(Keras)", y_test_np, nn_pred, nn_proba))
pd.DataFrame(results).sort_values(by="auc", ascending=False)

"""##  Confronto ROC curve (tutti i modelli)"""

plt.figure(figsize=(8,6))

for name, proba in [
    ("DecisionTree", tree_proba),
    ("RandomForest", rf_proba),
    ("GradientBoosting", gb_proba),
    ("LogisticRegression", log_proba),
    ("NeuralNetwork(Keras)", nn_proba),
]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    auc = roc_auc_score(y_test, proba)
    plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")

plt.plot([0,1], [0,1], "--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve — Confronto Modelli")
plt.legend()
plt.show()

"""##  Confronto Precision–Recall curve (tutti i modelli)"""

from sklearn.metrics import precision_recall_curve, average_precision_score

plt.figure(figsize=(8, 6))

for name, proba in [
    ("DecisionTree", tree_proba),
    ("RandomForest", rf_proba),
    ("GradientBoosting", gb_proba),
    ("LogisticRegression", log_proba),
    ("NeuralNetwork(Keras)", nn_proba),
]:
    precision, recall, _ = precision_recall_curve(y_test, proba)
    ap = average_precision_score(y_test, proba)  # AP standard
    plt.plot(recall, precision, label=f"{name} (AP={ap:.3f})")

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curve — Confronto Modelli")
plt.legend()
plt.show()

"""## Grafici training NN (loss/accuracy)"""

plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("NN Loss durante training")
plt.xlabel("Epoche")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])
plt.show()

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("NN Accuracy durante training")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])
plt.show()

"""# VISUALIZZAZIONE ALBERO DECISIONALE"""

from sklearn.tree import DecisionTreeClassifier, plot_tree

plt.figure(figsize=(20, 10))
plot_tree(tree,
          feature_names=X_train.columns,
          class_names=['Vince P2', 'Vince P1'],
          filled=True,
          rounded=True,
          fontsize=7)
plt.title("Logica del Decision Tree")
plt.show()

"""# Tabella Confronto Finale"""

# ----------------------------
# Calcolo metriche
# ----------------------------
results = []

for name, pred, proba in [
    ("DecisionTree", tree_pred, tree_proba),
    ("RandomForest", rf_pred, rf_proba),
    ("GradientBoosting", gb_pred, gb_proba),
    ("LogisticRegression", log_pred, log_proba),
    ("NeuralNetwork(Keras)", nn_pred, nn_proba),
]:

    acc = accuracy_score(y_test, pred)
    auc_roc = roc_auc_score(y_test, proba)
    ap_pr = average_precision_score(y_test, proba)

    results.append([name, acc, auc_roc, ap_pr])


# ----------------------------
# Creo DataFrame
# ----------------------------
results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "AUC_ROC", "AP_PR"]
)

# Ordino per AUC_ROC (facoltativo)
results_df = results_df.sort_values(by="AUC_ROC", ascending=False)

print("\n Confronto Finale Modelli \n")
print(results_df)