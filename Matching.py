import os
import glob
import pandas as pd
from Matcher import FuzzyMatcher
from Matcher import CodeMatcher

folder = 'trades projection titles - Copy'
code_matcher = CodeMatcher()

dfs = []

file_paths = []

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.startswith('national_'):
            file_path = os.path.join(root,file)
            file_paths.append(file_path)


file_paths.sort()
print(file_paths)

for file_path in file_paths:
    df = pd.read_excel(file_path)
    dfs.append(df)

year = 2013

for i in range(len(dfs)-1):
    df1 = dfs[i]
    df2 = dfs[i+1]

    unique_to_df1, unique_to_df2 = code_matcher.return_unique_code(df1.iloc[:,1],df2.iloc[:,1])
    print(f'difference between {year} and {year+1} is:')
    print(f'code unique to {year} is {unique_to_df1}')
    print(f'code unique to {year + 1} is {unique_to_df2}')

    year += 1