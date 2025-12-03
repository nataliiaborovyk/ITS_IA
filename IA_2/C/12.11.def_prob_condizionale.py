def probabilita_condizionale(p_a_inter_b, p_b):
    """
    Calcola la probabilità condizionata P(A|B) = P(A ∩ B) / P(B)

    Parametri:
        p_a_inter_b (float): probabilità dell'intersezione A ∩ B
        p_b (float): probabilità di B

    Ritorna:
        float: probabilità condizionata P(A|B)
    """
    if p_b == 0:
        raise ValueError("P(B) non può essere zero")
    return p_a_inter_b / p_b


# === Input utente ===
# print("Calcolo della probabilità condizionata P(A|B)")
# p_a_inter_b = float(input("Inserisci P(A ∩ B): "))
# p_b = float(input("Inserisci P(B): "))

p_a_inter_b = 54/300
p_b = 130/300

# === Calcolo ===
p_a_dato_b = probabilita_condizionale(p_a_inter_b, p_b)

# === Output ===
print("\nRisultato:")
print(f"P(A|B) = {p_a_dato_b:.4f} → {p_a_dato_b:.2%}")
print(f"Interpretazione: sapendo che B è avvenuto, la probabilità che si verifichi anche A è {p_a_dato_b:.2%}")

print(probabilita_condizionale(3/10, 7/10))
print(probabilita_condizionale(0.333, 0.333))
print(probabilita_condizionale(2/6, 3/6))
print(probabilita_condizionale(2/36, 5/36))