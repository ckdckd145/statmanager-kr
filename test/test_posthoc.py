import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats
import ast
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import MultiComparison
from itertools import combinations


import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)



def test_bonf_in_f_oneway():
    '''
    testing the bonferroni in f_oneway (vs. Statsmodels/Scipy)
    '''

    result_df = sm.progress(method = 'f_oneway', vars = 'income', group_vars = 'condition', posthoc = True).df_results[-1]

    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        
    
    
def test_tukey_in_f_oneway():
    '''
    testing the tukey in f_oneway (vs. Statsmodels)
    '''

    result_df = sm.progress(method = 'f_oneway', vars = 'income', group_vars = 'condition', posthoc = True, posthoc_method = 'tukey').df_results[-1]

    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        

def test_bonf_kruskal():
    
    '''
    testing the bonferroni posthoc in kruskal (vs. Statsmodels / Scipy)
    '''
    
    result_df = sm.progress(method = 'kruskal', vars = 'income', group_vars = 'condition', posthoc = True).df_results[-1]
    
    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        
def test_tukey_kruskal():
    '''
    testing the tukey HSD posthoc in kruskal (vs. Statsmodels)
    '''
    
    result_df = sm.progress(method = 'kruskal', vars = 'income', group_vars = 'condition', posthoc = True, posthoc_method = 'tukey').df_results[-1]
    
    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]

def test_bonf_oneway_ancova():
    '''
    testing the bonferroni in oneway_ancova (vs. Statsmodels/Scipy)
    '''
    
    result_df = sm.progress(method = 'oneway_ancova', vars = ['income', ['age']], group_vars = 'condition', posthoc = True).df_results[-1]
    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]

def test_tukey_oneway_ancova():
    '''
    testing the tukeyhsd in oneway_ancova (vs. Statsmodels)
    '''
    
    result_df = sm.progress(method = 'oneway_ancova', vars = ['income', ['age']], group_vars = 'condition', posthoc = True, posthoc_method = 'tukey').df_results[-1]
    groups = df['condition'].unique()
    
    cond_list = []
    for n in range(len(groups)):
        cond = df['condition'] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = df[selected_rows]
    
    mc = MultiComparison(selected_df['income'], selected_df['condition'])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]

def test_bonf_f_oneway_rm():
    '''
    testing the bonferroni in f_oneway_rm (vs. Statsmodels/Scipy)
    '''
    
    target_variables = ['prescore', 'postscore', 'fupscore']
    result_df = sm.progress(method = 'f_oneway_rm', vars = target_variables, posthoc = True).df_results[-1]
    
    index_col = df.index.name
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=target_variables)
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        
def test_tukey_f_oneway_rm():
    '''
    testing the tukey hsd in f_oneway_rm (vs. Statsmodels)
    '''
    
    target_variables = ['prescore', 'postscore', 'fupscore']
    result_df = sm.progress(method = 'f_oneway_rm', vars = target_variables, posthoc = True, posthoc_method = 'tukey').df_results[-1]
    
    index_col = df.index.name
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=['prescore', 'postscore', 'fupscore'])
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        

def test_bonf_friedman():
    '''
    testing the bonferroni in friedman (vs. Statsmodels/Scipy)
    '''
    
    target_variables = ['prescore', 'postscore', 'fupscore']
    result_df = sm.progress(method = 'friedman', vars = target_variables, posthoc = True).df_results[-1]
    
    index_col = df.index.name
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=['prescore', 'postscore', 'fupscore'])
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])

    result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        

def test_tukey_friedman():
    '''
    testing the tukey in friedman (vs. Statsmodels/Scipy)
    '''
    
    target_variables = ['prescore', 'postscore', 'fupscore']
    result_df = sm.progress(method = 'friedman', vars = target_variables, posthoc = True, posthoc_method = 'tukey').df_results[-1]
    
    index_col = df.index.name
    posthoc_df = df.reset_index().melt(id_vars=index_col, value_vars=['prescore', 'postscore', 'fupscore'])
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])

    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        

def test_bonf_rm_ancova():
    '''
    testing the bonferroni in rm_ancova (vs. Statsmodels/Scipy)
    '''
    
    result_df = sm.progress(method = 'rm_ancova', vars = ['prescore', 'postscore', 'fupscore', ['income']], posthoc = True).df_results[-1]
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = ['prescore', 'postscore', 'fupscore'])
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        

