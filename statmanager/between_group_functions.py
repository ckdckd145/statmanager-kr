import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
from .effectsize_functions import *
from .posthoc_functions import *

from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

AGG_FORMULA = ['count', 'mean', 'median', 'std', 'min', 'max'] # .round(3).rename(columns = {'count' : 'n'})

def ttest_ind(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, trim = None, group_names : list = None):
    result_for_save = []
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    if group_names == None:
        group_names = df[group_vars].unique()

    df = df.loc[df[group_vars].isin(group_names)]
    
    
    describe_df = df.groupby(group_vars)[vars].agg(AGG_FORMULA).round(3).rename(columns = {'count' : 'n'}).T
    describe_df.columns.name = None
    
    series = []
    for n in range(len(group_names)):
        ser = df.loc[df[group_vars] == group_names[n], dv]
        series.append(ser)
        
    if not trim :
        result_object = stats.ttest_ind(*series) #, trim = True --> Yuen's T-test (non-homoskedasticity)
    else:
        result_object = stats.ttest_ind(*series, trim = trim)
    
    
    s = result_object.statistic
    p = result_object.pvalue
    dof = result_object.df
    ci = result_object.confidence_interval() 
    cohen_d = calculate_cohen(series)
    
    reporting_one = compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[lang_set]
    reporting_two = ttest_ind_result_reporting_two (s, p, dof, ci, cohen_d)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
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

def ttest_ind_yuen(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, group_names : list = None):
    
    result_for_save = ttest_ind(df =df, vars = vars, group_vars = group_vars, group_names = group_names, lang_set = lang_set, testname=testname, trim = .2)

    return result_for_save

def mannwhitneyu(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, group_names : list = None):
    result_for_save = []
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    if group_names == None:
        group_names = df[group_vars].unique()

    df = df.loc[df[group_vars].isin(group_names)]
    
    describe_df = df.groupby(group_vars)[vars].agg(AGG_FORMULA).round(3).rename(columns = {'count' : 'n'}).T
    describe_df.columns.name = None
    
    series = []
    for n in range(len(group_names)):
        ser = df.loc[df[group_vars] == group_names[n], dv]
        series.append(ser)
        
    result_object = stats.mannwhitneyu(*series)
    s = result_object.statistic
    p = result_object.pvalue
    
    n1 = len(series[0])
    n2 = len(series[1])
    z = (s - n1 * n2 / 2) / ((n1 * n2 * (n1 + n2 + 1)) / 12)**0.5
    rank_biserial_correlation = 1 - (2 * s) / (n1 * n2)
    
    reporting_one = compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[lang_set]
    reporting_two = compare_btwgroup_result_reporting_two (s, p, z, rank_biserial_correlation)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
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

def brunner(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, group_names : list = None):
    result_for_save = []
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    if group_names == None:
        group_names = df[group_vars].unique()

    df = df.loc[df[group_vars].isin(group_names)]
    
    describe_df = df.groupby(group_vars)[vars].agg(AGG_FORMULA).round(3).rename(columns = {'count' : 'n'}).T
    describe_df.columns.name = None
    
    series = []
    for n in range(len(group_names)):
        ser = df.loc[df[group_vars] == group_names[n], dv]
        series.append(ser)
        
    result_object = stats.brunnermunzel(*series)
    s = result_object.statistic
    p = result_object.pvalue
    
    reporting_one = compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[lang_set]
    reporting_two = brunner_result_reporting_two(s, p)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
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

def f_oneway(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, group_names : list = None):
    result_for_save = []
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    if group_names == None:
        group_names = df[group_vars].unique()

    df = df.loc[df[group_vars].isin(group_names)]
    
    
    describe_df = df.groupby(group_vars)[vars].agg(AGG_FORMULA).round(3).rename(columns = {'count' : 'n'}).T
    describe_df.columns.name = None
    
    formula = f'{dv} ~ C({group_vars})'
    model = ols(formula, data = df).fit()
    anova_table = anova_lm(model, typ=3)
    anova_table.rename(columns = {'PR(>F)' : 'p-value'}, inplace=True)
    
    ss_intercept = anova_table.loc['Intercept', 'sum_sq']
    ss_dv = anova_table.loc[f"C({group_vars})", 'sum_sq']
    ss_residual = anova_table.loc['Residual', 'sum_sq']
    total_ss = ss_intercept + ss_dv + ss_residual
    
    anova_table['partial eta squared'] = anova_table['sum_sq'] / total_ss
    anova_table = anova_table.round(3)
    
    reporting_one = compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(anova_table)
    
    if posthoc:
        posthoc_table = posthoc_between(df = df, vars = vars, group_vars = group_vars, group_names = group_names, parametric = True, posthoc_method = posthoc_method)
        reporting_posthoc = 'Posthoc: '
        result_for_save.append(reporting_posthoc)
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
    
def kruskal(df: pd.DataFrame, vars: list or str, group_vars : str, lang_set, testname, posthoc = None, posthoc_method = None, group_names : list = None):
    result_for_save = []
    
    dv = vars[0] if isinstance(vars, list) else vars
    
    if group_names == None:
        group_names = df[group_vars].unique()

    df = df.loc[df[group_vars].isin(group_names)]
    
    describe_df = df.groupby(group_vars)[vars].agg(AGG_FORMULA).round(3).rename(columns = {'count' : 'n'}).T
    describe_df.columns.name = None
    
    series = []
    for n in range(len(group_names)):
        ser = df.loc[df[group_vars] == group_names[n], dv]
        series.append(ser)
        
    result_object = stats.kruskal(*series)
    s = result_object.statistic
    p = result_object.pvalue
    dof = len(group_names) -1
    
    reporting_one = compare_btwgroup_result_reporting_one(dv, group_vars, group_names)[lang_set]
    reporting_two = kruskal_result_reporting_two(s, p, dof)[lang_set]
    
    result_for_save.append(reporting_one)
    result_for_save.append(describe_df)
    result_for_save.append(reporting_two)
    
    if posthoc:
        posthoc_table = posthoc_between(df = df, vars = vars, group_vars = group_vars, group_names = group_names, parametric = False, posthoc_method = posthoc_method)
        reporting_posthoc = 'Posthoc: '
        result_for_save.append(reporting_posthoc)
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