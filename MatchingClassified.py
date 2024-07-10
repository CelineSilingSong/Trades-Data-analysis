import os
import glob
import pandas as pd
from Matcher import FuzzyMatcher
from Matcher import CodeMatcher

classified_df = pd.read_excel('national_classifed_sheet.xlsx')
df_2022 = pd.read_excel('national_M2022_dl.xlsx')

fuzzymatcher = FuzzyMatcher()

df_matched_list = fuzzymatcher.return_matched_list(classified_df[:,1], df_2022[:,1])

df_matched_list['Code'] = df_matched_list.apply(lambda row: fuzzymatcher.get_code(row, 4, df_2022[:,0]))
df_matched_list.to_csv('matched list')