import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats

import pytest

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_cohen_d_ttest_ind():
    '''
    testing the Cohen's D in ttest_ind
    '''
    
    sm_d = sm.progress(method = 'ttest_ind', vars = 'income', group_vars = 'sex').df_results[-1]["Cohen'd"].item()
    
    
    # raw calculation
    
    male_income = df.groupby('sex')['income'].get_group('male')
    female_income = df.groupby('sex')['income'].get_group('female')
    
    
    n1 = female_income.count()
    s1 = female_income.std()
    s1_squared = s1 ** 2
    x1 = female_income.mean()
    
    n2 = male_income.count()
    s2 = male_income.std()
    s2_squared = s2 ** 2
    x2 = male_income.mean()
    
    
    psd_up = ( (n1 - 1) * s1_squared ) + ( (n2 - 1) * s2_squared )
    psd_down = n1 + n2 - 2
    
    psd = np.sqrt(psd_up / psd_down)
    
    cohen_d = (x1 - x2) / psd
    cohen_d = np.round(cohen_d, 3)
    
    assert sm_d == cohen_d
    
def test_cohen_d_ttest_rel():
    '''
    testing the Cohen's D in ttest_ind
    '''
    
    sm_d = sm.progress(method = 'ttest_rel', vars = ['prescore', 'postscore']).df_results[-1]["Cohen's d"].item()
    
    
    # raw calculation
    
    prescores = df['prescore']
    postscores = df['postscore']
    
    
    n1 = prescores.count()
    s1 = prescores.std()
    s1_squared = s1 ** 2
    x1 = prescores.mean()
    
    n2 = postscores.count()
    s2 = postscores.std()
    s2_squared = s2 ** 2
    x2 = postscores.mean()
    
    
    psd_up = ( (n1 - 1) * s1_squared ) + ( (n2 - 1) * s2_squared )
    psd_down = n1 + n2 - 2
    
    psd = np.sqrt(psd_up / psd_down)
    
    cohen_d = (x1 - x2) / psd
    cohen_d = np.round(cohen_d, 3)
    
    assert sm_d == cohen_d