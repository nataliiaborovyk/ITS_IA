# ===============================
# Esercizio: Probabilità condizionata in un e-commerce
# ===============================

# Dati del problema
n_totale = 1000           # numero totale di visitatori
n_cliccato = 400          # evento B: ha cliccato un prodotto
n_acquistato = 150        # evento A: ha acquistato
n_cliccato_e_acquistato = 120  # evento A ∩ B: ha cliccato e acquistato

# Calcolo delle probabilità
p_b = n_cliccato / n_totale              # P(B)
p_a = n_acquistato / n_totale            # P(A)
p_a_inter_b = n_cliccato_e_acquistato / n_totale   # P(A ∩ B)

# Calcolo della probabilità condizionata: P(A|B) = P(A ∩ B) / P(B)
if p_b == 0:
    raise ValueError("P(B) non può essere zero")

p_a_dato_b = p_a_inter_b / p_b

# ===============================
# Stampa dei risultati
# ===============================

print("Esercizio: Comportamento utenti in un negozio online\n")
print(f"Visitatori totali: {n_totale}")
print(f"- Hanno cliccato: {n_cliccato}")
print(f"- Hanno acquistato: {n_acquistato}")
print(f"- Hanno cliccato e acquistato: {n_cliccato_e_acquistato}\n")

print("Probabilità:")
print(f"P(A)  = P(Acquisto)                = {p_a:.4f}")
print(f"P(B)  = P(Clic su prodotto)        = {p_b:.4f}")
print(f"P(A∩B)= P(Clic e acquisto)         = {p_a_inter_b:.4f}\n")

print("Probabilità condizionata:")
print(f"P(A|B)= P(A ∩ B) / P(B) = {p_a_inter_b:.4f} / {p_b:.4f} = {p_a_dato_b:.4f}")
print(f"\nInterpretazione:")
print(f"Sapendo che un visitatore ha cliccato un prodotto,")
print(f"la probabilità che abbia anche acquistato è {p_a_dato_b:.2%}.")