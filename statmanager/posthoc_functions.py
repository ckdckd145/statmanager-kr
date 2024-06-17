from statsmodels.stats.multicomp import MultiComparison
from scipy import stats
import pandas as pd
from .messages_for_reporting import *

def posthoc_within(df, vars, parametric: bool, posthoc_method):
    
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=vars)
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    results_for_return = []
    
    if posthoc_method == 'bonf':
        if parametric:
            result = mc.allpairtest(stats.ttest_ind, method ='bonf')
            result_table = result[0]
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')
            
            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
            
            results_for_return.append(annotation)
            results_for_return.append(result_table)
            
        
        if not parametric:
            result = mc.allpairtest(stats.mannwhitneyu, method ='bonf')
            result_table = result[0] 
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
            
            results_for_return.append(annotation)
            results_for_return.append(result_table)         
    
    elif posthoc_method == 'tukey':
        result = mc.tukeyhsd()
        result_table = result.summary()
        
        annotation = extract_caption(result_table.as_html())
        result_table = pd.DataFrame(result_table)
        result_table = result_table.drop(index = 0)
        result_table.columns = ['group1', 'group2', 'mean differences', 'adjusted p-value', 'lower', 'upper', 'reject']
        result_table['pair no.'] = [n for n in range(1, len(result_table.index) +1 )]
        result_table = result_table.set_index('pair no.')
        
        
        for index in result_table.index:
            for column in result_table.columns:
                result_table.loc[index, column] = result_table.loc[index, column].data        
        
        
        results_for_return.append(annotation)
        results_for_return.append(result_table)

    return results_for_return


def posthoc_between(df, vars, group_vars, group_names, parametric: bool, posthoc_method):

    cond_list = []
    for n in range(len(group_names)):
        cond = df[group_vars] == group_names[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df[vars], selected_df[group_vars])
    
    results_for_return = []
    
    if posthoc_method == 'bonf':
        if parametric:
            result = mc.allpairtest(stats.ttest_ind, method ='bonf')
            result_table = result[0]
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
            
            results_for_return.append(annotation)
            results_for_return.append(result_table)
            
        
        if not parametric:
            result = mc.allpairtest(stats.mannwhitneyu, method ='bonf')
            result_table = result[0] 
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
            
            results_for_return.append(annotation)
            results_for_return.append(result_table)
                    
    
    elif posthoc_method == 'tukey':
        result = mc.tukeyhsd()
        result_table = result.summary()
        
        annotation = extract_caption(result_table.as_html())
        result_table = pd.DataFrame(result_table)
        result_table = result_table.drop(index = 0)
        result_table.columns = ['group1', 'group2', 'mean differences', 'adjusted p-value', 'lower', 'upper', 'reject']
        result_table['pair no.'] = [n for n in range(1, len(result_table.index) +1 )]
        result_table = result_table.set_index('pair no.')

        for index in result_table.index:
            for column in result_table.columns:
                result_table.loc[index, column] = result_table.loc[index, column].data
        
        results_for_return.append(annotation)
        results_for_return.append(result_table)
        
    return results_for_return

def posthoc_ways(df, dv, group_vars, parametric, posthoc_method, interaction_columns, lang_set):
    results_for_return = []
    
    for n in group_vars:
        mc = MultiComparison(df[dv], df[n])
        
        if posthoc_method == 'bonf':
            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
            result_table = result[0]
            reporting = posthoc_message_for_main_effect(n)[lang_set]
            
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')                        

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
            
            results_for_return.append(reporting)
            results_for_return.append(annotation)
            results_for_return.append(result_table)
            
        
        elif posthoc_method == 'tukey':
            result = mc.tukeyhsd()
            result_table = result.summary()                
            reporting = posthoc_message_for_main_effect(n)[lang_set]
            
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'mean differences', 'adjusted p-value', 'lower', 'upper', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) +1 )]
            result_table = result_table.set_index('pair no.')

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data
    
            results_for_return.append(reporting)
            results_for_return.append(annotation)
            results_for_return.append(result_table)
            

            
    for n in interaction_columns:
        mc = MultiComparison(df[dv], df[n])

        if posthoc_method == 'bonf':
            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
            result_table = result[0]
            reporting = posthoc_message_for_interaction[lang_set]
            
            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'stat', 'p-value', 'corrected p-value', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) + 1)]
            result_table = result_table.set_index('pair no.')            

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data            
            
            results_for_return.append(reporting)
            results_for_return.append(annotation)
            results_for_return.append(result_table)

        
        elif posthoc_method == 'tukey':
            result = mc.tukeyhsd()    
            result_table = result.summary()               
            reporting = posthoc_message_for_interaction[lang_set]

            annotation = extract_caption(result_table.as_html())
            result_table = pd.DataFrame(result_table)
            result_table = result_table.drop(index = 0)
            result_table.columns = ['group1', 'group2', 'mean differences', 'adjusted p-value', 'lower', 'upper', 'reject']
            result_table['pair no.'] = [n for n in range(1, len(result_table.index) +1 )]
            result_table = result_table.set_index('pair no.')            

            for index in result_table.index:
                for column in result_table.columns:
                    result_table.loc[index, column] = result_table.loc[index, column].data

            results_for_return.append(reporting)
            results_for_return.append(annotation)
            results_for_return.append(result_table)
            
    return results_for_return


def extract_caption(html_str):
    '''
    optional method for extracting caption parts in the multicomparision result table (statsmodels.simpletable)
    '''
    
    
    start_tag = "<caption>"
    end_tag = "</caption>"
    start_idx = html_str.find(start_tag) + len(start_tag)
    end_idx = html_str.find(end_tag)
    return html_str[start_idx:end_idx].strip()