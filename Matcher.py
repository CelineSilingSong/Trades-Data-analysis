import os
import rapidfuzz
from rapidfuzz import fuzz
from rapidfuzz import process
import pandas as pd

class FuzzyMatcher:
    def __init__(self) -> None:
        pass

    def get_most_similar_string(self, row, choices):
        string1 = row[1]
        match_result = process.extractOne(string1, choices)
        if match_result is None:
            return string1, 'No Match', 'No Match', 0, 0
        else:
            match_string, score, index = process.extractOne(string1, choices)
            if score >= 100:
                return string1, match_string, 'Exact Match', score, index, 
            elif score >= 75:
                return string1, match_string, 'Similar Match', score, index
            else:
                return string1, match_string, 'Suspicious Match', score, index
    
    def return_matched_list(self, string_list_1, string_list_2):
        df_matched_list = pd.DataFrame()
        df_list_1 = pd.DataFrame(string_list_1)
        df_list_2 = pd.DataFrame(string_list_2)
        df_matched_list[['String', 'Matched String', 'Match_Type','Score','Source_Line']] = df_list_1.apply(lambda row: self.get_most_similar_string(row, df_list_2.iloc[:,0]), axis=1, result_type='expand')
        return df_matched_list
    
    def get_code(self, row, index_column_number, code_list):
        df_code_list = pd.DataFrame(code_list)
        index = row[index_column_number]
        code = df_code_list[0][index]
        return code
    
class CodeMatcher:
    def __init__(self) -> None:
        pass

    def return_unique_code(self, code_list_1, code_list_2):
        set1 = set(code_list_1)
        set2 = set(code_list_2)

        unique_to_list_1 = set1 - set2
        unique_to_list_2 = set2 - set1

        return unique_to_list_1, unique_to_list_2
    
    def if_match(self, code, code_list):
        if str(code).replace(' ','') in code_list.astype(str).replace(' ', ''):
            return True
        else:
            return False



