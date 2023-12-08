from statsmodels.stats.multicomp import MultiComparison
from scipy import stats
import pandas as pd
from .messages_for_reporting import *

def posthoc_within(df, vars, parametric: bool, posthoc_method):
    
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=vars)
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    if posthoc_method == 'bonf':
        if parametric:
            result = mc.allpairtest(stats.ttest_ind, method ='bonf')
            result_table = result[0]
        
        if not parametric:
            result = mc.allpairtest(stats.mannwhitneyu, method ='bonf')
            result_table = result[0]            
    
    elif posthoc_method == 'tukey':
        result = mc.tukeyhsd()
        result_table = result.summary()
        
    return result_table


def posthoc_between(df, vars, group_vars, group_names, parametric: bool, posthoc_method):

    cond_list = []
    for n in range(len(group_names)):
        cond = df[group_vars] == group_names[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df[vars], selected_df[group_vars])
    
    if posthoc_method == 'bonf':
        if parametric:
            result = mc.allpairtest(stats.ttest_ind, method ='bonf')
            result_table = result[0]
        
        if not parametric:
            result = mc.allpairtest(stats.mannwhitneyu, method ='bonf')
            result_table = result[0]            
    
    elif posthoc_method == 'tukey':
        result = mc.tukeyhsd()
        result_table = result.summary()
        
    return result_table

def posthoc_ways(df, dv, group_vars, group_names, parametric, posthoc_method, interaction_columns, lang_set):
    results_for_return = []
    
    for n in group_vars:
        mc = MultiComparison(df[dv], df[n])
        
        if posthoc_method == 'bonf':
            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
            result_table = result[0]
            reporting = posthoc_message_for_main_effect(n)[lang_set]
            results_for_return.append(reporting)
            results_for_return.append(result_table)
            
        
        elif posthoc_method == 'tukey':
            result = mc.tukeyhsd()
            result_table = result.summary()                
            reporting = posthoc_message_for_main_effect(n)[lang_set]
            results_for_return.append(reporting)
            results_for_return.append(result_table)
            

            
    for n in interaction_columns:
        mc = MultiComparison(df[dv], df[n])

        if posthoc_method == 'bonf':
            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
            result_table = result[0]
            reporting = posthoc_message_for_interaction[lang_set]
            results_for_return.append(reporting)
            results_for_return.append(result_table)

        
        elif posthoc_method == 'tukey':
            result = mc.tukeyhsd()    
            result_table = result.summary()               
            reporting = posthoc_message_for_interaction[lang_set]
            results_for_return.append(reporting)
            results_for_return.append(result_table)
            
    return results_for_return