import numpy as np

# 1) Generatore con seed
rng = np.random.default_rng(123)

# 2) Quanti campioni voglio?
n = 10_000

# 3) Servono due array di Uniform(0,1)
u1 = rng.random(n)
u2 = rng.random(n)

# 4) Box–Muller: creo Z0 ~ N(0,1)
z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)

# (z1 sarebbe l'altro normale, se serve)
# z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)

# 5) Se voglio una normale con media mu e dev std sigma:
mu = 10.0
sigma = 3.0
x = mu + sigma * z0

# 6) Controllo veloce: media ~ mu, std ~ sigma
print("Media simulata:", x.mean())
print("Dev. std simulata:", x.std(ddof=0))
