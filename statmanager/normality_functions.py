import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
from itertools import product

# result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname) <-- in .progress()

def kstest(df: pd.DataFrame, vars: str or list, lang_set : str, testname : str = 'Kolmogorov-Smirnov Test', group_vars : str or list = None): 
    result_for_save = []
    dv = vars[0] if isinstance(vars, list) else vars
    result_df = pd.DataFrame(columns = ['set', 'n', 'test statistic', 'p-value', 'maximum deviation location', 'deviation direction', 'conclusion']).set_index('set')
    df = df
    
    if group_vars == None:
        n = len(df)
        target_series = df[dv]
        compare_dist = (np.mean(target_series), np.std(target_series))
        result_object = stats.kstest(df[dv], cdf = 'norm', args = compare_dist)
        
        s = result_object.statistic
        p = result_object.pvalue
        rvs = result_object.statistic_location  
        ssn = result_object.statistic_sign 
        
        if p <= .05 :
            conclusion_key = 'under'
            
        else:
            conclusion_key = 'up'
            
        conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
        
        result_df.loc['all', :] = [n, s, p, rvs, ssn, conclusion]
        
    else:
        if isinstance(group_vars, list): #when group_vars were provided as list
            if len(group_vars) == 1: #only one
                group_vars = group_vars[0]
                target_series = []
                for _ in df[group_vars].unique():
                    series = df.groupby(group_vars).get_group(_)[dv]
                    series.name = _
                    target_series.append(series)
                    
                for _ in target_series:
                    compare_dist = (np.mean(_), np.std(_))
                    result_object = stats.kstest(_, cdf = 'norm', args = compare_dist)
                    n = len(_)
                    s = result_object.statistic
                    p = result_object.pvalue
                    rvs = result_object.statistic_location  
                    ssn = result_object.statistic_sign 
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                    
                    if p <= .05 :
                        conclusion_key = 'under'
                        
                    else:
                        conclusion_key = 'up'
                        
                    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
                    
                    result_df.loc[name , : ] = [n, s, p, rvs, ssn, conclusion]
                
            else: # more than one 
                combo_list = [df[group].unique() for group in group_vars]

                combi = product(*combo_list)

                target_series = []
                
                for combo in combi:
                    try:
                        series = df.groupby(group_vars).get_group(combo)[dv]
                        series.name = combo
                        target_series.append(series)
                    
                    except KeyError:
                        continue
                
                for _ in target_series:
                    compare_dist = (np.mean(_), np.std(_))
                    result_object = stats.kstest(_, cdf = 'norm', args = compare_dist)
                    n = len(_)
                    s = result_object.statistic
                    p = result_object.pvalue
                    rvs = result_object.statistic_location  
                    ssn = result_object.statistic_sign 
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                    if p <= .05 :
                        conclusion_key = 'under'
                        
                    else:
                        conclusion_key = 'up'
                        
                    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]

                    
                    result_df.loc[name , : ] = [n, s, p, rvs, ssn, conclusion]
                        
        else: # not list group_vars provided as str 
            target_series = []
            for _ in df[group_vars].unique():
                series = df.groupby(group_vars).get_group(_)[dv]
                series.name = _
                target_series.append(series)
                
            for _ in target_series:
                compare_dist = (np.mean(_), np.std(_))
                result_object = stats.kstest(_, cdf = 'norm', args = compare_dist)
                n = len(_)
                s = result_object.statistic
                p = result_object.pvalue
                rvs = result_object.statistic_location  
                ssn = result_object.statistic_sign 
                
                if isinstance(_.name, tuple):
                    name = " & ".join(_.name)
                else:
                    name = _.name
                if p <= .05 :
                    conclusion_key = 'under'
                    
                else:
                    conclusion_key = 'up'
                    
                conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]            
                result_df.loc[name , : ] = [n, s, p, rvs, ssn, conclusion]
                
    for _ in result_df.columns:
        if _ != 'conclusion':
            result_df[_] = result_df[_].astype(float).round(3)
        else:
            continue

    if result_df['n'].min() < 30:
        warning = warning_message_for_normality['kstest'][lang_set]
        result_for_save.append(warning)

    result_for_save.append(result_df)
    
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

def shapiro(df: pd.DataFrame, vars: str or list, lang_set: str, testname: str = 'Shapiro-Wilks Test', group_vars = None): 
    result_for_save = [] 
    dv = vars[0] if isinstance(vars, list) else vars
    result_df = pd.DataFrame(columns = ['set', 'n', 'test statistic', 'p-value', 'conclusion']).set_index('set')
    
    if group_vars == None:
        n = len(df)
        target_series = df[dv]
        result_object = stats.shapiro(target_series)
        
        s = result_object.statistic
        p = result_object.pvalue
        
        if p <= .05 :
            conclusion_key = 'under'
            
        else:
            conclusion_key = 'up'
            
        conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
        
        result_df.loc['all', : ] = [n, s, p, conclusion]       
    
    else:
        if isinstance(group_vars, list): # when group_vars were provided as list format
            if len(group_vars) == 1:
                group_vars = group_vars[0]
                target_series = []
                
                for _ in df[group_vars].unique():
                    series = df.groupby(group_vars).get_group(_)[dv]
                    series.name = _
                    target_series.append(series)
                    
                for _ in target_series:
                    result_object = stats.shapiro(_)
                    n = len(_)
                    s = result_object.statistic
                    p = result_object.pvalue
                    
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                    
                    if p <= .05 :
                        conclusion_key = 'under'
                        
                    else:
                        conclusion_key = 'up'
                        
                    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
                    
                    result_df.loc[name , : ] = [n, s, p, conclusion]        
            else: # if group_vars provided are more than one
                combo_list = [df[group].unique() for group in group_vars]

                combi = product(*combo_list)

                target_series = []
                
                for combo in combi:
                    try:
                        series = df.groupby(group_vars).get_group(combo)[dv]
                        series.name = combo
                        target_series.append(series)
                    
                    except KeyError:
                        continue
                
                for _ in target_series:
                    result_object = stats.shapiro(_)
                    n = len(_)
                    s = result_object.statistic
                    p = result_object.pvalue
                    
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                    if p <= .05 :
                        conclusion_key = 'under'
                        
                    else:
                        conclusion_key = 'up'
                        
                    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]

                    result_df.loc[name , : ] = [n, s, p, conclusion]
        
        else: # group_vars provided as str not list.
            target_series = []
            for _ in df[group_vars].unique():
                series = df.groupby(group_vars).get_group(_)[dv]
                series.name = _
                target_series.append(series)
                
            for _ in target_series:
                result_object = stats.shapiro(_)
                n = len(_)
                s = result_object.statistic
                p = result_object.pvalue

                if isinstance(_.name, tuple):
                    name = " & ".join(_.name)
                else:
                    name = _.name
                if p <= .05 :
                    conclusion_key = 'under'
                    
                else:
                    conclusion_key = 'up'
                    
                conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]            
                result_df.loc[name , : ] = [n, s, p, conclusion]
    
    for _ in result_df.columns:
        if _ != 'conclusion':
            result_df[_] = result_df[_].astype(float).round(3)
        else:
            continue    
    
    if result_df['n'].min() >= 30:
        warning = warning_message_for_normality['shapiro'][lang_set]
        result_for_save.append(warning)

    result_for_save.append(result_df)
    
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

def z_normal(df: pd.DataFrame, vars: str or list, lang_set: str, testname: str = 'z-skeweness & z-kurtosis test', group_vars = None):
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