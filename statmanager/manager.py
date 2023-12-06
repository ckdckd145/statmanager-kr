import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import MultiComparison
from statsmodels.stats.anova import AnovaRM, anova_lm
from statsmodels import api
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import re as repattern

# from itertools import product

from .menu_for_howtouse import *
from .messages_for_reporting import *
from .making_figure import *
from .__init__ import __version__

LINE = "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||"

VERSION = __version__

LINK = LINK_DOC

class Stat_Manager:
    def __init__(self, dataframe: pd.DataFrame, id: str = None, language: str = 'kor'):
        self.df = dataframe
        self.filtered_df = None
        self.result = None
        self.selector = None
        
        
        if language == 'kor' or language == 'eng':
            self.language_set = language
            self.link = LINK[self.language_set]
        
        else:
            raise KeyError(keyerror_message_for_languageset)
        
        SUCCESS_MESSAGE = success_message_for_creating_object(ver = VERSION, doclink = self.link)
        
        if self.language_set == 'kor':
            
            self.menu_for_howtouse = menu_for_howtouse_kor
            self.selector_for_howtouse = selector_for_howtouse_kor
            self.figure_for_howtouse = figure_for_howtouse_kor

        elif self.language_set == 'eng':
            
            self.menu_for_howtouse = menu_for_howtouse_eng
            self.selector_for_howtouse = selector_for_howtouse_eng
            self.figure_for_howtouse = figure_for_howtouse_eng 
        
        try: # df ; index set 여부 확인
            
            if self.df.index.name == None:
                self.df.set_index(id, inplace=True)
            
            else:
                pass
        except:
            raise TypeError(typeerror_message_for_indexsetting)
        
        else:
            print(SUCCESS_MESSAGE[self.language_set])

        self.id_var = self.df.index.name

        self.menu = {
        'kstest' : {
            'name' : 'Kolmogorov-Smirnov Test',
            'type' : 'normality',
            'group' : 1,
            'testfunc' : stats.kstest,
            'division' : None,
        },
        
        'shapiro' : {
            'name' : 'Shapiro-Wilks Test',
            'type' : 'normality',
            'group' : 1,
            'testfunc' : stats.shapiro,
            'division' : None,
        },
        
        'levene' : {
            'name' : 'Levene Test',
            'type' : 'homoskedasticity',
            'group' : 2,
            'testfunc' : stats.levene,
            'division' : None,
        },
        
        'ttest_ind' : {
            'name' : 'Indenpendent Samples T-test',
            'type' : 'compare_btwgroup',
            'group' : 2,
            'testfunc' : stats.ttest_ind,
            'division' : 'parametric'
        },
        
        'ttest_rel' : {
            'name' : 'Dependent Samples T-test',
            'type' : 'compare_ingroup',
            'group' : 1,
            'testfunc' : stats.ttest_rel,
            'division' : 'parametric'
        },
        
        'mannwhitneyu' : {
            'name' : 'Mann-Whitney U Test',
            'type' : 'compare_btwgroup',
            'group' : 2,
            'testfunc' : stats.mannwhitneyu,
            'division' : 'non_parametric'
        },
        'brunner' :{
            'name' : 'Brunner-Munzel Test',
            'type' : 'compare_btwgroup',
            'group' : 2,
            'testfunc' : stats.brunnermunzel,
            'division' : 'non_parametric'
        },        
        
        'wilcoxon' : {
            'name' : 'Wilcoxon-Signed Ranksum Test',
            'type' : 'compare_ingroup',
            'group' : 1,
            'testfunc' : stats.wilcoxon,
            'division' : 'non_parametric'        
        },
        
        'f_oneway' : {
            'name' : 'One-way ANOVA',
            'type' : 'compare_btwgroup',
            'group' : 3,
            'testfunc' : stats.f_oneway,
            'division' : 'parametric'
            
        },
        
        'kruskal' : {
            'name' : 'Kruskal-Wallis Test',
            'type' : 'compare_btwgroup',
            'group' : 3,
            'testfunc' : stats.kruskal,
            'division' : 'non_parametric'
            
        },
        
        'chi2_contingency' : {
            'name' : 'Chi-Squared Test',
            'type' : 'frequency_analysis',
            'group': 1,
            'testfunc' : stats.chi2_contingency,
            'division' : None
            },
        
        'fisher' : {
            'name' : "Fisher's Exact Test",
            'type' : 'frequency_analysis',
            'group' : 1,
            'testfunc' : stats.fisher_exact,
            'division' : None
        },
        
        'z_normal' : {
            'name' : 'z-skeweness & z-kurtosis test',
            'type' : 'normality_etc',
            'group' : 1,
            'testfunc' : self.zscore_normality,
            'division' : None
            },
        
        'fmax' : {
            'name' : 'F-max Test',
            'type' : 'homoskedasticity_etc',
            'group' : 2,
            'testfunc' : self.fmax_test,
            'division' : None,
            },
        
        'pearsonr' : {
            'name' : "Correlation analysis: Pearson's r",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        },
        
        'spearmanr' : {
            'name' : "Correlation analysis: Spearman's rho",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        },
        'kendallt' : {
            'name' : "Correlation analysis: Kendall's tau",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,   
        },
        
        'friedman' : {
            'name' : 'Friedman Test',
            'type' : 'compare_ingroup',
            'group' : 1,
            'testfunc' : stats.friedmanchisquare,
            'division' : 'non_parametric'
        },
        
        'f_oneway_rm' : {
            'name' : 'One-way Repeated Measures ANOVA',
            'type' : 'compare_ingroup',
            'group' : 1,
            'testfunc' : AnovaRM,
            'division' : 'parametric'
        },
        'bootstrap' : {
            'name' : 'Bootstrap percentile method: Resampling No. =',
            'type' : 'compare_etc',
            'group' : 1,
            'testfunc' : self.percentile_method,
            'division' : None,
        },
        
        'bootstrap_df' : {
            'name' : 'Bootstrap dataframe returning: Resampling NO. = ',
            'type' : 'returning_df',
            'group' : 1,
            'testfunc' : self.bootstrap_to_dataframe,
            'division' : None,
        },
        
        'linearr' : {
            'name' : 'Linear Regression',
            'type' : 'regression',
            'group' : 1,
            'testfunc' : api.OLS,
            'division' : None,
        },
        
        'logisticr' : {
            'name' : 'Logistic Regression',
            'type' : 'regression',
            'group' : 1,
            'testfunc' : api.Logit,
            'division' : None
        },
        'f_nway' : {
            'name' : "-way ANOVA",
            'type' : 'compare_ways',
            'group' : 2,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'f_nway_rm' : {
            'name' : "-way Repeated Measures ANOVA",
            'type' : 'compare_ways',
            'group' : 2,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'oneway_ancova' : {
            'name' : 'One-way ANCOVA',
            'type' : 'compare_ancova',
            'group' : 2,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'rm_ancova' : {
            'name' : 'Repeated-Measures ANCOVA',
            'type' : 'compare_ancova',
            'group' : 1,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'nway_ancova': {
            'name' : '-way ANCOVA',
            'type' : 'compare_ancova',
            'group' : 2,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'cronbach' : {
            'name' : "Calculating Cronbach's Alpha",
            'type' : 'reliability',
            'group' : 1,
            'testfunc' : self.calculate_cronbach_alpha,
            'division' : None 
        },
        'pp_plot' : {
            'name' : "Making p-p plot",
            'type' : 'making_figure',
            'group' : 1,
            'testfunc' : pp_plot,
            'division' : None 
        },
        
        'qq_plot' : {
            'name' : 'Making q-q plot',
            'type' : 'making_figure',
            'group' : 1,
            'testfunc' : qq_plot,
            'division' : None 
        },
        
        'hist' : {
            'name' : 'Making histogram',
            'type' : 'making_figure',
            'group' : 1,
            'testfunc' : hist,
            'division' : None             
        },
    }
        
    def progress(self, method: str, vars: list, group_vars: str = None, group_names: list = None, effectsize: bool = False, posthoc: bool = False, posthoc_method: str = 'bonf', selector: dict = None):
        """
        Please check the documentation : https://cslee145.notion.site/statmanager-kr-Documentation-c9d0886f29ea461d9d0f44449a145f8a?pvs=4
        
        """
        
        method = method.lower()
        posthoc_method = posthoc_method.lower()
        results_for_save = [] # for __init__

        if 'bootstrap' in method and not '_df' in method: #if method is percentile method
            
            resampling_no = method.replace('bootstrap', "")
            
            try : 
                if resampling_no == "":
                    print(notation_for_bootstrap_when_zero[self.language_set])
                    resampling_no = 1000

                else:   
                    
                    resampling_no = int(resampling_no)
                    
                    if resampling_no <= 0:
                        raise KeyError(keyerror_message_for_bootstrap[self.language_set])
            
            except :
                raise KeyError(keyerror_message_for_bootstrap[self.language_set])
            
            method = 'bootstrap' # rearrange method for matching in the menu
            
        
        if 'bootstrap' in method and '_df' in method: # if method is returning boostrapped df
            
            resampling_no = method.replace('bootstrap', "")
            resampling_no = resampling_no.replace('_df', "")
            
            try : 
                
                if resampling_no == "":
                    print(notation_for_bootstrap_when_zero[self.language_set])
                    resampling_no = 1000

                else:   
                    
                    resampling_no = int(resampling_no)
                    
                    if resampling_no <= 0:
                        raise KeyError(keyerror_message_for_bootstrap[self.language_set])
            
            except :
                raise KeyError(keyerror_message_for_bootstrap[self.language_set])

            method = 'bootstrap_df' # rearrange method for matching in the menu
            
        
        testtype = self.menu[method]['type']
        
        if selector == None:
            self.selector = None
            df = self.df
            self.filtered_df = None          
            conditions = None
            self.conditions_notification_texts = None
        else:
            
            if type(selector) != dict:
                raise TypeError(error_message_for_selector_type(doclink = self.link)[self.language_set])
            
            df = self.df
            self.selector = selector
            self.filtered_df = None 
            conditions  = []
            conditions_notification = []
            
            for key, value in selector.items():
                if isinstance(value, dict):  
                    for op, op_value in value.items():
                        if op == '<=':
                            conditions.append(df[key] <= op_value)
                            conditions_notification.append(f"{key} <= {op_value}")
                        elif op == '>=':
                            conditions.append(df[key] >= op_value)
                            conditions_notification.append(f"{key} >= {op_value}")
                        elif op == '<':
                            conditions.append(df[key] < op_value)
                            conditions_notification.append(f"{key} < {op_value}")
                        elif op == '>':
                            conditions.append(df[key] > op_value)
                            conditions_notification.append(f"{key} > {op_value}")
                        elif op == '=' or op == '==':
                            conditions.append(df[key] == op_value)
                            conditions_notification.append(f"{key} == {op_value}")
                        elif op == '!=':
                            conditions.append(df[key] != op_value)
                            conditions_notification.append(f"{key} != {op_value}")

                else: 
                    conditions.append(df[key] == value)
                    conditions_notification.append(f"{key} == {value}")
            
            combined_condition = conditions[0]
            
            if len(conditions) == 1: #selector 하나만 붙인 경우에는 그냥 진행 
                pass
            
            else: # selector가 2개 이상인 경우 
                for cond in conditions[1:]:
                    combined_condition &= cond
                    
            df = df.loc[combined_condition]
            self.filtered_df = df
            conditions_notification_texts = "\n".join(conditions_notification)
            self.conditions_notification_texts = conditions_notification_texts
            
        if testtype == 'regression':
            df = df.dropna(axis=0, how = 'any', subset = vars[1])
        
        elif testtype == 'compare_ancova':
            
            if method == 'oneway_ancova' or method == 'nway_ancova':
                df = df.dropna(axis=0, how = 'any', subset = [vars[0]] + vars[1])
                
            elif method == 'rm_anocva':
                df = df.dropna(axis=0, how = 'any', subset = vars[-1] + vars[-1])
        
        else:
            df = df.dropna(axis=0, how = 'any', subset = vars)
        
        testfunc = self.menu[method]['testfunc']
        group_fill = self.menu[method]['group']
        
        testname = self.menu[method]['name']
        if selector != None:
            
            selector_notation = selector_notification(condition_texts= conditions_notification_texts, test = testname)
            testname = selector_notation[self.language_set]

        testdivision = self.menu[method]['division']
        
        n = len(df)
        
        # saving for results
        self.method = method
        self.vars = vars
        self.group_vars = group_vars
        
        
        
        if testtype == 'frequency_analysis':
            
            ser = pd.crosstab(df[vars[0]], df[vars[1]])
            number_of_rows = len(df[vars[0]].unique())
            number_of_columns = len(df[vars[1]].unique())
            number_of_cells = number_of_rows * number_of_columns
            
            try:
                result = testfunc(ser)
                s = result[0]
                p = result[1]
                s = round(s, 3)
                p = round(p, 3)
            
            except:
                
                raise KeyError(keyerror_message_for_fisherexact[self.language_set])
            
            try: 
                predicted_value = result[3]
                
                values = []
                for row in range(number_of_rows):
                    for columns in range(number_of_columns):
                        value = predicted_value[row][columns]
                        values.append(value)
                
                under_five_values = 0
                for n in values:
                    if n < 5:
                        under_five_values += 1
                        
                percentage_of_under_five_values =  under_five_values / number_of_cells
            except:
                pass
            
            
            print(LINE)
            print(f"{testname}")
            print(frequency_analysis_result_reporting_one(vars)[self.language_set])
            
            try:
                print(frequency_analysis_result_reporting_two(s, p)[self.language_set])
            
            except:
                pass
            
            
            self.showing(ser)
            
            try:
                print(f"{percentage_of_under_five_values_word[self.language_set]} = {round(percentage_of_under_five_values * 100, 2):.2f}%")
                
                if percentage_of_under_five_values >= 0.25:
                    
                    print(warning_message_for_frequency_analysis[self.language_set])
            
            except:
                
                pass
            
            print(LINE)
            
        if testtype == 'normality':
            
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars
            
            ser = df[dv]
            print(LINE)
            print(f"{testname}")
            
            if method == 'kstest':
                s, p = testfunc(ser, 'norm')
                
                if n < 30:
                    print(warning_message_for_normality[method][self.language_set])
                    results_for_save += [warning_message_for_normality[method][self.language_set]]
                    
            else: # method == 'shapiro'
                s, p = testfunc(ser)
                
                if n >= 30:
                    print(warning_message_for_normality[method][self.language_set])
                    results_for_save += [warning_message_for_normality[method][self.language_set]]
            
            
            s = round(s, 3)
            p = round(p, 3)
            
            
            print(normality_test_result_reporting(dv, n, s, p)[self.language_set])
            
            results_for_save += [normality_test_result_reporting(dv, n, s, p)[self.language_set]]
            
            if p <= .05 : 
                print(conclusion_for_normality_assumption[self.language_set]['under'])
                results_for_save += [conclusion_for_normality_assumption[self.language_set]['under']]
            
            else:
                print(conclusion_for_normality_assumption[self.language_set]['up'])
                results_for_save += [conclusion_for_normality_assumption[self.language_set]['up']]
            
            print(LINE)
            
            result_object = self.saving_for_result(result = results_for_save, testname = testname)
            return result_object
            
            # return StatmanagerResult(method = method, vars = vars, result = results_for_save, group_vars = group_vars, group_names = group_names, selector = conditions_notification_texts)
            
        if testtype == 'homoskedasticity':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            
            series = []
            for n in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[n], dv]
                series.append(ser)
            
            s, p = testfunc(*series)
            s = round(s, 3)
            p = round(p, 3)
            
            print(LINE)
            print(f"{testname}")
            print(homoskedasticity_test_result_reporting(group_vars, group_names, s, p)[self.language_set])
            
            if p <= .05 :
                print(conclusion_for_homoskedasticity_assumption[self.language_set]['under'])
            
            else:
                print(conclusion_for_homoskedasticity_assumption[self.language_set]['up'])
            
            print(LINE)
            
        if testtype == 'compare_ingroup':
            
            if method == 'friedman' or method == 'f_oneway_rm':
                series = []
                
                for n in range(len(vars)):
                    ser = df[vars[n]]
                    series.append(ser)

                dict_var = {}
                
                for n in range(len(vars)):
                    dict_var[vars[n]] = {
                        'n' : "{:.2f}".format(series[n].count()), 
                        'mean' : "{:.2f}".format(series[n].mean().round(2)),
                        'median' : "{:.2f}".format(series[n].median().round(2)),
                        'sd' : "{:.2f}".format(series[n].std().round(2)),                        
                    }
                dict_var = pd.DataFrame(dict_var)

                print(LINE)
                print(f"{testname}")
                print(friedman_and_f_oneway_rm_result_reporting(vars)[self.language_set])
                self.showing(dict_var)
                
                if method == 'friedman':
                    s, p = testfunc(*series)
                    s = round(s, 3)
                    p = round(p, 3)
                    print(friedman_result_reporting_two(s, p)[self.language_set])
                
                elif method == 'f_oneway_rm':
                    reset_df = df.reset_index().melt(id_vars= self.id_var, value_vars = vars)
                    result = AnovaRM(data = reset_df, depvar = 'value', subject = self.id_var, within = ['variable']).fit()
                    s = result.anova_table['F Value']
                    p = result.anova_table['Pr > F']
                    s = round(s, 3)
                    p = round(p, 3)

                    for f, s, p in zip(result.anova_table.index, s, p):
                        print(f"F = {s:.3f}, p = {p:.3f}")

                if posthoc == True:
                    posthoc_df = df.reset_index().melt(id_vars=self.id_var, value_vars=vars)
                    mc = MultiComparison(posthoc_df['value'], posthoc_df['variable'])
                    print(LINE)
                    print('Posthoc: ')
                    
                    if posthoc_method == 'bonf':
                        if testdivision == 'parametric':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                            self.showing(result[0])
                            print(LINE)
                        
                        else: 
                            result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                            self.showing(result[0])
                            print(LINE)
                        
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()
                        self.showing(result.summary())
                        print(LINE)
                        
                if effectsize == True:
                    eta, grade = self.calculate_etasquared(series)
                    print("Calculating effect size: \n")
                    print(f"Eta-Sqaured (η2) =  {eta:.2f}\nGrade : {grade}")
            
            else: # method == 'ttest_rel' or 'wilcoxon' or 
                series = []
                for n in range(len(vars)):
                    ser = df[vars[n]]
                    series.append(ser)
                
                dict_var = {}
                for n in range(len(vars)):
                    dict_var[vars[n]] = {
                        'mean' : series[n].mean().round(2),
                        'median' : series[n].median().round(2),
                        'sd' : series[n].std().round(2),                        
                    }
                
                dict_var = pd.DataFrame(dict_var)
                
                s, p = testfunc(*series)
                s = round(s, 3)
                p = round(p, 3)
                degree_of_freedom = len(df) - 1
                
                n = len(df)
                
                print(LINE)
                print(f"{testname}")
                print(ttest_rel_and_wilcoxon_result_reporting_one(vars, n)[self.language_set])
                self.showing(dict_var)
                print(ttest_rel_and_wilcoxon_result_reporting_two(s, degree_of_freedom, p)[self.language_set])
                
                if method == 'wilcoxon':
                    z = (s - n * (n + 1) / 4) / (n * (n + 1) * (2 * n + 1) / 24)**0.5
                    print(f"z-statistic = {z:.3f}\n")
                
                if effectsize == True:
                    cohen_d, grade = self.calculate_cohen(series)
                    print(f"Cohen's d = {cohen_d:.2f}\Grade : {grade}")
                
        if testtype == 'compare_ways' :
            
            if method == 'f_nway_rm':
                
                melted_df = df.reset_index().melt(id_vars = self.id_var, value_vars = vars, var_name = 'time').set_index(self.id_var)
                df = df.drop(columns = vars).merge(melted_df, how = 'outer', on = self.id_var)
                
                if type(group_vars) == str:
                    group_vars = [group_vars]
                
                elif type(group_vars) == list:
                    pass
                
                group_vars.append('time')
                dv = 'value'
                
                way_len = len(group_vars)
                new_testname = f'{way_len}-way Repeated Measures ANOVA'
                
                if self.selector == None:
                    testname = new_testname
                
                else:
                    pattern = repattern.compile('-way Repeated Measures ANOVA')
                    new_testname = pattern.sub(new_testname, testname)
                    testname = new_testname
                
                df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                print(LINE)
                print(f"{testname}\n")
                print(f_nway_rm_result_reporting_one(vars, group_vars)[self.language_set])
                
                for n in group_vars:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f_nway_result_reporting_two (dv, n)[self.language_set])
                    self.showing(result_table)

                result_table = df.groupby(group_vars)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)  
                print(f_nway_result_reporting_three (dv)[self.language_set])
                self.showing(result_table)
                    
                iv_str = self.custom_join(group_vars)
                method_str = f"{dv} ~ {iv_str}"
                
                model = testfunc(method_str, data = df).fit()
                table = api.stats.anova_lm(model)
                
                result = table
                result.rename(columns = {'PR(>F)': 'p-value'}, inplace=True)
                
                print(f_nway_result_reporting_four (testname)[self.language_set])
                
                if effectsize == True:
                    result['eta_squared'] = result['sum_sq'] / result['sum_sq']['Residual']
                    print(notation_message_for_calculating_eta_squared[self.language_set])
                
                result = result.round(3)
                self.showing(result)
                
                print(LINE)
                
            elif method == 'f_nway': 
                df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                
                
                way_len = len(group_vars)
                new_testname = f'{way_len}-way ANOVA'
                
                if self.selector == None:
                    testname = new_testname
                
                else:
                    pattern = repattern.compile('-way ANOVA')
                    new_testname = pattern.sub(new_testname, testname)
                    testname = new_testname
                
                print(LINE)
                print(f"{testname}\n")
                print(f_nway_result_reporting_one(dv, group_vars)[self.language_set])
                
                for n in group_vars:
                    result_table = df.groupby(n)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f_nway_result_reporting_two(dv, n)[self.language_set])
                    self.showing(result_table)
                
                print(f_nway_result_reporting_three (dv)[self.language_set])
                result_table = df.groupby(group_vars)[dv].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                self.showing(result_table)
                    
                iv_str = self.custom_join(group_vars)
                method_str = f"{dv} ~ {iv_str}"
                
                model = testfunc(method_str, data = df).fit()
                table = api.stats.anova_lm(model)
                
                result = table
                result.rename(columns = {'PR(>F)': 'p-value'}, inplace=True)
                
                
                print(f_nway_result_reporting_four(testname)[self.language_set])
                
                if effectsize == True:
                    result['eta_squared'] = result['sum_sq'] / result['sum_sq']['Residual']
                    print(notation_message_for_calculating_eta_squared[self.language_set])
                    
                result = result.round(3)
                self.showing(result)
                print(LINE)
                
            if posthoc == True:
                
                print("Post-Hoc:")
                for n in group_vars:
                    mc = MultiComparison(df[dv], df[n])
                    
                    if posthoc_method == 'bonf':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        print(posthoc_message_for_main_effect(n)[self.language_set])
                        self.showing(result[0])
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()                
                        print(posthoc_message_for_main_effect(n)[self.language_set])
                        self.showing(result.summary())
                
                
                for n in interaction_columns:
                    mc = MultiComparison(df[dv], df[n])

                    if posthoc_method == 'bonf':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        print(posthoc_message_for_interaction[self.language_set])
                        self.showing(result[0])
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()                
                        print(posthoc_message_for_interaction[self.language_set])
                        self.showing(result.summary())

        if testtype == 'compare_ancova':

            
            if method == 'oneway_ancova':
                
                dv = vars[0]
                covars = vars[1]
                iv = group_vars
                
                
                if group_names == None:
                    group_names = list(df[group_vars].unique())
                
                else: # if group_names provided
                    cond = df[group_vars].isin(group_names)
                    df = df.loc[cond]
                
                #ols 모델 생성
                formula_for_olsmodel = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'oneway_ancova')
                olsmodel = testfunc(formula_for_olsmodel, data = df).fit()
                
                # formula =  "dv ~ C(group_var) + covar..covar2.."
                
                
                #dv + covar to list
                vars_for_showing = [dv] + covars 
                

                #기술통계 테이블 생성
                dict_var = df.groupby(group_vars)[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(
                    columns = {
                        'count' : 'n',
                        'std' : 'sd'
                    }).T.round(2)
                dict_var.columns.name = None
                
                #ANCOVA 결과테이블 생성
                ancova_result_table = anova_lm(olsmodel, typ=3)
                
                
                #Pair-coef table 만들기
                raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
                
                
                pair_coef_table = raw_coef_table.loc[['Intercept']]
                covar_coef_table = raw_coef_table.loc[covars]
                drop_col_for_coef_table = ['Intercept'] + covars
                
                for n in range(len(group_names)):
                    
                    formula_for_coef = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'oneway_ancova', purpose = 'coef', keys = n)
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
                    # working_table_for_coef['coef'] = working_table_for_coef['coef'].astype('float')
                    # working_table_for_coef = working_table_for_coef.loc[~working_table_for_coef['coef'].abs().duplicated(keep='first')]                    
                    
                    pair_coef_table = pd.concat([pair_coef_table, working_table_for_coef])
                    
                pair_coef_table['coef'] = pair_coef_table['coef'].astype('float')
                pair_coef_table = pair_coef_table.loc[~pair_coef_table['coef'].abs().duplicated(keep='first')] #before merge, delete duplicated rows
                pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) # concat with covar_coef_table 
                
                
                #reporting result

                
                print(LINE)
                print(testname)
                print(oneway_ancova_result_reporting(dv, group_vars, group_names, covars)[self.language_set])
                self.showing(dict_var)
                
                print(ancova_model_result_reporting[self.language_set])
                self.showing(olsmodel.summary().tables[0])
                
                print(ancova_statistic_result_reporting[self.language_set])
                
                if effectsize == True: #effectsize = True인 경우 eta-sqaured 계산 후 컬럼 추가. 
                    
                    ancova_result_table['eta_squared'] = ancova_result_table['sum_sq'] / ancova_result_table['sum_sq']['Residual']
                    print(notation_message_for_calculating_eta_squared[self.language_set])
                
                
                self.showing(ancova_result_table.rename(columns = {'PR(>F)': 'p-value'}).round(4))

                
                print(ancova_coef_result_reporting[self.language_set])
                print(ancova_coef_interpreting_message(covars)[self.language_set])
                self.showing(pair_coef_table)
            
                print(LINE)
            
                if posthoc == True:
                    print("Post-Hoc: ")
                    print(warning_message_for_ancova_posthoc[self.language_set])
                    
                    mc = MultiComparison(df[dv], df[group_vars])
                    
                    if posthoc_method == 'bonf':
                        if testdivision == 'parametric':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        
                        else: 
                            result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                        self.showing(result[0])
                        print(LINE)
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()
                        self.showing(result.summary())
                        print(LINE)
                
            elif method == 'rm_ancova':
                # group_vars = None
                # vars = [dv1, dv2, dv3, dv4, [covar1, covar2]]
                
                repeated_vars = vars[:-1]
                covars = vars[-1]
                vars_for_melting = [self.id_var] + covars
                
                melted_df = df.reset_index().melt(id_vars = self.id_var, value_vars = repeated_vars, var_name = 'time')
                melted_df = melted_df.merge(df.reset_index()[vars_for_melting], on = self.id_var, how = 'left').set_index(self.id_var)

                #ols 모델 생성
                formula_for_olsmodel = self.custom_join_for_ancova(vars = vars, method = 'rm_ancova')
                olsmodel = testfunc(formula_for_olsmodel, data = melted_df).fit()
                
                predicted_dv = olsmodel.predict(melted_df)
                melted_df['predicted_value'] = predicted_dv

                #dv + covar  list
                vars_for_showing = ['value'] + covars 
                
                #기술통계 테이블 생성
                
                dict_var = melted_df.groupby('time')[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(
                    columns = {
                        'count' : 'n',
                        'std' : 'sd'
                    }).T.round(2)
                dict_var.columns.name = None
                
                
                #ANCOVA 결과테이블 생성
                ancova_result_table = anova_lm(olsmodel, typ=3)
                
                
                #Pair-coef table 만들기
                raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')

                pair_coef_table = raw_coef_table.loc[['Intercept']]
                covar_coef_table = raw_coef_table.loc[covars]
                drop_col_for_coef_table = ['Intercept'] + covars
                
                for n in range( len (melted_df.time.unique() ) ):
                    formula_for_coef = self.custom_join_for_ancova(vars = vars, method = 'rm_ancova', purpose = 'coef', keys = n)
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
                    
                pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) #여기서 완성
                
                #결과 리포트
                print(LINE)
                print(testname)
                print(rm_ancova_result_reporting(repeated_vars, covars)[self.language_set])
                self.showing(dict_var)

                print(ancova_model_result_reporting[self.language_set])
                self.showing(olsmodel.summary().tables[0])
                

                print(ancova_statistic_result_reporting[self.language_set])
                
                if effectsize == True: #effectsize = True인 경우 eta-sqaured 계산 후 컬럼 추가. 
                    
                    ancova_result_table['eta_squared'] = ancova_result_table['sum_sq'] / ancova_result_table['sum_sq']['Residual']
                    print(notation_message_for_calculating_eta_squared[self.language_set])

                self.showing(ancova_result_table.rename(columns = {'PR(>F)': 'p-value'}).round(4))                
                
                
                print(ancova_coef_result_reporting[self.language_set])
                print(ancova_coef_interpreting_message(covars)[self.language_set])
                self.showing(pair_coef_table)
                
 
                if posthoc == True:
                    print('Post-Hoc: ')
                    print(warning_message_for_ancova_posthoc[self.language_set])
                    
                    mc = MultiComparison(melted_df['value'], melted_df['time'])
                    
                    if posthoc_method == 'bonf':
                        if testdivision == 'parametric':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                        
                        else: 
                            result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                        self.showing(result[0])
                        print(LINE)
                    
                    elif posthoc_method == 'tukey':
                        result = mc.tukeyhsd()
                        self.showing(result.summary())
                        print(LINE)
                
                
            elif method == 'nway_ancova':
                
                df, interaction_columns = self.create_interaction_columns(df, group_vars)
                
                
                dv = vars[0]
                covars = vars[1]
                iv = group_vars # type = list
                
                vars_for_showing = [dv] + covars 
                
                way_len = len(group_vars)
                new_testname = f'{way_len}-way ANCOVA'
                
                if self.selector == None:
                    testname = new_testname
                
                else:
                    pattern = repattern.compile('-way ANCOVA')
                    new_testname = pattern.sub(new_testname, testname)
                    testname = new_testname
                
                
                print(LINE)
                print(testname)
                print(nway_ancova_result_reporting(dv, group_vars, covars)[self.language_set])
                
                
                for n in group_vars:
                    result_table = df.groupby(n)[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                    print(f"{vars_for_showing} by {n}")
                    self.showing(result_table)
                    
                result_table = df.groupby(group_vars)[vars_for_showing].agg(['count', 'mean', 'median', 'std']).rename(columns = {'count' : "n"}).round(2)
                print(f"{vars_for_showing} by Interaction")
                self.showing(result_table)

                formula_for_olsmodel = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'nway_ancova')
                olsmodel = testfunc(formula_for_olsmodel, data = df).fit()
                
                ancova_result_table = anova_lm(olsmodel, typ=3)
                
                #making pair-coef-table 
                
                # raw_coef_table = pd.DataFrame(olsmodel.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
                
                # pair_coef_table = raw_coef_table.loc[['Intercept']]
                # covar_coef_table = raw_coef_table.loc[covars]                
                # drop_col_for_coef_table = ['Intercept'] + covars
                
                # group_var_values = [range(len(df[value].unique())) for value in group_vars]
                # # reference_combinations = list(product(*group_var_values))
                
                # ols_models_for_coef_table = {}
                
                # for reference_combination in reference_combinations:
                    
                #     formula_for_coef = self.custom_join_for_ancova(vars = vars, group_vars = group_vars, method = 'nway_ancova')
                    
                #     for i, j in enumerate(group_vars):
                #         formula_for_coef = formula_for_coef.replace(f"C({j})", f"C({j}, Treatment(reference={reference_combination[i]}))")

                #     olsmodel_by_combination = ols(formula_for_coef, data = df).fit()
                #     ols_models_for_coef_table[reference_combination] = olsmodel_by_combination
                    
                #     working_table_for_coef = pd.DataFrame(olsmodel_by_combination.summary().tables[1].data, columns = ['index','coef', 'std err', 't', 'p', '0.025', '0.975'])[1:].set_index('index')
                #     working_table_for_coef.drop(index = drop_col_for_coef_table, inplace=True)

                #     pair_list = working_table_for_coef.index.to_list()
                #     for i in range( len(pair_list)  ):
                #         for j in df.time.unique():
                #             if j in pair_list[i]:
                #                 pair_list[i] = j

                #     set_for_finding_ref_1 = set(df.time.unique())
                #     set_for_finding_ref_2 = set(pair_list)
                #     reference_col = list(set_for_finding_ref_1 - set_for_finding_ref_2)[0]                          

                #     for i in range( len(pair_list)  ):
                #         pair_list[i] = f"{reference_col} - {pair_list[i]}"                       

                #     working_table_for_coef.index = pair_list
                #     pair_coef_table = pd.concat([pair_coef_table, working_table_for_coef])

                # pair_coef_table['coef'] = pair_coef_table['coef'].astype('float')
                # pair_coef_table = pair_coef_table.loc[~pair_coef_table['coef'].abs().duplicated(keep='first')] #before merge, delete duplicated rows
                    
                # pair_coef_table = pd.concat([pair_coef_table, covar_coef_table]) #여기서 완성

                # self.showing(pair_coef_table)
                
                print(ancova_model_result_reporting[self.language_set])
                self.showing(olsmodel.summary().tables[0])
                
                print(ancova_statistic_result_reporting[self.language_set])
                
                if effectsize == True: #effectsize = True인 경우 eta-sqaured 계산 후 컬럼 추가. 
                    
                    ancova_result_table['eta_squared'] = ancova_result_table['sum_sq'] / ancova_result_table['sum_sq']['Residual']
                    print(notation_message_for_calculating_eta_squared[self.language_set])

                self.showing(ancova_result_table.rename(columns = {'PR(>F)': 'p-value'}).round(4))
                
                print('Coef Result Table: ')
                print(ancova_coef_interpreting_message(covars)[self.language_set])
                self.showing(olsmodel.summary().tables[1])        
                
                
                if posthoc == True:
                    print('Post-Hoc: ')
                    print(warning_message_for_ancova_posthoc[self.language_set])
                    
                    for n in group_vars:
                        mc = MultiComparison(df[dv], df[n])                        
                        
                        if posthoc_method == 'bonf':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                            print(posthoc_message_for_main_effect(n)[self.language_set])
                            self.showing(result[0])
                        
                        elif posthoc_method == 'tukey':
                            result = mc.tukeyhsd()                
                            print(posthoc_message_for_main_effect(n)[self.language_set])
                            print(f"\n{result.summary()}\n")                        
                    
                    
                    for n in interaction_columns:
                        mc = MultiComparison(df[dv], df[n])
                        
                        if posthoc_method == 'bonf':
                            result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                            print(posthoc_message_for_interaction[self.language_set])
                            self.showing(result[0])
                        
                        elif posthoc_method == 'tukey':
                            result = mc.tukeyhsd()                
                            print(posthoc_message_for_interaction[self.language_set])
                            self.showing(result.summary())
                
            elif method == 'nway_rm_ancova':
                pass # developing..
            
            else:
                pass
        
        if testtype == 'compare_btwgroup':
            
            if type(vars) == list:
                dv = vars[0]
                
            elif type(vars) == str:
                dv = vars
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            series = []
            for n in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[n], dv]
                series.append(ser)
            
            dict_var = {}
            for n in range(len(group_names)):
                dict_var[group_names[n]] = {
                    'n' : len(series[n]),
                    'mean' : series[n].mean().round(2),
                    'median' : series[n].median().round(2),
                    'sd' : series[n].std().round(2),
                    }
            
            dict_var = pd.DataFrame(dict_var)
            
            s, p = testfunc(*series)
            s = round(s, 3)
            p = round(p, 3)
            
            print(LINE)
            print(f"{testname}")
            print(compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[self.language_set])
            self.showing(dict_var)
            print(compare_btwgroup_result_reporting_two(s, p)[self.language_set])
            
            if method != 'kruskal' and method != 'f_oneway': #ttest 혹은 mannwhitney, brunner
                degree_of_freedom = 0
                for n in range(len(group_names)):
                    value = series[n].count()
                    degree_of_freedom += value
                
                degree_of_freedom = degree_of_freedom - 2
                print(f"Degree of freedom = {degree_of_freedom}")
                
                if method == 'mannwhitneyu':
                    n1 = len(series[0])
                    n2 = len(series[1])
                    z = (s - n1 * n2 / 2) / ((n1 * n2 * (n1 + n2 + 1)) / 12)**0.5
                    print(f"z-statistic = {z:.3f}\n")
                    
                elif method == 'brunner':
                    n1 = len(series[0])
                    n2 = len(series[1])
                    z = s / ((n1 * n2)**0.5)
                    print(f"z-statistic = {z:.3f}\n")
            
            
            else:
                degree_of_freedom_between_group = len(group_names) - 1
                degree_of_freedom = 0
                for n in range(len(group_names)):
                    value = series[n].count()
                    degree_of_freedom += value
                
                degree_of_freedom = degree_of_freedom - len(group_names)
                print(f_oneway_df_reporting(degree_of_freedom_between_group, degree_of_freedom)[self.language_set])

            print(LINE)
            
            if posthoc == True:
                
                cond_list = []
                for n in range(len(group_names)):
                    cond = df[group_vars] == group_names[n]
                    cond_list.append(cond)
                
                
                selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
                selected_df = df[selected_rows]
                
                mc = MultiComparison(selected_df[dv], selected_df[group_vars])
                
                if posthoc_method == 'bonf':
                
                    if testdivision == 'parametric':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                    
                    else: 
                        result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                    print('Post-hoc:')
                    self.showing(result[0])
                    print(LINE)
                
                elif posthoc_method == 'tukey':
                    print('Post-hoc:\n')
                    result = mc.tukeyhsd()
                    self.showing(result.summary())
                    print(LINE)
        
            if effectsize == True:
                print("Effect size is calculated : \n")
                
                if method != 'kruskal' and method != 'f_oneway': #ttest 혹은 뭐시기일때
                    
                    cohen_d, grade = self.calculate_cohen(series)
                    print(f"Cohen's d = {cohen_d:.2f}\nGrade : {grade}")
                    
                else:
                    eta, grade = self.calculate_etasquared(series)
                    print(f"Eta-Sqaured (η2) =  {eta:.2f}\nGrade : {grade}")
            
        if testtype == 'compare_etc':
            
            
            if group_vars == None: #percentile method within group
                print(LINE)
                print(f"{testname} {resampling_no} \n")
                
                ser1 = self.bootstrap(series = df[vars[0]], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series = df[vars[1]], n_bootstrap=resampling_no)
                bootstrap_df = self.bootstrap_to_dataframe(ser1, ser2, label = vars)
                testfunc(data = bootstrap_df, a_var = vars[0], b_var = vars[1])
                
            else: #percentile method between group
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                
                if group_names == None:
                    group_names = list(df[group_vars].unique())
                
                else:
                    pass
                
                if len(group_names) > 2:
                    raise ValueError(valueerror_message_for_bootstrap[self.language_set])
                
                
                print(LINE)
                print(f"{testname} {resampling_no} \n")
                
                ser1 = self.bootstrap(series= df.loc[df[group_vars] == group_names[0], dv], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series= df.loc[df[group_vars] == group_names[1], dv], n_bootstrap=resampling_no)
                a_var = f"{group_names[0]}_{dv}"
                b_var = f"{group_names[1]}_{dv}"
                bootstrap_df = self.bootstrap_to_dataframe(ser1, ser2, label = [a_var, b_var])
                testfunc(data = bootstrap_df, a_var = a_var, b_var = b_var)
        
        if testtype == 'returning_df':
            
            
            print(LINE)
            print(f"{testname} {resampling_no} \n")
                
            if group_vars == None:
                
                ser1 = self.bootstrap(series = df[vars[0]], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series = df[vars[1]], n_bootstrap=resampling_no)
                bootstrap_df = testfunc(ser1, ser2, label = vars)
            
            else: 
                if type(vars) == list:
                    dv = vars[0]
                elif type(vars) == str:
                    dv = vars
                    
                if group_names == None:
                    group_names = list(df[group_vars].unique())
                
                else:
                    pass
                
                if len(group_names) > 2:
                    raise ValueError(valueerror_message_for_bootstrap[self.language_set])          
                
                ser1 = self.bootstrap(series= df.loc[df[group_vars] == group_names[0], dv], n_bootstrap=resampling_no)
                ser2 = self.bootstrap(series= df.loc[df[group_vars] == group_names[1], dv], n_bootstrap=resampling_no)
                a_var = f"{group_names[0]}_{dv}"
                b_var = f"{group_names[1]}_{dv}"
                bootstrap_df = testfunc(ser1, ser2, label = [a_var, b_var])
                
            
            print(notation_message_for_returning_bootstrap_df[self.language_set])
            
            return bootstrap_df
        
        if testtype == 'normality_etc':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars            
            
            
            print(LINE)
            print(f"{testname}")
            testfunc(df[dv], dv)
            
        if testtype == 'homoskedasticity_etc':
            if type(vars) == list:
                dv = vars[0]
            elif type(vars) == str:
                dv = vars  
            
            if group_names == None:
                group_names = list(df[group_vars].unique())
            
            print(LINE)
            print(f"{testname}")
            print(f"Variables: {dv}")
            testfunc(vars = dv, group_vars = group_vars, group_names = group_names)
            
        if testtype == 'correlation':
            print(LINE)
            print(f"{testname}\n")
            testfunc(method = method, vars = vars)
            print(LINE)
    
        if testtype == 'regression':
            dv = vars[0]
            iv = vars[1]
            print(LINE)
            print(f"{testname}")
            
            if method == 'logisticr':
                
                dv_list = df[dv].astype('category').cat.categories.to_list()
                dv_len = len(dv_list)
                
                mapper = {}
                for number in range(dv_len):
                    mapper[dv_list[number]] = number
                
                dummy_label = f'dummy_{dv}'
                df[dummy_label] = df[dv].map(mapper)
                y = df[dummy_label]
                
                if dv_len >= 3:
                    testfunc = api.MNLogit
                    
                    print(notation_meesage_for_multinominal[self.language_set])
                
                print(logistic_regression_result_reporting_one(dv, mapper)[self.language_set])
            
            else: # method == 'linearr'
                y = df[dv]
                print(linear_regression_result_reporting_one (dv)[self.language_set])
            
            print(regression_result_reporting_ivs (iv)[self.language_set])

            x = df[iv]
            
            x = api.add_constant(x)
            model = testfunc(y, x).fit()
            
            self.showing(model.summary())
            self.showing(model.summary2())
            
            odd_ratio = np.exp(model.params)
            print('odds ratio (OR): \n')
            self.showing(odd_ratio)          
            print(LINE)

        if testtype == 'reliability':
            
            
            test_items = vars
            cronbach = testfunc(test_items)
            n = len(df)
            
            print(testname)
            print(notation_message_for_cronbach_alpha[self.language_set])
            print(cronbach_alpha_result_reporting(n, test_items, cronbach)[self.language_set])
            
            if cronbach < 0:
                print(warning_message_for_negative_cronbach_alpha[self.language_set])
            else:
                pass
    
        if testtype == 'making_figure':
            
            if method == 'pp_plot' or method == 'qq_plot':
                
                figure_object = testfunc(series = df[vars], language_set = self.language_set)
                
                return figure_object
            
            if method == 'hist':
                
                figure_object = testfunc(df = df, var = vars, n = n, language_set = self.language_set)
                
                return figure_object

            
    def zscore_normality(self, series, dv):
        
        n = series.count()
        
        skewness = series.skew().round(3)
        skewness_se = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3))).round(3)
        
        kurtosis = series.kurtosis().round(3)
        kurtosis_se = (np.sqrt((n**2 - 1) / ((n-3)*(n+5))) * skewness_se * 2).round(3)
        
        z_skewness = (skewness/skewness_se).round(3)
        z_kurtosis = (kurtosis/kurtosis_se).round(3)
        
        if n < 50:
            cutoff = 1.96
        elif n < 200:
            cutoff = 2.59
        elif n > 200:
            cutoff = 3.13
        
        print(z_normal_result_reporting(dv, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, n, cutoff)[self.language_set])
        
        z_skewness = abs(z_skewness)
        z_kurtosis = abs(z_kurtosis)
        
        if z_skewness < cutoff and z_kurtosis < cutoff: #up
 
            print(conclusion_for_normality_assumption[self.language_set]['up'])
        
        else: #under
            
            print(conclusion_for_normality_assumption[self.language_set]['under'])
            
            
        print(reference_of_z_normal)
        print(LINE)

    def fmax_test(self, vars, group_vars, group_names):
        if self.selector == None:
            df = self.df
        
        else:
            df = self.filtered_df
        
        df = df.loc[df[group_vars].isin(group_names)]
        group_n = len(group_names)
        
        max_variance = df.groupby(group_vars)[vars].var().max().round(3)
        min_variance = df.groupby(group_vars)[vars].var().min().round(3)
        
        f_max = max_variance / min_variance
        f_max = round(f_max, 3)
        
        print(fmax_result_reporting(group_n, group_names, max_variance, min_variance, f_max)[self.language_set])

        
        if f_max < 10: #up
            print(conclusion_for_homoskedasticity_assumption[self.language_set]['up'])
            
        else: #under
            print(conclusion_for_homoskedasticity_assumption[self.language_set]['under'])
            
        print(reference_of_fmax)
        print(LINE)
        
    def r_forargs(self, method, vars):
        
        if self.selector == None:
            df = self.df
        
        else:
            df = self.filtered_df
            
        
        df = df.dropna(axis=0, how = 'any', subset = vars)
        number_of_rows = len(df)
        
        statistic_valuedict = {
            'pearsonr' : "Pearson's r",
            'spearmanr' : "Spearman's rho",
            'kendallt' : "Kendall's tau"
        }
        
        if method == 'pearsonr':
            tf = stats.pearsonr
        
        elif method == 'spearmanr':
            tf = stats.spearmanr
            
        elif method == 'kendallt':
            tf = stats.kendalltau
        
        correlation_table = df[vars].corr().round(3)
        
        num = len(vars)
        sets = []
        
        statistic_value = statistic_valuedict[method]
        
        print(f'n = {number_of_rows}\n{notation_message_for_correlation[self.language_set]}')
        summary_correlation_table = pd.DataFrame()
        
        for i in range(num -1):
            for j in range(i +1, num):
                sets.append((df[vars[i]], df[vars[j]]))
            
        for n in sets:
            s, p = tf(n[0], n[1])
            s = round(s, 3)
            p = round(p, 3)
            var1 = n[0].name
            var2 = n[1].name
            
            if p <= .05:
                significant_r = '*'
                s_with_significancy = f'{s:.3f}{significant_r}'
            else:
                significant_r = ''
                s_with_significancy = s
            
            
            
            summary_correlation_table.loc[f"{var1} & {var2}", statistic_value] = s_with_significancy
            summary_correlation_table.loc[f"{var1} & {var2}", 'p-value'] = f"{p:.3f}"
            
            print(f"{var1} & {var2}  :  {statistic_value} = {s:.3f}, p = {p:.3f}{significant_r}")
            
            correlation_table.loc[var1, var2] = s_with_significancy
            correlation_table.loc[var2, var1] = s_with_significancy
        
        self.showing(correlation_table)
        self.showing(summary_correlation_table)
        print("* p < .05")
            
    def bootstrap(self, series, n_bootstrap=1000, statistic=np.mean):
        
        n = len(series)
        bootstrap_results = []
        for _ in range(n_bootstrap):
            bootstrap_sample = series.sample(n, replace=True)  # 재표집
            statistic_value = statistic(bootstrap_sample)
            bootstrap_results.append(statistic_value)
        
        return bootstrap_results
    
    def bootstrap_to_dataframe(self, *args, label):
        n = len(args)
        dict_var = {}
        for _ in range(n):
            key = f"{_}"
            value = args[_]
            dict_var[key] = value
        result = pd.DataFrame(dict_var)
        
        if label != None and type(label) == list:
            t = len(label)
            for n in range(t):
                result.rename(columns = {f'{n}' : label[n]}, inplace=True)
                
        return result

    def percentile_method(self, data, a_var, b_var, confidence_level = 0.95, hist=True):
        
        confidence_dict = {
            0.90 : [5, 95],
            0.95 : [2.5, 97.5],
            0.99 : [0.5, 99.5],
        }
    
        interval = confidence_dict[confidence_level]
        
        n = len(data)
        
        a_confidence_interval = np.percentile(data[a_var], interval)
        b_confidence_interval = np.percentile(data[b_var], interval)
        a_lower_bound = a_confidence_interval[0]
        a_upper_bound = a_confidence_interval[1]
        b_lower_bound = b_confidence_interval[0]
        b_upper_bound = b_confidence_interval[1]
        
        
        print(percentile_method_result_reporting(a_var, confidence_level, a_lower_bound, a_upper_bound, b_var, b_lower_bound, b_upper_bound)[self.language_set])
        
        
        if a_upper_bound < b_lower_bound or a_lower_bound > b_upper_bound:
            print(conclusion_for_percentile_method[self.language_set]['under'])
        
        else:
            print(conclusion_for_percentile_method[self.language_set]['up'])
        
        print("\nReference:\nEfron, B., & Tibshirani, R. (1986). Bootstrap methods for standard errors, confidence intervals, and other measures of statistical accuracy. Statistical Science, 1(1), 54-75.\n")
        print("Histogram: \n")
        
        
        if hist == True:
            plt.figure(figsize=(10, 8))
            if self.language_set == 'kor':            
                sns.set(font = "Gulim", font_scale = 1.5)
            else:
                sns.set(font = 'Times New Roman', font_scale = 1.5)
            plt.style.use('grayscale')
            plt.title(f'Histogram of {a_var} & {b_var}')
            sns.histplot(data = data[a_var], label = a_var, alpha=0.5, kde=True)
            sns.histplot(data = data[b_var], label = b_var, alpha=0.5, kde=True)
            
            plt.axvline(a_lower_bound, color='black', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({a_var})')
            plt.axvline(a_upper_bound, color='black', linestyle='--')
            plt.axvline(b_lower_bound, color='gray', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({b_var})')
            plt.axvline(b_upper_bound, color='gray', linestyle='--')
                    
            plt.xlabel(f"Value of {a_var} & {b_var}")
            plt.ylabel("No. of Samples")
            plt.legend(bbox_to_anchor=(1, 1))
            plt.grid(False)
            plt.show()
    
    def custom_join(self, vars):
        result = []
    
        for i in range(len(vars)):
            for j in range(i + 1, len(vars)):
                pair = f"{vars[i]}:{vars[j]}"
                result.append(pair)
        
        return ' + '.join(vars + result)

    def custom_join_for_ancova(self, vars = None, group_vars = None, method = None, purpose = 'normal', keys = None):
        
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

    def create_interaction_columns(self, df, elements):
        interactions = []
        new_df = df.copy()  # 원본 DataFrame 복사
        
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                element1 = elements[i]
                element2 = elements[j]
                
                interaction_name = f"interaction_{element1}_{element2}"
                interaction_values = df[element1] + "_" + df[element2]
                
                new_df[interaction_name] = interaction_values
                interactions.append(interaction_name)
        
        return new_df, interactions

    def calculate_cohen(self, series):
        groupa_n = series[0].count()
        groupb_n = series[1].count()
        
        groupa_mean = series[0].mean()
        groupb_mean = series[1].mean()
        
        groupa_std = series[0].std()
        groupb_std = series[1].std()                    
        
        son = groupa_mean - groupb_mean
        
        stage_1 = ((groupa_n - 1) * (groupa_std ** 2)) + ((groupb_n - 1) * (groupb_std ** 2))
        stage_2 = groupa_n + groupb_n - 2
        
        pooled_std = np.sqrt(stage_1/stage_2)
        
        cohen_d = (son / pooled_std)
        
        if cohen_d < 0.2:
            grade = '해석 불가'
        elif cohen_d < 0.5:
            grade = '작은 효과크기'
        elif cohen_d < 0.8:
            grade = '중간 효과크기'
        elif cohen_d >= 0.8:
            grade = '큰 효과크기'
        
        return cohen_d, grade

    def calculate_etasquared(self, series):
        k = len(series)

        group_means = [ser.mean() for ser in series]

        overall_mean = np.mean(group_means)

        ss_between = sum([(group_mean - overall_mean) ** 2 * len(ser) for group_mean, ser in zip(group_means, series)])
        all_data = pd.concat(series)
        ss_total = sum((all_data - overall_mean) ** 2)

        # Eta-squared (\(\eta^2\))
        eta_squared = ss_between / ss_total

        if eta_squared < 0.06:
            grade = '작은 효과크기'
        elif eta_squared < 0.14:
            grade = '중간 효과크기'
        elif eta_squared >= 0.14:
            grade = '큰 효과크기'

        return eta_squared, grade
    
    def showing(self, result):
        try:
            display(result)
        except:
            print(result)
    
    def howtouse(self, keyword: str = None):
        
        print(self.link)
        
        search_base = {
            'menu_for_howtouse' : self.menu_for_howtouse,
            'figure_for_howtouse' : self.figure_for_howtouse,
        }
        
        if self.language_set == 'kor':
            
            search_logic = {
                'menu_for_howtouse' : {
                    'index_for_howtouse' : '분석명',
                    'search_column_1' : '목적',
                    'search_column_2' : 'method'
                    },
                'figure_for_howtouse' : {
                    'index_for_howtouse' : '구분',
                    'search_column_1' : 'method',
                    'search_column_2' : 'vars',
                }
            }
            
        elif self.language_set == 'eng':
            
            search_logic = {
                'menu_for_howtouse' : {
                    'index_for_howtouse' : 'Analysis',
                    'search_column_1' : 'Purpose',
                    'search_column_2' : 'method'
                    },
                'figure_for_howtouse' : {
                    'index_for_howtouse' : 'Index',
                    'search_column_1' : 'method',
                    'search_column_2' : 'vars',
                }
            }
            
        if keyword != None:
            
            if keyword == 'selector':
                self.showing(self.selector_for_howtouse)

                return self
            
            elif keyword == 'figure':
                self.showing(self.figure_for_howtouse.set_index(search_logic['figure_for_howtouse']['index_for_howtouse']))

                return self
            
            else:    
                for key, value in search_logic.items():
                    target_menu = search_base[key]
                    
                    cond1 = target_menu[value['index_for_howtouse']].str.contains(keyword)
                    cond2 = target_menu[value['search_column_1']].str.contains(keyword)
                    cond3 = target_menu[value['search_column_2']].str.contains(keyword)
                    
                    self.showing(target_menu[cond1 | cond2 | cond3].set_index(value['index_for_howtouse']))
                
                return self
        
        else: # keyword == None. ( when user just run .howtouse() )
            
            print(NOTATION_FOR_HOWTOUSE[self.language_set])
            self.showing(self.menu_for_howtouse.set_index(index_for_howtouse))
            
            print(NOTATION_FOR_HOWTOUSE_SELECTOR[self.language_set])
            self.showing(self.selector_for_howtouse)
            
            return self
    
    def calculate_cronbach_alpha (self, vars):
        if self.selector == None:
            df = self.df
        
        else:
            df = self.filtered_df      
            
        target_columns = vars
        
        if not type(target_columns) == list:
            raise KeyError(keyerror_message_for_cronbach[self.language_set]) 
        
        k = len(target_columns)
        
        covariance_matrix = df[target_columns].cov()
        sum_of_variances = np.trace(covariance_matrix)
        total_variance = covariance_matrix.sum().sum()
        
        cronbach_alpha = (k / (k-1)) * (1 - sum_of_variances / total_variance )
        
        return cronbach_alpha
    
    def saving_for_result(self, result: list, testname: str):
        
        return StatmanagerResult(method = self.method, vars = self.vars, group_vars=self.group_vars, result = result, selector = self.selector, testname = testname)
    
    
    def set_language(self, lang: str ):
        
        lang = lang.lower()
        
        if lang == 'kor' or lang == 'eng':
            
            self.language_set = lang
            self.link = LINK[self.language_set]
            
            if lang == 'kor':
                self.menu_for_howtouse = menu_for_howtouse_kor
                self.selector_for_howtouse = selector_for_howtouse_kor
                self.figure_for_howtouse = figure_for_howtouse_kor
            
            else: # lang == 'eng'
                self.menu_for_howtouse = menu_for_howtouse_eng
                self.selector_for_howtouse = selector_for_howtouse_eng
                self.figure_for_howtouse = figure_for_howtouse_eng
            
            print(message_for_change_languageset[self.language_set])
            
            return self
        
        else:
            KeyError(keyerror_message_for_languageset)