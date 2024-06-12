import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats
import ast
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import MultiComparison


import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


# between
## f_oneway 
## kruskal
## oneway_ancova

# within
## f_oneway_rm
## friedman
## rm_ancova

# mix
# f_nway
# f_nway_rm


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