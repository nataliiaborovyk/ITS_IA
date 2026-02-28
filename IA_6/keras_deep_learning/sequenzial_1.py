import numpy as np
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

# ----- Dataset finto (stile XOR esteso) -----
X = np.random.rand(1000, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)  # etichetta 0/1 semplice

# ----- Split: train / val / test -----
X_temp, X_test, y_temp, y_test = train_test_split(
   X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
   X_temp, y_temp, test_size=0.25, random_state=42
)

# ----- Modello (Sequential) -----
model_seq = Sequential()
model_seq.add(Dense(8, input_dim=2, activation='relu'))
model_seq.add(Dense(4, activation='relu'))
model_seq.add(Dense(1, activation='sigmoid'))

model_seq.compile(
   optimizer=SGD(learning_rate=0.1),
   loss='binary_crossentropy',
   metrics=['accuracy']
)

# ----- Fit -----
history_seq = model_seq.fit(
   X_train, y_train,
   epochs=20,
   batch_size=32,
   validation_data=(X_val, y_val),
   verbose=1  # Stampa barra di progresso + metriche per epoca o batch.
              # verbose = 0  Non stampa nulla.
              # verbose = 2 Stampa una riga per epoca, senza barra grafica.
)

# ----- Cosa restituisce fit (history) -----
print("\nChiavi disponibili in history:")
print(history_seq.history.keys())

print("\nUltima epoca:")
print("train_loss =", history_seq.history['loss'][-1])
print("train_acc  =", history_seq.history['accuracy'][-1])
print("val_loss   =", history_seq.history['val_loss'][-1])
print("val_acc    =", history_seq.history['val_accuracy'][-1])

# ----- Test -----    evaluate = forward + loss + metriche
test_loss, test_acc = model_seq.evaluate(X_test, y_test, verbose=0)

print("\nTest:")
print("test_loss =", test_loss)
print("test_acc  =", test_acc)


# ----- Grafico Loss -----
import matplotlib.pyplot as plt

plt.plot(history_seq.history['loss'])
plt.plot(history_seq.history['val_loss'])

plt.title("Loss durante training")
plt.xlabel("Epoche")
plt.ylabel("Loss")

plt.legend(["Train", "Validation"])
plt.show()

# ----- Grafico Accuracy -----
plt.plot(history_seq.history['accuracy'])
plt.plot(history_seq.history['val_accuracy'])

plt.title("Accuracy durante training")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")

plt.legend(["Train", "Validation"])
plt.show()
