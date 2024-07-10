import os
import rapidfuzz
from rapidfuzz import fuzz
from rapidfuzz import process
import pandas as pd

class FuzzyMatcher:
    def __init__(self, filepath1, filepath2, columnindex1, columnindex2, codecolumn):
        self.filepath1 = filepath1
        self.filepath2 = filepath2
        self.columnindex1 = columnindex1
        self.columnindex2 = columnindex2
        self.codecolumn = codecolumn

    def get_most_similar_string(self, row, choices):
        string1 = row[self.columnindex1]
        match_result = process.extractOne(string1,choices)
        if match_result is None:
            return string1, 'No Match', 'No Match', 0, 0, 0
        else:
            match_string, score, index = process.extractOne(string1, choices)
            if score >= 100:
                return string1, match_string, 'Exact Match', score, index, 
            elif score >= 75:
                return string1, match_string, 'Similar Match', score, index
            else:
                return string1, match_string, 'Suspicious Match', score, index
    
    def return_matched_list (self):
        df_matched_list = pd.DataFrame()
        df2 = pd.read_csv(self.filepath2)
        df1 = pd.read_csv(self.filepath1)
        df_matched_list[['String', 'Matched String', 'Match_Type','Score','Source_Line']] = df1.apply(lambda row: self.get_most_similar_string(row, df2.iloc[self.columnindex2]), axis=1, result_type='expand')
        df_matched_list['code'] = df2['source_Line'][self.codecolumn]
        return df_matched_list
    
class CodeMatcher:
    def __init__(self) -> None:
        pass

    def return_unique_code(self, code_list_1, code_list_2):
        set1 = set(code_list_1)
        set2 = set(code_list_2)

        unique_to_list_1 = set1 - set2
        unique_to_list_2 = set2 - set1

        return unique_to_list_1, unique_to_list_2



