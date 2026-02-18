import pandas as pd

df = pd.read_csv("AusOpen-men-2013.csv")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

print("\nInfo:")
print(df.info())

print("\nDescribe:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())


X = df.drop(["Result", "Player1", "Player2", 
             "ST1.1", "ST1.2",
             "ST2.1", "ST2.2",
             "ST3.1", "ST3.2",
             "ST4.1", "ST4.2", 
             "ST5.1", "ST5.2",
             "NPW.1", "NPW.2",
             "TPW.1", "TPW.2",
             "FNL1", "FNL2"
            ], axis=1)
y = df["Result"]

print(df["Result"].value_counts())
print(X.dtypes.value_counts())




# X.head()

# nel Net Points (NPA / NPW) coctituiamo con la media per valutazione del esperto 

X["NPA.1"].fillna(X["NPA.1"].mean(), inplace=True)
X["NPA.2"].fillna(X["NPA.2"].mean(), inplace=True)

X["DBF.1"] = X["DBF.1"].fillna(0)
X["DBF.2"] = X["DBF.2"].fillna(0)

print("\nMissing values:")
print(X.isnull().sum())

import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
X.boxplot()
plt.xticks(rotation=90)
plt.show()

X.hist(figsize=(20,15))
plt.show()

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train, y_train)

y_pred = tree_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))