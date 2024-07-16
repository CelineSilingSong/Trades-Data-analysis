# Compiling all the files into one:

import os
import pandas as pd
import re

pattern = r'M(\d{4})'
directory = os.getcwd()

files = []

main_stats = ['OCC_CODE', 'OCC_TITLE']

key_stats = ['TOT_EMP',	'EMP_PRSE',	'H_MEAN',	'A_MEAN',	'MEAN_PRSE',	'H_PCT10',	'H_PCT25',	'H_MEDIAN',	'H_PCT75',	'H_PCT90',	'A_PCT10',	'A_PCT25',	'A_MEDIAN',	'A_PCT75',	'A_PCT90',	'ANNUAL',	'HOURLY']

df_matched = pd.read_excel('national_classifed_sheet.xlsx')
df_only_trade = df_matched[df_matched.iloc[:,5].astype(str) == 'IN']
df_only_trade.iloc[:,7] = df_only_trade.iloc[:,7].astype(str)
df_only_trade.iloc[:,7]= df_only_trade.iloc[:,7].str.replace('-','')


directory_path = 'trades projection titles - Copy'

code_list = []
for row in df_only_trade.iterrows():
    codes = row[1].iloc[7]
    code_list.append(codes)


for file in os.listdir(directory):
    if file.endswith('.xlsx') and file.startswith('only trade national'):
        file_path = os.path.join(directory, file)
        files.append(file_path)
    
for key_stat in key_stats:
    data = {
        'OCC_CODE': [],
        'OCC_TITLE': [],
        '2013':[],
        '2014':[],
        '2015':[],
        '2016':[],
        '2017':[],
        '2018':[],
        '2019':[],
        '2020':[],
        '2021':[],
        '2022':[],
        '2023':[],
    }    
    
    for code in code_list:
        data['OCC_CODE'].append(code)
        row = df_only_trade[df_only_trade.iloc[:,7] == code]
        occupation = row['2022 National Employment Matrix title']
        data['OCC_TITLE'].append(occupation)
        for file in files:
            df_file = pd.read_excel(file)
            file_name = os.path.basename(file)
            df_file.iloc[:,1] = df_file.iloc[:,1].astype(str)
            df_file.iloc[:,1] = df_file.iloc[:,1].str.replace('-','')
            print(df_file.iloc[:,1])
            print(f'code is {code}')
            match = re.search(pattern, file_name)
            if match:
                year = match.group(1)
                print(f'the year is {year}')
                df_file = pd.read_excel(file)
                if str(code).replace(' ','') in df_file.iloc[:,1].astype(str).replace(' ',''):                    
                    row = df_file[df_file[:,1].astype(str) == str(code)]
                    value = row[key_stat]
                    data[year].append(value)
                else:
                    data[year].append('NA')
                    print('not found')
            else:
                print('something is wrong')

    finished_df = pd.DataFrame(data)
    finished_df.to_excel(f'{key_stat} yearly data.xlsx')

                
