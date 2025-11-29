def teorema_bayes(p_a_dato_b, p_b, p_a):
    """
    Calcola P(B|A) = P(A|B) · P(B) / P(A)
    
    Args:
        p_a_dato_b: P(A|B) - verosimiglianza
        p_b: P(B) - probabilità a priori
        p_a: P(A) - evidenza
    
    Returns:
        P(B|A) - probabilità a posteriori
    """
    return (p_a_dato_b * p_b) / p_a

def teorema_bayes_completo(p_a_dato_b, p_b, p_a_dato_non_b):
    """
    Calcola P(B|A) usando la legge della probabilità totale per P(A)
    """
    p_non_b = 1 - p_b
    p_a = p_a_dato_b * p_b + p_a_dato_non_b * p_non_b
    return teorema_bayes(p_a_dato_b, p_b, p_a)


if __name__ == "__main__":
    res1 = teorema_bayes_completo(0.99, 0.01, 0.05)
    print(res1)

    res2 = teorema_bayes_completo(0.9, 0.2, 0.6)
    print(res2)
# Test con l'esempio delle fabbriche
# Dato un prodotto difettoso, qual è la probabilità che provenga dalla Fabbrica A?

# p_a_dato_difettoso = teorema_bayes(
#     p_a_dato_b=p_difettoso_dato_a,  # P(Difettoso | A)
#     p_b=p_fabbrica_a,                # P(A)
#     p_a=p_difettoso                  # P(Difettoso)
# )

# print("Inversione della Condizionalità con Bayes")
# print(f"P(Difettoso | Fabbrica A) = {p_difettoso_dato_a:.2%}")
# print(f"P(Fabbrica A | Difettoso) = {p_a_dato_difettoso:.2%}")
# print(f"\nInterpretazione: Dato un prodotto difettoso,")
# print(f"c'è una probabilità del {p_a_dato_difettoso:.2%} che provenga dalla Fabbrica A")