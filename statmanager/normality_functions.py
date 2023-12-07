import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *


# result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname) <-- in .progress()

def kstest(df: pd.DataFrame, vars: str or list, lang_set : str, testname : str = 'Kolmogorov-Smirnov Test'): 
    n = len(df)
    dv = vars[0] if isinstance(vars, list) else vars

    result_object = stats.kstest(df[dv], cdf = 'norm')
    
    s = result_object.statistic
    p = result_object.pvalue
    rvs = result_object.statistic_location  # what is?
    ssn = result_object.statistic_sign # what is?

    # -- making reporting -- #
    result_for_save = []
    
    if n < 30:
        
        warning = warning_message_for_normality['kstest'][lang_set]
        result_for_save.append(warning)
    
    reporting = normality_test_result_reporting(dv, n, s, p)[lang_set]
    result_for_save.append(reporting)
    
    if p <= .05 :
        conclusion_key = 'under'
        
    else:
        conclusion_key = 'up'
        
    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
    
    result_for_save.append(conclusion)
    
    # -----print---- - #
    
    print(testname)
    for n in result_for_save:
        print(n)
    
    return result_for_save

def shapiro(df: pd.DataFrame, vars: str or list, lang_set: str, testname: str = 'Shapiro-Wilks Test'): 
    
    n = len(df)
    dv = vars[0] if isinstance(vars, list) else vars
    
    result_object = stats.shapiro(df[dv])
    
    s = result_object.statistic
    p = result_object.pvalue
    
    # -- making reporting -- #
    result_for_save = []        
    
    if n >= 30:
        
        warning = warning_message_for_normality['shapiro'][lang_set]
        result_for_save.append(warning) 
    
    reporting = normality_test_result_reporting(dv, n, s, p)[lang_set]
    result_for_save.append(reporting)
    
    if p <= .05 :
        conclusion_key = 'under'
        
    else:
        conclusion_key = 'up'
        
    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key] 
    result_for_save.append(conclusion)
    
    #--print--#
    print(testname)
    for n in result_for_save:
        print(n)
    
    return result_for_save

def z_normal(df: pd.DataFrame, vars: str or list, lang_set: str, testname: str = 'z-skeweness & z-kurtosis test'):
    n = len(df)
    dv = vars[0] if isinstance(vars, list) else vars
    
    series = df[dv]
    result_for_save = []
    
    skewness = series.skew()
    skewness_se = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    
    kurtosis = series.kurtosis()
    kurtosis_se = (np.sqrt((n**2 - 1) / ((n-3)*(n+5))) * skewness_se * 2)
    
    z_skewness = (skewness/skewness_se).round(3)
    z_kurtosis = (kurtosis/kurtosis_se).round(3)
    
    if n < 50:
        cutoff = 1.96
    elif n < 200:
        cutoff = 2.59
    elif n > 200:
        cutoff = 3.13
    
    reporting = z_normal_result_reporting(dv, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, n, cutoff)[lang_set]
    
    
    z_skewness = abs(z_skewness)
    z_kurtosis = abs(z_kurtosis)    
    
    if z_skewness < cutoff and z_kurtosis < cutoff:
        conclusion_key = 'up'
    else:
        conclusion_key = 'down'
        
    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
    
    result_for_save.append(reporting)
    result_for_save.append(conclusion)
    result_for_save.append(reference_of_z_normal)
    
    print(testname)
    for n in result_for_save:
        print(n)
    
    return result_for_save    