import pandas as pd
from .messages_for_reporting import *
from .posthoc_functions import *

from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

# RULE :  args for 'vars' --> [dv, [covar]]

def oneway_ancova(df:pd.DataFrame, vars: list, lang_set, testname, posthoc, posthoc_method, group_vars = None):
    
    result_for_save = []
    
    group_names = df[group_vars].unique()
    
    
    dv = vars[0] # str
    covars = vars[1] # list
    
    iv = group_vars # str
    
    covar_df = pd.get_dummies(df[covars], drop_first=True, dtype='float', prefix = 'dummy_')
    
    new_covars = []
    for covar in covars:
        if covar in covar_df.columns:
            covar_df = covar_df.drop(columns = covar)
            new_covars.append(covar)
    new_covars += covar_df.columns.to_list()
    
    df = df.merge(covar_df, left_index=True, right_index = True, how = 'left')
    
    vars_for_custom_join = [dv, new_covars]
    
    describe_vars = [dv] + new_covars
    
    formula_for_olsmodel = custom_join_for_ancova(vars = vars_for_custom_join, group_vars = group_vars, method = 'oneway_ancova')
    print(formula_for_olsmodel)
    olsmodel = ols(formula_for_olsmodel, data = df).fit()    
    
    describe_df = df.groupby(group_vars)[describe_vars].agg(['count', 'mean', 'median', 'std']).rename(
                    columns = {
                        'count' : 'n',
                        'std' : 'sd'
                    }).T.round(2)
    describe_df.columns.name = None

    anova_table = anova_lm(olsmodel, typ=3)
    anova_table.rename(columns = {'PR(>F)' : 'p-value'}, inplace=True)
    anova_table['partial_eta_squared'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + anova_table['sum_sq'].loc['Residual'])
    anova_table = anova_table.round(3)
    
    
    raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')

    pair_coef_table = raw_coef_table.loc[['Intercept']]
    covar_coef_table = raw_coef_table.loc[new_covars]
    drop_col_for_coef_table = ['Intercept'] + new_covars

    for n in range(len(group_names)):
                    
        formula_for_coef = custom_join_for_ancova(vars = vars_for_custom_join, group_vars = group_vars, method = 'oneway_ancova', purpose = 'coef', keys = n)
        model_for_coef = ols(formula_for_coef, data = df).fit()
        working_table_for_coef = pd.DataFrame(model_for_coef.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
        working_table_for_coef.drop(index = drop_col_for_coef_table, inplace=True)

        pair_list = working_table_for_coef.index.to_list()
        
        for i in range( len(pair_list)  ):
            for j in group_names:
                if j in pair_list[i]:
                    pair_list[i] = j
                    
        set_for_finding_ref_1 = set(group_names)
        set_for_finding_ref_2 = set(pair_list)
        reference_col = list(set_for_finding_ref_1 - set_for_finding_ref_2)[0]
        
        for i in range( len(pair_list)  ):
            pair_list[i] = f"{reference_col} - {pair_list[i]}"
        
        working_table_for_coef.index = pair_list
        pair_coef_table = pd.concat([pair_coef_table, working_table_for_coef])
                    
    pair_coef_table['coef'] = pair_coef_table['coef'].astype('float')
    pair_coef_table = pair_coef_table.loc[~pair_coef_table['coef'].abs().duplicated(keep='first')] #before merge, delete duplicated rows
    pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) # concat with covar_coef_table 

    reporting_one = oneway_ancova_result_reporting(dv, group_vars, group_names, covars)[lang_set]
    reporting_two = ancova_model_result_reporting[lang_set]
    reporting_three = ancova_statistic_result_reporting[lang_set]
    reporting_four = ancova_coef_result_reporting[lang_set]
    reporting_five = ancova_coef_interpreting_message(covars)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    result_for_save.append(olsmodel.summary().tables[0])
    result_for_save.append(reporting_three)
    result_for_save.append(anova_table)
    result_for_save.append(reporting_four)
    result_for_save.append(reporting_five)
    result_for_save.append(pair_coef_table)

    if posthoc:
        posthoc_table = posthoc_between(df = df, vars = dv, group_vars = group_vars, group_names = group_names, parametric = True, posthoc_method = posthoc_method)
        reporting_posthoc = 'Posthoc: '
        warning= warning_message_for_ancova_posthoc[lang_set]
        result_for_save.append(reporting_posthoc)
        result_for_save.append(warning)
        result_for_save.append(posthoc_table)

    print(testname)
    for n in result_for_save:
        if isinstance(n, str):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
                
    return result_for_save 
    

