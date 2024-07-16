import pandas as pd
import os

classified_df = pd.read_excel('national_classifed_sheet.xlsx')
classified_df['2022 National Employment Matrix code'] = classified_df['2022 National Employment Matrix code'].astype(str)
classified_df['2022 National Employment Matrix code'] = classified_df['2022 National Employment Matrix code'].str.replace('-','')

def ReturnProjection(row, df, code_key_1, code_key, projection_key):
    try:
        code = row[code_key_1]
        row_match = df[df[code_key].astype(str) == str(code)]
        if not row_match.empty:
            projection = row_match.iloc[0][projection_key]
            return projection
        else:
            return None  # or handle as needed for your application
    except KeyError as e:
        print(f"KeyError: {e}. Check if '{code_key}' exists in the DataFrame.")

directory = os.getcwd()

files = []
for file in os.listdir(directory):
    if file.endswith('yearly_data.xlsx'):
        file_path = os.path.join(directory, file)
        files.append(file_path)

for file in files:
    filename = os.path.basename(file)
    df = pd.read_excel(file)
    
    # Check for leading/trailing spaces in column names
    df.columns = df.columns.str.strip()
    
    # Ensure the column exists in the DataFrame
    if '2022 National Employment Matrix code' in classified_df.columns:
        df['Projection'] = df.apply(lambda row: ReturnProjection(row, classified_df, 'OCC_CODE','2022 National Employment Matrix code', 'Employment, 2032'), axis=1)
        print(df)
    else:
        print(f"Column '2022 National Employment Matrix code' not found")
    
    df.to_excel(f'with projection {filename}', index = False)