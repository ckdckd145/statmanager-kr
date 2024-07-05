import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_cronbach():
    '''
    testing the cronbach's alpha caclucalation (vs. Pandas)
    '''
    
    # copy of the cronbach() in reliability_functions.py
    target_columns = ['prescore', 'postscore', 'fupscore']
    
    k = len(target_columns)
    n = len(df)
    
    covariance_matrix = df[target_columns].cov()
    sum_of_variances = np.trace(covariance_matrix)
    total_variance = covariance_matrix.sum().sum()
    
    cronbach = (k / (k-1)) * (1 - sum_of_variances / total_variance )
    
    
    result_df = sm.progress(method = 'cronbach', vars = target_columns).df_results[0]
    sm_cronbach = result_df["cronbach's alpha"].item()
    
    assert sm_cronbach == np.round(cronbach, 3)