def test_tukey_rm_ancova():
    '''
    testing tukey in rm_ancova (vs. Statsmodels/Scipy)
    '''

    result_df = sm.progress(method = 'rm_ancova', vars = ['prescore', 'postscore', 'fupscore', ['income']], posthoc = True, posthoc_method = 'tukey').df_results[-1]
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = ['prescore', 'postscore', 'fupscore'])
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
            
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
            
    sm_1 = result_df.loc[1].to_list()
    sm_2 = result_df.loc[2].to_list()
    sm_3 = result_df.loc[3].to_list()
    
    statsmodels_1 = result_table.iloc[0].to_list()
    statsmodels_2 = result_table.iloc[1].to_list()
    statsmodels_3 = result_table.iloc[2].to_list()
    
    for n in range(len(sm_1)):
        assert sm_1[n] == statsmodels_1[n]
        assert sm_2[n] == statsmodels_2[n]
        assert sm_3[n] == statsmodels_3[n]
        
def test_bonf_f_nway():
    '''
    Testing the bonf in 2-way ANOVA (vs. Statsmodels/Scipy)
    '''
    group_vars = ['sex','condition']
    dv = 'income'

    result_dfs = sm.progress(method = 'f_nway',vars = dv, group_vars = group_vars, posthoc = True).df_results[-3:]
    
    # main-effect-posthoc
    for n in range(len(group_vars)):
        group_var = group_vars[n]    
        groups = df[group_var].unique()
        
        result_df = result_dfs[n]
        
        
        cond_list = []
        for n in range(len(groups)):
            cond = df[group_var] == groups[n]
            cond_list.append(cond)
        
        selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
        selected_df = df[selected_rows]
        
        mc = MultiComparison(selected_df[dv], selected_df[group_var])
        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
        result_table = pd.DataFrame(result[0])
        original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
        result_table = result_table.drop(index = 0)
        result_table.columns = original_columns
        
        for index in result_table.index:
            for column in result_table.columns:
                result_table.loc[index, column] = result_table.loc[index, column].data
                
        
        for n in range(len(result_table.index)):
            
            statmanager = result_df.iloc[n].to_list()
            statsmodels = result_table.iloc[n].to_list()
            
            
            for n in range(len(statmanager)):
                assert statmanager[n] == statsmodels[n]
    
    # interaction-effect-posthoc 
    interactions = []
    new_df = df.copy() 
    result_df = result_dfs[-1]

    for n in range(2, len(group_vars) + 1):
        for combo in combinations(group_vars, n):
            interaction_name = "interaction_" + "_".join(combo)
            
            interaction_values = df[list(combo)].astype(str).agg('_'.join, axis=1)
            
            new_df[interaction_name] = interaction_values
            interactions.append(interaction_name)


    groups = new_df[interaction_name].unique()

    cond_list = []

    for n in range(len(groups)):
        cond = new_df[interaction_name] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = new_df[selected_rows]
    mc = MultiComparison(selected_df[dv], selected_df[interaction_name])
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns

    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
            
            
def test_tukey_f_nway():
    '''
    Testing the bonf in 2-way ANOVA (vs. Statsmodels/Scipy)
    '''
    group_vars = ['sex','condition']
    dv = 'income'

    result_dfs = sm.progress(method = 'f_nway',vars = dv, group_vars = group_vars, posthoc = True, posthoc_method = 'tukey').df_results[-3:]
    
    # main-effect-posthoc
    for n in range(len(group_vars)):
        group_var = group_vars[n]    
        groups = df[group_var].unique()
        
        result_df = result_dfs[n]
        
        
        cond_list = []
        for n in range(len(groups)):
            cond = df[group_var] == groups[n]
            cond_list.append(cond)
        
        selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
        selected_df = df[selected_rows]
        
        mc = MultiComparison(selected_df[dv], selected_df[group_var])
        result = mc.tukeyhsd()
        result_table = result.summary()

        result_table = pd.DataFrame(result_table)
        result_table = result_table.drop(index = 0)
        result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
        
        for index in result_table.index:
            for column in result_table.columns:
                result_table.loc[index, column] = result_table.loc[index, column].data
                
        
        for n in range(len(result_table.index)):
            
            statmanager = result_df.iloc[n].to_list()
            statsmodels = result_table.iloc[n].to_list()
            
            
            for n in range(len(statmanager)):
                assert statmanager[n] == statsmodels[n]
    
    # interaction-effect-posthoc 
    interactions = []
    new_df = df.copy() 
    result_df = result_dfs[-1]

    for n in range(2, len(group_vars) + 1):
        for combo in combinations(group_vars, n):
            interaction_name = "interaction_" + "_".join(combo)
            
            interaction_values = df[list(combo)].astype(str).agg('_'.join, axis=1)
            
            new_df[interaction_name] = interaction_values
            interactions.append(interaction_name)


    groups = new_df[interaction_name].unique()

    cond_list = []

    for n in range(len(groups)):
        cond = new_df[interaction_name] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = new_df[selected_rows]
    mc = MultiComparison(selected_df[dv], selected_df[interaction_name])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']

    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
            
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]

