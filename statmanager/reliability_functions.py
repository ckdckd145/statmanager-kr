import pandas as pd
from .messages_for_reporting import *
from .making_figure import *
import numpy as np

def cronbach(df: pd.DataFrame, vars: list, lang_set: str, testname = "Calculating Cronbach's alpha"):
    
    result_df = pd.DataFrame(columns = ['set', 'n', "cronbach's alpha"]).set_index('set')
    result_for_save = []  
    
    target_columns = vars
    
    if not type(target_columns) == list or len(target_columns) <= 0:
        raise KeyError(keyerror_message_for_cronbach[lang_set]) 
    
    k = len(target_columns)
    n = len(df)
    
    covariance_matrix = df[target_columns].cov()
    sum_of_variances = np.trace(covariance_matrix)
    total_variance = covariance_matrix.sum().sum()
    
    cronbach = (k / (k-1)) * (1 - sum_of_variances / total_variance )
    
    notation = notation_message_for_cronbach_alpha[lang_set]
    
    result_df.loc[str(target_columns), : ] = [n, cronbach]
    #reporting = cronbach_alpha_result_reporting(n, target_columns, cronbach)[lang_set]
    
    result_for_save.append(notation)
    result_for_save.append(result_df)
    #result_for_save.append(reporting)
    
    if cronbach < 0:
        warning = warning_message_for_negative_cronbach_alpha[lang_set]
        result_for_save.append(warning)
        
        
    for _ in result_df.columns:
        try:
            result_df[_] = result_df[_].astype(float).round(3)
        except:
            continue
    
    print(testname)
    for n in result_for_save:
        if isinstance(n, str or list):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
        
    return result_for_save