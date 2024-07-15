# Returning Trade Codes:
import pandas as pd
import os
from Matcher import CodeMatcher

df_matched = pd.read_excel('national_classifed_sheet.xlsx')
df_only_trade = df_matched[df_matched.iloc[:,5].astype(str) == 'IN']

directory_path = 'trades projection titles - Copy'
codeMatcher = CodeMatcher()

code_list = []
for row in df_only_trade.iterrows():
    codes = row[1].iloc[7].replace('-','')
    code_list.append(codes)



files = [ ]
for root, _, filenames in os.walk(directory_path):
    for filename in filenames:
        if filename.endswith('.xlsx') and filename.startswith('nation'):
            file_path = os.path.join(root, filename)
            files.append(file_path)

files = sorted(files)


for file in files:
    file_name = os.path.basename(file)
    df_new = []
    df = pd.read_excel(file)
    df.iloc[:,0] = df.iloc[:,0].astype(str)
    df.dropna(how = 'all', inplace = True)
    for row in df.iterrows():
        code = row[1].iloc[0].replace('-', '')
        if code in code_list:
            print('found!')
            print(row[1])
            df_new.append(row[1])
        else:
            print('row deleted')
    df_new_frame = pd.DataFrame(df_new)
    print(df_new_frame)
    df_new_frame.to_excel(f'only trade {file_name}')


   
# file_path =   'national_M2013_dl.csv'
# df_new = []
# df = pd.read_csv(file_path)
# df.iloc[:,0] = df.iloc[:,0].astype(str)
# df.dropna(how = 'all', inplace = True)
# for row in df.iterrows():
#     code = row[1].iloc[0].replace('-', '')
#     if code in code_list:
#         print('found!')
#         print(row[1])
#         df_new.append(row[1])
#     else:
#         print('row deleted')
# df_new_frame = pd.DataFrame(df_new)
# print(df_new_frame)
# df_new_frame.to_excel(f'only trade national_M2013_dl.xlsx')      

