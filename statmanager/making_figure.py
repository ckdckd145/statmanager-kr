import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
import datetime as dt

font_properties = {
    'kor' : {'family' : 'Gulim', 'color': 'Black', 'weight': 'normal', 'size': 16},
    'eng' : {'family': 'Times New Roman', 'color': 'Black', 'weight': 'normal', 'size': 16},
}

TODAY = dt.datetime.now().strftime('%Y-%m-%d')
NOW_TIME = dt.datetime.now().strftime("%H:%M:%S")

class StatmanagerResult:
    def __init__(self, method, vars, result, testname, group_vars = None, selector = None, df = None):
        
        self.df = df
        self.saving_date = TODAY
        self.saving_time = NOW_TIME
        
        self.method = method
        self.vars = vars
        self.result = result
        
        self.group_vars = group_vars
        self.selector = selector
        
        self.testname = testname
        
        self.df_results = []
        for _ in result:
            if type(_) == pd.DataFrame:
                self.df_results.append(_)
        
    def show(self, only_result = False):
        
        if only_result == False:
        
            print(f'::: Note :::\n\nSaving Date : {TODAY}\nSaving Time : {NOW_TIME}\n\n')
            
            showing_one = {
                'Method' : self.method,
                'Vars' : self.vars,
                'Group_vars' : self.group_vars,
                'Selector' : self.selector,            
            }
            
            print("::: Kwargs and Args Info :::\n")
            for key, value in showing_one.items():
                print(f"{key} : {value}")
            print("\n")
        
        print("::: Original Reports :::\n\n")
        
        print(self.testname)
        for n in self.result:
            if isinstance(n, str or list):
                print(n)
            else:
                try:
                    display(n)
                except:
                    print(n)
        
        return self

    def figure(self):
        
        if self.method == 'kstest':
            result = plot_cdf(df = self.df, dv = self.vars)
            return result
        
        elif self.method == 'shapiro' or self.method == 'z_normal':
            result = qq_plot(self.df[self.vars], language_set='kor')
            return result
        
        elif self.method == 'levene' or self.method == 'fmax':
            result = boxplot_homoskedasticity(df = self.df, vars = self.vars, group_vars = self.group_vars)
            return result
        
        elif self.method == 'pearsonr' or self.method == 'spearmanr' or self.method == 'kendallt':
            result = correlation_heatmap(self.df_results[1])
            return result

class FigureInStatmanager:
    def __init__(self, xlabel, ylabel, title, xticks=None, yticks=None, figure=None, style='grayscale', language_set = 'kor'):
        
        self.language_set = language_set
        self.font_properties = font_properties[self.language_set]
        
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xticks = xticks
        self.yticks = yticks
        self.ax = figure
        self.style = style
        plt.style.use(self.style)
        
        if figure is not None:
            self.apply_settings()

        # plt.show(False)
        
    def revise(self, xlabel=None, ylabel=None, title=None, xticks=None, yticks=None, style=None):
        
        if xlabel is not None:
            self.xlabel = xlabel
        
        if ylabel is not None:
            self.ylabel = ylabel
        
        if title is not None:
            self.title = title
        
        if xticks is not None:
            self.xticks = xticks
        
        if yticks is not None:
            self.yticks = yticks
            
        if style is not None:
            self.style = style

        self.apply_settings()
        
        return self

    def apply_settings(self):
        
        plt.style.use(self.style)
        
        self.ax.set_xlabel(self.xlabel, fontdict = self.font_properties)
        
        self.ax.set_ylabel(self.ylabel, fontdict = self.font_properties)
        
        self.ax.set_title(self.title, fontdict = self.font_properties)
        
        if self.xticks is not None:
            self.ax.set_xticks(self.xticks)
        
        if self.yticks is not None:
            self.ax.set_yticks(self.yticks)
    
    def show(self):
        plt.show(False)
        
        return self
    
    def save():
        pass

# make sure that all function should be finished with returning FigureInStatmanager object... Don't forget...

