import pandas as pd

df_2022 = pd.read_excel('national_M2022_dl.xlsx')
df_2022_occ = df_2022.iloc[:,:3]
df_2022_occ.iloc[:,0] = df_2022_occ.iloc[:,0].astype(str)
df_2022_occ.iloc[:,1] = df_2022_occ.iloc[:,1].astype(str)
df_2022_occ.iloc[:,2] = df_2022_occ.iloc[:,2].astype(str)

# Step 1: Identify duplicates based on 'Occupation'
duplicates = df_2022_occ[df_2022_occ.duplicated(subset=['OCC_TITLE'], keep=False)]

# Step 2: Prioritize deletion of 'broad' entries among duplicates
# First, sort by 'Broad' column in descending order to prioritize True (broad) values
duplicates_sorted = duplicates.sort_values(by='O_GROUP', ascending=True)

# Step 3: Remove duplicates, keeping the first occurrence (default behavior of drop_duplicates)
# Inplace=True modifies the original DataFrame
df_cleaned = df_2022_occ.drop_duplicates(subset=['OCC_TITLE'], keep='last', inplace=False)

# Output the cleaned DataFrame
print("\nCleaned DataFrame:")
print(df_cleaned)

df_cleaned.drop(df_cleaned.columns[1],axis=1)

print(df_cleaned)
df_cleaned.to_csv('cleaned 2022.csv', index = False)