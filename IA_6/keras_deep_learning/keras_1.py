# ============================================================
# ALLENA RETI NEURALI CON KERAS (TENSORFLOW)
# Lezione base - Classificazione MNIST
# ============================================================

# ------------------------------------------------------------
# 0) Import delle librerie
# ------------------------------------------------------------

import tensorflow as tf                 # libreria principale per deep learning
from tensorflow import keras             # Keras è l'API "alta" dentro TensorFlow
from tensorflow.keras import layers      # qui ci sono i "mattoni" della rete (Dense, Flatten, ecc.)

import numpy as np                       # calcoli numerici, array
import matplotlib.pyplot as plt          # grafici e visualizzazione immagini

print("TensorFlow version:", tf.__version__)
print("Keras è integrato in TensorFlow a partire dalla 2.0+")

# ------------------------------------------------------------
# 1) Carichiamo il dataset MNIST
# ------------------------------------------------------------
# MNIST = immagini 28x28 di cifre scritte a mano (0-9)
# Il dataset è già diviso in:
# - train (per imparare)
# - test (per valutare dopo l'allenamento)

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print("\nDimensioni dei dati:")
print("Train images:", x_train.shape)   # (60000, 28, 28) -> 60.000 immagini 28x28
print("Train labels:", y_train.shape)   # (60000,)        -> 60.000 etichette (numero 0..9)
print("Test  images:", x_test.shape)    # (10000, 28, 28) -> 10.000 immagini
print("Test  labels:", y_test.shape)    # (10000,)

# ------------------------------------------------------------
# 2) Esploriamo visivamente qualche esempio
# ------------------------------------------------------------
# Mostriamo 10 immagini del training set per capire com'è fatto il dataset

plt.figure(figsize=(10, 4))

for i in range(10):
    plt.subplot(2, 5, i + 1)                 # griglia 2 righe x 5 colonne
    plt.imshow(x_train[i], cmap="gray")      # immagine in scala di grigi
    plt.title(f"Label: {y_train[i]}")        # la classe vera (0..9)
    plt.axis("off")                          # togli assi

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3) Preprocessiamo i dati (passo fondamentale)
# ------------------------------------------------------------
# Le immagini sono pixel 0..255 (valori interi).
# Per le reti neurali è molto meglio usare valori piccoli tipo 0..1:
# - rende l'allenamento più stabile
# - spesso accelera la convergenza

x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

# In molti casi (soprattutto CNN - reti convoluzionali) si vuole una dimensione "canale":
# (N, 28, 28)  -> (N, 28, 28, 1)
# Qui 1 significa: 1 canale, perché è scala di grigi.
#
# axis=-1 significa: aggiungi la nuova dimensione ALLA FINE
# Prima: (60000, 28, 28)
# Dopo : (60000, 28, 28, 1)

x_train = np.expand_dims(x_train, axis=-1)
x_test  = np.expand_dims(x_test, axis=-1)

print("\nNuove forme dopo preprocessing:")
print("x_train:", x_train.shape)
print("x_test :", x_test.shape)

# ------------------------------------------------------------
# 4) Costruiamo la rete neurale (versione semplice - solo Dense)
# ------------------------------------------------------------
# Useremo un modello "Sequential":
# significa che i layer sono in fila, uno dopo l'altro.
#
# Architettura:
# Input (28,28,1)
# -> Flatten (trasforma matrice in vettore: 28*28 = 784)
# -> Dense(128, relu)
# -> Dense(64, relu)
# -> Dense(10, softmax)  (10 classi: cifre 0..9)
#
# Nota su Softmax:
# softmax produce una distribuzione di probabilità:
# es. [0.01, 0.02, ..., 0.90] -> la rete dice "credo che sia 9 con 90%"

model = keras.Sequential([
    layers.Input(shape=(28, 28, 1)),         # forma di UNA immagine (senza batch)
    layers.Flatten(),                        # (28,28,1) -> (784,)
    layers.Dense(128, activation="relu"),    # 128 neuroni, ReLU = attivazione comune
    layers.Dense(64, activation="relu"),     # secondo layer denso
    layers.Dense(10, activation="softmax")   # output: 10 probabilità
])

# ------------------------------------------------------------
# 5) Compiliamo il modello (scegliamo come imparare)
# ------------------------------------------------------------
# optimizer: come aggiorniamo i pesi (Adam è un'ottima scelta base)
# loss: funzione di errore
# - SparseCategoricalCrossentropy si usa quando y sono numeri interi (0..9), non one-hot
# metrics: cosa vogliamo vedere durante training (accuratezza)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Stampa una tabella del modello (layer, parametri, ecc.)
model.summary()

# ------------------------------------------------------------
# 6) Alleniamo la rete (training)
# ------------------------------------------------------------
# epochs = quante "passate" complete su tutti i dati di train
# validation_split = teniamo una parte del training set per controllare durante training

history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=128,
    validation_split=0.1
)

# ------------------------------------------------------------
# 7) Valutiamo sul test set (dati mai visti)
# ------------------------------------------------------------
test_loss, test_acc = model.evaluate(x_test, y_test)
print("\nRisultato su test:")
print("Loss:", test_loss)
print("Accuracy:", test_acc)

# ------------------------------------------------------------
# 8) Facciamo previsioni su alcune immagini
# ------------------------------------------------------------
# model.predict ritorna probabilità (softmax). Poi prendiamo la classe con argmax.

