import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *

def chi2(df: pd.DataFrame, vars: list, lang_set :str, testname = 'Chi-Squared Test'):
    
    result_for_save = []
    cross_df = pd.crosstab(df[vars[0]], df[vars[1]])
    cross_df.columns.name = None
    number_of_cells = cross_df.count().sum()
    
    result_object = stats.chi2_contingency(cross_df)
    
    s = result_object.statistic
    p = result_object.pvalue
    dof = result_object.dof #to be-
    expected_frequency_df = pd.DataFrame(result_object.expected_freq, index = cross_df.index, columns = cross_df.columns)
    expected_frequency_df.columns.name = None
    
    num_under_five_expected_frequency = (expected_frequency_df < 5).sum().sum()
    
    percentage_of_under_five_values = num_under_five_expected_frequency / number_of_cells
    
    # -- #
    reporting = frequency_analysis_result_reporting_one(vars)[lang_set]
    reporting_two = frequency_analysis_result_reporting_two(s, p, dof)[lang_set]
    reporting_three = f"{percentage_df_word[lang_set]}\n{percentage_of_under_five_values_word[lang_set]} = {round(percentage_of_under_five_values * 100, 2):.2f}%\n"
    
    result_for_save.append(reporting)
    result_for_save.append(reporting_two)
    result_for_save.append(cross_df) 
    result_for_save.append(reporting_three)
    result_for_save.append(expected_frequency_df)
    
    if percentage_of_under_five_values >= 0.25:
        warning = warning_message_for_frequency_analysis[lang_set]
        result_for_save.append(warning)
    
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
    
def fisher(df: pd.DataFrame, vars: list, lang_set :str, testname = 'Fisher Exact Test'):
    result_for_save = []
    cross_df = pd.crosstab(df[vars[0]], df[vars[1]])
    cross_df.name = None
    number_of_cells = cross_df.count().sum()
    
    if len(cross_df.columns) == 2 and len(cross_df.index) == 2:
        result_object = stats.fisher_exact(cross_df)
        s = result_object.statistic
        p = result_object.pvalue
    
    
    elif len(cross_df.columns) > 2 or len(cross_df.index) > 2:
        # montecarlo prompt --- tobe
        raise KeyError(keyerror_message_for_fisherexact[lang_set])
    
    else:
        raise KeyError(keyerror_message_for_fisherexact[lang_set])
    
    # --- #
    reporting = frequency_analysis_result_reporting_one(vars)[lang_set]
    reporting_two = frequency_analysis_result_reporting_two_fisher(s, p)[lang_set]
    
    result_for_save.append(reporting)
    result_for_save.append(reporting_two)
    result_for_save.append(cross_df)    
    
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