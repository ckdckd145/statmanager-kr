import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf2.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_chi2():
    '''
    testing the Chi-squared test (vs. Scipy)
    '''
    result_df = sm.progress(method = 'chi2_contingency', vars = ['sex','condition'])
    
    cross_df = pd.crosstab(df['sex'], df['condition'])
    result_object = stats.chi2_contingency(cross_df)
    
    chi2 = result_object.statistic
    pvalue = result_object.pvalue
    dof = result_object.dof
    
    sm_chi2 = result_df['Chi Squared'].item()
    sm_pvalue = result_df['p-value'].item()
    sm_dof = result_df['degree of freedom'].item()
    
    assert sm_chi2 == np.round(chi2, 3)
    assert sm_pvalue == np.round(pvalue, 3)
    assert sm_dof == np.round(dof, 3)
    
    
def test_fisher():
    '''
    testing the fisher-exact test (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'fisher', vars = ['sex','condition'])
    
    cross_df = pd.crosstab(df['sex'], df['condition'])
    result_object = stats.fisher_exact(cross_df)
    
    statistic = result_object.statistic
    pvalue = result_object.pvalue
    
    sm_statistic = result_df['statistic'].item()
    sm_pvalue = result_df['p-value'].item()
    
    assert sm_statistic == np.round(statistic, 3)
    assert sm_pvalue == np.round(pvalue, 3)