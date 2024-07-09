import pandas as pd

xls = pd.read_excel('2013 data.xlsx')

def remove_dot(string):
    cleaned_string = string.replace('.', '')
    return cleaned_string

xls['cleaned job'] = xls['Occupation'].apply(remove_dot)

xls.to_csv('2013 data cleaned.csv', index = False)