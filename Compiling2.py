import os
import pandas as pd
import re

pattern = r'M(\d{4})'
directory = os.getcwd()

files = []

main_stats = ['OCC_CODE', 'OCC_TITLE']

key_stats = ['TOT_EMP', 'EMP_PRSE', 'H_MEAN', 'A_MEAN', 'MEAN_PRSE', 'H_PCT10', 'H_PCT25', 'H_MEDIAN',
             'H_PCT75', 'H_PCT90', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90', 'ANNUAL', 'HOURLY']

df_matched = pd.read_excel('national_classifed_sheet.xlsx')
df_only_trade = df_matched[df_matched.iloc[:, 5].astype(str) == 'IN']
df_only_trade.iloc[:, 7] = df_only_trade.iloc[:, 7].astype(str)
df_only_trade.iloc[:, 7] = df_only_trade.iloc[:, 7].str.replace('-', '')

directory_path = 'trades projection titles - Copy'

code_list = df_only_trade.iloc[:, 7].tolist()  # Convert to list for easier iteration

for file in os.listdir(directory):
    if file.endswith('.xlsx') and file.startswith('only trade national'):
        file_path = os.path.join(directory, file)
        files.append(file_path)

for key_stat in key_stats:
    data = {
        'OCC_CODE': [],
        'OCC_TITLE': [],
        '2013': [],
        '2014': [],
        '2015': [],
        '2016': [],
        '2017': [],
        '2018': [],
        '2019': [],
        '2020': [],
        '2021': [],
        '2022': [],
        '2023': [],
    }

    for code in code_list:
        data['OCC_CODE'].append(code)
        row = df_only_trade[df_only_trade.iloc[:, 7] == code]
        if not row.empty:
            occupation = row.iloc[0]['2022 National Employment Matrix title']
            data['OCC_TITLE'].append(occupation)
        else:
            data['OCC_TITLE'].append('Not Found')

        for file in files:
            df_file = pd.read_excel(file)
            file_name = os.path.basename(file)
            df_file.iloc[:, 1] = df_file.iloc[:, 1].astype(str)
            df_file.iloc[:, 1] = df_file.iloc[:, 1].str.replace('-', '')

            match = re.search(pattern, file_name)
            if match:
                year = match.group(1)
                print(f'File: {file}, Year: {year}')

                if str(code) in df_file.iloc[:, 1].astype(str).values:
                    row = df_file[df_file.iloc[:, 1].astype(str) == str(code)]
                    if key_stat in df_file.columns:
                        value = row.iloc[0][key_stat]
                        print(f'Found {key_stat}: {value}')
                    else:
                        lower_key_stat = key_stat.lower()
                        value = row.iloc[0][lower_key_stat]
                        print(f'Found {lower_key_stat}: {value}')
                    data[year].append(value)
                else:
                    data[year].append('NA')
                    print(f'{code} not found in {file}')
            else:
                print(f'No year found in file: {file}')

    finished_df = pd.DataFrame(data)
    finished_df.to_excel(f'{key_stat}_yearly_data.xlsx')