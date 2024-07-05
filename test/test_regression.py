import pandas as pd
from statmanager import Stat_Manager
import numpy as np
from scipy import stats
from statsmodels import api
import ast

df = pd.read_csv(r"./testdata/testdf.csv", index_col = 'id')
sm = Stat_Manager(df)


def test_linearr():
    '''
    testing the linear regression (vs. Statsmodels)
    '''
    
    dv = 'income'
    iv = ['age', 'sex']
    
    
    y = df[dv]
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
    x = api.add_constant(x)
    model = api.OLS(y, x).fit()
    
    table1 = model.summary2().tables[0]
    table2 = model.summary2().tables[1]
    table3 = model.summary2().tables[2]
    
    result_dfs = sm.progress(method = 'linearr', vars = [dv, iv]).df_results
    result_df1 = result_dfs[0]
    result_df2 = result_dfs[1]
    
    
    statsmodels_result1 = table1[1].to_list() + table1[3].to_list() + table3[1].to_list() + table3[3].to_list()
    sm_result1 = result_df1['Summary'].to_list()
    
    
    statsmodels_const = table2.loc['const'].to_list()
    statsmodels_age = table2.loc['age'].to_list()
    statsmodels_sex = table2.loc['dummy_male'].to_list()
    
    sm_const = result_df2.drop(columns = 'standardized coefficient beta').loc['const'].to_list()
    sm_age = result_df2.drop(columns = 'standardized coefficient beta').loc['age'].to_list()
    sm_sex = result_df2.drop(columns = 'standardized coefficient beta').loc['dummy_male'].to_list()
    
    for n in range(len(statsmodels_result1)):
        assert sm_result1[n] == statsmodels_result1[n]
    
    for n in range(len(statsmodels_const)):
        assert sm_const[n] == statsmodels_const[n]
        
    for n in range(len(statsmodels_age)):
        assert sm_age[n] == statsmodels_age[n]
        
    for n in range(len(statsmodels_sex)):
        assert sm_sex[n] == statsmodels_sex[n]
        

def test_hierlinearr():
    '''
    testing the Hierarchical Linear Regression (vs. Stasmodels & Scipy)
    '''
    
    dv = 'income'
    iv1 = ['age', 'sex']
    iv2 = ['prescore', 'postscore']
    
    y = df[dv]
    x = df[iv1]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
    x = api.add_constant(x)
    model1 = api.OLS(y, x).fit()
    
    x = df[iv1 + iv2]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
    x = api.add_constant(x)
    model2 = api.OLS(y, x).fit()
    
    m1_table1 = model1.summary2().tables[0]
    m1_table2 = model1.summary2().tables[1]
    m1_table3 = model1.summary2().tables[2]
    
    m2_table1 = model2.summary2().tables[0]
    m2_table2 = model2.summary2().tables[1]
    m2_table3 = model2.summary2().tables[2]
    
    m1_r2 = float(m1_table1.loc[6, 1])
    m2_r2 = float(m2_table1.loc[6, 1])

    statsmodels_r2_increased = m2_r2 - m1_r2

    m1_dof = float( m1_table1.loc[4, 1])
    m2_dof = float(m2_table1.loc[4, 1])

    m2_dof_residuals = float(m2_table1.loc[5, 1])

    numerator = statsmodels_r2_increased / (m2_dof - m1_dof)
    denominator = (1 - m2_r2) / m2_dof_residuals

    statsmodels_f_for_increased = numerator / denominator
    scipy_pvalue_for_f_for_increased = stats.f.sf(statsmodels_f_for_increased, m2_dof - m1_dof, m2_dof_residuals)
    
    
    result_dfs = sm.progress(method = 'hier_linearr', vars = [dv, iv1, iv2]).df_results
    
    result_df1 = result_dfs[0]
    result_df2 = result_dfs[1]
    result_df3 = result_dfs[2]
    
    sm_r2_increased = result_df1.loc['Step 2', 'R-squared increased']
    sm_f_for_increased = result_df1.loc['Step 2', 'F']
    sm_pvalue_f_for_increased = result_df1.loc['Step 2', 'p-value of F']
    
    
    # model1 
    statsmodels_m1_const = m1_table2.loc['const'].to_list()
    statsmodels_m1_age = m1_table2.loc['age'].to_list()
    statsmodels_m1_male = m1_table2.loc['dummy_male'].to_list()

    sm_m1_const = result_df3['Step 1'].loc[['const', 'age', 'dummy_male']].drop(columns = 'standardized coefficient beta').loc['const'].to_list()
    sm_m1_age = result_df3['Step 1'].loc[['const', 'age', 'dummy_male']].drop(columns = 'standardized coefficient beta').loc['age'].to_list()
    sm_m1_male = result_df3['Step 1'].loc[['const', 'age', 'dummy_male']].drop(columns = 'standardized coefficient beta').loc['dummy_male'].to_list()
    
    
    # model 2
    statsmodels_m2_const = m2_table2.loc['const'].to_list()
    statsmodels_m2_age = m2_table2.loc['age'].to_list()
    statsmodels_m2_male = m2_table2.loc['dummy_male'].to_list()    
    statsmodels_m2_prescore = m2_table2.loc['prescore'].to_list()    
    statsmodels_m2_postscore = m2_table2.loc['postscore'].to_list()    
    
    sm_m2_const = result_df3['Step 2'].drop(columns = 'standardized coefficient beta').loc['const'].to_list()
    sm_m2_age = result_df3['Step 2'].drop(columns = 'standardized coefficient beta').loc['age'].to_list()
    sm_m2_male = result_df3['Step 2'].drop(columns = 'standardized coefficient beta').loc['dummy_male'].to_list()
    sm_m2_prescore = result_df3['Step 2'].drop(columns = 'standardized coefficient beta').loc['prescore'].to_list()
    sm_m2_postscore = result_df3['Step 2'].drop(columns = 'standardized coefficient beta').loc['postscore'].to_list()
    
    
    
    statsmodels_m1_statistics = m1_table1[1].to_list() + m1_table1[3].to_list() + m1_table3[1].to_list() + m1_table3[3].to_list()
    statsmodels_m2_statistics = m2_table1[1].to_list() + m2_table1[3].to_list() + m2_table3[1].to_list() + m2_table3[3].to_list()
    
    sm_m1_statistics = result_df2['Step 1'].to_list()
    sm_m2_statistics = result_df2['Step 2'].to_list()
    
    # --- #
    
    assert sm_r2_increased == np.round(statsmodels_r2_increased, 3)
    assert sm_f_for_increased == np.round(statsmodels_f_for_increased, 3)
    assert sm_pvalue_f_for_increased == np.round(scipy_pvalue_for_f_for_increased, 3)
    
    
    for n in range(5):
        assert sm_m1_const[n] == statsmodels_m1_const[n]
        assert sm_m1_age[n] == statsmodels_m1_age[n]
        assert sm_m1_male[n] == statsmodels_m1_male[n]

        assert sm_m2_const[n] == statsmodels_m2_const[n]
        assert sm_m2_age[n] == statsmodels_m2_age[n]
        assert sm_m2_male[n] == statsmodels_m2_male[n]
        assert sm_m2_prescore[n] == statsmodels_m2_prescore[n]
        assert sm_m2_postscore[n] == statsmodels_m2_postscore[n]
        
        
    for n in range(len(statsmodels_m1_statistics)):
        
        assert sm_m1_statistics[n] == statsmodels_m1_statistics[n]
        assert sm_m2_statistics[n] == statsmodels_m2_statistics[n]
        

