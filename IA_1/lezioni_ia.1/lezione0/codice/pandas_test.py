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
print("Un dataframe creato leggendo un dizionario Python")
print(df)
print("\n")
