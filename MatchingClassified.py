import pandas as pd
from rapidfuzz import process
from Matcher import FuzzyMatcher, CodeMatcher  # Assuming Matcher.py file exists in the same directory

# Assuming 'national_classified_sheet.xlsx' and 'national_M2022_dl.xlsx' exist in the current working directory
# Read data from Excel files
classified_df = pd.read_excel('national_classifed_sheet.xlsx')
df_2022 = pd.read_csv('cleaned 2022.csv')
df_2022_occ = df_2022.iloc[:,:2]
df_2022_occ.iloc[:,0] = df_2022_occ.iloc[:,0].astype(str)

# Initialize FuzzyMatcher
fuzzymatcher = FuzzyMatcher()

# Get matched list using FuzzyMatcher
classified_df[['Original Occupation','Best Match', 'Degree of Match','Score', 'index']] = classified_df.apply(lambda row: pd.Series(fuzzymatcher.get_most_similar_string(row, df_2022_occ.iloc[:,1])), axis = 1)

classified_df.to_csv('pre_merged list.csv', index = False)

merged_file = pd.merge(classified_df, df_2022_occ, left_on= 'Best Match', right_on = 'OCC_TITLE', how = 'left')

# Save df_matched_list to CSV file
merged_file.to_csv('matched_list.csv', index=False)  # Specify index=False to avoid saving index as a column