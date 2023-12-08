import pandas as pd
from .messages_for_reporting import *
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

# RULE :  args for 'vars' --> [dv, [covar]]

def oneway_ancova(df:pd.DataFrame, ):
    pass

def rm_ancova():
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