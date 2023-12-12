import pandas as pd
from .messages_for_reporting import *
from .making_figure import *
from statsmodels import api

def linear(df: pd.DataFrame, vars : list, lang_set, testname):
    result_for_save = []
    
    dv = vars[0]
    iv = vars[1] # should be list "in the list"
    
    
    y = df[dv]
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_' )
    
    x = api.add_constant(x)
    model = api.OLS(y, x).fit()
    
    reporting_one = linear_regression_result_reporting_one (dv)[lang_set]
    reporting_two = regression_result_reporting_ivs (iv)[lang_set]
    
    model_df1 = model.summary()
    model_df2 = model.summary2()
    
    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    result_for_save.append(model_df1)
    result_for_save.append(model_df2)
    
    print(testname)
    for n in result_for_save:
        if isinstance(n, str or list):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)

    return result_for_save

def logistic(df: pd.DataFrame, vars : list, lang_set, testname):
    result_for_save = []
    
    dv = vars[0]
    iv = vars[1] # should be list "in the list"
    
    y = df[dv]

    if len(y.unique()) == 2:    
        y = pd.get_dummies(data = y, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_')
        x = df[iv]
        x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_' )
        
        x = api.add_constant(x)
        model = api.Logit(y, x).fit()
        
    elif len(y.unique()) > 2:
        y = pd.get_dummies(data = y, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_')
        x = df[iv]
        x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_' )
        
        x = api.add_constant(x)
        model = api.MNLogit(y, x).fit()
        notation = notation_meesage_for_multinominal[lang_set]
        result_for_save.append(notation)
    
    else:
        raise ValueError
    
    model_df1 = model.summary()
    model_df2 = model.summary2()
    
    reporting_one = logistic_regression_result_reporting_one(dv)[lang_set]
    reporting_two = regression_result_reporting_ivs (iv)[lang_set]
    
    odds_ratio = np.exp(model.params)
    odds_ratio = pd.DataFrame(odds_ratio)
    odds_ratio.rename(columns= {0 : 'OR (Odds ratio)'}, inplace = True)
    
    
    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    result_for_save.append(model_df1)
    result_for_save.append(model_df2)
    result_for_save.append(odds_ratio)
    
    print(testname)
    for n in result_for_save:
        if isinstance(n, str or list):
            print (n)
        else:
            try:
                display(n)
            except:
                print(n)
                
    return result_for_save