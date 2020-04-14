import pandas as pd
import numpy as np

df2 = pd.read_csv('../Datasets/Olympic2016Rio.csv', usecols=['NOC'])
print(df2)
array_test = df2.to_numpy()

test = []
for x in range(0,df2.size):
    test.append({'label': df2.iloc[x]['NOC'], 'value': df2.iloc[x]['NOC']})

print(test)