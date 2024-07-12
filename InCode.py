# Returning Trade Codes:
import pandas as pd
import os
from Matcher import CodeMatcher


df_matched = pd.read_excel('national_classifed_sheet.xlsx')

df_only_trade = df_matched[df_matched.iloc[:,5] == 'IN']

directory_path = 'trades projection titles - Copy'

codeMatcher = CodeMatcher()

files = [ ]
for root, _, filenames in os.walk(directory_path):
    for filename in filenames:
        if filename.endswith('.xlsx'):
            files.append(filename)

files = sorted(files)
print(files)

for file in files:
    file_path = os.path.join(directory_path,file)
    df = pd.read_excel(file_path)
    for row in df.iterrows():
        code = row[0]
    df['if trade'] = df.apply(lambda row: codeMatcher.if_match(row, df_only_trade['2022 National Employment Matrix code']))   
    df = df[df['if trade'] == True]
    df.to_csv(f'only trades {file}', index = False)
   
        