def rm_ancova(df:pd.DataFrame, vars: list, group_vars, lang_set, testname, posthoc, posthoc_method):
    
    result_for_save = []
    
    index_col = df.index.name
    repeated_vars = vars [:-1]
    covars = vars[-1]
    vars_for_melting  = [index_col] + covars

    decribe_vars = ['value'] + covars


    melted_df = df.reset_index().melt(id_vars = index_col, value_vars = repeated_vars, var_name = 'time')
    melted_df = melted_df.merge(df.reset_index()[vars_for_melting], on = index_col, how = 'left').set_index(index_col)
    
    formula_for_olsmodel = custom_join_for_ancova(vars = vars, method = 'rm_ancova')
    olsmodel = ols(formula_for_olsmodel, data = melted_df).fit()
    
    describe_df = melted_df.groupby('time')[decribe_vars].agg(['count', 'mean', 'median', 'std']).rename(
                    columns = {
                        'count' : 'n',
                        'std' : 'sd'
                    }).T.round(2)
    describe_df.columns.name = None
    
    anova_table = anova_lm(olsmodel, typ=3)
    anova_table.rename(columns = {'PR(>F)' : 'p-value'}, inplace=True)
    anova_table['partial_eta_squared'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + anova_table['sum_sq'].loc['Residual'])
    anova_table = anova_table.round(3)
    
    raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')

    pair_coef_table = raw_coef_table.loc[['Intercept']]
    covar_coef_table = raw_coef_table.loc[covars]
    drop_col_for_coef_table = ['Intercept'] + covars
    
    for n in range( len (melted_df.time.unique() ) ):
        formula_for_coef = custom_join_for_ancova(vars = vars, method = 'rm_ancova', purpose = 'coef', keys = n)
        model_for_coef = ols(formula_for_coef, data = melted_df).fit()
        working_table_for_coef = pd.DataFrame(model_for_coef.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
        working_table_for_coef.drop(index = drop_col_for_coef_table, inplace=True)
        
        pair_list = working_table_for_coef.index.to_list()
        
        for i in range( len(pair_list)  ):
            for j in melted_df.time.unique():
                if j in pair_list[i]:
                    pair_list[i] = j
    
        set_for_finding_ref_1 = set(melted_df.time.unique())
        set_for_finding_ref_2 = set(pair_list)
        reference_col = list(set_for_finding_ref_1 - set_for_finding_ref_2)[0]            
        
        for i in range( len(pair_list)  ):
            pair_list[i] = f"{reference_col} - {pair_list[i]}"                    

        working_table_for_coef.index = pair_list
        pair_coef_table = pd.concat([pair_coef_table, working_table_for_coef])
    
    pair_coef_table['coef'] = pair_coef_table['coef'].astype('float')
    pair_coef_table = pair_coef_table.loc[~pair_coef_table['coef'].abs().duplicated(keep='first')] #before merge, delete duplicated rows
        
    pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) 

    reporting_one = rm_ancova_result_reporting(repeated_vars, covars)[lang_set]
    reporting_two = ancova_model_result_reporting[lang_set]
    reporting_three = ancova_statistic_result_reporting[lang_set]
    reporting_four = ancova_coef_result_reporting[lang_set]
    reporting_five = ancova_coef_interpreting_message(covars)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    result_for_save.append(olsmodel.summary().tables[0])
    result_for_save.append(reporting_three)
    result_for_save.append(anova_table)
    result_for_save.append(reporting_four)
    result_for_save.append(reporting_five)
    result_for_save.append(pair_coef_table)
    
    
    if posthoc:
        posthoc_table = posthoc_within(df = df, vars = repeated_vars, parametric=True, posthoc_method=posthoc_method)
        reporting_posthoc = 'Posthoc: '
        warning= warning_message_for_ancova_posthoc[lang_set]
        result_for_save.append(reporting_posthoc)
        result_for_save.append(warning)
        result_for_save.append(posthoc_table)        
    
    print(testname)
    for n in result_for_save:
        if isinstance(n, str):
            print(n)
        else:
            try:
                display(n)
            except:
                print(n)
                
    return result_for_save     



