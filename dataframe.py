import pandas as pd
df = pd.read_csv('animals.csv', encoding='ISO-8859-1', skiprows=2)
df = df.drop(df.columns[[4,5,6,7,9,10]], axis='columns')
df = df.dropna()