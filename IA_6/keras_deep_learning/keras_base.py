from keras.models import Sequential		# → contenitore della rete
from keras.layers import Dense			# → layer fully connected
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import numpy as np

# ----- Dataset finto -----
X = np.random.rand(1000, 2)
y = np.random.randint(0, 2, 1000)

# ----- Split -----
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42
)

# ----- Modello -----
model = Sequential()
model.add(Dense(3, input_dim=2, activation='relu')) 
                # input_dim=2 Perché hai 2 feature: x1, x2
model.add(Dense(1, activation='sigmoid'))

model.compile(
    optimizer='sgd',  # Usa gradient descent classico.
    loss='binary_crossentropy', # Loss per classificazione binaria L = −[ y·log(ŷ) + (1−y)·log(1−ŷ) ]
    metrics=['accuracy']
)

# ----- Training -----

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    X_train,
    y_train,
    epochs=20,
    validation_data=(X_val, y_val),
    batch_size=32,
    callbacks=[early_stop]
)

# ----- Test -----
test_loss, test_acc = model.evaluate(X_test, y_test)
# loss, accuracy = model.evaluate(X, y)

print("\nRisultati finali:")
print("Test loss:", test_loss)
print("Test accuracy:", test_acc)

# ----- Accesso storico metriche -----
print("\nUltima training loss:", history.history['loss'][-1])
print("Ultima validation loss:", history.history['val_loss'][-1])