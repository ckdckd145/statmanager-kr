import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats
import ast

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)

def test_ttest_ind():
    '''
    testing the ttest_ind (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'ttest_ind', vars = 'income', group_vars = 'sex').df_results[1]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.ttest_ind(*series, equal_var = True)

    scipy_t = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_dof = result_object.df
    scipy_ci = result_object.confidence_interval()
    scipy_ci_low = scipy_ci[0]
    scipy_ci_high = scipy_ci[1]
    
    sm_t = result_df.loc['income', 't-value']
    sm_pvalue = result_df.loc['income', 'p-value']
    sm_dof = result_df.loc['income', 'degree of freedom']
    sm_ci = ast.literal_eval(result_df.loc['income', '95% CI'])
    sm_ci_low = sm_ci[0]
    sm_ci_high = sm_ci[1]
    
    
    assert sm_t == np.round(scipy_t, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    assert sm_dof == np.round(scipy_dof, 3)
    assert sm_ci_low == np.round(scipy_ci_low, 3)
    assert sm_ci_high == np.round(scipy_ci_high, 3)
    
    
def test_ttest_ind_unequal():
    '''
    testing the ttest_ind_welch (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'ttest_ind_welch', vars = 'income', group_vars = 'sex').df_results[1]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.ttest_ind(*series, equal_var = False)

    scipy_t = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_dof = result_object.df
    scipy_ci = result_object.confidence_interval()
    scipy_ci_low = scipy_ci[0]
    scipy_ci_high = scipy_ci[1]
    
    sm_t = result_df.loc['income', 't-value']
    sm_pvalue = result_df.loc['income', 'p-value']
    sm_dof = result_df.loc['income', 'degree of freedom']
    sm_ci = ast.literal_eval(result_df.loc['income', '95% CI'])
    sm_ci_low = sm_ci[0]
    sm_ci_high = sm_ci[1]
    
    
    assert sm_t == np.round(scipy_t, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    assert sm_dof == np.round(scipy_dof, 3)
    assert sm_ci_low == np.round(scipy_ci_low, 3)
    assert sm_ci_high == np.round(scipy_ci_high, 3)
    

def test_ttest_ind_trim():
    '''
    testing the ttest_ind_trim (yuen) (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'ttest_ind_trim', vars = 'income', group_vars = 'sex').df_results[1]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.ttest_ind(*series, trim = 0.2)

    scipy_t = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_dof = result_object.df
    scipy_ci = result_object.confidence_interval()
    scipy_ci_low = scipy_ci[0]
    scipy_ci_high = scipy_ci[1]
    
    sm_t = result_df.loc['income', 't-value']
    sm_pvalue = result_df.loc['income', 'p-value']
    sm_dof = result_df.loc['income', 'degree of freedom']
    sm_ci = ast.literal_eval(result_df.loc['income', '95% CI'])
    sm_ci_low = sm_ci[0]
    sm_ci_high = sm_ci[1]
    
    
    assert sm_t == np.round(scipy_t, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    assert sm_dof == np.round(scipy_dof, 3)
    assert sm_ci_low == np.round(scipy_ci_low, 3)
    assert sm_ci_high == np.round(scipy_ci_high, 3)


def test_mannwhitneyu():
    '''
    testing the mann-whitney u test (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'mannwhitneyu', vars = 'income', group_vars = 'sex').df_results[1]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.mannwhitneyu(*series)

    scipy_u = result_object.statistic
    scipy_pvalue = result_object.pvalue

    sm_u = result_df.loc['income', 'U-value']
    sm_pvalue = result_df.loc['income', 'p-value']

    
    assert sm_u == np.round(scipy_u, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)
    
def test_brunner():
    '''
    testing the brunner-munzel test (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'brunner', vars = 'income', group_vars = 'sex').df_results[1]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.brunnermunzel(*series)

    scipy_w = result_object.statistic
    scipy_pvalue = result_object.pvalue

    sm_w = result_df.loc['income', 'W-value']
    sm_pvalue = result_df.loc['income', 'p-value']

    
    assert sm_w == np.round(scipy_w, 3)
    assert sm_pvalue == np.round(scipy_pvalue, 3)