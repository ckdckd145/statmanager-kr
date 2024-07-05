import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
import numpy as np
import itertools


def pearson(df: pd.DataFrame, vars : list, lang_set, testname):
    
    tf = stats.pearsonr
    method = 'pearson'
    
    if isinstance(vars, str) or (isinstance(vars, list) and len(vars) < 2):
        raise ValueError(error_message_for_more_vars_within_rm_anova[lang_set])
    
    print(testname)
    result_for_save = correlations(df = df, vars = vars, method = method, tf = tf, lang_set = lang_set)
    return result_for_save
    
def spearman(df: pd.DataFrame, vars : list, lang_set, testname):
    tf = stats.spearmanr
    method = 'spearman'

    if isinstance(vars, str) or (isinstance(vars, list) and len(vars) < 2):
        raise ValueError(error_message_for_more_vars_within_rm_anova[lang_set])
    
    print(testname)
    result_for_save = correlations(df = df, vars = vars, method = method, tf = tf, lang_set = lang_set)
    return result_for_save
    
def kendall(df: pd.DataFrame, vars : list, lang_set, testname):
    tf = stats.kendalltau
    method = 'kendall'

    if isinstance(vars, str) or (isinstance(vars, list) and len(vars) < 2):
        raise ValueError(error_message_for_more_vars_within_rm_anova[lang_set])
    
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
    
    statistic_value = statistic_valuedict[method]
    
    reporting = f'Max n = {number_of_rows}'
    results = []
    for combo in itertools.combinations(vars, 2):
        combo = list(combo)
        
        subset = df[combo].dropna()
        result_object = tf(subset[combo[0]], subset[combo[1]])
        n = len(subset)
        s = result_object.statistic
        p = result_object.pvalue
        
        if method == 'pearson':
            ci = result_object.confidence_interval()
            ci_high = ci.high
            ci_low = ci.low
        else:
            pass
        
        if p <= .05:
            significant_r = '*'
            s_with_significancy = f'{s:.3f}{significant_r}'
        else:
            significant_r = ''
            s_with_significancy = f"{s:.3f}"
        
        if method == 'pearson':
            result = [" & ".join(combo), n, s_with_significancy, f"{p:.3f}", [f"{ci_low:.3f}", f"{ci_high:.3f}"]]
        else:
            result = [" & ".join(combo), n, s_with_significancy, f"{p:.3f}"]
        results.append(result)
        
        correlation_table.loc[combo[0], combo[1]] = s # prevent future error 
        correlation_table.loc[combo[1], combo[0]] = s # prevent future error 
    
    if method == 'pearson':
        summary_correlation_table = pd.DataFrame(results, columns = ['set', 'n', statistic_value, 'p-value', '95%_confidence_interval']).set_index('set')
    else:
        summary_correlation_table = pd.DataFrame(results, columns = ['set', 'n', statistic_value, 'p-value']).set_index('set')
    
    correlation_table = correlation_table.round(3)
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