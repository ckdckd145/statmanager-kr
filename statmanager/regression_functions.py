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
    
    # model_df1 = model.summary()
    # model_df2 = model.summary2(
    
    model_df1 = model.summary2().tables[0]
    model_df1.columns = ['index', 'value', 'index_', 'value']
    model_df1 = model_df1.set_index('index')
    model_df2 = model.summary2().tables[1].round(3)
    model_df3 = model.summary2().tables[2].round(3)
    model_df3.columns = ['index', 'value', 'index_', 'value']
    model_df3 = model_df3.set_index('index')
    warning_message = "\n".join(model.summary2().extra_txt)    
    

    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    result_for_save.append(model_df1)
    result_for_save.append(model_df2)
    result_for_save.append(model_df3)
    result_for_save.append(warning_message)

    # result_for_save.append(model_df1)
    # result_for_save.append(model_df2)
    
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
        
        model_df1 = model.summary2().tables[0]
        model_df1.columns = ['index', 'value', 'index_', 'value']
        model_df1 = model_df1.set_index('index')       
        model_df2 = model.summary2().tables[1].round(3)
        
        odds_ratio = np.exp(model.params)
        odds_ratio = pd.DataFrame(odds_ratio)
        odds_ratio.rename(columns= {0 : 'OR (Odds ratio)'}, inplace = True).round(4)
        
        results_temp = []
        results_temp.append(model_df1)
        results_temp.append(model_df2)
        results_temp.append(odds_ratio)
        
    elif len(y.unique()) > 2:
        # y = pd.get_dummies(data = y, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_')
        mapper = {}
        
        results_temp = []
        
        reference_value = y.unique()[-1]
        
        for n in range(len(y.unique())):
            mapper[y.unique()[n]] = n
        
        y = y.map(mapper)
        x = df[iv]
        x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_' )
        
        x = api.add_constant(x)
        model = api.MNLogit(y, x).fit()
        notation = notation_meesage_for_multinominal[lang_set]
        result_for_save.append(notation)
        
        model_dfs = model.summary2().tables
        
        for n in range(len(model_dfs)):
            if n == 0:
                modeldf = model_dfs[n]
                modeldf.columns = ['index', 'value', 'index_', 'value']
                modeldf = modeldf.set_index('index').round(3)
                results_temp.append(modeldf)
            else:
                modeldf = model_dfs[n].round(3)
                modeldf = modeldf.reset_index(drop=True).set_index(f"{dv} = {n-1}")
                results_temp.append(modeldf)
        
        switched_mapper = {value : key for key, value in mapper.items()}
        for key, value in switched_mapper.items():
            switched_mapper[key] = f"odds ratio: {switched_mapper[key]} vs. {reference_value}"
        
        odds_ratio = np.exp(model.params)
        odds_ratio = pd.DataFrame(odds_ratio).rename(columns = switched_mapper).round(4)
        
        results_temp.append(odds_ratio)      
        
    else:
        raise ValueError
    
    # model_df1 = model.summary()
    # model_df2 = model.summary2()
    
    reporting_one = logistic_regression_result_reporting_one(dv)[lang_set]
    reporting_two = regression_result_reporting_ivs (iv)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    
    result_for_save.extend(results_temp)
    # result_for_save.append(model_df1)
    # result_for_save.append(model_df2)
    # result_for_save.append(odds_ratio)
    
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