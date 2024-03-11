import pandas as pd
import numpy as np
from .messages_for_reporting import *
from .making_figure import *
from statsmodels import api

def linear(df: pd.DataFrame, vars : list, lang_set, testname):
    result_for_save = []
    
    dv = vars[0]
    iv = vars[1] # should be list "in the list"
    
    
    y = df[dv]
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
    
    x = api.add_constant(x)
    model = api.OLS(y, x).fit()
    df_for_model = pd.concat([x, y], axis = 1)
    y_std = np.std(df_for_model[dv])
    
    reporting_one = linear_regression_result_reporting_one (dv)[lang_set]
    reporting_two = regression_result_reporting_ivs (iv)[lang_set]
    
    
    model_df1 = model.summary2().tables[0]
    # model_df1.columns = ['index', 'value', 'index_', 'value']
    # model_df1 = model_df1.set_index('index')
    model_df2 = model.summary2().tables[1].round(3)
    model_df2.columns = ['unstandadrized coefficient', 'standard error', 't', 'p-value', '95% CI Low', '95% CI High']
    model_df3 = model.summary2().tables[2].round(3)
    # model_df3.columns = ['index', 'value', 'index_', 'value']
    # model_df3 = model_df3.set_index('index')
    warning_message = "\n".join(model.summary2().extra_txt)    
    
    for index in model_df2.index:
        x_std = np.std(df_for_model[index])
        coef = model_df2.loc[index, 'unstandadrized coefficient']
        stand_coef = coef * (x_std/y_std)
        model_df2.loc[index, 'standardized coefficient beta'] = stand_coef
    
    model_df2 = model_df2[['unstandadrized coefficient', 'standard error', 'standardized coefficient beta', 'p-value', '95% CI Low', '95% CI High']]
    
    data1 = model_df1[[0, 1]]
    data2 = model_df1[[2, 3]]
    data3 = model_df3[[0, 1]]
    data4 = model_df3[[2, 3]]
    
    key = data1[0].to_list() + data2[2].to_list() + data3[0].to_list() + data4[2].to_list()
    value = data1[1].to_list() + data2[3].to_list() + data3[1].to_list() + data4[3].to_list()
    
    reframed_model_df = {}
    for j in range(len(key)):
        key_v = key[j]
        value_v = value[j]
        
        reframed_model_df[key_v] = value_v
        
    reframed_model_df = pd.DataFrame(reframed_model_df, index = ['Summary']).T.round(4)

    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    result_for_save.append(reframed_model_df)
    # result_for_save.append(model_df1)
    result_for_save.append(model_df2)
    # result_for_save.append(model_df3)
    result_for_save.append(warning_message)


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