def custom_join_for_ancova(vars = None, group_vars = None, method = None, purpose = 'normal', keys = None):
    
    if method == 'oneway_ancova':
    
        dv = vars[0]
        covars = vars[1]
        iv = group_vars 
        number = keys
        
        if purpose == 'normal':
            formula_result = f"{dv} ~ C({iv}) + {' + '.join(covars)}"
        
        elif purpose == 'coef':
            formula_result = f"{dv} ~ C({iv}, Treatment(reference={number})) + {' + '.join(covars)}"
        
        return formula_result
    
    elif method == 'rm_ancova':
        dv = 'value'
        covars = vars[-1]
        iv = 'time'
        number = keys
        
        if purpose == 'normal':
        
            formula_result = f"{dv} ~ C({iv}) + {' + '.join(covars)}"
        
        
        elif purpose == 'coef':
            
            formula_result = f"{dv} ~ C({iv}, Treatment(reference={number})) + {' + '.join(covars)}"
        
        return formula_result

    elif method == 'nway_ancova':
        
        # vars = ['dv', [covar1, covar2...] ]
        # group_vars = [group1, group2..]
        
        dv = vars[0]
        covars = vars[1]
        iv = group_vars #list 형태임
        
        formula_ivs = ""
        
        for var in iv:
            formula_ivs += f"C({var}) + "
            
        for i in range(len(iv)):
            for j in range(i + 1, len(iv)):
                item1 = f"C({iv[i]})"
                item2 = f"C({iv[j]})"
                items = f"{item1} * {item2}"
                
                formula_ivs += f"{items} + "

        formula_ivs = formula_ivs[:-2]        
        formula_result = f"{dv} ~ {formula_ivs} + {' + '.join(covars)}"

        return formula_result
    elif method == 'nway_rm_ancova':
        pass

