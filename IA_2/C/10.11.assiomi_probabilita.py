#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Spazio campionario (esempio: lancio di un dado)
S = {1, 2, 3, 4, 5, 6}

# Definizione degli eventi
A = {1, 2, 3}         # evento A: ottenere 1, 2 o 3
B = {4, 5, 6}         # evento B: ottenere 4, 5 o 6
C = {3, 6}            # evento C: ottenere 3 o 6

print("Spazio campionario S =", S)
print("\nEventi definiti:")
print(f"  A = {A}  (numeri ≤ 3)")
print(f"  B = {B}  (numeri > 3)")
print(f"  C = {C}  (numeri multipli di 3)")


# In[2]:


def probabilita(evento, spazio_campionario):
    """Calcola P(evento) = |evento| / |spazio_campionario|"""
    return len(evento) / len(spazio_campionario)


# In[3]:


P_A = probabilita(A, S)
P_B = probabilita(B, S)
P_C = probabilita(C, S)
P_S = probabilita(S, S)
P_vuoto = probabilita(set(), S)


# In[4]:


print("=" * 60)
print("VERIFICA DEGLI ASSIOMI DELLA PROBABILITÀ")
print("=" * 60)

# ASSIOMA 1: Non negatività
print("\n[Assioma 1] Non-negatività: P(E) ≥ 0")
print(f"  P(A) = {P_A:.3f} ≥ 0 ✓")
print(f"  P(B) = {P_B:.3f} ≥ 0 ✓")
print(f"  P(C) = {P_C:.3f} ≥ 0 ✓")

# ASSIOMA 2: Normalizzazione
print("\n[Assioma 2] Normalizzazione: P(S) = 1")
print(f"  P(S) = {P_S:.3f} = 1 ✓")

# ASSIOMA 3: Additività per eventi disgiunti
print("\n[Assioma 3] Additività per eventi disgiunti")

# Caso 1: eventi disgiunti (A e B)
print(f"  A e B sono disgiunti: A ∩ B = {A.intersection(B)}")
P_A_union_B = probabilita(A.union(B), S)
print(f"  P(A ∪ B) = {P_A_union_B:.3f}")
print(f"  P(A) + P(B) = {P_A:.3f} + {P_B:.3f} = {P_A + P_B:.3f}")
print("  → P(A ∪ B) = P(A) + P(B) ✓  (A e B disgiunti)")

# Caso 2: eventi NON disgiunti (A e C)
print(f"\n  A e C NON sono disgiunti: A ∩ C = {A.intersection(C)}")
P_A_union_C = probabilita(A.union(C), S)
P_A_inter_C = probabilita(A.intersection(C), S)
print(f"  P(A ∪ C) = {P_A_union_C:.3f}")
print(f"  P(A) + P(C) - P(A ∩ C) = {P_A:.3f} + {P_C:.3f} - {P_A_inter_C:.3f} = {P_A + P_C - P_A_inter_C:.3f}")
print("  → P(A ∪ C) = P(A) + P(C) - P(A ∩ C) ✓  (A e C non disgiunti)")