def test_bonf_f_nway_rm():
    '''
    testing the bonf in f_nway_rm (vs. Statsmodels/Scipy)
    '''
    
    dvs = ['prescore', 'postscore', 'fupscore']
    group_vars = 'condition'
    
    result_dfs = sm.progress(method = 'f_nway_rm', vars = dvs, group_vars = 'condition', posthoc = True).df_results[-3:]

    
    # main-effect-posthoc (repeated-measures)
    
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs)
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
    
    result_df = result_dfs[1]
    
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
            
    # main-effect-posthoc (group variable)
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs, var_name = 'time').set_index(index_col)
    merged_df = df.drop(columns = dvs).merge(posthoc_df, how = 'outer', on = index_col)
    new_dv = 'value'

    mc = MultiComparison(merged_df[new_dv], merged_df['condition'])
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns

    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data


    result_df = result_dfs[0]
        
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
    
    
    # interaction
    index_col = df.index.name
    group_vars = ['condition', 'time']


    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs, var_name = 'time').set_index(index_col)
    merged_df = df.drop(columns = dvs).merge(posthoc_df, how = 'outer', on = index_col)

    interactions = []
    new_df = merged_df.copy()

    for n in range(2, len(group_vars) + 1):
        for combo in combinations(group_vars, n):
            interaction_name = "interaction_" + "_".join(combo)
            
            interaction_values = merged_df[list(combo)].astype(str).agg('_'.join, axis=1)
            
            new_df[interaction_name] = interaction_values
            interactions.append(interaction_name)
            
    groups = new_df[interaction_name].unique()

    cond_list = []

    for n in range(len(groups)):
        cond = new_df[interaction_name] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = new_df[selected_rows]
    mc = MultiComparison(selected_df['value'], selected_df[interaction_name])
    result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    result_table = pd.DataFrame(result[0])
    original_columns = ['group1', 'group2', 'stat', 'pval', 'pval_corr', 'reject']
    result_table = result_table.drop(index = 0)
    result_table.columns = original_columns


    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data

    result_df = result_dfs[-1]
            
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
            
            
def test_tukey_f_nway_rm():
    '''
    testing the tukey in f_nway_rm (vs. Statsmodels)
    '''
    
    dvs = ['prescore', 'postscore', 'fupscore']
    group_vars = 'condition'
    
    result_dfs = sm.progress(method = 'f_nway_rm', vars = dvs, group_vars = 'condition', posthoc = True, posthoc_method = 'tukey').df_results[-3:]

    
    # main-effect-posthoc (repeated-measures)
    
    index_col = df.index.name
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs)
    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
    
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']
    
    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data
    
    result_df = result_dfs[1]
    
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
            
    # main-effect-posthoc (group variable)
    
    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs, var_name = 'time').set_index(index_col)
    merged_df = df.drop(columns = dvs).merge(posthoc_df, how = 'outer', on = index_col)
    new_dv = 'value'

    mc = MultiComparison(merged_df[new_dv], merged_df['condition'])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']

    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data


    result_df = result_dfs[0]
        
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]
    
    
    # interaction
    index_col = df.index.name
    group_vars = ['condition', 'time']


    posthoc_df = df.reset_index().melt(id_vars = index_col, value_vars = dvs, var_name = 'time').set_index(index_col)
    merged_df = df.drop(columns = dvs).merge(posthoc_df, how = 'outer', on = index_col)

    interactions = []
    new_df = merged_df.copy()

    for n in range(2, len(group_vars) + 1):
        for combo in combinations(group_vars, n):
            interaction_name = "interaction_" + "_".join(combo)
            
            interaction_values = merged_df[list(combo)].astype(str).agg('_'.join, axis=1)
            
            new_df[interaction_name] = interaction_values
            interactions.append(interaction_name)
            
    groups = new_df[interaction_name].unique()

    cond_list = []

    for n in range(len(groups)):
        cond = new_df[interaction_name] == groups[n]
        cond_list.append(cond)
        
    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
    selected_df = new_df[selected_rows]
    mc = MultiComparison(selected_df['value'], selected_df[interaction_name])
    result = mc.tukeyhsd()
    result_table = result.summary()

    result_table = pd.DataFrame(result_table)
    result_table = result_table.drop(index = 0)
    result_table.columns = ['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject']


    for index in result_table.index:
        for column in result_table.columns:
            result_table.loc[index, column] = result_table.loc[index, column].data

    result_df = result_dfs[-1]
            
    for n in range(len(result_table.index)):
        statmanager = result_df.iloc[n].to_list()
        statsmodels = result_table.iloc[n].to_list()
        
        for n in range(len(statmanager)):
            assert statmanager[n] == statsmodels[n]