def pp_plot(series: pd.Series, language_set = 'kor'):
    sorted_data = series.sort_values()
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    
    theoretical_cdf = stats.norm.cdf(sorted_data, np.mean(series), np.std(series))
    slope, intercept, r_value, _, _ = stats.linregress(theoretical_cdf, cdf)
    
    ax = plt.subplot()
    ax.plot(theoretical_cdf, cdf, marker='o', linestyle = '', markersize=6)
    ax.plot([0, 1], [0, 1], color='red', linestyle='-', linewidth=2)
    ax.text(x= 0.7, y= 0.2, s = f"R\u00B2 = {r_value:.4f}", style = 'italic')
    ax.grid(False)
    
    return FigureInStatmanager(xlabel = 'Theoretical cumulative distribution', 
                               ylabel = 'Empirical cumulative distribution',
                               title = 'p-p plot',
                               figure = ax,
                               language_set = language_set,
                               )

def qq_plot(series: pd.Series, language_set = 'kor'):
    ax = plt.subplot()
    stats.probplot(series, dist='norm', plot=ax, rvalue = True, fit = True)
    ax.grid(False)

    ax.get_lines()[1].set_color('red')
    ax.get_lines()[1].set_linewidth(2)

    ax.get_lines()[0].set_markerfacecolor('Black')
    ax.get_lines()[0].set_markeredgecolor('Black')
    ax.get_lines()[0].set_markersize(6)
    
    return FigureInStatmanager(xlabel = 'Theoretical quantiles',
                               ylabel = 'Ordered Values',
                               title = 'q-q plot',
                               figure = ax,
                               language_set = language_set)

def hist(df: pd.DataFrame, var, n, statistic = 'count', language_set = 'kor', cumulate = False):
    ax = sns.histplot(data = df, x = var, stat = statistic, cumulative = cumulate, element="bars", kde=True)
    
    return FigureInStatmanager(xlabel = f'Value of {var}',
                               ylabel = statistic,
                               title = f"Histogram of {var} (n = {n})",
                               figure = ax,
                               language_set = language_set)

def hist_cumulative(df: pd.DataFrame, var, n, statistic = 'count', language_set = 'kor'):
    
    result_ax = hist(df = df, var = var, n = n, statistic = statistic, language_set = language_set, cumulate = True)
    
    return result_ax


def plot_cdf(df, dv): # 'kstest'
    plt.style.use('grayscale')
    data_sorted = np.sort(df[dv])
    cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
    norm_cdf = stats.norm.cdf(data_sorted, np.mean(data_sorted), np.std(data_sorted))

    # Figure와 Axes 객체 생성
    fig, ax = plt.subplots(figsize=(8, 4))

    # Axes 객체에 두 CDF 그래프를 그림
    sns.lineplot(x=data_sorted, y=cdf, label='Data CDF', ax=ax, linewidth=3, errorbar = None)
    sns.lineplot(x=data_sorted, y=norm_cdf, label='Normal CDF', ax=ax, linewidth=3, errorbar = None)

    return FigureInStatmanager(xlabel = dv,
                               ylabel = 'CDF',
                               title = 'Kolmogorov-Smirnov Test: CDF Comparison',
                               figure = ax,
                               language_set='eng')
    
    
def boxplot_homoskedasticity(df, vars, group_vars):
    plt.style.use('grayscale')
    ax = sns.boxplot(x = group_vars, y = vars, data = df, hue = group_vars)    
    
    return FigureInStatmanager(xlabel = group_vars,
                               ylabel = vars,
                               title = f'Box plot for {vars}',
                               figure = ax,
                               language_set='eng')    
    
    
def correlation_heatmap(df_result:pd.DataFrame):
    plt.style.use('grayscale')
    ax = sns.heatmap(df_result.abs(), annot=df_result, fmt = '.3f', cmap ='gray')
    
    return FigureInStatmanager(xlabel = None,
                               ylabel = None,
                               title = 'Heatmap for correlation coefficients',
                               figure = ax,
                               language_set= 'kor')