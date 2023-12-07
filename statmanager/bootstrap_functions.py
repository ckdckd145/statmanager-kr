import pandas as pd
from scipy import stats
from .messages_for_reporting import *
from .making_figure import *
import numpy as np

confidence_cutoff = {
    0.90 : [5, 95],
    0.95 : [2.5, 97.5],
    0.99 : [0.5, 99.5],
}

def percentile_method(df: pd.DataFrame, vars: list or str, group_vars: str, lang_set :str, resampling_no : int, testname = 'Bootstrapping Percentile method', group_names = None):
    
    testname = f"{testname} {resampling_no} \n"
    result_for_save = []
    confidence_level = .95
    interval = confidence_cutoff[confidence_level]    
    ref = "\nReference:\nEfron, B., & Tibshirani, R. (1986). Bootstrap methods for standard errors, confidence intervals, and other measures of statistical accuracy. Statistical Science, 1(1), 54-75.\n"
    
    if group_vars == None: #within groups
        a_var = vars[0]
        b_var = vars[1]
        
        target_series1 = df[a_var]
        target_series2 = df[b_var]

        series_1 = bootstrapping(series = target_series1, resampling_no = resampling_no)
        series_2 = bootstrapping(series = target_series2, resampling_no = resampling_no)
        bootstrap_df = bootstrap_to_dataframe(series_1, series_2, label = vars)
        
        
        n = len(bootstrap_df)
        a_confidence_interval = np.percentile(bootstrap_df[a_var], interval)
        b_confidence_interval = np.percentile(bootstrap_df[b_var], interval)
        a_lower_bound = a_confidence_interval[0]
        a_upper_bound = a_confidence_interval[1]
        b_lower_bound = b_confidence_interval[0]
        b_upper_bound = b_confidence_interval[1]
        
        reporting = percentile_method_result_reporting(a_var, confidence_level, a_lower_bound, a_upper_bound, b_var, b_lower_bound, b_upper_bound)[lang_set]

        if a_upper_bound < b_lower_bound or a_lower_bound > b_upper_bound:
            conclusion_key = 'under'
        
        else:
            conclusion_key = 'up'
        
        conclusion = conclusion_for_percentile_method[lang_set][conclusion_key]
        
        
        
    else: #between groups
        dv = vars[0] if isinstance(vars, list) else vars
        
        if group_names == None:
            group_names = df[group_vars].unique()
        
        if len(group_names) > 2:
            raise ValueError(valueerror_message_for_bootstrap[lang_set])
        
        a_var = f"{group_names[0]}_{dv}"
        b_var = f"{group_names[1]}_{dv}"
        
        target_series1 = df.loc[df[group_vars] == group_names[0], dv]
        target_series2 = df.loc[df[group_vars] == group_names[1], dv]
        
        series_1 = bootstrapping(series = target_series1, resampling_no = resampling_no)
        series_2 = bootstrapping(series = target_series2, resampling_no = resampling_no)
        bootstrap_df = bootstrap_to_dataframe(series_1, series_2, label = [a_var, b_var])

        n = len(bootstrap_df)
        a_confidence_interval = np.percentile(bootstrap_df[a_var], interval)
        b_confidence_interval = np.percentile(bootstrap_df[b_var], interval)
        a_lower_bound = a_confidence_interval[0]
        a_upper_bound = a_confidence_interval[1]
        b_lower_bound = b_confidence_interval[0]
        b_upper_bound = b_confidence_interval[1]
        
        reporting = percentile_method_result_reporting(a_var, confidence_level, a_lower_bound, a_upper_bound, b_var, b_lower_bound, b_upper_bound)[lang_set]

        if a_upper_bound < b_lower_bound or a_lower_bound > b_upper_bound:
            conclusion_key = 'under'
        
        else:
            conclusion_key = 'up'
        
        conclusion = conclusion_for_percentile_method[lang_set][conclusion_key]
        
        
    result_for_save.append(reporting)
    result_for_save.append(conclusion)
    result_for_save.append(ref)
    result_for_save.append(bootstrap_df)
    
    print(testname)
    
    for n in range(len(result_for_save) - 1):
        print(result_for_save[n])
        
    plt.figure(figsize=(10, 8))
    if lang_set == 'kor':            
        sns.set(font = "Gulim", font_scale = 1.5)
    else:
        sns.set(font = 'Times New Roman', font_scale = 1.5)
    plt.style.use('grayscale')
    plt.title(f'Histogram of {a_var} & {b_var}')
    sns.histplot(data = bootstrap_df[a_var], label = a_var, alpha=0.5, kde=True)
    sns.histplot(data = bootstrap_df[b_var], label = b_var, alpha=0.5, kde=True)
    
    plt.axvline(a_lower_bound, color='black', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({a_var})')
    plt.axvline(a_upper_bound, color='black', linestyle='--')
    plt.axvline(b_lower_bound, color='gray', linestyle='--', label=f'{confidence_level * 100:.0f}% CI ({b_var})')
    plt.axvline(b_upper_bound, color='gray', linestyle='--')
            
    plt.xlabel(f"Value of {a_var} & {b_var}")
    plt.ylabel("No. of Samples")
    plt.legend(bbox_to_anchor=(1, 1))
    plt.grid(False)
    plt.show()
    
    return result_for_save

def bootstrapping(series: pd.Series, resampling_no, statistic=np.mean):
    
    n = len(series)
    bootstrap_results = []
    
    for _ in range(resampling_no):
        sample = series.sample(n, replace = True)
        statistic_value = statistic(sample)
        bootstrap_results.append(statistic_value)
        
    return bootstrap_results


def bootstrap_to_dataframe(*args, label):
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