import numpy as np

#  DISCRETE

# Bernouli 

d_bern = np.random.binomial(n=1, p=0.5, size=10)  #  è come lanciare 10 monete
    # n=1 → una prova sola → quindi Bernoulli
    # p=0.5 → probabilità di successo
    # size=10 → quante volte ripeto l’esperimento
print("\nBernouli: ", d_bern, "sucesso o falimento in ognuno di 10 lanci")


# Binomiale

d_bin = np.random.binomial(n=5, p=0.3, size=8)
    # n=10 → quante prove per esperimento
    # p=0.3 → probabilità di successo
    # size=10 → quante volte ripeto l’esperimento
print("\nBinomiale: ", d_bin, "mostra quantita di sucessi in 5 lanci della moneta\
      \n esperimento si ripete 8 volte")


# Uniforme discreta

d_unif_d = np.random.randint(1, 7, size=10)
    # 1 → minimo incluso
    # 7 → massimo escluso
    # size=10 → lanci
print("\nUniforme discreta: ", d_unif_d, "valori equiprobabili da 1 a 6, come dado in 10 lanci")


# Poisson

d_pois = np.random.poisson(lam=3, size=5)
    # lam  -> λ = media degli eventi
    # size -> 
print("\nPoisson: ", d_pois, "Numero di eventi osservati in un intervallo di tempo\
      \n esperimento è ripetuto 5 volte")


# Geometrica

d_geom = np.random.geometric(p=0.2, size=10)
    # p -> probabilita di successo
    # size -> numero di osservazioni
print("\nGeometrica: ", d_geom, "Ogni numero = quante prove sono servite per ottenere il primo successo in 10 esperimenti")


#  CONTINUE

# Uniforme continua

d_unif_c = np.random.uniform(0, 1, size=5)
    # 0 → minimo
    # 1 → massimo
    # size=5 → campioni
print("\nUniforme continua: ", d_unif_c, "array di 5 valori casuali")


# Normale / Gausiana

d_norm = np.random.normal(loc=0, scale=1, size=7)
    # loc → media μ =0
    # scale → deviazione standard σ = 1
    # size=7 → osservazioni
print("\nNormale / Gausiana: ", d_norm, "risultato = misure attorno a una media")

# Esponenziale

d_esp = np.random.exponential(scale=0.5, size=5)
    # scale ->  tempo medio di attesa = 0.5,  quindi λ = 2 eventi per unità di tempo
    # size -> 
print("\nEsponenziale: ", d_esp, "tempo di attesa fino al prossimo evento.\
      \n 5 tempi di attesa simulati")