#!/usr/bin/env python
# coding: utf-8

# In[9]:


import matplotlib.pyplot as plt


# In[10]:


# Spazio campionario: lancio di un dado
S = {1, 2, 3, 4, 5, 6}

# Definizione di eventi
A = {2, 4, 6}  # Numeri pari
B = {1, 2, 3}  # Numeri minori o uguali a 3
C = {5, 6}     # Numeri maggiori o uguali a 5

print("Spazio campionario S =", S)
print("\nEventi definiti:")
print(f"  A = {A}  (numeri pari)")
print(f"  B = {B}  (numeri ≤ 3)")
print(f"  C = {C}  (numeri ≥ 5)")


# In[11]:


# Unione (OR)
A_union_B = A.union(B)
print("Unione (A ∪ B):")
print(f"  A ∪ B = {A_union_B}")
print(f"  Significato: numeri pari O numeri ≤ 3")


# In[12]:


# Intersezione (AND)
A_inter_B = A.intersection(B)
print("\nIntersezione (A ∩ B):")
print(f"  A ∩ B = {A_inter_B}")
print(f"  Significato: numeri pari E numeri ≤ 3")


# In[13]:


# Complemento (NOT)
A_complement = S.difference(A)
print("\nComplemento (Aᶜ):")
print(f"  Aᶜ = {A_complement}")
print(f"  Significato: numeri NON pari (dispari)")


# In[14]:


# Verifica che A e C siano disgiunti
A_inter_C = A.intersection(C)
print("\nVerifica disgiunzione:")
print(f"  A ∩ C = {A_inter_C}")
if len(A_inter_C) == 0:
    print("  ✓ A e C sono disgiunti (non hanno elementi in comune)")
else:
    print("  ✗ A e C NON sono disgiunti")


# In[15]:


# Visualizzazione delle operazioni
def visualizza_eventi(S, eventi_dict, titolo):
    """Visualizza gli eventi come barre colorate"""
    fig, ax = plt.subplots(figsize=(12, 4))

    y_pos = 0
    for nome, evento in eventi_dict.items():
        for elem in S:
            if elem in evento:
                ax.barh(y_pos, 1, left=elem-0.5, height=0.6, 
                       color='steelblue', edgecolor='black', linewidth=2)
            else:
                ax.barh(y_pos, 1, left=elem-0.5, height=0.6, 
                       color='lightgray', edgecolor='gray', linewidth=1, alpha=0.3)
        y_pos += 1

    ax.set_yticks(range(len(eventi_dict)))
    ax.set_yticklabels(eventi_dict.keys())
    ax.set_xticks(range(1, 7))
    ax.set_xlabel('Elementi dello Spazio Campionario', fontsize=11)
    ax.set_title(titolo, fontsize=13, fontweight='bold')
    ax.set_xlim(0.5, 6.5)
    plt.tight_layout()
    plt.show()

# Visualizzazione eventi base
visualizza_eventi(S, {'A (pari)': A, 'B (≤3)': B, 'C (≥5)': C}, 
                 'Eventi Base')

# Visualizzazione operazioni
visualizza_eventi(S, {'A ∪ B': A_union_B, 'A ∩ B': A_inter_B, 'Aᶜ': A_complement}, 
                 'Operazioni sugli Eventi')


# In[ ]:




