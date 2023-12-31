import pandas as pd

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

VERSION = __version__

LINK = LINK_DOC

class Stat_Manager:
    def __init__(self, dataframe: pd.DataFrame, id: str = None, language: str = 'kor'):
        self.df = dataframe
        self.df_original = dataframe
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
        
        try: # df ; index set checking
            
            if self.df.index.name == None:
                self.df.set_index(id, inplace=True)
            
            else:
                pass
        except:
            raise TypeError(typeerror_message_for_indexsetting)
        
        else:
            print(SUCCESS_MESSAGE[self.language_set])

        self.id_var = self.df.index.name

        self.menu = menu
        self.menu.update(figure_functions)
        
    def progress(self, method: str, vars: list, group_vars: str = None, posthoc: bool = False, posthoc_method: str = 'bonf', selector: dict = None):
        """
        Please check the documentation : https://cslee145.notion.site/statmanager-kr-Documentation-c9d0886f29ea461d9d0f44449a145f8a?pvs=4
        
        """
        method = method.lower()
        posthoc_method = posthoc_method.lower()

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
        
        
        if 'ttest_ind_trim' in method:
            trim_ratio = method.replace('ttest_ind_trim', "") 
            
            try:
                if trim_ratio == "":
                    print(notation_for_trim_ratio_when_zero[self.language_set])
                    trim_ratio = 0.2
                
                else:
                    trim_ratio = float(trim_ratio)
                    
                    if trim_ratio >= 0.5 or trim_ratio <= 0:
                        raise ValueError(valueerror_message_for_trim_ratio[self.language_set])
                    else:
                        pass
            except:
                raise KeyError(keyerror_message_for_trim[self.language_set])
            
            method = 'ttest_ind_trim'
        
        
        testtype = self.menu[method]['type']
        
        if selector == None:
            self.selector = None
            df = self.df_original
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
            
            variables = []
            for variable in vars:
                if isinstance(variable, str):
                    variables.append(variable)
                else:
                    variables = variables + variable
            
            df = df.dropna(axis=0, how = 'any', subset = variables)
        
        elif testtype == 'compare_ancova':
            
            if method == 'oneway_ancova':
                df = df.dropna(axis=0, how = 'any', subset = [vars[0]] + vars[1])
                
            elif method == 'rm_anocva':
                df = df.dropna(axis=0, how = 'any', subset = vars[-1] + vars[-1])
        
        elif testtype == 'correlation':
            pass
        
        else:
            df = df.dropna(axis=0, how = 'any', subset = vars)
        
        testfunc = self.menu[method]['testfunc']
        testname = self.menu[method]['name']
        
        if selector != None:
            
            selector_notation = selector_notification(condition_texts= conditions_notification_texts, test = testname)
            testname = selector_notation[self.language_set]

        
        n = len(df)
        
        self.method = method
        self.vars = vars
        self.group_vars = group_vars
        self.df = df
        
        if testtype == 'frequency_analysis': # done
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object            
            
        if testtype == 'normality':  # done
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname, group_vars = group_vars)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
        if testtype == 'homoskedasticity': # done
            result = testfunc(df = df, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
        
        if testtype == 'bootstrap': # done
            result, figure_object = testfunc(df = df, vars = vars, group_vars = group_vars, resampling_no = resampling_no, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object, figure_object
        
        if testtype == 'within_group': # done 
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
        if testtype == 'anova_nways' : # done
            result = testfunc(df = df, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method, selector = self.selector)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object                       
            
        if testtype == 'compare_ancova': #done
            result = testfunc(df = df, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object                       
        
        if testtype == 'between_group': # done
            
            if method == 'ttest_ind_trim':
                result = testfunc(df = df, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method, trim = trim_ratio)
            else:
                result = testfunc(df = df, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object            
            
        if testtype == 'correlation': # done
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
    
        if testtype == 'regression': # done
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object 

        if testtype == 'reliability': # done
            
            result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
    
        if testtype == 'making_figure': # done
            
            if method == 'pp_plot' or method == 'qq_plot':
                
                figure_object = testfunc(series = self.df[self.vars])
                return figure_object
            
            if 'hist' in method: 
                
                figure_object = testfunc(df = self.df, var = self.vars, n = n)
                return figure_object
 
            if 'boxplot' in method:
                
                figure_object = testfunc(df = self.df, vars = self.vars, group_vars = self.group_vars)
                return figure_object
            
            if method == 'point_within':
                
                figure_object = testfunc(df = self.df, vars = self.vars, parametric = True)
                return figure_object
            
            if method == 'bar_between':
                figure_object = testfunc(df = self.df, vars = self.vars, group_vars = self.group_vars, parametric = True)
                return figure_object
    
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
            self.showing(self.figure_for_howtouse.set_index(search_logic['figure_for_howtouse']['index_for_howtouse']))
            
            print(NOTATION_FOR_HOWTOUSE_SELECTOR[self.language_set])
            self.showing(self.selector_for_howtouse)
            
            return self
    
    def saving_for_result(self, result: list, testname: str):
        
        return StatmanagerResult(method = self.method, vars = self.vars, group_vars=self.group_vars, result = result, selector = self.selector, testname = testname, df = self.df, lang_set = self.language_set)
    
    def change_dataframe(self, dataframe:pd.DataFrame, id :str = None):

        if dataframe.index.name == None and id != None:
            self.df = dataframe
            self.df.set_index(id, inplace=True)
            self.df_original = dataframe
        
        elif dataframe.index.name != None:
            self.df = dataframe
            self.df_original = dataframe
            
        else:
            raise TypeError(typeerror_message_for_indexsetting)
        
        self.result = None
        self.selector = None        
        self.filtered_df = None
        
        self.id_var = self.df.index.name
        
        print(success_message_for_changing_dataframe[self.language_set])
        
        return self
    
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