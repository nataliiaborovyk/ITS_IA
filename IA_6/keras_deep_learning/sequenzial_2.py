import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from keras.models import Sequential, load_model
from keras.layers import Dense, Input
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint

# ----------------------------
# 0) (Opzionale) rendere output TF meno rumoroso
# ----------------------------
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 2 = no WARNING/INFO (spesso basta)

# ----------------------------
# 1) Dataset finto
# ----------------------------
X = np.random.rand(1000, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# ----------------------------
# 2) Split: train / val / test
# ----------------------------
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42
)

# ----------------------------
# 3) Modello (Sequential) - stile consigliato: Input(shape)
# ----------------------------
model_seq = Sequential([
    Input(shape=(2,)),
    Dense(8, activation='relu'),
    Dense(4, activation='relu'),
    Dense(1, activation='sigmoid')
])

# ----------------------------
# 4) Compile
# ----------------------------
model_seq.compile(
    optimizer=SGD(learning_rate=0.1),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ----------------------------
# 5) Callbacks: EarlyStopping + ModelCheckpoint
# ----------------------------
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath="./IA_6/keras_deep_learning/best_model_seq.keras",  # file creato sul disco
    monitor='val_loss',
    save_best_only=True
)

# ----------------------------
# 6) Fit
# ----------------------------
history_seq = model_seq.fit(
    X_train, y_train,
    epochs=100,              # metto alto, tanto early stopping fermerà prima
    batch_size=32,
    validation_data=(X_val, y_val),
    callbacks=[early_stop, checkpoint],
    verbose=1
)

# ----------------------------
# 7) Metriche finali da history
# ----------------------------
print("\nChiavi disponibili in history:")
print(history_seq.history.keys())

print("\nUltima epoca (valori):")
print("train_loss =", history_seq.history['loss'][-1])
print("train_acc  =", history_seq.history['accuracy'][-1])
print("val_loss   =", history_seq.history['val_loss'][-1])
print("val_acc    =", history_seq.history['val_accuracy'][-1])

# ----------------------------
# 8) Evaluate sul test (modello attuale in RAM)
# ----------------------------
test_loss, test_acc = model_seq.evaluate(X_test, y_test, verbose=0)
print("\nTest (model attuale in RAM):")
print("test_loss =", test_loss)
print("test_acc  =", test_acc)

# ----------------------------
# 9) Carico il BEST model salvato dal checkpoint e rivaluto sul test
# ----------------------------
best_model = load_model("./IA_6/keras_deep_learning/best_model_seq.keras")
best_test_loss, best_test_acc = best_model.evaluate(X_test, y_test, verbose=0)

print("\nTest (BEST model dal checkpoint):")
print("best_test_loss =", best_test_loss)
print("best_test_acc  =", best_test_acc)

# ----------------------------
# 10) Predict + soglia -> classi + metriche sklearn
# ----------------------------
y_prob = best_model.predict(X_test, verbose=0)            # probabilità (N,1)
y_pred = (y_prob > 0.5).astype(int).reshape(-1)          # classi (N,)

acc_sklearn = accuracy_score(y_test, y_pred)
print("\nAccuracy calcolata con sklearn:", acc_sklearn)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification report:")
print(classification_report(y_test, y_pred))

# ----------------------------
# 11) Grafici: loss e accuracy
# ----------------------------
plt.plot(history_seq.history['loss'])
plt.plot(history_seq.history['val_loss'])
plt.title("Loss durante training")
plt.xlabel("Epoche")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])
plt.show()

plt.plot(history_seq.history['accuracy'])
plt.plot(history_seq.history['val_accuracy'])
plt.title("Accuracy durante training")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])
plt.show()

# ----------------------------
# 12) (Opzionale) Salvo anche il modello finale in RAM
# ----------------------------
model_seq.save("./IA_6/keras_deep_learning/final_model_seq.keras")
print("\nSalvati: best_model_seq.keras e final_model_seq.keras")