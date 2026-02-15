# import os
import pandas as pd

dict =     {

        "Name": [

            "Braund, Mr. Owen Harris",

            "Allen, Mr. William Henry",

            "Bonnell, Miss. Elizabeth",
            
            "Taylor, Miss. Jane"

        ],

        "Age": [22, 35, 58, 55],

        "Sex": ["male", "male", "female", "female"],
        
        "Location": ["Rome", "London", "Berlin", "New York"],

    }
 
df = pd.DataFrame(dict)
print("Un dataframe creato da un dizionario Python")
print(df)
print("\n")

# script_dir: str = os.path.dirname(os.path.abspath(__file__))
# # csv_path: str = os.path.join(script_dir, "../dati/titanic.csv")
# csv_path: str = os.path.join(script_dir, "../dati/clean_data.csv")
# df = pd.read_csv(csv_path)
# df = pd.read_csv("../dati/titanic.csv")
# print("Un dataframe creato da un file csv")
# print(df.head())
# print("\n")

# print(df.Age)
# print("\n")
# print(df['Age'])
# print("\n")
# print(df[['Age']])
# print("\n")
# print(df['Age', 'Location'])
# print("\n")

# print(df.iloc[2])
# print(type(df.iloc[2]))
# print("\n")

# df.set_index("Name", inplace=True)
# print(df.loc["Taylor, Miss. Jane"])
# df.reset_index()
# print(df)


# print(df.tail(7).head(1))

# print(df.head(2))
# print("\n")
# print (df.tail(2))
# print("\n")
# print(df.describe())
# print("\n")
# print(df["Age"].describe())
# print("\n")
# print(df.dtypes)
# print("\n")
# print (df.info())
# print("\n")
# print(df.columns)
# print("\n")
# print (df.index)
# print("\n")
# print(df.shape)
# print("\n")
# df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Aritra'],

#                     'Age': [25, 30, 35],

#                     'Location': ['Seattle', 'New York', 'Kona']},

#                   index=([10, 20, 30]))
# print("Un dataframe creato da un dizionario Python")
# print(df)
# print("\n")
# print(type(df))
# print("\n")

# print(df.Location)
# print(df['Location'])
# print(df[['Location']])
# print("\n")
# print(type(df.Location))
# print(type(df['Location']))
# print(type(df[['Location']]))
# print("\n")

# print(type(dict.get("Age")))
# print("\n")
# print(df)
# print("\n")
# print(type(df["Age"]))

# ages = pd.Series([22, 35, 58], name="Age")
# print(type(ages))

# print(df["Location"].max())

# print(df.Location)
# print("\n")
# print(df[['Age', 'Sex']])

# df_1 = df.loc[:,['Name', 'Sex']].head(2) 
# df_2 = df[['Name', 'Sex']].head(2) 
# df_1 = df[df['Age'] > 70]
# df_2 = df.loc[df['Age'] < 26]
# print(df_1)
# print(df_2)

# # print(df.Age.describe())
# print(students.describe())

# iloc uses integer-based indexing (position-based)
# loc uses label-based indexing
# Row Selection:
#     iloc[0:2] → Rows 0 and 1 (excludes 2)
#     loc[0:2] → Rows 0, 1, and 2 (includes 2)
# Column Selection:
#     iloc[0:3] → Columns at positions 0, 1, 2 (all columns in this case)
#     loc['Name':'Sex'] → Columns from Name to Sex (also all columns here)

# print(type(df.iloc[2]))
# print(type(df.iloc[[2]]))
# print(df.iloc[0:2, 0:3])
# print("\n")
# print(df[['Name', 'Sex']].head(2))
# print("\n")
# print(df[['Name', 'Sex']])
# print("\n")
# print(df.loc[:, 'Age':'Location'])
# print(type(df.loc[:, 'Age':'Location']))

# print(df[df['Age'] <= 55])
# print(df.loc[df['Age'] < 56])

# print(df.tail(11)['Name'])
# print("\n")
# print(df.iloc[df.shape[0]-11:]['Name'])
      
