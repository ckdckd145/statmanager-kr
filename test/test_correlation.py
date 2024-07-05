import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)

def test_pearsonr():
    '''
    testing the pearson's r (vs. Scipy)
    '''
    
    target_columns = ['prescore', 'postscore', 'fupscore']
    
    result_object_1 = stats.pearsonr(df[target_columns[0]], df[target_columns[1]])
    result_object_2 = stats.pearsonr(df[target_columns[0]], df[target_columns[2]])
    result_object_3 = stats.pearsonr(df[target_columns[1]], df[target_columns[2]])
    
    scipy_pair_1_r = result_object_1.statistic
    scipy_pair_1_pvalue = result_object_1.pvalue
    scipy_pair_1_ci = result_object_1.confidence_interval()
    scipy_pair_1_ci_low = scipy_pair_1_ci[0]
    scipy_pair_1_ci_high = scipy_pair_1_ci[1]
    
    scipy_pair_2_r = result_object_2.statistic
    scipy_pair_2_pvalue = result_object_2.pvalue
    scipy_pair_2_ci = result_object_2.confidence_interval()
    scipy_pair_2_ci_low = scipy_pair_2_ci[0]
    scipy_pair_2_ci_high = scipy_pair_2_ci[1]
    
    scipy_pair_3_r = result_object_3.statistic
    scipy_pair_3_pvalue = result_object_3.pvalue
    scipy_pair_3_ci = result_object_3.confidence_interval()
    scipy_pair_3_ci_low = scipy_pair_3_ci[0]
    scipy_pair_3_ci_high = scipy_pair_3_ci[1]
    
    result_df = sm.progress(method = 'pearsonr', vars = target_columns).df_results[0]
    
    sm_pair_1_r = float(result_df.iloc[0, 1])
    sm_pair_1_pvalue = float(result_df.iloc[0, 2])
    sm_pair_1_ci = list(result_df.iloc[0, 3])
    sm_pair_1_ci_low = float(sm_pair_1_ci[0])
    sm_pair_1_ci_high = float(sm_pair_1_ci[1])
    
    sm_pair_2_r = float(result_df.iloc[1, 1])
    sm_pair_2_pvalue = float(result_df.iloc[1, 2])
    sm_pair_2_ci = list(result_df.iloc[1, 3])
    sm_pair_2_ci_low = float(sm_pair_2_ci[0])
    sm_pair_2_ci_high = float(sm_pair_2_ci[1])
    
    sm_pair_3_r = float(result_df.iloc[2, 1])
    sm_pair_3_pvalue = float(result_df.iloc[2, 2])
    sm_pair_3_ci = list(result_df.iloc[2, 3])
    sm_pair_3_ci_low = float(sm_pair_3_ci[0])
    sm_pair_3_ci_high = float(sm_pair_3_ci[1])
    
    assert sm_pair_1_r == np.round(scipy_pair_1_r, 3)
    assert sm_pair_1_pvalue == np.round(scipy_pair_1_pvalue, 3)
    assert sm_pair_1_ci_low == np.round(scipy_pair_1_ci_low, 3)
    assert sm_pair_1_ci_high == np.round(scipy_pair_1_ci_high, 3)
    
    assert sm_pair_2_r == np.round(scipy_pair_2_r, 3)
    assert sm_pair_2_pvalue == np.round(scipy_pair_2_pvalue, 3)
    assert sm_pair_2_ci_low == np.round(scipy_pair_2_ci_low, 3)
    assert sm_pair_2_ci_high == np.round(scipy_pair_2_ci_high, 3)
    
    assert sm_pair_3_r == np.round(scipy_pair_3_r, 3)
    assert sm_pair_3_pvalue == np.round(scipy_pair_3_pvalue, 3)
    assert sm_pair_3_ci_low == np.round(scipy_pair_3_ci_low, 3)
    assert sm_pair_3_ci_high == np.round(scipy_pair_3_ci_high, 3)
    

