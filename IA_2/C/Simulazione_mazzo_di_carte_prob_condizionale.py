# Simulazione mazzo di carte
semi = ['Cuori', 'Quadri', 'Fiori', 'Picche']
valori = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# Creiamo il mazzo
mazzo = [(valore, seme) for seme in semi for valore in valori]
print(f"Mazzo completo: {len(mazzo)} carte\n")

# Definiamo gli eventi
# A: carta è un Re
# B: carta è di Cuori

carte_re = [c for c in mazzo if c[0] == 'K']
carte_cuori = [c for c in mazzo if c[1] == 'Cuori']
carte_re_cuori = [c for c in mazzo if c[0] == 'K' and c[1] == 'Cuori']

print(f"Carte Re: {len(carte_re)}")
print(f"Carte Cuori: {len(carte_cuori)}")
print(f"Carte Re di Cuori: {len(carte_re_cuori)}\n")

# Calcolo probabilità
p_re = len(carte_re) / len(mazzo)
p_cuori = len(carte_cuori) / len(mazzo)
p_re_e_cuori = len(carte_re_cuori) / len(mazzo)

# Probabilità condizionale: P(Re | Cuori)
p_re_dato_cuori = p_re_e_cuori / p_cuori

print("Probabilità:")
print(f"P(Re) = {p_re:.4f}")
print(f"P(Cuori) = {p_cuori:.4f}")
print(f"P(Re ∩ Cuori) = {p_re_e_cuori:.4f}")
print(f"\nP(Re | Cuori) = {p_re_dato_cuori:.4f}")
print(f"\nInterpretazione: Sapendo che la carta è di Cuori,")
print(f"la probabilità che sia un Re è {p_re_dato_cuori:.2%}")