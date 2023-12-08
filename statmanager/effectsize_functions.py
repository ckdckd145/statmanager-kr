import numpy as np
import pandas as pd

def calculate_etasquared(df, vars):
    
    series = []
    for _ in range(len(vars)):
        ser = df[vars[_]]
        series.append(ser)    
    
    
    
    k = len(series)

    group_means = [ser.mean() for ser in series]
    overall_mean = np.mean(group_means)

    ss_between = sum([(group_mean - overall_mean) ** 2 * len(ser) for group_mean, ser in zip(group_means, series)])
    ss_error = sum([sum((ser - group_mean) ** 2) for ser, group_mean in zip(series, group_means)])

    # Partial Eta-squared (\(\eta_p^2\))
    eta_squared = ss_between / (ss_between + ss_error)    
    
    return eta_squared

def calculate_cohen(series):
    
    groupa_n = series[0].count()
    groupb_n = series[1].count()
    
    groupa_mean = series[0].mean()
    groupb_mean = series[1].mean()
    
    groupa_std = series[0].std()
    groupb_std = series[1].std()                    
    
    son = groupa_mean - groupb_mean
    
    stage_1 = ((groupa_n - 1) * (groupa_std ** 2)) + ((groupb_n - 1) * (groupb_std ** 2))
    stage_2 = groupa_n + groupb_n - 2
    
    pooled_std = np.sqrt(stage_1/stage_2)
    
    cohen_d = (son / pooled_std)
    
    return cohen_d