# -- just for saving.. future development #
# def nway_ancova():
    # df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                
    #             dv = vars[0]
    #             covars = vars[1]
    #             iv = group_vars # type = list
                
    #             vars_for_showing = [dv] + covars 
                
    #             way_len = len(group_vars)
    #             new_testname = f'{way_len}-way ANCOVA'
                
    #             if self.selector == None:
    #                 testname = new_testname
                
    #             else:
    #                 pattern = repattern.compile('-way ANCOVA')
    #                 new_testname = pattern.sub(new_testname, testname)
    #                 testname = new_testname
                
                
    #             print(LINE)
    #             print(testname)
    #             print(nway_ancova_result_reporting(dv, group_vars, covars)[self.language_set])
                
                
    #             for n in group_vars:
    #                 result_table = df.groupby(n)[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
    #                 print(f"{vars_for_showing} by {n}")
    #                 self.showing(result_table)
                    
    #             result_table = df.groupby(group_vars)[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
    #             print(f"{vars_for_showing} by Interaction")
    #             self.showing(result_table)

    #             formula_for_olsmodel = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'nway_ancova')
    #             olsmodel = testfunc(formula_for_olsmodel, data = df).fit()
                
    #             ancova_result_table = anova_lm(olsmodel, typ=3)
                
    #             #making pair-coef-table 
                
    #             # raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
                
    #             # pair_coef_table = raw_coef_table.loc[['Intercept']]
    #             # covar_coef_table = raw_coef_table.loc[covars]                
    #             # drop_col_for_coef_table = ['Intercept'] + covars
                
    #             # group_var_values = [range(len(df[value].unique())) for value in group_vars]
    #             # # reference_combinations = list(product(*group_var_values))
                
    #             # ols_models_for_coef_table = {}
                
    #             # for reference_combination in reference_combinations:
                    
    #             #     formula_for_coef = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'nway_ancova')
                    
    #             #     for i, j in enumerate(group_vars):
    #             #         formula_for_coef = formula_for_coef.replace(f"C({j})", f"C({j}, Treatment(reference={reference_combination[i]}))")

    #             #     olsmodel_by_combination = ols(formula_for_coef, data = df).fit()
    #             #     ols_models_for_coef_table[reference_combination] = olsmodel_by_combination
                    
    #             #     working_table_for_coef = pd.DataFrame(olsmodel_by_combination.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
    #             #     working_table_for_coef.drop(index = drop_col_for_coef_table, inplace=True)

    #             #     pair_list = working_table_for_coef.index.to_list()
    #             #     for i in range( len(pair_list)  ):
    #             #         for j in df.time.unique():
    #             #             if j in pair_list[i]:
    #             #                 pair_list[i] = j

    #             #     set_for_finding_ref_1 = set(df.time.unique())
    #             #     set_for_finding_ref_2 = set(pair_list)
    #             #     reference_col = list(set_for_finding_ref_1 - set_for_finding_ref_2)[0]                          

    #             #     for i in range( len(pair_list)  ):
    #             #         pair_list[i] = f"{reference_col} - {pair_list[i]}"                       

    #             #     working_table_for_coef.index = pair_list
    #             #     pair_coef_table = pd.concat([pair_coef_table, working_table_for_coef])

    #             # pair_coef_table['coef'] = pair_coef_table['coef'].astype('float')
    #             # pair_coef_table = pair_coef_table.loc[~pair_coef_table['coef'].abs().duplicated(keep='first')] #before merge, delete duplicated rows
                    
    #             # pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) #여기서 완성

    #             # self.showing(pair_coef_table)
                
    #             print(ancova_model_result_reporting[self.language_set])
    #             self.showing(olsmodel.summary().tables[0])
                
    #             print(ancova_statistic_result_reporting[self.language_set])
                
    #             if effectsize == True: #effectsize = True인 경우 eta-sqaured 계산 후 컬럼 추가. 
                    
    #                 ancova_result_table['eta_squared'] = ancova_result_table['sum_sq'] / ancova_result_table['sum_sq']['Residual']
    #                 print(notation_message_for_calculating_eta_squared[self.language_set])

    #             self.showing(ancova_result_table.rename(columns = {'PR(>F)': 'p-value'}).round(4))
                
    #             print('Coef Result Table: ')
    #             print(ancova_coef_interpreting_message(covars)[self.language_set])
    #             self.showing(olsmodel.summary().tables[1])        
                
                
    #             if posthoc == True:
    #                 print('Post-Hoc: ')
    #                 print(warning_message_for_ancova_posthoc[self.language_set])
                    
    #                 for n in group_vars:
    #                     mc = MultiComparison(df[dv], df[n])                        
                        
    #                     if posthoc_method == 'bonf':
    #                         result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    #                         print(posthoc_message_for_main_effect(n)[self.language_set])
    #                         self.showing(result[0])
                        
    #                     elif posthoc_method == 'tukey':
    #                         result = mc.tukeyhsd()                
    #                         print(posthoc_message_for_main_effect(n)[self.language_set])
    #                         print(f"\n{result.summary()}\n")                        
                    
                    
    #                 for n in interaction_columns:
    #                     mc = MultiComparison(df[dv], df[n])
                        
    #                     if posthoc_method == 'bonf':
    #                         result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
    #                         print(posthoc_message_for_interaction[self.language_set])
    #                         self.showing(result[0])
                        
    #                     elif posthoc_method == 'tukey':
    #                         result = mc.tukeyhsd()                
    #                         print(posthoc_message_for_interaction[self.language_set])
    #                         self.showing(result.summary())