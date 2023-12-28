import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *

def levene(df: pd.DataFrame, vars: str or list, group_vars: str or list, lang_set : str, testname = 'Levene Test'):
    result_for_save = []        
    
    dv = vars[0] if isinstance(vars, list) else vars
    group_vars = group_vars[0] if isinstance(group_vars, list) else group_vars
    
    group_names = df[group_vars].unique()
        
    series = []
    for _ in range(len(group_names)):
        ser = df.loc[df[group_vars] == group_names[_], dv]
        series.append(ser)
        
    result_object = stats.levene(*series)
    s = result_object.statistic
    p = result_object.pvalue
    
    reporting = homoskedasticity_test_result_reporting(group_vars, group_names, s, p)[lang_set]
    
    conclusion_key = 'under' if p <= .05 else 'up'
    conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
    
    result_for_save.append(reporting)
    result_for_save.append(conclusion)
    
    for n in result_for_save:
        print(n)
        
    return result_for_save

def fmax(df: pd.DataFrame, vars: str or list, group_vars: str, lang_set : str, testname = 'Fmax Test'):
    result_for_save = [] 
    dv = vars[0] if isinstance(vars, list) else vars
    group_vars = group_vars[0] if isinstance(group_vars, list) else group_vars
    
    group_names = df[group_vars].unique()
    
    df = df.loc[df[group_vars].isin(group_names)]
    group_n = len(group_names)
    
    max_variance = df.groupby(group_vars)[vars].var().max().round(3)
    min_variance = df.groupby(group_vars)[vars].var().min().round(3)
    
    f_max = max_variance / min_variance
    
    reporting = fmax_result_reporting(dv, group_n, group_names, max_variance, min_variance, f_max)[lang_set]
    
    conclusion_key = 'up' if f_max < 10 else 'under'
    conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
    ref = reference_of_fmax
    
    result_for_save.append(reporting)
    result_for_save.append(conclusion)
    result_for_save.append(ref)
    
    print(testname)
    for n in result_for_save:
        print(n)
        
    return result_for_save