

import numpy as np
from scipy import stats


def separatore(titolo: str) -> None:
    print("\n" + "-" * 60)
    print(titolo)
    print("-" * 60)


def main() -> None:
    # RNG (Random Number Generator) con seed fisso: stessi risultati ad ogni run
    rng = np.random.default_rng(seed=42)

    # rvs (Random Variates Samples) 
    # .rvs() → campioni casuali
    # .pmf() / .pdf() → funzione di probabilità
    # .cdf() → funzione cumulativa
    # .mean() → valore atteso
    # .var() → varianza
    # .ppf(probabilita) -> da z, inversa di cdf

    # ============================================================
    # 1) Bernoulli (discreta) - "moneta": 0/1
    # ============================================================
    separatore("1) Bernoulli (moneta) - stats.bernoulli(p)")
    p = 0.5

    # Creo l'oggetto distribuzione:
    # Definisco la variabile aleatoria X ~ Bernoulli(p=0.5)
    bern = stats.bernoulli(p=p)   # definisco la distribuzione

    # Campioni casuali (equivalente concettuale a np.random.binomial(n=1, p=p, size=...))
    campioni = bern.rvs(size=10, random_state=rng)
        # random_state=rng -> usa questo generatore casuale, con questo seed, così il risultato è riproducibile
    print("Campioni (10 lanci):", campioni)

    # PMF: P(X = x) per x in {0, 1}
    print("PMF P(X=0):", bern.pmf(0))
    print("PMF P(X=1):", bern.pmf(1))

    # CDF: P(X <= x)
    print("CDF P(X<=0):", bern.cdf(0))
    print("CDF P(X<=1):", bern.cdf(1))

    # Media e varianza teoriche (da formula, non dai campioni)
    # stats(..., moments='mv') ritorna (mean, var)
    media, varianza = bern.stats(moments="mv")
    print("Media teorica:", float(media))
    print("Varianza teorica:", float(varianza))



    # ============================================================
    # 2) Binomiale (discreta) - numero di successi su n prove
    # ============================================================
    separatore("2) Binomiale - stats.binom(n, p)")
    n = 5
    p = 0.3
    binom = stats.binom(n=n, p=p)

    campioni = binom.rvs(size=8, random_state=rng)
    print("Campioni (8 esperimenti, ognuno con n=5 prove):", campioni)
    print("Interpretazione: ogni numero = quanti successi in 5 prove")

    # Esempio PMF: probabilità di avere esattamente k successi
    k = 2
    print(f"PMF P(X={k}) =", binom.pmf(k))

    # Esempio CDF: probabilità di avere al massimo k successi
    print(f"CDF P(X<={k}) =", binom.cdf(k))

    media, varianza = binom.stats(moments="mv")
    print("Media teorica:", float(media), "(= n*p)")
    print("Varianza teorica:", float(varianza), "(= n*p*(1-p))")



    # ============================================================
    # 3) Uniforme discreta (dado) - valori equiprobabili
    # ============================================================
    separatore("3) Uniforme discreta (dado) - stats.randint(low, high)")
    # randint(low, high) genera interi in [low, high)  (high escluso!)
    low = 1
    high = 7  # 7 escluso -> {1,2,3,4,5,6}
    dado = stats.randint(low=low, high=high)

    campioni = dado.rvs(size=10, random_state=rng)
    print("Campioni (10 lanci):", campioni)

    # PMF: per un dado giusto, P(X=x) = 1/6 per x=1..6
    print("PMF P(X=1):", dado.pmf(1))
    print("PMF P(X=6):", dado.pmf(6))

    # CDF: P(X <= x)
    print("CDF P(X<=3):", dado.cdf(3))

    media, varianza = dado.stats(moments="mv")
    print("Media teorica:", float(media))
    print("Varianza teorica:", float(varianza))



    # ============================================================
    # 4) Poisson (discreta) - numero di eventi in un intervallo
    # ============================================================
    separatore("4) Poisson - stats.poisson(mu=lambda)")
    lam = 3  # lambda = numero medio di eventi in 1 intervallo di riferimento
    pois = stats.poisson(mu=lam)

    # size=5 = ripeto 5 volte lo stesso scenario:
    # "quanti eventi in 1 intervallo?"
    campioni = pois.rvs(size=5, random_state=rng)
    print("Campioni (5 intervalli):", campioni)
    print("Interpretazione: ogni numero = eventi osservati in UN intervallo")

    # PMF: P(X = k)
    k = 4
    print(f"PMF P(X={k}) =", pois.pmf(k))

    # CDF: P(X <= k)
    print(f"CDF P(X<={k}) =", pois.cdf(k))

    media, varianza = pois.stats(moments="mv")
    print("Media teorica:", float(media), "(= lambda)")
    print("Varianza teorica:", float(varianza), "(= lambda)")



    # ============================================================
    # 5) Geometrica (discreta) - prove fino al primo successo
    # ============================================================
    separatore("5) Geometrica - stats.geom(p)  (supporto: 1,2,3,...)")
    p = 0.2
    geom = stats.geom(p=p)

    campioni = geom.rvs(size=10, random_state=rng)
    print("Campioni (10 esperimenti):", campioni)
    print("Interpretazione: ogni numero = quante prove servono per il primo successo")

    # PMF: P(X = k) = (1-p)^(k-1) * p
    k = 3
    print(f"PMF P(X={k}) =", geom.pmf(k))

    # CDF: P(X <= k) = 1 - (1-p)^k
    print(f"CDF P(X<={k}) =", geom.cdf(k))

    media, varianza = geom.stats(moments="mv")
    print("Media teorica:", float(media), "(= 1/p)")
    print("Varianza teorica:", float(varianza), "(= (1-p)/p^2)")



    # ============================================================
    # 6) Uniforme continua - valori equiprobabili in [a, b]
    # ============================================================
    separatore("6) Uniforme continua - stats.uniform(loc=a, scale=b-a)")
    a = 0.0
    b = 1.0
    # In SciPy: uniform(loc, scale) rappresenta [loc, loc+scale]
    unif = stats.uniform(loc=a, scale=b - a)

    campioni = unif.rvs(size=5, random_state=rng)
    print("Campioni (5 valori):", campioni)

    # PDF: densità f(x), NON è una probabilità puntuale
    x = 0.25
    print(f"PDF f({x}) =", unif.pdf(x))

    # CDF: P(X <= x)
    print(f"CDF F({x}) = P(X<={x}) =", unif.cdf(x))

    # Probabilità su un intervallo [u, v]:
    # P(u <= X <= v) = F(v) - F(u)
    u, v = 0.2, 0.6
    prob_intervallo = unif.cdf(v) - unif.cdf(u)
    print(f"P({u} <= X <= {v}) =", prob_intervallo)

    media, varianza = unif.stats(moments="mv")
    print("Media teorica:", float(media), "(= (a+b)/2)")
    print("Varianza teorica:", float(varianza), "(= (b-a)^2 / 12)")



    # ============================================================
    # 7) Normale / Gaussiana (continua)
    # ============================================================
    separatore("7) Normale / Gaussiana - stats.norm(loc=mu, scale=sigma)")
    mu = 0.0
    sigma = 1.0
    norm = stats.norm(loc=mu, scale=sigma)

    campioni = norm.rvs(size=7, random_state=rng)
    print("Campioni (7 valori):", campioni)
    print("Interpretazione: misure attorno alla media con rumore")

    x = 1.0
    print(f"PDF f({x}) =", norm.pdf(x))
    print(f"CDF F({x}) = P(X<={x}) =", norm.cdf(x))

    # z-score (standardizzazione): Z = (X - mu) / sigma
    # Se X ~ N(mu, sigma^2) allora Z ~ N(0,1)
    z = (x - mu) / sigma
    print(f"z-score di x={x}:", z)

    media, varianza = norm.stats(moments="mv")
    print("Media teorica:", float(media), "(= mu)")
    print("Varianza teorica:", float(varianza), "(= sigma^2)")



    # ============================================================
    # 8) Esponenziale (continua) - tempo di attesa
    # ============================================================
    separatore("8) Esponenziale - stats.expon(scale=1/lambda)")
    lam = 2.0  # lambda = tasso (eventi per unità di tempo)
    # In SciPy: expon(scale) usa scale = media = 1/lambda
    scale = 1.0 / lam
    expo = stats.expon(scale=scale)

    campioni = expo.rvs(size=5, random_state=rng)
    print("Campioni (5 tempi di attesa):", campioni)
    print("Interpretazione: ogni numero = tempo fino al prossimo evento")

    t = 1.0
    print(f"PDF f({t}) =", expo.pdf(t))
    print(f"CDF F({t}) = P(T<={t}) =", expo.cdf(t))
    print(f"Survival S({t}) = P(T>{t}) =", expo.sf(t))  # sf = 1 - cdf

    media, varianza = expo.stats(moments="mv")
    print("Media teorica:", float(media), "(= scale = 1/lambda)")
    print("Varianza teorica:", float(varianza), "(= scale^2 = 1/lambda^2)")



    # ============================================================
    # Bonus: un mini "promemoria" per non confondere i parametri
    # ============================================================
    separatore("PROMEMORIA PARAMETRI (super breve)")
    print("Poisson: mu=lambda = eventi medi per intervallo")
    print("Esponenziale: lambda = tasso eventi/tempo, scale = 1/lambda (tempo medio)")
    print("Normale: loc=mu, scale=sigma")
    print("Uniforme continua: loc=a, scale=b-a")
    print("Randint: low incluso, high escluso")


if __name__ == "__main__":
    main()
