def regola_prodotto(p_a_dato_b, p_b):
    """
    Calcola P(A ∩ B) = P(A|B) · P(B)
    """
    return p_a_dato_b * p_b

# Esempio: Estrazioni senza reinserimento
# Urna con 5 palline rosse e 3 blu
# Qual è la probabilità di estrarre 2 palline rosse?

p_r1 = 5/8  # P(prima rossa)
p_r2_dato_r1 = 4/7  # P(seconda rossa | prima rossa)

p_due_rosse = regola_prodotto(p_r2_dato_r1, p_r1)

print("Esempio: Estrazioni senza reinserimento")
print(f"P(prima rossa) = {p_r1:.4f}")
print(f"P(seconda rossa | prima rossa) = {p_r2_dato_r1:.4f}")
print(f"P(due rosse) = {p_due_rosse:.4f} = {p_due_rosse:.2%}")

# Verifica con simulazione
n_simulazioni = 100000
successi = 0

for _ in range(n_simulazioni):
    urna = ['R']*5 + ['B']*3
    np.random.shuffle(urna)
    if urna[0] == 'R' and urna[1] == 'R':
        successi += 1

p_simulata = successi / n_simulazioni
print(f"\nVerifica con simulazione ({n_simulazioni} prove):")
print(f"P(due rosse) simulata = {p_simulata:.4f}")
print(f"Differenza: {abs(p_due_rosse - p_simulata):.4f}")