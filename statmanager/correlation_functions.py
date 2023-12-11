import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
import numpy as np


def pearson(df: pd.DataFrame, vars : list, lang_set, testname):
    
    tf = stats.pearsonr
    method = 'pearson'
    
    print(testname)
    result_for_save = correlations(df = df, vars = vars, method = method, tf = tf, lang_set = lang_set)
    return result_for_save
    
def spearman(df: pd.DataFrame, vars : list, lang_set, testname):
    tf = stats.spearmanr
    method = 'spearman'
    
    print(testname)
    result_for_save = correlations(df = df, vars = vars, method = method, tf = tf, lang_set = lang_set)
    return result_for_save
    
def kendall(df: pd.DataFrame, vars : list, lang_set, testname):
    tf = stats.kendalltau
    method = 'kendall'
    
    print(testname)
    result_for_save = correlations(df = df, vars = vars, method = method, tf = tf, lang_set = lang_set)
    return result_for_save



# core-functions in correlation

def correlations(df, vars, tf, method, lang_set):
    
    result_for_save = []
    
    df.dropna(axis=0, how = 'any', subset = vars)
    number_of_rows = len(df)
    
    statistic_valuedict = {
            'pearson' : "Pearson's r",
            'spearman' : "Spearman's rho",
            'kendall' : "Kendall's tau"
        }
        
    correlation_table = df[vars].corr().round(3)
    
    num = len(vars)
    sets = []
    
    statistic_value = statistic_valuedict[method]
    
    reporting = f'n = {number_of_rows}\n{notation_message_for_correlation[lang_set]}'
    summary_correlation_table = pd.DataFrame()
    
    for i in range(num -1):
        for j in range(i +1, num):
            sets.append((df[vars[i]], df[vars[j]]))
        
    for n in sets:
        s, p = tf(n[0], n[1])
        s = round(s, 3)
        p = round(p, 3)
        var1 = n[0].name
        var2 = n[1].name
        
        if p <= .05:
            significant_r = '*'
            s_with_significancy = f'{s:.3f}{significant_r}'
        else:
            significant_r = ''
            s_with_significancy = f"{s}"
        
        summary_correlation_table.loc[f"{var1} & {var2}", statistic_value] = s_with_significancy
        summary_correlation_table.loc[f"{var1} & {var2}", 'p-value'] = f"{p:.3f}"

        correlation_table.loc[var1, var2] = s # prevent future error 
        correlation_table.loc[var2, var1] = s # prevent future error 
    
    correlation_table
    summary_correlation_table
    note = "* p < .05"
    
    result_for_save.append(reporting)
    result_for_save.append(summary_correlation_table)
    result_for_save.append(correlation_table)
    result_for_save.append(note)
    
    for n in result_for_save:
        if isinstance(n, str or list):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
    
    return result_for_save