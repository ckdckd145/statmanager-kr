import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
from statsmodels.stats.anova import AnovaRM

from .posthoc_functions import *
from .effectsize_functions import *

AGG_FORMULA = ['count', 'mean', 'median', 'std', 'min', 'max']

def ttest_rel(df: pd.DataFrame, vars: list, lang_set, testname, posthoc = None, posthoc_method = None):
    result_for_save = []
    
    n = len(df)
    
    series = []
    for _ in range(len(vars)):
        ser = df[vars[_]]
        series.append(ser)
    
    describe_df = df[vars].agg(AGG_FORMULA).round(3).rename(index = {'count' : 'n'})
    
    result_object = stats.ttest_rel(*series)
    
    s = result_object.statistic
    p = result_object.pvalue
    dof = result_object.df
    ci = result_object.confidence_interval()
    cohen_d = calculate_cohen(series)
    
    reporting_one = ttest_rel_and_wilcoxon_result_reporting_one(vars, n)[lang_set]
    reporting_two = ttest_rel_result_reporting_two(s, dof, p, ci, cohen_d)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
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
    
def wilcoxon(df: pd.DataFrame, vars: list, lang_set, testname, posthoc = None, posthoc_method = None):
    result_for_save =[]
    
    n = len(df)
    
    series = []
    for _ in range(len(vars)):
        ser = df[vars[_]]
        series.append(ser)
    
    describe_df = df[vars].agg(AGG_FORMULA).round(3).rename(index = {'count' : 'n'})
    
    result_object = stats.wilcoxon(*series, method='approx')
    
    s = result_object.statistic
    p = result_object.pvalue
    z = result_object.zstatistic
    rank_biserial_correlation = z / np.sqrt(n)
    
    reporting_one = ttest_rel_and_wilcoxon_result_reporting_one(vars, n)[lang_set]
    reporting_two = wilcoxon_result_reporting_two (s, z, p, rank_biserial_correlation)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)

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

def friedman(df: pd.DataFrame, vars: list, lang_set, testname, posthoc: bool = False, posthoc_method = 'bonf'):
    result_for_save =[]
    
    n = len(df)
    
    series = []
    for _ in range(len(vars)):
        ser = df[vars[_]]
        series.append(ser)
    
    describe_df = df[vars].agg(AGG_FORMULA).round(3).rename(index = {'count' : 'n'})
    
    result_object = stats.friedmanchisquare(*series)
    s = result_object.statistic
    p = result_object.pvalue
    
    reporting_one = friedman_and_f_oneway_rm_result_reporting(vars)[lang_set]
    reporting_two = friedman_result_reporting_two(s, p)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
    if posthoc:
        posthoc_table = posthoc_within(df, vars, parametric = False, posthoc_method = posthoc_method)
        reporting_posthoc = 'Posthoc: '
        result_for_save.append(reporting_posthoc)
        result_for_save.append(posthoc_table)
    
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
    
def rm_anova(df: pd.DataFrame, vars: list, lang_set, testname, posthoc: bool = False, posthoc_method = 'bonf'):
    result_for_save =[]
    
    n = len(df)
    index_col = df.index.name
    
    reset_df = df.reset_index().melt(id_vars = index_col, value_vars=vars)
    result_object = AnovaRM(data = reset_df, depvar = 'value', subject = index_col, within = ['variable']).fit()
    
    anova_table = result_object.anova_table.rename(columns = {'Pr > F' : 'p-value'})
    anova_table['partial etq squared'] = calculate_etasquared(df, vars)
    anova_table = anova_table.round(3)
    
    describe_df = df[vars].agg(AGG_FORMULA).round(3).rename(index = {'count' : 'n'})
    
    reporting = friedman_and_f_oneway_rm_result_reporting(vars)[lang_set]
    
    result_for_save.append(reporting)
    result_for_save.append(describe_df)
    result_for_save.append(anova_table)
    
    if posthoc:
        posthoc_table = posthoc_within(df, vars, parametric = True, posthoc_method = posthoc_method)
        reporting_posthoc = 'Posthoc: '
        result_for_save.append(reporting_posthoc)
        result_for_save.append(posthoc_table)
    
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

