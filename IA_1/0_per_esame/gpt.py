import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Studente": ["Anna", "Anna", "Luca", "Luca", "Marco", "Marco"],
    "Materia": ["Python", "Web", "Python", "Web", "Python", "Web"],
    "Voto": [28, 30, 25, 27, 30, 26]
})



# Domanda: Disegna un bar chart con la media dei voti per materia.
# asse X → Materia
# asse Y → Media vo

media = df.groupby('Materia').agg(avg=('Voto','mean'))
media.plot(kind='bar', figsize=(10,4))
plt.title('Media')
plt.xlabel('Materia')
plt.ylabel('Media')
plt.savefig('./fs')
plt.show()
plt.close()


# Disegna un istogramma dei voti.
# NON groupby
# solo colonna Voto

bins_v = [25, 26, 28, 30, 40]


df1 = df['Voto']
df1.hist(bins=3)

plt.hist(df['Voto'], bins=3)

df['Voto'].plot(kind='hist',bins=3)
df1.plot(kind='hist',bins=bins_v)



# Disegna due istogrammi separati:
# uno per Python
# uno per Web
bins_v = [25, 26, 28, 30, 40]
p = df[df['Materia']=='Python']
w = df[df['Materia']=='Web']

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
p['Voto'].plot(kind='hist', bins=bins_v)
plt.title('Python')

plt.subplot(1,2,2)
plt.hist(w['Voto'],bins=bins_v)
plt.title('Web')


# Disegna uno scatter plot:
# asse X → Materia (codificata)
# asse Y → Voto


df['Materia']
