import numpy as np
import matplotlib.pyplot as plt

# Schema logico (passo-passo)

# Input: p, N
# Processo:
    # genero N risultati casuali (0/1)
    # calcolo la somma progressiva
    # divido per 1..N per ottenere le medie progressive
    # confronto con la media teorica p
    # Output: grafico + ultimo valore della media


# # 1) Parametri dell'esperimento
# p = 0.6          # probabilità di successo (media teorica = 0.6)
# N = 10000        # numero di prove (più è grande, meglio si vede la LLN)

# # 2) Simulazione: generiamo N valori 0/1 con probabilità p di ottenere 1
# #    np.random.binomial(n=1, p=p, size=N) produce N lanci di Bernoulli
# campione = np.random.binomial(n=1, p=p, size=N)

# # 3) Somma progressiva: [x1, x1+x2, x1+x2+x3, ...]
# somma_progressiva = np.cumsum(campione)

# # 4) Indici 1..N (servono per dividere correttamente)
# n = np.arange(1, N + 1)

# # 5) Media progressiva: (x1)/1, (x1+x2)/2, ..., (x1+...+xN)/N
# media_progressiva = somma_progressiva / n

# # 6) Stampiamo l'ultima media (dopo N prove)
# print("Media teorica =", p)
# print("Media campionaria (dopo N prove) =", media_progressiva[-1])

# # 7) Grafico: media progressiva e linea della media teorica
# plt.plot(n, media_progressiva)    
# plt.axhline(y=p, linestyle="--")  # linea orizzontale alla media teorica
# plt.xlabel("Numero di prove (n)")
# plt.ylabel("Media progressiva")
# plt.title("Legge dei Grandi Numeri: la media campionaria tende a p")
# plt.show()


# LGN
osservazioni = 1000
mu = 3.5
media = []
lanci = []
somma = 0

for i in range(1, osservazioni+1):
    dado = np.random.randint(1,7)
    somma += dado
    avg = somma/i
    media.append(avg)
    lanci.append(i)

plt.plot(lanci, media)
plt.axhline(mu, linestyle='--')
plt.title('LGN')
plt.show()


#CLT
simulazioni = 1000
campione = 30
medie = []

for i in range(simulazioni):
    somma = 0
    for k in range(campione):
        dado = np.random.randint(1,7)
        somma += dado
    avg = somma / campione
    medie.append(avg)

plt.hist(medie, bins=30)
plt.xlabel('Media campionaria')
plt.ylabel('Frequenza')
plt.title('CLT')
plt.show()
