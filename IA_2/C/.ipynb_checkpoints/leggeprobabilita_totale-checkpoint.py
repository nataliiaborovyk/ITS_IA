import matplotlib.pyplot as plt

def probabilita_totale(p_a_dato_b_list, p_b_list):
    """
    Calcola P(A) = Σᵢ P(A|Bᵢ) · P(Bᵢ)
    dove {Bᵢ} è una partizione dello spazio campionario
    """
    return sum(p_a_b * p_b for p_a_b, p_b in zip(p_a_dato_b_list, p_b_list))

# Esempio: Fabbriche e prodotti difettosi
# Fabbrica A produce 60% dei prodotti, con 2% difettosi
# Fabbrica B produce 40% dei prodotti, con 5% difettosi
# Qual è la probabilità che un prodotto scelto a caso sia difettoso?

p_fabbrica_a = 0.60
p_fabbrica_b = 0.40

p_difettoso_dato_a = 0.02
p_difettoso_dato_b = 0.05

p_difettoso = probabilita_totale(
    [p_difettoso_dato_a, p_difettoso_dato_b],
    [p_fabbrica_a, p_fabbrica_b]
)

print("Esempio: Fabbriche e prodotti difettosi")
print(f"P(Fabbrica A) = {p_fabbrica_a:.2%}")
print(f"P(Fabbrica B) = {p_fabbrica_b:.2%}")
print(f"P(Difettoso | A) = {p_difettoso_dato_a:.2%}")
print(f"P(Difettoso | B) = {p_difettoso_dato_b:.2%}")
print(f"\nP(Difettoso) = {p_difettoso:.4f} = {p_difettoso:.2%}")

# Visualizzazione
fig, ax = plt.subplots(figsize=(10, 6))

fabbriche = ['Fabbrica A', 'Fabbrica B']
contributi = [
    p_difettoso_dato_a * p_fabbrica_a,
    p_difettoso_dato_b * p_fabbrica_b
]

bars = ax.bar(fabbriche, contributi, color=['#3182ce', '#f6ad55'])
ax.axhline(y=p_difettoso, color='red', linestyle='--', linewidth=2, label=f'P(Difettoso) totale = {p_difettoso:.4f}')

# Annotazioni
for i, (bar, val) in enumerate(zip(bars, contributi)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.4f}',
            ha='center', va='bottom', fontweight='bold')

ax.set_ylabel('Contributo a P(Difettoso)', fontsize=12)
ax.set_title('Legge della Probabilità Totale: Prodotti Difettosi', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()