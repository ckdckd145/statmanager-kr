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
    """
    Summary
    ----
    This is a mandatory class that must be created in order to use statmanager-kr.   
    If you haven't read the officical documentation, it is recommended to check this: [Documentation](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4)
    
    Parameters:
    ----
    dataframe (pandas.DataFrame):   
        - The pandas.DataFrame to which statistical analysis will conducted.   
        - The DataFrame must follow a wide-range shape.   
        
    id (str, optional): Defaults to None.   
        - If the DataFrame has no index columns, specify the index.   
        
    language (str, optional): Defaults to 'kor'.   
        - Language settings. Supported Languages are English ('eng') and Korean ('kor').
            
            
    Functions:
    ----
    `.progress()`
        - Main method to conduct statistical analysis
        - For more details, see the docstrings of .progress() or [Documentation](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4)
    
    `.howtouse()`
        - Method to see how to use the statmanager-kr
        - For more details, see the docstrings of .howtouse()
        
    `.set_language()`
        - Method to change language setting
        - For more details, see the docstrings of .set_language()

    `.change_dataframe()`
        - Method to change dataframe
        - For more details, see the docstrings of .change_dataframe()
    """
    def __init__(self, dataframe: pd.DataFrame, id: str = None, language: str = 'kor'):

        self.df = dataframe
        self.df_original = dataframe
        self.df_analysis = None
        self.filtered_df = None
        self.conditions = None
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
        Summary
        ----
        Method to apply the statistical anaylsis based on the key argument provided to method parameter.   
        The results of the analysis will printed in format of str and pandas.DataFrame.   
        Also, an object of StatmanagerResult class will returned.   
        For more information of addtional methods for StatmanagerResult, see the 'Returns' sections below.   
           
        If you haven't read the officical documentation, it is recommended to check this: [Documentation](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4)
           
        Parameters:
        ----
        method (str): Key value of statistical analysis   
            - `kstest`: Kolmogorov-Smirnov Test, Required: vars, Optional: group_vars
            - `shapiro`: Shapiro-Wilks Test, Required: vars, Optional: group_vars
            - `z_normal`: Z-skeweness & z-kurtosis test, Required: vars, Optional: group_vars
            - `levene`: Levene Test, Required: vars, group_vars
            - `fmax`: Fmax Test, Required: vars, group_vars
            - `chi2_contingency`: Chi-squared Test, Required: vars
            - `fisher`: Fisher's Exact Test, Required: vars
            - `pearsonr`: Pearson's r, Required: vars
            - `spearmanr`: Spearman's rho, Required: vars
            - `kendallt`: Kendall's tau, Required: vars
            - `ttest_ind`: Independent Samples T-test, Required: vars, group_vars
            - `ttest_rel`: Dependent Samples T-test, Required: vars
            - `ttest_ind_trim`: Yuen's Two Samples T-test, Required: vars, group_vars
            - `ttest_ind_welch`: Welch's Two Samples T-test, Required: vars, group_vars
            - `mannwhitneyu`: Mann-Whitney U Test, Required: vars, group_vars
            - `brunner`: Brunner-Munzel Test, Required: vars, group_vars
            - `wilcoxon`: Wilcoxon-Signed Rank Test, Required: vars
            - `bootstrap`: Bootstrap Percentile Method, Required: vars, Optional: group_vars
            - `f_oneway`: One-way ANOVA, Required: vars, group_vars, Optional: posthoc, posthoc_method
            - `f_oneway_rm`: One-way Repeated Measures ANOVA, Required: vars, Optional: posthoc, posthoc_method
            - `kruskal`: Kruskal-Wallis Test, Required: vars, group_vars, Optional: posthoc, posthoc_method
            - `friedman`: Friedman Test, Required: vars, Optional: posthoc, posthoc_method
            - `f_nway`: N-way ANOVA, Required: vars, group_vars, Optional: posthoc, posthoc_method
            - `f_nway_rm`: N-way Mixed Repeated Measures ANOVA, Required: vars, group_vars, Optional: posthoc, posthoc_method
            - `linearr`: Linear Regression, Required: vars
            - `hier_linearr`: Hierarchical Linear Regression, Required: vars
            - `logisticr`: Logistic Regression, Required: vars
            - `oneway_ancova`: One-way ANCOVA, Required: vars, group_vars
            - `rm_ancova`: One-way Repeated Measures ANCOVA, Required: vars
            - `cronbach`: Calculating Cronbach's Alpha, Required: vars
            
        vars (str or list): Dependent Variables
            - Provide dependent variable
            
        group_vars (str or list, optional): Group variables
            - Must be provided when applying between group functions. 
        
        posthoc (bool, optional): Whether to conduct posthoc analysis
            - Defaults to False.
            - Posthoc analysis will conducted when True 
            - Only for ANOVA, ANCOVA 
            
        posthoc_method (str, optional): Method for posthoc analysis 
            - Defaults to 'bonf'
            - Bonferroni correction ('bonf') and Tukey HSD ('tukey') are supported   
            
        selector (dict, optional): 
            - Defaults to None
            - Use it if only data that meets certain conditions should be analyzed. 
            - For more informations, run .howtouse('selector')
            
            - if a == b: Use {'a': 'b'} → Same in Pandas: df.loc[df['a'] == 'b']
            - if a != b: Use {'a': {'!=', 'b'}} → Same in Pandas: df.loc[df['a'] != 'b']
            - if a > b: Use {'a': {'>', 'b'}} → Same in Pandas: df.loc[df['a'] > 'b']
            - if a >= b: Use {'a': {'>=', 'b'}} → Same in Pandas: df.loc[df['a'] >= 'b']
            - if a < b: Use {'a': {'<', 'b'}} → Same in Pandas: df.loc[df['a'] < 'b']
            - if a <= b: Use {'a': {'<=', 'b'}} → Same in Pandas: df.loc[df['a'] <= 'b']

        Returns:
        ----
        Object of StatmanagerResult Class.
        
        Functions of StatmanagerResult
        ----
        `.figure()`
            - Generating Figure (matplotlib.axes.Axes)
        
        `.show()`
            - Reprinting the results
            - Useful when the object of StatmanagerResult Class are declared in certain variable
        
        `.save()`
            - method for saving the results
            
            Parameters:
                filename (str)
                    - Specify the filename
                    - Do not include extensions such as .txt or .xlsx
                
                fileformat (str) 
                    - Default to 'txt'
                    - file format : 'txt' and 'xlsx' are supported
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
            self.df_analysis = self.df_original
            #df = self.df_original
            self.filtered_df = None          
            self.conditions = None
            #conditions = None
            self.conditions_notification_texts = None
        
        else:
            
            if type(selector) != dict:
                raise TypeError(error_message_for_selector_type(doclink = self.link)[self.language_set])
            
            #always init the selector and related variables for repeated running
            self.selector = None
            self.df_analysis = self.df_original
            self.filtered_df = None          
            self.conditions = None
            self.conditions_notification_texts = None
            
            self.selector = selector
            
            conditions  = []
            conditions_notification = []
            
            for key, value in selector.items():
                if isinstance(value, dict):  
                    for op, op_value in value.items():
                        if op == '<=':
                            conditions.append(self.df_analysis[key] <= op_value)
                            conditions_notification.append(f"{key} <= {op_value}")
                        elif op == '>=':
                            conditions.append(self.df_analysis[key] >= op_value)
                            conditions_notification.append(f"{key} >= {op_value}")
                        elif op == '<':
                            conditions.append(self.df_analysis[key] < op_value)
                            conditions_notification.append(f"{key} < {op_value}")
                        elif op == '>':
                            conditions.append(self.df_analysis[key] > op_value)
                            conditions_notification.append(f"{key} > {op_value}")
                        elif op == '=' or op == '==':
                            conditions.append(self.df_analysis[key] == op_value)
                            conditions_notification.append(f"{key} == {op_value}")
                        elif op == '!=':
                            conditions.append(self.df_analysis[key] != op_value)
                            conditions_notification.append(f"{key} != {op_value}")

                else: 
                    conditions.append(self.df_analysis[key] == value)
                    conditions_notification.append(f"{key} == {value}")
            
            combined_condition = conditions[0]
            
            if len(conditions) == 1: # when the selector is only one 
                pass
            
            else: # when the selector are more than one
                for cond in conditions[1:]:
                    combined_condition &= cond
                    
            self.df_analysis = self.df_analysis.loc[combined_condition]
            self.filtered_df = self.df_analysis
            conditions_notification_texts = "\n".join(conditions_notification)
            self.conditions = conditions
            self.conditions_notification_texts = conditions_notification_texts
            
        if testtype == 'regression':
            
            variables = []
            for variable in vars:
                if isinstance(variable, str):
                    variables.append(variable)
                else:
                    variables = variables + variable
            
            self.df_analysis = self.df_analysis.dropna(axis=0, how = 'any', subset = variables)
        
        elif testtype == 'compare_ancova':
            
            if method == 'oneway_ancova':
                self.df_analysis = self.df_analysis.dropna(axis=0, how = 'any', subset = [vars[0]] + vars[1])
                
            elif method == 'rm_anocva':
                self.df_analysis = self.df_analysis.dropna(axis=0, how = 'any', subset = vars[-1] + vars[-1])
        
        elif testtype == 'correlation':
            pass
        
        else:
            self.df_analysis = self.df_analysis.dropna(axis=0, how = 'any', subset = vars)
        
        testfunc = self.menu[method]['testfunc']
        testname = self.menu[method]['name']
        
        if selector != None:
            
            selector_notation = selector_notification(condition_texts= conditions_notification_texts, test = testname)
            testname = selector_notation[self.language_set]

        
        n = len(self.df_analysis)
        
        self.method = method
        self.vars = vars
        self.group_vars = group_vars
        self.df = self.df_analysis
        
        
        if testtype == 'frequency_analysis': # done
            
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            
            return result_object            
            
        if testtype == 'normality':  # done
            
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname, group_vars = group_vars)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
        if testtype == 'homoskedasticity': # done
            result = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
        
        if testtype == 'bootstrap': # done
            result, figure_object = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, resampling_no = resampling_no, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object, figure_object
        
        if testtype == 'within_group': # done 
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
            
        if testtype == 'anova_nways' : # done
            result = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method, selector = self.selector)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object                       
            
        if testtype == 'compare_ancova': #done
            result = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object                       
        
        if testtype == 'between_group': # done
            
            if method == 'ttest_ind_trim':
                result = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method, trim = trim_ratio)
            else:
                result = testfunc(df = self.df_analysis, vars = vars, group_vars = group_vars, lang_set = self.language_set, testname = testname, posthoc = posthoc, posthoc_method = posthoc_method)
            result_object = self.saving_for_result(result = result, testname = testname)
            
            return result_object            
            
        if testtype == 'correlation': # done
            
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object
    
        if testtype == 'regression': # done
            
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname)
            result_object = self.saving_for_result(result = result, testname = testname)
            return result_object 

        if testtype == 'reliability': # done
            
            result = testfunc(df = self.df_analysis, vars = vars, lang_set = self.language_set, testname = testname)
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
        """
        Summary
        ----
        Method to search and check how to use the statmanager-kr.
        If you haven't read the officical documentation, it is recommended to check this: [Documentation](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4)
        
        Parameters:
        ----
            keyword (str, optional): 
                - Defaults to None. If None, print everything users should know to use the statmanager
                - Enter a specific search term

        Note
        ----
        If `.howtouse("selector")` is run, it will display how to use the `selector` parameter of the `.progress()` method.   
        """
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
        """
        Summary
        ----
        Method to change dataframe in Stat_Manager object

        Parameters:
        ----
        dataframe (pandas.DataFrame): 
            - The pandas.DataFrame
            - The DataFrame must follow a wide-range shape.  
            
        id (str, optional): 
            - Defaults to None.
            - If the DataFrame has no index columns, specify the index.   
        """
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
        """
        Summary
        ----
        Method to change language setting in Stat_Manager object

        Parameters:
        ----
        lang (str): 
            - Languages to apply
            - English ('eng') and Korean ('kor') are supported
        """
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