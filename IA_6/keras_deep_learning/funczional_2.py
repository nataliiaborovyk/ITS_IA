import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Dataset
X = np.random.rand(1000, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# Split
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# Modello Functional
inputs = Input(shape=(2,))
x = Dense(8, activation='relu')(inputs)
x = Dense(4, activation='relu')(x)
outputs = Dense(1, activation='sigmoid')(x)
model_fun = Model(inputs, outputs)

# Compile
model_fun.compile(
    optimizer=SGD(learning_rate=0.1),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Callbacks
early_stop = EarlyStopping(
    monitor='val_loss', patience=5, restore_best_weights=True)
checkpoint = ModelCheckpoint(
    "./IA_6/keras_deep_learning/best_model_fun.keras", monitor='val_loss', save_best_only=True)

# Fit
history_fun = model_fun.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_val, y_val),
    callbacks=[early_stop, checkpoint],
    verbose=1
)

# Evaluate
test_loss, test_acc = model_fun.evaluate(X_test, y_test, verbose=0)
print("\nTest (model in RAM):", test_loss, test_acc)

best_model = load_model("./IA_6/keras_deep_learning/best_model_fun.keras")
best_test_loss, best_test_acc = best_model.evaluate(X_test, y_test, verbose=0)
print("Test (BEST checkpoint):", best_test_loss, best_test_acc)

# Predict + sklearn metriche
y_prob = best_model.predict(X_test, verbose=0)
y_pred = (y_prob > 0.5).astype(int).reshape(-1)

print("\nAccuracy sklearn:", accuracy_score(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print("Report:\n", classification_report(y_test, y_pred))

# Grafici
plt.plot(history_fun.history['loss'])
plt.plot(history_fun.history['val_loss'])
plt.title("Loss (Functional)")
plt.legend(["Train", "Val"])
plt.show()