# df.shape[0])

# print(df.dtypes)
# print(df[['Name', 'Sex']].head(2))
# print("\n")
# print(df.loc[0:2, 'Name':'Sex'])
# print("\n")
# print(df.loc[0:2][['Age','Location']])

# simple_condition_1 = df['Age'] >= 40
# print(df[df['Age'] >= 40])
# print(df.query('Age >= 40'))
      
# simple_condition_1 = df['Age'] > 40
# print(simple_condition_1)
# print(type(simple_condition_1))
# print("\n")
# print(df[simple_condition_1])
# print("\n")
# simple_condition_2 = df['Location'].str.contains('ne', case=False)
# print(simple_condition_2)
# print("\n")
# print(df[simple_condition_2])
# print("\n")
# print(df[simple_condition_1 & simple_condition_2])
# df.loc[df['Location'].str.contains('r', case=False), 'Location'] = '?'
# print("\n")
# print(df[df['Location'].str.contains('r', case=False)])
# df[df['Location'].str.contains('r', case=False)]['Location'] = 'pippo'
# df.loc[df['Location'].str.contains('r', case=False), 'Location'] = '?'
# print("\n")
# print(df.loc[df['Location'].str.contains('r', case=False)])
# print("\n")
# print(df)

# print(df.index)
# print("\n")
# print(df.shape)
# print("\n")
# print(df.iloc[665:678][['Age']])
# print("\n")
# print(type(df.iloc[665:678][['Age']]))
# print("\n")
# print(df.index)
# print(type(df.index))
# print("\n")
# df.set_index('Age', inplace=True)
# print(df.index)
# print(type(df.index))
# print("\n")
# print(df.loc[['Taylor, Miss. Jane']])
# df.reset_index(inplace=True)
# print(df.index)
# print("\n")
# print(df.loc['Taylor, Miss. Jane'])


# print(df.loc[0:1, 'Name':'Sex'])
# print("\n")
# print(df.iloc[2:4, 0:3])
# print(df.loc[2:3, 'Name':'Location'])

# print("Stampa indici")
# print(df.index)
# print("\n")
# print(df.loc[2:, 'Name':'Sex'])
# print("\n")
# print(df.loc[0:2])
# print("\n")
# df_test = df.loc[0:2]
# df_test_1 = df_test[['Age']]
# df_test_1 = df.loc[0:2,['Age','Sex']]
# df_test_1 = df.loc[0:2, 'Age':'Location']
# print(df_test_1)
# print(type(df_test_1)) 

# print("Cambia indici")
# new_index=['a','b','c','d']
# df.index = new_index
# print("Stampa indici")
# print(df.index)
# print("\n")
# print(df)
# print("\n")
# # print("Affetta il dataframe")
# # print("df.loc['a', 'Name']")
# # print(df.loc['a', 'Name'])
# # print("\n")
# # print("df.loc['a', 'Name':'Age']")
# # print(df.loc['a', 'Name':'Age'])
# # print("\n")
# print("df.loc['a':'c', 'Name']")
# print(df.loc['a':'c', 'Name'])
# print(type(df.loc['a':'c', 'Name']))
# print("\n")
# print("df.loc['a':'c', 'Name:'Age']")
# print(df.loc['a':'c', 'Name':'Age'])
# print(type(df.loc['a':'c', 'Name':'Age']))
# print("\n")
# print("df.loc['b':'d'][['Age','Location']]")
# print(df.loc['b':'d'][['Age','Location']])
# print(type(df.loc['b':'d'][['Age','Location']]))

# print(df.sort_values('Age', ascending=False))

#df = pd.read_csv("../dati/SomeMusicAlbums.csv")
# ## Prove per altri esercizi
# print(df.iloc[3:6, 0:3])
# print(df.loc[3:5, 'Artist':'Released'])
# df_new = df[['Artist','Soundtrack']]
# print(df_new.loc[3:5])
# print(df_new.iloc[3:6])
