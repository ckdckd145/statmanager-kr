import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats
from statsmodels.stats.anova import AnovaRM
import ast

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_ttest_rel():
    '''
    testing the dependent samples t test (vs. Scipy)
    '''
    
    result_df = sm.progress(method ='ttest_rel', vars = ['prescore', 'postscore']).df_results[1]

    prescore = df['prescore']
    postscore = df['postscore']
    series = [prescore, postscore]

    result_object = stats.ttest_rel(*series)
    
    scipy_t = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_dof = result_object.df
    scipy_ci = result_object.confidence_interval()
    scipy_ci_low = scipy_ci[0]
    scipy_ci_high = scipy_ci[1]
    
    sm_t = result_df['t-value'].item()
    sm_pvalue = result_df['p-value'].item()
    sm_dof = result_df['degree of freedom'].item()
    sm_ci = ast.literal_eval(result_df['95% CI'].item())
    sm_ci_low = sm_ci[0]
    sm_ci_high = sm_ci[1]
    
    
    assert sm_t == np.round(scipy_t, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    assert sm_dof == np.round(scipy_dof, 3)
    assert sm_ci_low == np.round(scipy_ci_low, 3)
    assert sm_ci_high == np.round(scipy_ci_high, 3)
    
    
def test_wilcoxon():
    '''
    testing the wilcoxon-signed rank test (vs. Scipy)
    '''
    
    result_df = sm.progress(method ='wilcoxon', vars = ['prescore', 'postscore']).df_results[1]

    prescore = df['prescore']
    postscore = df['postscore']
    series = [prescore, postscore]

    result_object = stats.wilcoxon(*series, method = 'approx')
    
    scipy_s = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_z = result_object.zstatistic
    
    sm_s = result_df['Test-Statistic'].item()
    sm_pvalue = result_df['p-value'].item()
    sm_z = result_df['Z-value'].item()    
    
    assert sm_s == np.round(scipy_s, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    assert sm_z == np.round(scipy_z, 3)

def test_friedman():
    '''
    testing the friedman test (vs. Scipy)
    '''
    result_df = sm.progress(method = 'friedman', vars = ['prescore', 'postscore', 'fupscore']).df_results[1]
    result_object = stats.friedmanchisquare(df['prescore'], df['postscore'], df['fupscore'])
    
    scipy_s = result_object.statistic
    scipy_pvalue = result_object.pvalue
    
    sm_s = result_df['correcting for ties'].item()
    sm_pvalue = result_df['p-value'].item()
    
    assert sm_s == np.round(scipy_s, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    

def test_rm_anova():
    '''
    testing the One-way Repeated Measures ANOVA (vs. Statsmodels)
    '''
    
    target_columns = ['prescore', 'postscore', 'fupscore']
    melted_df = df.reset_index().melt(id_vars = 'id', value_vars = target_columns)
    result_object = AnovaRM(melted_df, depvar = 'value', subject = 'id', within= ['variable']).fit()
    anova_table = result_object.anova_table
    
    result_df = sm.progress(method = 'f_oneway_rm', vars = target_columns).df_results[1]
    
    statsmodels_f = anova_table['F Value'].item()
    statsmodels_numdf = anova_table['Num DF'].item()
    statsmodels_dendf = anova_table['Den DF'].item()
    statsmodels_pvalue = anova_table['Pr > F'].item()
    
    sm_f = result_df['F Value'].item()
    sm_numdf = result_df['Num DF'].item()
    sm_dendf = result_df['Den DF'].item()
    sm_pvalue = result_df['p-value'].item()
    
    assert sm_f == np.round(statsmodels_f, 3)
    assert sm_numdf == np.round(statsmodels_numdf, 3)
    assert sm_dendf == np.round(statsmodels_dendf, 3)
    assert sm_pvalue == np.round(statsmodels_pvalue, 3)