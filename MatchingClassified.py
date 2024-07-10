import pandas as pd
from rapidfuzz import process
from Matcher import FuzzyMatcher, CodeMatcher  # Assuming Matcher.py file exists in the same directory

# Assuming 'national_classified_sheet.xlsx' and 'national_M2022_dl.xlsx' exist in the current working directory

# Read data from Excel files
classified_df = pd.read_excel('national_classifed_sheet.xlsx')
df_2022 = pd.read_excel('national_M2022_dl.xlsx')

# Initialize FuzzyMatcher
fuzzymatcher = FuzzyMatcher()

# Get matched list using FuzzyMatcher
df_matched_list = fuzzymatcher.return_matched_list(classified_df.iloc[:, 1], df_2022.iloc[:, 1])

# Apply get_code function to get codes and add a 'Code' column to df_matched_list
df_matched_list['Code'] = df_matched_list.apply(lambda row: fuzzymatcher.get_code(row, 4, df_2022.iloc[:, 0]), axis=1)

# Save df_matched_list to CSV file
df_matched_list.to_csv('matched_list.csv', index=False)  # Specify index=False to avoid saving index as a column