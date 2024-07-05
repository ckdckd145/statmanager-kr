import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)



def test_kstest():
    '''
    testing the Kolmogorov-Smirnov Test (vs. Scipy)
    '''
    result_df = sm.progress(method = 'kstest', vars = 'income').df_results[0]
    
    compare_dist = (np.mean(df['income']), np.std(df['income']))
    result_object = stats.kstest(df['income'], cdf = 'norm', args = compare_dist)
    
    scipy_statistic = result_object.statistic
    scipy_pvalue = result_object.pvalue
    scipy_rvs = result_object.statistic_location
    scipy_ssn = result_object.statistic_sign 
    
    statmanager_statistic = result_df['test statistic'].item()
    statmanager_pvalue = result_df['p-value'].item()
    statmanager_rvs = result_df['maximum deviation location'].item()
    statmanager_ssn = result_df['deviation direction'].item()
    
    assert statmanager_statistic == np.round(scipy_statistic, 3)
    assert statmanager_pvalue == np.round(scipy_pvalue, 3)
    assert statmanager_rvs == np.round(scipy_rvs, 3)
    assert statmanager_ssn == np.round(scipy_ssn, 3)
    
def test_shapiro():
    '''
    testing the Shapiro-Wilks test (vs. Scipy)
    '''
    result_df = sm.progress(method = 'shapiro', vars = 'income').df_results[0]
    result_object = stats.shapiro(df['income'])
    
    scipy_statistic = result_object.statistic
    scipy_pvalue = result_object.pvalue
    
    statmanager_statistic = result_df['test statistic'].item()
    statmanager_pvalue = result_df['p-value'].item()
    
    assert statmanager_statistic == np.round(scipy_statistic, 3)
    assert statmanager_pvalue == np.round(scipy_pvalue, 3)