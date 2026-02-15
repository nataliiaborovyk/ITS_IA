
import numpy as np



# y_real = [1, 0, 0, 1]
# y_pred = [1, 0, 1, 1]

# confusione_matrix = np.zeros([2,2])

# for idx in range(len(y_pred)):
#     if y_pred[idx] == y_real[idx]: # becca
#         if y_real[idx] == 0.:
#             confusione_matrix[0][0] += 1
#         else:
#             confusione_matrix[1][1] += 1

#     else:                           # non becca
#         if y_real[idx] == 0.:
#             confusione_matrix[0][1] += 1
#         else:
#             confusione_matrix[1][0] += 1

# print(confusione_matrix)



# # Filippo

# def confusion(l1:list,l2:list):

#     if len(l2)!=len(l1):
#         return 'errore, le liste devono avere la stessa lunghezza!'

#     confusion_matrix=np.zeros([2,2])
    
#     for x in range(len(l1)):
#         if l1[x]==0 and l2[x]==0:
#             confusion_matrix[0][0]+=1
#         elif l1[x]==0 and l2[x]==1:
#             confusion_matrix[0][1]+=1
#         elif l1[x]==1 and l2[x]==0:
#             confusion_matrix[1][0]+=1
#         else:
#             confusion_matrix[1][1]+=1
#     return confusion_matrix 


# Nico

# confusion_matrix = np.zeros([2,2])
# print(confusion_matrix)
# print(confusion_matrix[0][0])

# input:  n classi

y_real = [1, 0, 1, 1, 2, 2]
y_pred = [1, 0, 0, 1, 0, 2]

classi = set(y_real)
print(classi)
n_classi = len(classi)
confusion_matrix = np.zeros([n_classi,n_classi])

for i in range(len(y_real)): # ciclo su tutti gli indici del campione 
    real = y_real[i] # etichetta real del i-esimo campione
    predittivo = y_pred[i] # etichetta predetta per lo stesso campione 
    # confusion_matrix[predittivo][real] += 1 # aggiorno la confusion matrix, aggiungendo 1 alla cella corrispondente alla coppia (predittivo, real)
    confusion_matrix[real][predittivo] += 1 # aggiorno la confusion matrix, aggiungendo 1 alla cella corrispondente alla coppia (predittivo, real)

print(confusion_matrix)


sum_diagon = np.trace(confusion_matrix)

tutti_elem = confusion_matrix.sum()
# se confusion_matrix.sum(0) somma di righe, confusion_matrix.sum(1) somma su colonna

accurasy = sum_diagon/tutti_elem

print('Accurasy', accurasy)

print('somma per riga .sum(1): ', confusion_matrix.sum(1))

print('somma per colonna .sum(0): ', confusion_matrix.sum(0))

