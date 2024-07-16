# Returning codes for dataset 1 of skilled trade
import os
import pandas as pd

file = pd.read_excel('Occupation dataset1.xlsx')


list = []

for row in file.iterrows():
    if row[1].iloc[5] == 'IN':
        code = row[1].iloc[0]
        list.append(code)

print(list)

print(len(list))

print(len(file))



