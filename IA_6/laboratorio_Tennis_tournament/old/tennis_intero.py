#!pip install ucimlrepo
import pandas as pd
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 
  
# Scarico dataset UCI (tutto il dataset)
tennis_major_tournament_match_statistics = fetch_ucirepo(id=300) 
  
# Features e target come DataFrame
X_row = tennis_major_tournament_match_statistics.data.features 
y_row = tennis_major_tournament_match_statistics.data.targets 

# Unisco in un unico dataframe (più comodo per EDA)
df = pd.concat([X_row, y_row], axis=1)

#print(X.head())
# metadata 
#print(tennis_major_tournament_match_statistics.metadata) 
  
# variable information 
 #print(tennis_major_tournament_match_statistics.variables) 


# Controlli base
print("Shape df:", df.shape)
print("\nColonne (prime 30):")
print(list(df.columns)[:30])

print("\nInfo:")
print(df.info())

# Separiamo X e y
y = df["Result"]      # target
X = df.drop("Result", axis=1)

print(X.dtypes.value_counts())
print("Vecchia shape:", X.shape)

categorical_cols = X.select_dtypes(include="object").columns
print("Colonne categoriche: ", categorical_cols)

# decisione didattica eliminiamo le colonne categoriche
    # eliminiamo Player1 / Player2 perche cosi evitiamo il bias da identita. Voliamo che il modello impara statistiche e non che Federer = vittoria
    # eliminiamo Tournament perche voliamo modello basato su statistiche match e non su dove si è svolto. È una semplificazione didattica.
X = X.drop(categorical_cols, axis=1)
print("Nuova shape:", X.shape)

# Controllo missing values

print(X.isnull().sum().sort_values(ascending=False))


# Definiamo le colonne da eliminare (Data Leakage + Target)
colonne_da_eliminare = [
    'ST1.1', 'ST1.2',         # Game set 1
    'ST2.1', 'ST2.2',         # Game set 2
    'ST3.1', 'ST3.2',         # Game set 3
    'ST4.1', 'ST4.2',         # Game set 4 
    'ST5.1', 'ST5.2',         # Game set 5                             
    'TPW.1', 'TPW.2',         # Punti totali (troppo vicini al risultato)  leakage!!
    'FNL1',  'FNL2'           # Risultato finale set                       leakage!!
]
print("Vecchia shape:", X.shape)

X = X.drop(colonne_da_eliminare, axis=1)

print("Features rimaste in X:")
print(X.columns.tolist())
print("Nuova shape:", X.shape)


# Media imputazione
for col in ["UFE.1","UFE.2","WNR.1","WNR.2",
            "NPA.1","NPA.2","NPW.1","NPW.2",
            "BPC.1","BPW.1","BPC.2","BPW.2"]:
    X[col] = X[col].fillna(X[col].mean())

# Zero imputazione
for col in ["ACE.1","ACE.2","DBF.1","DBF.2"]:
        X[col] = X[col].fillna(0)

print(X.isnull().sum())

# .....     Grafici EDA ......

import pandas as pd

df_plot = X.copy()
df_plot["Result"] = y

# Boxplot per ogni singola feature (uno alla volta)
# Serve per:
#     vedere outlier
#     vedere scala
#     vedere distribuzione

# Boxplot per ogni singola feature (uno alla volta)
import math
import matplotlib.pyplot as plt

cols = list(X.columns)

per_fig = 6   # quanti boxplot per figura
n_fig = math.ceil(len(cols) / per_fig)

for f in range(n_fig):

    subset = cols[f*per_fig:(f+1)*per_fig]

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    axes = axes.ravel()

    for ax, col in zip(axes, subset):
        ax.boxplot(X[col].dropna())
        ax.set_title(col)
        ax.set_xticks([])

    # Se restano celle vuote → le spegniamo
    for ax in axes[len(subset):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()

# Boxplot per classe (Result=0 vs Result=1)
                    
# Serve per verificare se:
#     La mediana (linea nel box) è diversa tra 0 e 1?
#     I box sono separati o sovrapposti?
#     Una classe ha valori molto più alti?

# Se sì → quella feature distingue bene le classi e quindi aiuta a prevedere Result

import math
import seaborn as sns
import matplotlib.pyplot as plt

cols = list(X.columns)
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


corr_target = df_corr.corr()['Result'].sort_values(ascending=False)

print(corr_target)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,   # 20% test
    stratify=y,      # mantiene proporzione classi
    random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


#adestramento Decision Tree

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train, y_train)

y_pred = tree_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)



#confusion matrix

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Decision Tree - Confusion Matrix")
plt.show()



# Classification Report (Precision, Recall, F1)

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))


#ROC Curve e AUC - separazione generale

from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

y_proba = tree_model.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_proba)
auc_score = roc_auc_score(y_test, y_proba)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
plt.plot([0,1],[0,1],"--")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.title("ROC Curve - Decision Tree")
plt.legend()
plt.show()
print(auc_score)


from sklearn.tree import DecisionTreeClassifier, plot_tree
plt.figure(figsize=(20, 10))
plot_tree(tree_model,
          feature_names=X_train.columns,
          class_names=['Vince P2', 'Vince P1'],
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Logica del Decision Tree")
plt.show()

#  Random Forest e Gradient Boosting
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Random Forest
rf_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_proba = rf_model.predict_proba(X_test)[:, 1]

# Gradient Boosting
gb_model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
gb_model.fit(X_train, y_train)

gb_pred = gb_model.predict(X_test)
gb_proba = gb_model.predict_proba(X_test)[:, 1]

# Accuracy
print("Decision Tree:", accuracy_score(y_test, y_pred))
print("Random Forest:", accuracy_score(y_test, rf_pred))
print("Gradient Boosting:", accuracy_score(y_test, gb_pred))

# AUC
print("Tree AUC:", roc_auc_score(y_test, y_proba))
print("RF AUC:", roc_auc_score(y_test, rf_proba))
print("GB AUC:", roc_auc_score(y_test, gb_proba))


#    Estrazione Feature Importance
import pandas as pd

importances = rf_model.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
})

