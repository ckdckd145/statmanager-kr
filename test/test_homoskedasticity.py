import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_levene():
    '''
    testing the Levene test (vs. Scipy)
    '''
    
    result_df = sm.progress(method = 'levene', vars = 'income', group_vars = 'sex').df_results[0]
    
    female = df.loc[df['sex'] == 'female', 'income']
    male = df.loc[df['sex'] == 'male', 'income']
    series = [female, male]
    result_object = stats.levene(*series)
    
    scipy_statistic = result_object.statistic
    scipy_pvalue = result_object.pvalue
    
    statmanager_statistic = result_df['test statistic'].item()
    statmanager_pvalue = result_df['p-value'].item()
    
    assert statmanager_statistic == np.round(scipy_statistic, 3)
    assert statmanager_pvalue == np.round(scipy_pvalue, 3)
    


# def test_fmax():
#     '''
#     testing the Fmax test     
#     '''
#     result_df = sm.progress(method = 'fmax', vars = 'income', group_vars = 'sex')
    
#     max_variance = df.groupby('sex')['income'].var().max().round(3)
#     min_variance = df.groupby('sex')['income'].var().min().round(3)
#     fmax = np.round(max_variance / min_variance, 3)
    
#     statmanager_max_variance = result_df['Max variance'].item()
#     statmanager_min_variance = result_df['Min variance'].item()
#     statmanager_fmax = result_df['F-max statistic'].item()
    
#     assert statmanager_max_variance == max_variance
#     assert statmanager_min_variance == min_variance
#     assert statmanager_fmax == fmax