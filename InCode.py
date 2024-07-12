# Returning Trade Codes:
import pandas as pd
import os
from Matcher import CodeMatcher

df_matched = pd.read_excel('national_classifed_sheet.xlsx')

df_only_trade = df_matched[df_matched.iloc[:,5].astype(str) == 'IN']
print(df_matched.iloc[:,5])
print(df_only_trade)

directory_path = 'trades projection titles - Copy'

codeMatcher = CodeMatcher()

files = [ ]
for root, _, filenames in os.walk(directory_path):
    for filename in filenames:
        if filename.endswith('.xlsx') and filename.startswith('national'):
            file_path = os.path.join(root, filename)
            files.append(file_path)

files = sorted(files)


for file in files:
    df = pd.read_excel(file)
    df['if trade'] = df.apply(lambda row: codeMatcher.if_match(row[0], df_only_trade.iloc[:,7]))   
    df = df[df['if trade'] == True]
    file_name = os.path.basename(file_path)
    df.to_csv(f'only trades {file_name}.csv', index = False)
   
        

