import numpy as np
import matplotlib.pyplot as plt



# Parametri della distribuzione
a = 2
# estremo sinistro
b = 8
# estremo destro
# Asse x
x = np.linspace(a - 2, b + 2, 400)
# np.linspace(start, stop, num)  Genera num numeri “spaziati in modo uniforme” tra start e stop (inclusi).

# PDF della distribuzione uniforme
pdf = np.where((x >= a) & (x <= b),   1 / (b - a),   0)
# np.where(condizione, valore_se_vero, valore_se_falso)

# Grafico
# plt.figure()
# plt.plot(x, pdf,'.')
# plt.title(f"PDF - Distribuzione Uniforme U({a}, {b})")
# plt.xlabel("x")
# plt.ylabel("f(x)")
# plt.grid()
# plt.show()

#oppure

from scipy.stats import uniform

valori_X = np.linspace(a - 2, b + 2, 400)
pdf_2 = uniform.pdf(valori_X, loc=2, scale=6) # a=loc b=loc+scale

cdf_2 = uniform.cdf(valori_X, loc=2, scale=6) # a=loc b=loc+scale
# cdf_uniform = np.where(x < 0, 0, np.where(x > 1, 1, x))

plt.figure()
plt.subplot(1,2,1)
plt.plot(valori_X, pdf_2, '.')
plt.title('distribuzione uniforme')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()

plt.subplot(1,2,2)
plt.plot(valori_X, cdf_2, '.')
plt.title('distribuzione uniforme')
plt.xlabel('x')
plt.ylabel('F(x)')
plt.grid()
plt.show()

# # np.random.uniform(low, high, size)
# # dove:
#     # low → valore minimo (INCLUSO)
#     # high → valore massimo (ESCLUSO)
#     # size → quante estrazioni vuoi


a= 2
b= 8
n_estrazioni = 50000

# Simulazione di una variabile uniforme U(a, b)

dati_simulati = np.random.uniform(a, b, n_estrazioni)


valori_X = np.linspace(a, b, 300)    # Asse valori_X per la densità teorica

pdf = np.ones_like(valori_X) / (b - a)   # crea un array di 1, con stessa lungezza di valori_X

# pdf = [1/(b-a), 1/(b-a), 1/(b-a), ..., 1/(b-a)]

# plt.figure(figsize=(8,5))

# # Istogramma normalizzato (density=True)

# plt.hist(dati_simulati, bins=40, density=True)
# # bins: in quante parti divido l’asse x
# # density=True --> l’area totale dell’istogramma = 1

# # Curva della PDF teorica
# plt.plot(valori_X, pdf)
# plt.xlabel("valori_X")
# plt.ylabel("Densità")
# plt.title("Distribuzione Uniforme U(a, b) simulata")
# plt.grid(True)
# plt.show()

print(dati_simulati.var())

var_teorica = (b-a)**2 / 12
print(var_teorica)



# PDF	uniform.pdf(x, loc=a, scale=b-a)
# CDF	uniform.cdf(x, loc=a, scale=b-a)
# PPF	uniform.ppf(p, loc=a, scale=b-a)
# RVS	uniform.rvs(loc=a, scale=b-a, size=n)

#  Parametri:
#     a = inizio intervallo
#     b = a + scale