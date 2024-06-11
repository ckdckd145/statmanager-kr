from .messages_for_reporting import *
from .posthoc_functions import *
from .effectsize_functions import *

import pandas as pd
from statsmodels.formula.api import ols
from statsmodels import api

from .effectsize_functions import *
from .posthoc_functions import *
import re as repattern
from itertools import combinations
import copy


AGG_FORMULA = ['count', 'mean', 'median', 'std', 'min', 'max'] # .round(3).rename(columns = {'count' : 'n'})


def f_nway(df: pd.DataFrame, vars: list | str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, selector = None):
    result_for_save = []
    
    if group_vars == None:
        raise ValueError(error_message_for_group_vars_are_none[lang_set])

    if isinstance(vars, list) and len(vars) != 1:
        raise ValueError(error_message_for_more_vars[lang_set])
    
    df, interaction_columns = create_interaction_columns(df, group_vars)
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    way_len = len(group_vars)
    new_testname = f'{way_len}-way ANOVA'    
    
    if selector == None:
        testname = new_testname

    else:
        pattern = repattern.compile('-way ANOVA')
        new_testname = pattern.sub(new_testname, testname)
        testname = new_testname    
    
    reporting_one = f_nway_result_reporting_one(dv, group_vars)[lang_set]
    result_for_save.append(reporting_one)
    
    for n in group_vars:
        result_table = df.groupby(n)[dv].agg(AGG_FORMULA).rename(columns = {'count' : "n"}).round(2)
        reporting_two = f_nway_result_reporting_two(dv, n)[lang_set]
        
        result_for_save.append(reporting_two)
        result_for_save.append(result_table)
    
    reporting_three = f_nway_result_reporting_three (dv)[lang_set]
    result_table = df.groupby(group_vars)[dv].agg(AGG_FORMULA).rename(columns = {'count' : "n"}).round(2)
    
    result_for_save.append(reporting_three)
    result_for_save.append(result_table)
    
    iv_str = custom_join(group_vars)
    method_str = f"{dv} ~ {iv_str}"
    
    model = ols(method_str, data = df).fit()
    anova_table = api.stats.anova_lm(model, typ=3)
    anova_table.rename(columns = {'PR(>F)' : 'p-value'}, inplace=True)
    anova_table['partial_eta_squared'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + anova_table['sum_sq'].loc['Residual'])
    anova_table = anova_table.round(3)
    
    reporting_four = f_nway_result_reporting_four (testname)[lang_set]
    
    result_for_save.append(reporting_four)
    result_for_save.append(anova_table)
    
    if posthoc:
        posthoc_results = posthoc_ways(df = df, dv = dv, group_vars = group_vars, parametric = True, posthoc_method = posthoc_method, interaction_columns = interaction_columns, lang_set = lang_set)
        result_for_save.extend(posthoc_results)
        
    print(testname)
    for n in result_for_save:
        if isinstance(n, str):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
                
    return result_for_save 
    
    
    
def f_nway_rm(df: pd.DataFrame, vars: list, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, selector = None):
    result_for_save = []

    if group_vars == None:
        raise ValueError(error_message_for_group_vars_are_none[lang_set])

    if isinstance(vars, str) or (isinstance(vars, list) and len(vars) < 2):
        raise ValueError(error_message_for_more_vars_within_rm_anova[lang_set])
    
    group_vars_for_reporting = copy.copy(group_vars)
    index_col = df.index.name
    
    melted_df = df.reset_index().melt(id_vars = index_col, value_vars = vars, var_name = 'time').set_index(index_col)
    df = df.drop(columns = vars).merge(melted_df, how = 'outer', on = index_col)
    
    group_vars = [group_vars] if isinstance(group_vars, str) else group_vars
    group_vars.append('time')
    dv = 'value'
    
    way_len = len(group_vars)
    new_testname = f'{way_len}-way Mixed Repeated Measures ANOVA'
    
    if selector == None:
        testname = new_testname

    else:
        pattern = repattern.compile('-way Mixed Repeated Measures ANOVA')
        new_testname = pattern.sub(new_testname, testname)
        testname = new_testname    
        
    df, interaction_columns = create_interaction_columns(df, group_vars)

    reporting_one = f_nway_rm_result_reporting_one(vars, group_vars_for_reporting)[lang_set]
    result_for_save.append(reporting_one)
    for n in group_vars:
        result_table = df.groupby(n)[dv].agg(AGG_FORMULA).rename(columns = {'count' : "n"}).round(2)
        reporting_two = f_nway_result_reporting_two(dv, n)[lang_set]
        
        result_for_save.append(reporting_two)
        result_for_save.append(result_table)
        
    reporting_three = f_nway_result_reporting_three (dv)[lang_set]
    result_table = df.groupby(group_vars)[dv].agg(AGG_FORMULA).rename(columns = {'count' : "n"}).round(2)
    
    result_for_save.append(reporting_three)
    result_for_save.append(result_table)
    
    iv_str = custom_join(group_vars)
    method_str = f"{dv} ~ {iv_str}"
    
    model = ols(method_str, data = df).fit()
    anova_table = api.stats.anova_lm(model, typ=3)
    anova_table.rename(columns = {'PR(>F)' : 'p-value'}, inplace=True)
    anova_table['partial_eta_squared'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + anova_table['sum_sq'].loc['Residual'])
    anova_table = anova_table.round(3)
    
    reporting_four = f_nway_result_reporting_four (testname)[lang_set]
    
    result_for_save.append(reporting_four)
    result_for_save.append(anova_table)

    if posthoc:
        posthoc_results = posthoc_ways(df = df, dv = dv, group_vars = group_vars, parametric = True, posthoc_method = posthoc_method, interaction_columns = interaction_columns, lang_set = lang_set)
        result_for_save.extend(posthoc_results)
        
    print(testname)
    for n in result_for_save:
        if isinstance(n, str):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
                
    return result_for_save 

# ------ #
def create_interaction_columns(df, elements):
    interactions = []
    new_df = df.copy() 

    for n in range(2, len(elements) + 1):
        for combo in combinations(elements, n):
            interaction_name = "interaction_" + "_".join(combo)
            
            interaction_values = df[list(combo)].astype(str).agg('_'.join, axis=1)
            
            new_df[interaction_name] = interaction_values
            interactions.append(interaction_name)
    
    return new_df, interactions

def custom_join(vars):
    formatted_vars = [f"C({var})" for var in vars]
    
    result = []

    for n in range(2, len(formatted_vars) + 1):
        for combo in combinations(formatted_vars, n):
            result.append(':'.join(combo))
    
    return ' + '.join(formatted_vars + result)