pred_probs = model.predict(x_test[:10])             # probabilità per 10 immagini
pred_labels = np.argmax(pred_probs, axis=1)         # classe scelta (indice del max)

print("\nPredizioni (prime 10):")
print("Vero     :", y_test[:10])
print("Predetto :", pred_labels)

# Visualizziamo le 10 immagini con predizione
plt.figure(figsize=(10, 4))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap="gray")    # squeeze: (28,28,1) -> (28,28)
    plt.title(f"V:{y_test[i]} P:{pred_labels[i]}")
    plt.axis("off")
plt.tight_layout()
plt.show()



# ------------------------------------------------------------
# 4) Costruiamo la rete neurale (versione semplice - solo Dense)
# ------------------------------------------------------------
# Useriamo keras.Sequential: significa "una lista di layer in sequenza",
# dove l'output di un layer va in input al layer successivo.

model = keras.Sequential([
    # Input: diciamo a Keras com'è fatta UNA singola immagine
    # (28, 28, 1) = altezza 28, larghezza 28, 1 canale (grigio)
    layers.Input(shape=(28, 28, 1)),

    # Flatten: trasforma la matrice 28x28 in un vettore lungo 784
    # 28*28 = 784 (i pixel diventano una "riga" di numeri)
    layers.Flatten(),

    # Dense = layer "denso" (fully connected): ogni neurone vede tutti gli input
    # activation='relu' è una funzione molto usata: lascia passare solo valori positivi
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),

    # Output finale: 10 neuroni (una classe per cifra 0..9)
    # softmax trasforma l'output in probabilità che sommano a 1
    layers.Dense(10, activation='softmax')
])

# Nota: a volte vedrai anche questa scrittura "più esplicita":
# (è equivalente; cambia solo lo stile)
"""
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28, 1)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
"""

# summary() stampa la struttura: layer, output shape, numero parametri
model.summary()

# ------------------------------------------------------------
# 5) Compiliamo il modello (loss, ottimizzatore, metriche)
# ------------------------------------------------------------
# optimizer='adam' = regola per aggiornare i pesi (molto usata, buon default)
# loss='sparse_categorical_crossentropy' = errore per classificazione multiclasse
#   "sparse" si usa perché le etichette sono interi (0..9), non one-hot.
# metrics=['accuracy'] = vogliamo vedere anche la percentuale di correttezza

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ------------------------------------------------------------
# 6) Addestriamo il modello
# ------------------------------------------------------------
print("\nInizio addestramento...\n")

# fit() = training vero e proprio
# epochs=8: quante "passate complete" sui dati di training
# batch_size=128: quante immagini insieme per ogni aggiornamento dei pesi
# validation_split=0.1: usa il 10% del TRAIN come validazione (non è il test)
# verbose=1: mostra la barra e i valori durante training

history = model.fit(
    x_train, y_train,
    epochs=8,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# ------------------------------------------------------------
# 7) Valutiamo sul test set (dati mai visti in training)
# ------------------------------------------------------------
# evaluate() calcola loss e accuracy sul test set
# verbose=0 = non stampa barra, solo ritorno valori

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)

print("\nRisultato sul test set:")
print(f"Accuracy: {test_acc:.4f}")
print(f"Loss:     {test_loss:.4f}")

# ------------------------------------------------------------
# 8) Facciamo alcune previsioni e le visualizziamo
# ------------------------------------------------------------
# Prendiamo 10 indici casuali dal test set
# replace=False => non ripete lo stesso indice due volte
indices = np.random.choice(len(x_test), size=10, replace=False)

plt.figure(figsize=(12, 6))

for i, idx in enumerate(indices):
    # img è una singola immagine del test set
    img = x_test[idx]
    true_label = y_test[idx]

    # model.predict si aspetta un BATCH di immagini, non una singola immagine.
    # Quindi aggiungiamo una dimensione davanti: (28,28,1) -> (1,28,28,1)
    # img[np.newaxis, ...] significa: "aggiungi una dimensione all'inizio"
    pred_probs = model.predict(img[np.newaxis, ...], verbose=0)[0]

    # argmax trova l'indice della probabilità più alta => classe predetta
    pred_label = np.argmax(pred_probs)

    # confidenza = probabilità della classe scelta (in percentuale)
    confidence = pred_probs[pred_label] * 100

    # Disegniamo l'immagine
    plt.subplot(2, 5, i + 1)
    plt.imshow(img.squeeze(), cmap='gray')  # squeeze: (28,28,1) -> (28,28)

    # Se la predizione è corretta, verde; se sbagliata, rosso
    color = 'green' if pred_label == true_label else 'red'

    plt.title(f"True: {true_label}\nPred: {pred_label} ({confidence:.1f}%)", color=color)
    plt.axis('off')

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Bonus: grafico andamento accuracy e loss (train vs validation)
# ------------------------------------------------------------
# history.history è un dizionario con i valori salvati ad ogni epoch.
# Chiavi tipiche:
# - 'accuracy', 'val_accuracy'
# - 'loss', 'val_loss'

plt.figure(figsize=(12, 4))

# Grafico Accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.title('Accuracy')
plt.legend()
plt.grid(True)

# Grafico Loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.legend()
plt.grid(True)

plt.show()