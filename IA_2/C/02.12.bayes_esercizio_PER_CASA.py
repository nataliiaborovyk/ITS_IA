
# Esercizio sull'aggiornamento Bayesiano sequenziale

import matplotlib.pyplot as plt

from mia_bayes import bayer_sequenza

def teorema_bayes(p_a_dato_b, p_b, p_a):
    """
    Calcola P(B|A)=P(A|B)*P(B) / P(A)
    
    Arg
    p_a_dato_b : P(A|B) - verosimiglianza
    p_b : P(B) - probabilità a priori
    p_a : P(A) - evidenza

    Returns
    P(B|A) - probabilità a posteriori
    """
    return(p_a_dato_b*p_b) / p_a


def teorema_bayes_completo(p_a_dato_b, p_b, p_a_dato_non_b):
    """
    Calcola P(B|A) usando la legge di probabilità totale per P(A)
    """
    p_non_b = 1-p_b
    p_a = p_a_dato_b*p_b + p_a_dato_non_b*p_non_b
    return teorema_bayes(p_a_dato_b, p_b, p_a)


# Aggiornamento Bayesiano sequenziale
# Stima della probabilità di un dado truccato
# Prior: P(Truccata)= 0.3
# Osserviamo una sequenza di lanci ed aggiorniamo la probabilità

# scenario: dado truccatp (0.3) vs equa (1/6)
p_6_dadotruccato = 0.3
p_6_dadoequo = 1/6


# => 

lanci = [6, 3, 6, 1, 6, 2, 6]
prior = 0.3
p_a_dato_b = p_6_dadotruccato
p_a_dato_non_b = p_6_dadoequo

lista_result = bayer_sequenza(lanci, 6, p_a_dato_b, p_a_dato_non_b, prior)
print(lista_result)



# sequenza lanci osservati
# ----

# Prior iniziale 
# ----