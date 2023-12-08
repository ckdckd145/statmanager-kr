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

from .menu_for_howtouse import *
from .messages_for_reporting import *
from .making_figure import *

from .normality_functions import *
from .frequency_functions import *
from .homoskedasticity_functions import *
from .reliability_functions import *
from .bootstrap_functions import *
from .correlation_functions import *
from .regression_functions import *
from .within_group_functions import *
from .between_group_functions import *
from .ways_anova_functions import *
from .ancova_functions import *

from .posthoc_functions import *
from .effectsize_functions import *

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
            'testfunc' : kstest, #normality_fuctions
            'division' : None,
        },
        
        'shapiro' : {
            'name' : 'Shapiro-Wilks Test',
            'type' : 'normality',
            'group' : 1,
            'testfunc' : shapiro,
            'division' : None,
        },
        
        'levene' : {
            'name' : 'Levene Test',
            'type' : 'homoskedasticity',
            'group' : 2,
            'testfunc' : levene,
            'division' : None,
        },
        
        'ttest_ind' : {
            'name' : 'Indenpendent Samples T-test',
            'type' : 'between_group',
            'group' : 2,
            'testfunc' : ttest_ind,
            'division' : 'parametric'
        },
        
        'ttest_rel' : {
            'name' : 'Dependent Samples T-test',
            'type' : 'within_group',
            'group' : 1,
            'testfunc' : ttest_rel,
            'division' : 'parametric'
        },
        
        'mannwhitneyu' : {
            'name' : 'Mann-Whitney U Test (Wilcoxon Rank Sum Test)',
            'type' : 'between_group',
            'group' : 2,
            'testfunc' : mannwhitneyu,
            'division' : 'non_parametric'
        },
        'brunner' :{
            'name' : 'Brunner-Munzel Test',
            'type' : 'between_group',
            'group' : 2,
            'testfunc' : brunner,
            'division' : 'non_parametric'
        },        
        
        'wilcoxon' : {
            'name' : 'Wilcoxon-Signed Rank Test',
            'type' : 'within_group',
            'group' : 1,
            'testfunc' : wilcoxon,
            'division' : 'non_parametric'        
        },
        
        'f_oneway' : {
            'name' : 'One-way ANOVA',
            'type' : 'between_group',
            'group' : 3,
            'testfunc' : f_oneway,
            'division' : 'parametric'
            
        },
        
        'kruskal' : {
            'name' : 'Kruskal-Wallis Test',
            'type' : 'between_group',
            'group' : 3,
            'testfunc' : kruskal,
            'division' : 'non_parametric'
            
        },
        
        'chi2_contingency' : {
            'name' : 'Chi-Squared Test',
            'type' : 'frequency_analysis',
            'group': 1,
            'testfunc' : chi2,
            'division' : None
            },
        
        'fisher' : {
            'name' : "Fisher's Exact Test",
            'type' : 'frequency_analysis',
            'group' : 1,
            'testfunc' : fisher,
            'division' : None
        },
        
        'z_normal' : {
            'name' : 'z-skeweness & z-kurtosis test',
            'type' : 'normality',
            'group' : 1,
            'testfunc' : z_normal,
            'division' : None
            },
        
        'fmax' : {
            'name' : 'F-max Test',
            'type' : 'homoskedasticity',
            'group' : 2,
            'testfunc' : fmax,
            'division' : None,
            },
        
        'pearsonr' : {
            'name' : "Correlation analysis: Pearson's r",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : pearson,
            'division' : None,
        },
        
        'spearmanr' : {
            'name' : "Correlation analysis: Spearman's rho",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : spearman,
            'division' : None,
        },
        'kendallt' : {
            'name' : "Correlation analysis: Kendall's tau",
            'type' : 'correlation',
            'group' : 1,
            'testfunc' : kendall,
            'division' : None,   
        },
        
        'friedman' : {
            'name' : 'Friedman Test',
            'type' : 'within_group',
            'group' : 1,
            'testfunc' : friedman,
            'division' : 'non_parametric'
        },
        
        'f_oneway_rm' : {
            'name' : 'One-way Repeated Measures ANOVA',
            'type' : 'within_group',
            'group' : 1,
            'testfunc' : rm_anova,
            'division' : 'parametric'
        },
        'bootstrap' : {
            'name' : 'Bootstrap percentile method: Resampling No. =',
            'type' : 'bootstrap',
            'group' : 1,
            'testfunc' : percentile_method,
            'division' : None,
        },
        'linearr' : {
            'name' : 'Linear Regression',
            'type' : 'regression',
            'group' : 1,
            'testfunc' : linear,
            'division' : None,
        },
        
        'logisticr' : {
            'name' : 'Logistic Regression',
            'type' : 'regression',
            'group' : 1,
            'testfunc' : logistic,
            'division' : None
        },
        'f_nway' : {
            'name' : "-way ANOVA",
            'type' : 'anova_nways',
            'group' : 2,
            'testfunc' : f_nway,
            'division' : 'parametric'
        },
        'f_nway_rm' : {
            'name' : "-way Mixed Repeated Measures ANOVA",
            'type' : 'anova_nways',
            'group' : 2,
            'testfunc' : f_nway_rm,
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
            'type' : 'anova_nways',
            'group' : 2,
            'testfunc' : ols,
            'division' : 'parametric'
        },
        'cronbach' : {
            'name' : "Calculating Cronbach's Alpha",
            'type' : 'reliability',
            'group' : 1,
            'testfunc' : cronbach,
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
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object            
            
        if testtype == 'normality':
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
        if testtype == 'homoskedasticity':
            result = testfunc(df = df, vars = vars, group_vars = group_vars, group_names = group_names, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
        
        if testtype == 'bootstrap':
            result, figure_object = testfunc(df = df, vars = vars, group_vars = group_vars, group_names = group_names, resampling_no = resampling_no, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object, figure_object
        
        if testtype == 'within_group':
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
            
        if testtype == 'anova_nways' :
            result = testfunc(df = df, vars = vars, group_vars = group_vars, group_names = group_names, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method, selector = self.selector)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object                       
            
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
        
        if testtype == 'between_group':
            result = testfunc(df = df, vars = vars, group_vars = group_vars, group_names = group_names, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object            
            
        if testtype == 'correlation':
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
    
        if testtype == 'regression':
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object 

        if testtype == 'reliability':
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
    
        if testtype == 'making_figure':
            
            if method == 'pp_plot' or method == 'qq_plot':
                
                figure_object = testfunc(series = df[vars], language_set = self.language_set)
                
                return figure_object
            
            if method == 'hist':
                
                figure_object = testfunc(df = df, var = vars, n = n, language_set = self.language_set)
                
                return figure_object

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
            self.showing(self.menu_for_howtouse.set_index(search_logic['menu_for_howtouse']['index_for_howtouse']))
            
            print(NOTATION_FOR_HOWTOUSE_SELECTOR[self.language_set])
            self.showing(self.selector_for_howtouse)
            
            return self
    
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
            raise KeyError(keyerror_message_for_languageset)