def test_spearmanr():
    '''
    testing the pearson's r (vs. Scipy)
    '''
    
    target_columns = ['prescore', 'postscore', 'fupscore']
    
    result_object_1 = stats.spearmanr(df[target_columns[0]], df[target_columns[1]])
    result_object_2 = stats.spearmanr(df[target_columns[0]], df[target_columns[2]])
    result_object_3 = stats.spearmanr(df[target_columns[1]], df[target_columns[2]])
    
    scipy_pair_1_r = result_object_1.statistic
    scipy_pair_1_pvalue = result_object_1.pvalue
    
    scipy_pair_2_r = result_object_2.statistic
    scipy_pair_2_pvalue = result_object_2.pvalue
    
    scipy_pair_3_r = result_object_3.statistic
    scipy_pair_3_pvalue = result_object_3.pvalue
    
    result_df = sm.progress(method = 'spearmanr', vars = target_columns).df_results[0]
    
    sm_pair_1_r = float(result_df.iloc[0, 1])
    sm_pair_1_pvalue = float(result_df.iloc[0, 2])
    
    sm_pair_2_r = float(result_df.iloc[1, 1])
    sm_pair_2_pvalue = float(result_df.iloc[1, 2])
    
    sm_pair_3_r = float(result_df.iloc[2, 1])
    sm_pair_3_pvalue = float(result_df.iloc[2, 2])
    
    assert sm_pair_1_r == np.round(scipy_pair_1_r, 3)
    assert sm_pair_1_pvalue == np.round(scipy_pair_1_pvalue, 3)

    assert sm_pair_2_r == np.round(scipy_pair_2_r, 3)
    assert sm_pair_2_pvalue == np.round(scipy_pair_2_pvalue, 3)
    
    assert sm_pair_3_r == np.round(scipy_pair_3_r, 3)
    assert sm_pair_3_pvalue == np.round(scipy_pair_3_pvalue, 3)
    
    

def test_kendallt():
    '''
    testing the pearson's r (vs. Scipy)
    '''
    
    target_columns = ['prescore', 'postscore', 'fupscore']
    
    result_object_1 = stats.kendalltau(df[target_columns[0]], df[target_columns[1]])
    result_object_2 = stats.kendalltau(df[target_columns[0]], df[target_columns[2]])
    result_object_3 = stats.kendalltau(df[target_columns[1]], df[target_columns[2]])
    
    scipy_pair_1_r = result_object_1.statistic
    scipy_pair_1_pvalue = result_object_1.pvalue
    
    scipy_pair_2_r = result_object_2.statistic
    scipy_pair_2_pvalue = result_object_2.pvalue
    
    scipy_pair_3_r = result_object_3.statistic
    scipy_pair_3_pvalue = result_object_3.pvalue
    
    result_df = sm.progress(method = 'kendallt', vars = target_columns).df_results[0]
    
    sm_pair_1_r = float(result_df.iloc[0, 1])
    sm_pair_1_pvalue = float(result_df.iloc[0, 2])
    
    sm_pair_2_r = float(result_df.iloc[1, 1])
    sm_pair_2_pvalue = float(result_df.iloc[1, 2])
    
    sm_pair_3_r = float(result_df.iloc[2, 1])
    sm_pair_3_pvalue = float(result_df.iloc[2, 2])
    
    assert sm_pair_1_r == np.round(scipy_pair_1_r, 3)
    assert sm_pair_1_pvalue == np.round(scipy_pair_1_pvalue, 3)

    assert sm_pair_2_r == np.round(scipy_pair_2_r, 3)
    assert sm_pair_2_pvalue == np.round(scipy_pair_2_pvalue, 3)
    
    assert sm_pair_3_r == np.round(scipy_pair_3_r, 3)
    assert sm_pair_3_pvalue == np.round(scipy_pair_3_pvalue, 3)