import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
from itertools import product

def levene(df: pd.DataFrame, vars: str or list, group_vars: str or list, lang_set : str, testname = 'Levene Test'):
    result_for_save = []        
    dv = vars[0] if isinstance(vars, list) else vars
    
    if isinstance(group_vars, list):
        if len(group_vars) == 1:
            group_vars = group_vars[0]
            group_names = df[group_vars].unique()
            series = []
            
            for _ in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[_], dv]
                series.append(ser)
            
            result_object = stats.levene(*series)
            s = result_object.statistic
            p = result_object.pvalue
            
            conclusion_key = 'under' if p <= .05 else 'up'
            conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
            
            reporting = homoskedasticity_test_result_reporting(group_vars, group_names, s, p)[lang_set]
            
        else:
            combo_list = [df[group].unique() for group in group_vars]
            combi = product(*combo_list)
            
            series = []
            group_names = []
            for combo in combi:
                try:
                    ser = df.groupby(group_vars).get_group(combo)[dv]
                    name = combo
                    name = " & ".join(name) if isinstance(name, tuple) else name
                    group_names.append(name)
                    series.append(ser)
                    
                except KeyError:
                    continue
            result_object = stats.levene(*series)
            s = result_object.statistic
            p = result_object.pvalue
            
            conclusion_key = 'under' if p <= .05 else 'up'
            conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
            
            reporting = homoskedasticity_test_result_reporting(group_vars, group_names, s, p)[lang_set]
            
    else: # group_vars were provided as str format
        group_names = df[group_vars].unique()
        series = []
        for _ in range(len(group_names)):
            ser = df.loc[df[group_vars] == group_names[_], dv]
            series.append(ser)
        
        result_object = stats.levene(*series)
        s = result_object.statistic
        p = result_object.pvalue
        
        conclusion_key = 'under' if p <= .05 else 'up'
        conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
        
        reporting = homoskedasticity_test_result_reporting(group_vars, group_names, s, p)[lang_set]
    
    
    result_for_save.append(reporting)
    result_for_save.append(conclusion)
    
    for n in result_for_save:
        print(n)
        
    return result_for_save

def fmax(df: pd.DataFrame, vars: str or list, group_vars: str, lang_set : str, testname = 'Fmax Test'):
    
    
    result_for_save = [] 
    dv = vars[0] if isinstance(vars, list) else vars
    
    if isinstance(group_vars, list):
        if len(group_vars) == 1:
            group_vars = group_vars[0]
            group_names = df[group_vars].unique()
            group_n = len(group_names)     
            max_variance = df.groupby(group_vars)[vars].var().max().round(3)
            min_variance = df.groupby(group_vars)[vars].var().min().round(3)
        
            f_max = max_variance / min_variance
            
            reporting = fmax_result_reporting(dv, group_vars, group_n, group_names, max_variance, min_variance, f_max)[lang_set]
            
            conclusion_key = 'up' if f_max < 10 else 'under'
            conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
        
        else:
            combi_list = [ df[group].unique() for group in group_vars ]
            combi = product(*combi_list)
            
            series = []
            group_names = []
            
            for combo in combi:
                try:
                    ser = df.groupby(group_vars).get_group(combo)[dv]
                    name = combo
                    name = " & ".join(name) if isinstance(name, tuple) else name
                    group_names.append(name)
                    series.append(ser)
                
                except KeyError:
                    continue
            
            group_n = len(group_names)
            max_variance = df.groupby(group_vars)[vars].var().max().round(3)
            min_variance = df.groupby(group_vars)[vars].var().min().round(3)
            
            f_max = max_variance / min_variance
            
            reporting = fmax_result_reporting(dv, group_vars, group_n, group_names, max_variance, min_variance, f_max)[lang_set]
            
            conclusion_key = 'up' if f_max < 10 else 'under'
            conclusion = conclusion_for_homoskedasticity_assumption[lang_set][conclusion_key]
            
    else:
        group_names = df[group_vars].unique()
        group_n = len(group_names)     
        max_variance = df.groupby(group_vars)[vars].var().max().round(3)
        min_variance = df.groupby(group_vars)[vars].var().min().round(3)
    
        f_max = max_variance / min_variance
        
        reporting = fmax_result_reporting(dv, group_vars, group_n, group_names, max_variance, min_variance, f_max)[lang_set]
        
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