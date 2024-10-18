import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
from itertools import product

# result = testfunc(df = df, vars = vars, lang_set = self.language_set, testname = testname) <-- in .progress()

def kstest(df: pd.DataFrame, vars: str | list, lang_set : str, testname : str = 'Kolmogorov-Smirnov Test', group_vars : str | list = None): 
    result_for_save = []
    
    if isinstance(vars, list) and len(vars) != 1:
        raise ValueError(error_message_for_more_vars[lang_set])
    
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

def shapiro(df: pd.DataFrame, vars: str | list, lang_set: str, testname: str = 'Shapiro-Wilks Test', group_vars: str | list = None): 
    result_for_save = [] 

    if isinstance(vars, list) and len(vars) != 1:
        raise ValueError(error_message_for_more_vars[lang_set])

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

def z_normal(df: pd.DataFrame, vars: str | list, lang_set: str, testname: str = 'z-skeweness & z-kurtosis test', group_vars: str | list = None):

    if isinstance(vars, list) and len(vars) != 1:
        raise ValueError(error_message_for_more_vars[lang_set])
    
    dv = vars[0] if isinstance(vars, list) else vars
    result_df = pd.DataFrame(columns = ['set', 'n', 'skewness', 'SE of skewness', 'z-skewness', 'kurtosis', 'SE of kurtosis', 'z-kurtosis', 'cutoff', 'conclusion']).set_index('set')
    result_for_save = []
    
    if group_vars == None:
        n = len(df)
        cutoff = select_cutoff_in_z_normal(n)
        
        target_series = df[dv]
        skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, conclusion = calculating_in_z_normal(target_series, cutoff, lang_set)
        
        result_df.loc['all', :] = [n, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, cutoff, conclusion]
    
    else:  # when group_vars were provided
        if isinstance(group_vars, list):
            if len(group_vars) == 1:
                group_vars = group_vars[0]
                target_series = []
                
                for _ in df[group_vars].unique():
                    series = df.groupby(group_vars).get_group(_)[dv]
                    series.name = _
                    target_series.append(series)
                    
                for _ in target_series:
                    n = len(_)
                    cutoff = select_cutoff_in_z_normal(n)
                    skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, conclusion = calculating_in_z_normal(_, cutoff, lang_set)
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                        
                    result_df.loc[name, :] = [n, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, cutoff, conclusion]

            else: #more than 1 group_vars were provided
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
                    n = len(_)
                    cutoff = select_cutoff_in_z_normal(n)
                    skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, conclusion = calculating_in_z_normal(_, cutoff, lang_set)
                    if isinstance(_.name, tuple):
                        name = " & ".join(_.name)
                    else:
                        name = _.name
                        
                    result_df.loc[name, :] = [n, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, cutoff, conclusion]                    
        else: # group_vars were str format
            target_series = []
            
            for _ in df[group_vars].unique():
                series = df.groupby(group_vars).get_group(_)[dv]
                series.name = _
                target_series.append(series)
                
            for _ in target_series:
                n = len(_)
                cutoff = select_cutoff_in_z_normal(n)
                skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, conclusion = calculating_in_z_normal(_, cutoff, lang_set)
                if isinstance(_.name, tuple):
                    name = " & ".join(_.name)
                else:
                    name = _.name
                    
                result_df.loc[name, :] = [n, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, cutoff, conclusion]

    for _ in result_df.columns:
        if _ != 'conclusion':
            result_df[_] = result_df[_].astype(float).round(3)
        else:
            continue
    
    result_for_save.append(result_df)
    result_for_save.append(reference_of_z_normal)
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


def select_cutoff_in_z_normal(n):
    if n < 50:
        cutoff = 1.96
    
    elif n <= 200:
        cutoff = 2.59
    
    elif n > 200:
        cutoff = 3.13
        
    return cutoff


def calculating_in_z_normal(series, cutoff, lang_set):
    n = len(series)
    
    skewness = series.skew()
    skewness_se = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3)))
    
    kurtosis = series.kurtosis()
    kurtosis_se = (np.sqrt((n**2 - 1) / ((n-3)*(n+5))) * skewness_se * 2)
    
    z_skewness = (skewness/skewness_se).round(3)
    z_kurtosis = (kurtosis/kurtosis_se).round(3)
    
    if abs(z_skewness) < cutoff and abs(z_kurtosis) < cutoff:
        conclusion_key = 'up'
    else:
        conclusion_key = 'under'
    
    conclusion = conclusion_for_normality_assumption[lang_set][conclusion_key]
    
    return skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, conclusion