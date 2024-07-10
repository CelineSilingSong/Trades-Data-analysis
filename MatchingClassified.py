import os
import glob
import pandas as pd
from Matcher import FuzzyMatcher
from Matcher import CodeMatcher

classified_df = 'national_classified_sheet.xlsx'
df_2022 = 'national_M2022_dl.xlsx'

fuzzymatcher = FuzzyMatcher(classified_df, df_2022,1,1,0)

df_matched_list = fuzzymatcher.return_matched_list()

df_matched_list.to_csv('matched list')