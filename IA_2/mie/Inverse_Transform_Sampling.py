import numpy as np

# 1) Creo un generatore con seed (riproducibile)
rng = np.random.default_rng(123)

# 2) Parametro dell'esponenziale: rate lambda (eventi per unità di tempo)
lam = 2.0  # esempio: 2 eventi per unità di tempo

# 3) Genero tanti Uniform(0,1)
n = 10_000
u = rng.random(n)  # array di numeri tra 0 e 1

# 4) Inverse Transform: X = F^{-1}(U)
#    Per Exp(lam): X = -ln(1-U)/lam
x = -np.log(1 - u) / lam

# 5) Controllo veloce: la media teorica di Exp(lam) è 1/lam
print("Media simulata:", x.mean())
print("Media teorica :", 1 / lam)
