import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"     # forza CPU
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"      # riduce log (0=all, 1=INFO-, 2=WARNING-, 3=ERROR-)


import numpy as np
from sklearn.model_selection import train_test_split

from keras.models import Model
from keras.layers import Input, Dense
from keras.optimizers import SGD

# ----- Dataset finto -----
X = np.random.rand(1000, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# ----- Split: train / val / test -----
X_temp, X_test, y_temp, y_test = train_test_split(
   X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
   X_temp, y_temp, test_size=0.25, random_state=42
)

# ----- Modello (Functional) -----
inputs = Input(shape=(2,))
x = Dense(8, activation='relu')(inputs)
x = Dense(4, activation='relu')(x)
outputs = Dense(1, activation='sigmoid')(x)

model_fun = Model(inputs=inputs, outputs=outputs)

model_fun.compile(
   optimizer=SGD(learning_rate=0.1),
   loss='binary_crossentropy',
   metrics=['accuracy']
)

# ----- Fit -----
history_fun = model_fun.fit(
   X_train, y_train,
   epochs=20,
   batch_size=32,
   validation_data=(X_val, y_val),
   verbose=1
)

print("\nChiavi disponibili in history:")
print(history_fun.history.keys())

print("\nUltima epoca:")
print("train_loss =", history_fun.history['loss'][-1])
print("train_acc  =", history_fun.history['accuracy'][-1])
print("val_loss   =", history_fun.history['val_loss'][-1])
print("val_acc    =", history_fun.history['val_accuracy'][-1])

# ----- Test -----
test_loss, test_acc = model_fun.evaluate(X_test, y_test, verbose=0)
print("\nTest:")
print("test_loss =", test_loss)
print("test_acc  =", test_acc)

# ----- Grafico Loss -----
import matplotlib.pyplot as plt

plt.plot(history_fun.history['loss'])
plt.plot(history_fun.history['val_loss'])

plt.title("Loss durante training")
plt.xlabel("Epoche")
plt.ylabel("Loss")

plt.legend(["Train", "Validation"])
plt.show()

# ----- Grafico Accuracy -----
plt.plot(history_fun.history['accuracy'])
plt.plot(history_fun.history['val_accuracy'])

plt.title("Accuracy durante training")
plt.xlabel("Epoche")
plt.ylabel("Accuracy")

plt.legend(["Train", "Validation"])
plt.show()