def hierarchical_linear (df: pd.DataFrame, vars : list, lang_set, testname):
    result_for_save=[]
    
    dv = vars[0]
    
    steps = []
    for v in vars:
        if isinstance(v, list):
            steps.append(v)
        else:
            pass
    
    number_of_steps = len(steps)
    y = df[dv]
    
    models = []
    df_for_models = []
    for n in range(number_of_steps):
        if n == 0 :
            x = df[steps[n]]
            x = pd.get_dummies(data = x ,drop_first=True, dtype = 'int', prefix = 'dummy', prefix_sep='_')
            x = api.add_constant(x)
            model = api.OLS(y, x).fit()
            df_for_model = pd.concat([x, y], axis = 1)
            df_for_models.append(df_for_model)
            models.append(model)
        else:
            ivs = []
            for _ in range(n + 1):
                ivs += steps[_]
            x = df[ivs]
            x = pd.get_dummies(data = x ,drop_first=True, dtype = 'int', prefix = 'dummy', prefix_sep='_')
            x = api.add_constant(x)
            model = api.OLS(y, x).fit()
            df_for_model = pd.concat([x, y], axis = 1)
            df_for_models.append(df_for_model)            
            models.append(model)
    
    model_statistic_dfs = []
    variable_coeff_dfs = []
    warning_messages = []
    
    for n in range(number_of_steps):
        model = models[n]
        
        df_for_model_ = df_for_models[n]
        y_std = np.std(df_for_model_[dv])
        
        model_df1 = model.summary2().tables[0]
        model_df2 = model.summary2().tables[1]
        model_df2.columns = ['unstandadrized coefficient', 'standard error', 't', 'p-value', '95% CI Low', '95% CI High']
        
        for index in model_df2.index:
            x_std = np.std(df_for_model_[index])
            coef = model_df2.loc[index, 'unstandadrized coefficient']
            stand_coef = coef * (x_std/y_std)
            model_df2.loc[index, 'standardized coefficient beta'] = stand_coef
        
        model_df2 = model_df2[['unstandadrized coefficient', 'standard error', 'standardized coefficient beta', 'p-value', '95% CI Low', '95% CI High']]
        model_df2.columns = pd.MultiIndex.from_product([[f'Step {n+1}'], model_df2.columns])
        model_df3 = model.summary2().tables[2]
        warning_message = "\n".join(model.summary2().extra_txt)
        warning_messages.append(warning_message)

        data1 = model_df1[[0, 1]]
        data2 = model_df1[[2, 3]]
        data3 = model_df3[[0, 1]]
        data4 = model_df3[[2, 3]]

        key = data1[0].to_list() + data2[2].to_list() + data3[0].to_list() + data4[2].to_list()
        value = data1[1].to_list() + data2[3].to_list() + data3[1].to_list() + data4[3].to_list()
        
        reframed_model_df = {}
        for j in range(len(key)):
            key_v = key[j]
            value_v = value[j]
            
            reframed_model_df[key_v] = value_v
        
        reframed_model_df = pd.DataFrame(reframed_model_df, index = [f'Step {n+1}']).T # df in statistics . model_df2 = coeff df
        model_statistic_dfs.append(reframed_model_df)
        variable_coeff_dfs.append(model_df2)
    
    model_statistic_dfs_result = pd.concat(model_statistic_dfs, axis = 1).round(3) # for showing
    variable_coeff_dfs_result = pd.concat(variable_coeff_dfs, axis = 1).round(3) # for showing
    
    results = []
    
    first_model_r2 = float(model_statistic_dfs[0].loc['R-squared:'].item())
    first_model_p_value = float(model_statistic_dfs[0].loc['Prob (F-statistic):'].item())
    
    results.append([None, first_model_r2, first_model_p_value, None, None, None])  # added, r2, p(of model), r2_in, f_, p (of f)
    for i in range(1, len(model_statistic_dfs)):
        prev_model = model_statistic_dfs[i - 1]
        current_model = model_statistic_dfs[i]
        
        r2_prev_model = float(prev_model.loc['R-squared:'].item())
        r2_current_model = float(current_model.loc['R-squared:'].item())
        
        dof_prev_model = float(prev_model.loc['Df Model:'].item())
        dof_current_model = float(current_model.loc['Df Model:'].item())
        
        dof_residuals_current_model = float(current_model.loc['Df Residuals:'].item())
        
        r2_increased = r2_current_model - r2_prev_model
        
        numerator = r2_increased / (dof_current_model - dof_prev_model)
        denominator = (1 - r2_current_model) / dof_residuals_current_model
        
        f_value = numerator / denominator
        p_value_of_f = stats.f.sf(f_value, dof_current_model - dof_prev_model, dof_residuals_current_model)
        
        p_value_of_current_model = float(current_model.loc['Prob (F-statistic):'].item())
        
        vars_list_prev_model = variable_coeff_dfs[i - 1].index.to_list()
        vars_list_current_model = variable_coeff_dfs[i].index.to_list()
        
        for var in vars_list_prev_model:
            if var in vars_list_current_model:
                vars_list_current_model.remove(var)
        added_vars = ", ".join(vars_list_current_model)
        
        results.append([added_vars, r2_current_model, p_value_of_current_model, r2_increased, f_value, p_value_of_f])
        
    result_df = pd.DataFrame(results, columns = ['added_vars', 'R-squared of Model', 'p-value of Model', 'R-squared increased', 'F', 'p-value of F']).round(3)
    result_df.index = [f'Step {i}' for i in range(1, len(results) + 1)]

    
    result_for_save.append(result_df)
    result_for_save.append(model_statistic_dfs_result)
    result_for_save.append(variable_coeff_dfs_result)
    result_for_save.append(warning_messages[-1])
    
    
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
        mapper = ""
        y = pd.get_dummies(data = y, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_')
        x = df[iv]
        x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
        
        x = api.add_constant(x)
        model = api.Logit(y, x).fit()
        
        model_df1 = model.summary2().tables[0]
        data1 = model_df1[[0, 1]]
        data2 = model_df1[[2, 3]]
        
        key = data1[0].to_list() + data2[2].to_list()
        value = data1[1].to_list() + data2[3].to_list()
        
        reframed_model_df = {}
        for j in range(len(key)):
            key_v = key[j]
            value_v = value[j]
            
            reframed_model_df[key_v] = value_v
        reframed_model_df = pd.DataFrame(reframed_model_df, index = ['Summary']).T.round(4)
        
        # model_df1.columns = ['index', 'value', 'index_', 'value']
        # model_df1 = model_df1.set_index('index')       
        model_df2 = model.summary2().tables[1].round(3)
        model_df2.columns = ['coefficient', 'standard error', 't', 'p-value', '95% CI Low', '95% CI High']
        
        odds_ratio = np.exp(model.params)
        odds_ratio = pd.DataFrame(odds_ratio)
        odds_ratio.rename(columns= {0 : 'OR (Odds ratio)'}, inplace = True)
        
        results_temp = []
        results_temp.append(reframed_model_df)
        # results_temp.append(model_df1)
        results_temp.append(model_df2)
        results_temp.append(odds_ratio)
        
    elif len(y.unique()) > 2:
        
        mapper = {}
        
        results_temp = []
        
        reference_value = y.unique()[-1]
        
        for n in range(len(y.unique())):
            mapper[y.unique()[n]] = n
        
        y = y.map(mapper)
        x = df[iv]
        x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy',prefix_sep='_' )
        
        x = api.add_constant(x)
        model = api.MNLogit(y, x).fit()
        notation = notation_meesage_for_multinominal[lang_set]
        result_for_save.append(notation)
        
        model_dfs = model.summary2().tables
        
        for n in range(len(model_dfs)):
            if n == 0:
                modeldf = model_dfs[n]
                
                data1 = modeldf[[0,1]]
                data2 = modeldf[[2,3]]
                
                key = data1[0].to_list() + data2[2].to_list()
                value = data1[1].to_list() + data2[3].to_list()
                
                reframed_model_df = {}
                for j in range(len(key)):
                    key_v = key[j]
                    value_v = value[j]
                    
                    reframed_model_df[key_v] = value_v
                reframed_model_df = pd.DataFrame(reframed_model_df, index = ['Summary']).T.round(4)

                # modeldf.columns = ['index', 'value', 'index_', 'value']
                # modeldf = modeldf.set_index('index').round(3)
                results_temp.append(reframed_model_df)
            else:
                modeldf = model_dfs[n].round(3)
                modeldf = modeldf.reset_index(drop=True).set_index(f"{dv} = {n-1}")
                modeldf.columns = ['coefficient', 'standard error', 't', 'p-value', '95% CI Low', '95% CI High']
                results_temp.append(modeldf)
        
        switched_mapper = {value : key for key, value in mapper.items()}
        for key, value in switched_mapper.items():
            switched_mapper[key] = f"odds ratio: {switched_mapper[key]} vs. {reference_value}"
        
        odds_ratio = np.exp(model.params)
        odds_ratio = pd.DataFrame(odds_ratio).rename(columns = switched_mapper)
        
        results_temp.append(odds_ratio)      
        
    else:
        raise ValueError
    
    reporting_one = logistic_regression_result_reporting_one(dv, mapper)[lang_set]
    reporting_two = regression_result_reporting_ivs (iv)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(reporting_two)
    
    result_for_save.extend(results_temp)
    
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