def test_logistic_singel():
    '''
    testing the logistic regression (vs. Statsmodels)
    '''
    
    dv = 'sex'
    iv = ['age', 'income']

    y = df[dv]
    y = pd.get_dummies(data = y, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_')
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )

    x = api.add_constant(x)
    model = api.Logit(y, x).fit()

    model_df1 = model.summary2().tables[0]
    model_df2 = model.summary2().tables[1]
    
    result_dfs = sm.progress(method = 'logisticr', vars = [dv, iv]).df_results
    
    statsmodels_statistics = model_df1[1].to_list() + model_df1[3].to_list()
    statsmodels_const = model_df2.loc['const'].round(3).to_list()
    statsmodels_age = model_df2.loc['age'].round(3).to_list()
    statsmodels_income = model_df2.loc['income'].round(3).to_list()
    
    sm_statistics = result_dfs[0]['Summary'].to_list()
    sm_const = result_dfs[1].loc['const'].to_list()
    sm_age = result_dfs[1].loc['age'].to_list()
    sm_income = result_dfs[1].loc['income'].to_list()

    
    for n in range(len(statsmodels_statistics)):
        assert sm_statistics[n] == statsmodels_statistics[n]
        
    for n in range(len(statsmodels_const)):
        assert sm_const[n] == statsmodels_const[n]
        assert sm_age[n] == statsmodels_age[n]
        assert sm_income[n] == statsmodels_income[n]
    
def test_logistic_multiple():
    '''
    testing the multiple logistic regression (vs. Statsmodels)
    '''
    
    dv = 'condition'
    iv = ['age', 'income']
    y = df[dv]

    mapper = {}
    reference_value = y.unique()[-1]

    for n in range(len(y.unique())):
        mapper[y.unique()[n]] = n

    y = y.map(mapper)
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )

    x = api.add_constant(x)
    model = api.MNLogit(y, x).fit()
    
    model_df1 = model.summary2().tables[0]
    model_df2 = model.summary2().tables[1].round(3).reset_index(drop=True).set_index('condition = 0')
    model_df3 = model.summary2().tables[2].round(3).reset_index(drop=True).set_index('condition = 1')

    result_dfs = sm.progress(method = 'logisticr', vars = [dv, iv]).df_results
    
    statsmodels_statistics = model_df1[1].to_list() + model_df1[3].to_list()
    
    statsmodels_const_cond1 = model_df2.loc['const'].to_list()
    statsmodels_age_cond1 = model_df2.loc['age'].to_list()
    statsmodels_income_cond1 = model_df2.loc['income'].to_list()
    
    statsmodels_const_cond2 = model_df3.loc['const'].to_list()
    statsmodels_age_cond2 = model_df3.loc['age'].to_list()
    statsmodels_income_cond2 = model_df3.loc['income'].to_list()
    
    sm_statistics = result_dfs[0]['Summary'].to_list()
    
    sm_const_cond1 = result_dfs[1].loc['const'].to_list()
    sm_age_cond1 = result_dfs[1].loc['age'].to_list()
    sm_income_cond1 = result_dfs[1].loc['income'].to_list()
    
    sm_const_cond2 = result_dfs[2].loc['const'].to_list()
    sm_age_cond2 = result_dfs[2].loc['age'].to_list()
    sm_income_cond2 = result_dfs[2].loc['income'].to_list()
    
    for n in range(len(statsmodels_statistics)):
        assert sm_statistics[n] == statsmodels_statistics[n]
        
    for n in range(len(statsmodels_const_cond1)):
        assert sm_const_cond1[n] == statsmodels_const_cond1[n]
        assert sm_age_cond1[n] == statsmodels_age_cond1[n]
        assert sm_income_cond1[n] == statsmodels_income_cond1[n]
        assert sm_const_cond2[n] == statsmodels_const_cond2[n]
        assert sm_age_cond2[n] == statsmodels_age_cond2[n]
        assert sm_income_cond2[n] == statsmodels_income_cond2[n]