feature_importance_df = feature_importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(feature_importance_df)


# Grafico Feature Importance
import matplotlib.pyplot as plt

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


#     Cross-Validation Decision Tree
from sklearn.model_selection import cross_val_score

tree_cv_scores = cross_val_score(
    tree_model,
    X_train,
    y_train,
    cv=5,
    scoring="roc_auc"
)

print("Tree CV AUC:", tree_cv_scores)
print("Media Tree:", tree_cv_scores.mean())


#     Cross-Validation Random Forest
rf_cv_scores = cross_val_score(
    rf_model,
    X_train,
    y_train,
    cv=5,
    scoring="roc_auc"
)

print("RF CV AUC:", rf_cv_scores)
print("Media RF:", rf_cv_scores.mean())


#     Cross-Validation Gradient Boosting
gb_cv_scores = cross_val_score(
    gb_model,
    X_train,
    y_train,
    cv=5,
    scoring="roc_auc"
)

print("GB CV AUC:", gb_cv_scores)
print("Media GB:", gb_cv_scores.mean())


#    Confronto finale
# La cross-validation è stata utilizzata per stimare la performance attesa dei modelli e confrontarne la robustezza.
print("\n=== CV AUC Media ===")

print(f"Decision Tree: {tree_cv_scores.mean():.3f}")
print(f"Random Forest: {rf_cv_scores.mean():.3f}")
print(f"Gradient Boosting: {gb_cv_scores.mean():.3f}")


#     Cambiamo famigli di modelli da alberi a Logistic Regression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# Pipeline
logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression(max_iter=1000))
])

# Fit
logistic_pipeline.fit(X_train, y_train)

# Predict
log_pred = logistic_pipeline.predict(X_test)
log_proba = logistic_pipeline.predict_proba(X_test)[:, 1]

# Metriche
print("Logistic Accuracy:", accuracy_score(y_test, log_pred))
print("Logistic AUC:", roc_auc_score(y_test, log_proba))


#    ROC curve - separazione generale
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# Probabilità
tree_proba = tree_model.predict_proba(X_test)[:, 1]
rf_proba   = rf_model.predict_proba(X_test)[:, 1]
gb_proba   = gb_model.predict_proba(X_test)[:, 1]
log_proba  = logistic_pipeline.predict_proba(X_test)[:, 1]

# ROC curve
fpr_tree, tpr_tree, _ = roc_curve(y_test, tree_proba)
fpr_rf,   tpr_rf,   _ = roc_curve(y_test, rf_proba)
fpr_gb,   tpr_gb,   _ = roc_curve(y_test, gb_proba)
fpr_log, tpr_log,   _ = roc_curve(y_test, log_proba)


# AUC
auc_tree = roc_auc_score(y_test, tree_proba)
auc_rf   = roc_auc_score(y_test, rf_proba)
auc_gb   = roc_auc_score(y_test, gb_proba)
auc_log  = roc_auc_score(y_test, log_proba)


# Grafico
plt.figure(figsize=(8,6))

plt.plot(fpr_tree, tpr_tree,
         label=f"Decision Tree (AUC={auc_tree:.3f})")

plt.plot(fpr_rf, tpr_rf,
         label=f"Random Forest (AUC={auc_rf:.3f})")

plt.plot(fpr_gb, tpr_gb,
         label=f"Gradient Boosting (AUC={auc_gb:.3f})")

plt.plot(fpr_log, tpr_log,
         label=f"Logistic (AUC={auc_log:.3f})")

# linea casuale
plt.plot([0,1], [0,1], "--", color="gray")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Confronto Modelli")
plt.legend()

plt.show()

#     PR curve - focus sui positivi
from sklearn.metrics import precision_recall_curve, auc
import matplotlib.pyplot as plt

# Probabilità
tree_proba = tree_model.predict_proba(X_test)[:, 1]
rf_proba   = rf_model.predict_proba(X_test)[:, 1]
gb_proba   = gb_model.predict_proba(X_test)[:, 1]
log_proba  = logistic_pipeline.predict_proba(X_test)[:, 1]

# PR curve
precision_tree, recall_tree, _ = precision_recall_curve(y_test, tree_proba)
precision_rf, recall_rf, _     = precision_recall_curve(y_test, rf_proba)
precision_gb, recall_gb, _     = precision_recall_curve(y_test, gb_proba)
precision_log, recall_log, _  = precision_recall_curve(y_test, log_proba)

# AP
ap_tree = auc(recall_tree, precision_tree)
ap_rf   = auc(recall_rf, precision_rf)
ap_gb   = auc(recall_gb, precision_gb)
ap_log  = auc(recall_log, precision_log)

# Grafico
plt.figure()

plt.plot(recall_tree, precision_tree,
         label=f"Decision Tree (AP={ap_tree:.3f})")

plt.plot(recall_rf, precision_rf,
         label=f"Random Forest (AP={ap_rf:.3f})")

plt.plot(recall_gb, precision_gb,
         label=f"Gradient Boosting (AP={ap_gb:.3f})")

plt.plot(recall_log, precision_log,
         label=f"Logistic (AP={ap_gb:.3f})")

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve - Confronto Modelli")
plt.legend()

plt.show()


