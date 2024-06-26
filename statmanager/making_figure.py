import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
import datetime as dt
from itertools import product
import re 

font_properties = 'Times New Roman'


sns.set(font = font_properties, font_scale = 1.5, style = None, rc = None, palette=None)
plt.style.use('grayscale')

TODAY = dt.datetime.now().strftime('%Y-%m-%d')
NOW_TIME = dt.datetime.now().strftime("%H:%M:%S")

class StatmanagerResult:
    """
    Summary
    ----
    This is the Class that is automatically created when the analysis is run through an object of the `Stat_Manager` class. 
    This class supports several methods that can be applied to the results of the applied statistical analysis. 
    
    
    Functions
    ----
    `.show()`
        - Method to re-print the result of statistical analysis conducted
    
    `.save()`
        - Method to save the result of statistical analysis conducted
    
    `.figure()`
        - Method to generate the figure presenting the results of statistical analysis conducted
    
    Note
    ----
    All of the functions of `StatamanagerReuslt` can be used as method chaining
    
    """
    
     
    def __init__(self, method, vars, result, testname, group_vars = None, selector = None, df = None, lang_set = None):
        
        self.df = df
        self.saving_date = TODAY
        self.saving_time = NOW_TIME
        
        self.method = method
        self.vars = vars
        self.result = result
        
        self.group_vars = group_vars
        self.selector = selector
        self.language_set = lang_set
        
        self.testname = testname
        
        self.df_results = []
        
        
        for _ in result:
            if type(_) == pd.DataFrame:
                self.df_results.append(_)
        
    def show(self, only_result = False):
        """
        Summary
        ----
        Method to re-print the result of statistical analysis conducted.   
        It's useful to declare the results of your analysis in a specific variable, and then re-check the results when needed. 

        Run
        ----
        It is recommended to use after declaring the result to specific variable.   
        For more details, see the example in the 'Sample Code' section.
        
        Sample Code
        ----
        ```
        # declaring the result into specific varialble 
        result_of_ttest = sm.progress(method = 'ttest_ind', vars = ...)
        
        ...
        ...
        
        # run when re-checking is needed
        result_of_ttest.show()
        ```
        

        Result
        ----
        The results of the statistical analysis conducted as well as the informations about the arguments and parameters when the analysis were conducted.
        """
        
        
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
    
    def save(self, filename: str, file_format: str ='txt'):
        """
        Summary
        ----
        Method to save the results of statistical analysis conducted into .txt or .xlsx file. 
        

        Parameters
        ----
        filename (str): filename
            - The filename without the format (.txt, .xlsx)
            - It is also possible to specify a directory, such as `r"./resultdata/result_"`
            
        file_format (str): file format
            - Default to 'txt'
            - 'txt' and 'xlsx' are supported

        Result
        ----
        If the path is not specified in the filename parameter, the resulting file will be saved in the same path as the code file (.py or .ipynb) from which the analysis was run. 
        """

        if file_format == 'txt':
            content = []
            content.append(f'::: Note :::\n\nSaving Date : {TODAY}\nSaving Time : {NOW_TIME}\n\n')

            showing_one = {
                'Testname' : self.testname,
                'Method': self.method,
                'Variables': self.vars,
                'Group_vars': self.group_vars,
                'Selector': self.selector,
            }

            for key, value in showing_one.items():
                content.append(f"{key} : {value}")
            content.append("\n")

            content.append("::: Original Reports :::\n\n")
            content.append(self.testname)            
            
            for n in self.result:
                if isinstance(n, str) or isinstance(n, list):
                    content.append(str(n))
                elif isinstance(n, pd.DataFrame):
                    content.append(n.to_string())

            content_str = '\n'.join(content)
            
            with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
                file.write(content_str)

        elif file_format == 'xlsx':
            writer = pd.ExcelWriter(f'{filename}.xlsx', engine='xlsxwriter')

            basic_infos = {
                'Saving Date' : TODAY,
                'Saving Time' : NOW_TIME,
                'Testname' : self.testname,
                'method' : self.method,
                'variables' : self.vars,
                'Group_vars' : self.group_vars,
                'Selector' : self.selector,
            }

            basic_infos = pd.DataFrame(list(basic_infos.items()), columns = ['type', 'info'])
            basic_infos.to_excel(writer, sheet_name='basic_info', index=False)

            non_dfs = {}
            for i, item in enumerate(self.result):
                if isinstance(item, pd.DataFrame):
                    item.to_excel(writer, sheet_name=f'result_{i + 1}')
                else:
                    non_dfs[f'Item{i}'] = item
            
            if non_dfs:
                non_dfs = pd.DataFrame(list(non_dfs.items()), columns=['Item', 'Content']).set_index('Item')
                non_dfs.to_excel(writer, sheet_name='results_', index=False)
            
            writer.close()

        else:
            raise ValueError("Unsupported fileformat. You must choose 'txt' or 'xlsx'.")        
    
    
    def figure(self, method = 'auto'):
        """
        Summary
        ----
        Method to generate the figure presenting the results of the analysis conducted.
        
        Run
        ----
        Just run as method chaining.    
        For example, if `sm.progress(method = 'ttest_ind', vars = ...).figure()` conducted, statmanager-kr will show the results of independent samples t-test and the related figure.

        Returns
        ----
        Object of `matplotlib.axes.Axes' 
            
        Note
        ----
        By applying methods to `Axes` object from the `seaborn` or `matplotlib` libraries, it's possible to freely manipulate the properties of the figure.         
        """
        
        if method == 'auto':
            if self.method == 'kstest':
                if self.group_vars == None:
                    result = plot_cdf(df = self.df, dv = self.vars)
                    return result
                else:
                    result = multiple_plot_cdf(df = self.df, vars = self.vars, group_vars = self.group_vars)
                    return result
            
            elif self.method == 'shapiro' or self.method == 'z_normal':
                
                if self.group_vars == None:
                    result =  result = qq_plot(self.df[self.vars])
                    return result
                else:
                    result = multiple_qq_plot(df = self.df, result_df = self.df_results[0], vars = self.vars, group_vars = self.group_vars)
                    return result
            
            elif self.method == 'levene' or self.method == 'fmax':
                result = boxplot_homoskedasticity(df = self.df, vars = self.vars, group_vars = self.group_vars)
                return result
            
            elif self.method == 'pearsonr' or self.method == 'spearmanr' or self.method == 'kendallt':
                result = correlation_heatmap(self.df_results[1], testname = self.method)
                return result
            
            elif self.method == 'ttest_rel' or self.method == 'f_oneway_rm':
                result = point_within(df = self.df, vars = self.vars, parametric = True)
                return result
            
            elif self.method == 'wilcoxon' or self.method == 'friedman':
                result = point_within(df = self.df, vars = self.vars, parametric = False)
                return result
            
            elif self.method == 'ttest_ind' or self.method == 'f_oneway' or self.method == 'ttest_ind_welch': # or self.method == 'oneway_ancova'  --> should be different
                result = bar_between(df = self.df, vars = self.vars, group_vars = self.group_vars, parametric = True)
                return result
            
            elif self.method == 'ttest_ind_trim':
                result = bar_between_trim(df = self.df_results[0],  vars = self.vars, group_vars = self.group_vars, result = self.result)
                return result
            
            elif self.method == 'mannwhitneyu' or self.method == 'brunner' or self.method == 'kruskal':# or self.method == 'rm_ancova'  --> should be different
                result = bar_between(df = self.df, vars = self.vars, group_vars = self.group_vars, parametric = False)
                return result                
            
            elif self.method == 'f_nway':
                result = f_nway_plot(df = self.df, vars = self.vars, group_vars = self.group_vars)
                return result
            
            elif self.method == 'f_nway_rm':
                result = f_nway_rm_plot(df = self.df, vars = self.vars, group_vars = self.group_vars)
                return result
            
            elif 'linearr' in self.method:
                result = residual_plot(df = self.df, vars = self.vars)
                return result
            
            elif self.method == 'logisticr':
                result = roc_curve (df = self.df, vars = self.vars)
                return result
        
        else:
            from .menu_for_howtouse import figure_functions
            testfunc = figure_functions[method]['testfunc']
            n = len(self.df)
            
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

def pp_plot(series: pd.Series):
    sorted_data = series.sort_values()
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    
    theoretical_cdf = stats.norm.cdf(sorted_data, np.mean(series), np.std(series))
    slope, intercept, r_value, _, _ = stats.linregress(theoretical_cdf, cdf)
    
    ax = plt.subplot()
    ax.plot(theoretical_cdf, cdf, marker='o', linestyle = '', markersize=6)
    ax.plot([0, 1], [0, 1], color='red', linestyle='-', linewidth=2)
    ax.text(x= 0.7, y= 0.2, s = f"R\u00B2 = {r_value:.4f}", style = 'italic')
    ax.grid(False)
    ax.set_title('p-p plot')
    ax.set_xlabel('Theoretical cumulative distribution')
    ax.set_ylabel('Empirical cumulative distribution')
    ax.figure.set_size_inches(10, 8)
    
    return ax

def qq_plot(series: pd.Series):
    ax = plt.subplot()
    stats.probplot(series, dist='norm', plot=ax, rvalue = True, fit = True)
    ax.grid(False)

    ax.get_lines()[1].set_color('red')
    ax.get_lines()[1].set_linewidth(2)

    ax.get_lines()[0].set_markerfacecolor('Black')
    ax.get_lines()[0].set_markeredgecolor('Black')
    ax.get_lines()[0].set_markersize(6)
    ax.grid(False)
    ax.set_xlabel('Theoretical quantiles')
    ax.set_ylabel('Ordered Values')
    ax.set_title('q-q plot')
    ax.figure.set_size_inches(10, 8)
    
    return ax 

def hist(df: pd.DataFrame, var, n, statistic = 'count', cumulate = False):
    ax = sns.histplot(data = df, x = var, stat = statistic, cumulative = cumulate, element="bars", kde=True)
    ax.set_xlabel(f'Value of {var}')
    ax.set_ylabel('Frequency')
    ax.set_title(f"Histogram of {var} (n = {n})")
    ax.grid(False)
    ax.figure.set_size_inches(10, 8)
    return ax 

def hist_cumulative(df: pd.DataFrame, var, n, statistic = 'count', ):
    result_ax = hist(df = df, var = var, n = n, statistic = statistic, cumulate = True)
    
    return result_ax

def multiple_qq_plot(df, result_df, vars, group_vars=None): 

    def qqplot(data, **kwargs):
        ax = plt.gca()  
        (osm, osr), (slope, intercept, r) = stats.probplot(data[vars], dist="norm")
        ax.plot(osm, osr, 'o', color='black') 
        ax.plot(osm, slope*osm + intercept, color='red')
        ax.text(0.05, 0.95, f'R² = {r**2:.3f}', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.grid(False)

    if isinstance(group_vars, list) and len(group_vars) > 1:
        g = sns.FacetGrid(df, col = group_vars[0], row = group_vars[1], margin_titles=True, aspect = 1.5)
    else:
        g = sns.FacetGrid(df, col=group_vars, aspect = 1.5)
    
    for group in result_df.index:
        if '&' in group:
            key = tuple(group.split(' & '))
        else:
            key = group
        
        group_data = df[df[group_vars].isin([key])]
        
        g.map_dataframe(qqplot, data=group_data)

    g.set_titles(col_template="{col_name}")
    g.set_axis_labels("Theoretical quantiles", "Ordered Values")
    
    return g

def multiple_plot_cdf(df,  vars, group_vars) :
    if not isinstance(vars, list):
        vars = [vars]
    if not isinstance(group_vars, list):
        group_vars = [group_vars]

    plot_data = pd.DataFrame()

    for var in vars:
        for _, group_df in df.groupby(group_vars):
            sorted_data = np.sort(group_df[var])
            cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            norm_cdf = stats.norm.cdf(sorted_data, np.mean(sorted_data), np.std(sorted_data))

            temp_df = pd.DataFrame({
                var: sorted_data,
                'Empirical CDF': cdf,
                'Normal CDF': norm_cdf
            })

            for group_var in group_vars:
                temp_df[group_var] = group_df[group_var].iloc[0]

            plot_data = pd.concat([plot_data, temp_df])

    g = sns.FacetGrid(plot_data, col=group_vars[0], row=group_vars[1] if len(group_vars) > 1 else None, height=5, aspect=1.5)
    g = g.map(plt.plot, var, 'Empirical CDF', color='black', label='Empirical CDF')
    g = g.map(plt.plot, var, 'Normal CDF', color='grey', label='Normal CDF')

    g.add_legend()
    g.set_titles('{col_name} & {row_name}' if len(group_vars) > 1 else '{col_name}')
    g.set_axis_labels(var, 'CDF')
    plt.subplots_adjust(top=0.8)
    g.fig.suptitle('Kolmogorov-Smirnov Test: CDF Comparison')

    return g

        
def plot_cdf(df, dv): # 'kstest'
    data_sorted = np.sort(df[dv])
    cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
    norm_cdf = stats.norm.cdf(data_sorted, np.mean(data_sorted), np.std(data_sorted))

    fig, ax = plt.subplots()

    sns.lineplot(x=data_sorted, y=cdf, label='Empirical CDF', ax=ax, linewidth=3, errorbar = None)
    sns.lineplot(x=data_sorted, y=norm_cdf, label='Normal CDF', ax=ax, linewidth=3, errorbar = None)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    ax.grid(False)
    ax.set_xlabel(dv)
    ax.set_ylabel('CDF')
    ax.set_title('Kolmogorov-Smirnov Test: CDF Comparison')
    ax.figure.set_size_inches(10, 8)
    
    return ax 
    
def boxplot_homoskedasticity(df, vars, group_vars):
    
    if isinstance(group_vars, list):
        if len(group_vars) == 1:
            ax = sns.boxplot(x = group_vars, y = vars, data = df, hue = group_vars)    
            
        else:
            combi_list = [ df[group].unique() for group in group_vars ]
            combi = product(*combi_list)
            
            df['group'] = None
            
            for combo in combi:
                name = ' & '.join(combo)
                conditions = [(df[var] == value) for var, value in zip(group_vars, combo)]
                all_conditions = conditions[0]
                for condition in conditions[1:]:
                    all_conditions &= condition
                    
                df.loc[all_conditions, 'group'] = name
            
            ax = sns.boxplot(x = 'group', y = vars, data = df, hue = 'group', palette='dark:Gray')
            labels = [item.get_text() for item in ax.get_xticklabels()]
            xt = ax.get_xticks()
            ax.set_xticks(xt)
            ax.set_xticklabels(labels, rotation=90)
        
    else: # group_vars were provided as str format
        ax = sns.boxplot(x = group_vars, y = vars, data = df, hue = group_vars)    

    ax.grid(False)
    ax.figure.set_size_inches(10, 8)
    ax.set_xlabel(f"{' & '.join(group_vars) if isinstance(group_vars, list) and len(group_vars) > 1 else group_vars}")
    ax.set_ylabel(vars)
    ax.set_title(f'Variance of {vars} by {group_vars if isinstance(group_vars, str) else ", ".join(group_vars)}')
    ax.figure.set_size_inches(10, 8)
    
    return ax 
    
def correlation_heatmap(df_result:pd.DataFrame, testname):
    
    coefficient_name = {
        'pearsonr' : "Pearson's r",
        'spearmanr' : "Spearman's r",
        'kendallt' : "Kendall's tau"
    }
    
    ax = sns.heatmap(df_result.abs(), annot=df_result, fmt = '.3f', cmap ='gray')
    ax.grid(False)
    ax.set_title(f'Heatmap for correlation coefficients ({coefficient_name[testname]})')
    ax.figure.set_size_inches(10, 8)
    
    return ax 


def point_within (df, vars, parametric):
    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars = index_col, value_vars = vars)
    
    if parametric:
        stat = np.mean
        stat_value = 'Mean'
    else:
        stat = np.median
        stat_value = 'Median'
    
    ax = sns.pointplot(data = melted_df, x = 'variable', y = 'value', errorbar = 'ci', estimator = stat, capsize = 0.1)
    
    min_value = melted_df['value'].min()
    max_value = melted_df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)
    ax.set_ylim(bottom = min_value, top = max_value)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.grid(False)
    ax.set_title(f'{stat_value} difference between {", ".join(vars)}')
    ax.figure.set_size_inches(10, 8)
    
    return ax 
    
def bar_between (df, vars, group_vars, parametric):
    
    if parametric:
        stat = np.mean
        stat_value = 'Mean'
    else:
        stat = np.median
        stat_value = 'Median'
        
    ax = sns.barplot(data = df, y = vars, x = group_vars, estimator = stat, hue = group_vars, errorbar = 'ci', capsize=0.1)
    
    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)
    ax.set_ylim(bottom = min_value, top = max_value)    
    ax.grid(False)
    ax.set_xlabel(group_vars)
    ax.set_ylabel(vars)
    ax.set_title(f'{stat_value} differences in {vars} by {group_vars}')
    ax.figure.set_size_inches(10, 8)
    
    return ax
    

def bar_between_trim (df: pd.DataFrame, vars, group_vars, result):
    
    categories = df.columns
    means = df.loc['mean'].to_list()
    stds = df.loc['std'].to_list()
    
    warning = re.search('Warning', result[0])
    
    if warning: 
        trim_ratio = ""
    else:
        trim_ratio = re.search(r'\b\d+(\.\d+)?%', result[0]).group()
        trim_ratio = ' (Trim ratio :' + trim_ratio + ')'
    x = np.arange(len(categories)) # set the barplot location
    
    fig, ax = plt.subplots()
    barplot = ax.bar(x, means, yerr=stds, align = 'center', alpha = 0.7, color=['Black', 'Grey'], capsize=10)
    ax.grid(False)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlabel(group_vars)
    ax.set_ylabel(vars)
    ax.set_title(f'Mean differences in {vars} by {group_vars}{trim_ratio}')
    ax.figure.set_size_inches(10, 8)
    
    return ax


def point_between_twogroup (df, vars, group_vars):
    ax = sns.pointplot(data = df, y = vars, x = group_vars[0], hue = group_vars[1], errorbar = 'ci', capsize=0.1)
    
    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)  
    ax.grid(False)
    ax.set_xlabel(group_vars[0])
    ax.set_ylabel(vars)
    ax.set_title(f'Mean difference in {vars} between {", ".join(group_vars)}')
    ax.figure.set_size_inches(10, 8)
    
    return ax
    
def mulitway_interaction_plot (df, vars, group_vars):
    if len(group_vars) < 3:
        raise ValueError("group_vars should contain at least three variables for multi-way interaction plot.")
    point_vars = group_vars[:2]
    facet_vars = group_vars[2:]       

    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
        
    g = sns.FacetGrid(df, col=facet_vars[0], row=facet_vars[1] if len(facet_vars) > 1 else None, margin_titles=True, palette='Greys')
    g.map_dataframe(sns.pointplot, point_vars[0], vars, point_vars[1], palette = 'Greys', capsize=0.1)

    g.set_axis_labels(point_vars[0], vars)
    g.add_legend()
    
    for ax in g.axes.flatten():
        ax.set_yticks(ticks)
        ax.yaxis.grid(False)
    
    g.fig.subplots_adjust(top=0.8)
    g.fig.suptitle(f'Interaction Plot for {", ".join(group_vars)}')
    
    return g

    
def f_nway_plot(df, vars, group_vars):
    
    if len(group_vars) == 2:
        result = point_between_twogroup(df = df, vars = vars, group_vars = group_vars)
        return result
    
    elif len(group_vars)>= 3:
        result = mulitway_interaction_plot(df = df, vars = vars, group_vars = group_vars)
        return result
    


def plot_rm_onegroup(df, vars, group_vars):
    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars=index_col, value_vars=vars, var_name='time').set_index(index_col)
    df = df.drop(columns = vars).merge(melted_df, how = 'outer', on = index_col)

    ax = sns.pointplot(data=df, x='time', y='value', hue=group_vars, capsize=0.1)

    min_value = df['value'].min()
    max_value = df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)  
    
    # Enhancing the plot
    plt.legend(title=group_vars)
    ax.grid(False)
    ax.set_xlabel('time')
    ax.set_ylabel('value')
    ax.set_title(f"Interaction Plot for {group_vars}")
    ax.figure.set_size_inches(10, 8)
    
    return ax


def plot_rm_twogroup(df, vars, group_vars):
    if len(group_vars) < 2:
        raise ValueError("group_vars should contain at least two variables for interaction plot.")

    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars=index_col, value_vars=vars, var_name='time').set_index(index_col)
    df = df.drop(columns=vars).merge(melted_df, how='outer', on=index_col)

    point_vars = group_vars[:2]
    facet_vars = group_vars[2:] if len(group_vars) > 2 else None

    min_value = df['value'].min()
    max_value = df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)

    if facet_vars:
        g = sns.FacetGrid(df, col=facet_vars[0], row=facet_vars[1] if len(facet_vars) > 1 else None, margin_titles=True, palette='Greys')
    else:
        g = sns.FacetGrid(df, col=point_vars[0], margin_titles=True, palette='Greys')

    g.map_dataframe(sns.pointplot, point_vars[0] if facet_vars else 'time', 'value', point_vars[1], errorbar = 'ci', palette='Greys', capsize=0.1)

    g.set_axis_labels(point_vars[0] if facet_vars else 'time', 'Value')
    g.add_legend()
    
    for ax in g.axes.flatten():
        ax.set_yticks(ticks)
        ax.yaxis.grid(False)
        
    g.figure.subplots_adjust(top=0.8)
    g.figure.suptitle(f'Interaction Plot for {", ".join(group_vars)}', fontsize=16)
    plt.grid(False)
    
    return g

def f_nway_rm_plot(df, vars, group_vars):
    
    if isinstance(group_vars, list) and len(group_vars) >= 2:
        result = plot_rm_twogroup (df = df, vars = vars, group_vars = group_vars)
        return result
    else:
        result = plot_rm_onegroup (df = df, vars = vars, group_vars = group_vars)
        return result        
    
def residual_plot (df, vars):
    from statsmodels import api
    dv = vars[0]
    
    iv = []
    if len(vars) > 2:
        for i in range(1, len(vars)):
            iv += vars[i]
    else:
        iv = vars[1] 

    y = df[dv]
    x = df[iv]
    x = pd.get_dummies(data = x, drop_first=True, dtype='int', prefix='dummy_',prefix_sep='_' )
    
    x = api.add_constant(x)
    model = api.OLS(y, x).fit()
    prediction = model.predict(x)
    
    residuals = y - prediction
    
    fig, ax = plt.subplots()

    ax.scatter(prediction, residuals, alpha=0.5)
    ax.axhline(y=0, color='r', linestyle='--')
    ax.grid(False)
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Residuals')
    ax.set_title('Residual plot')
    ax.figure.set_size_inches(10, 8)
    
    return ax
    
def roc_curve(df, vars):
    from statsmodels import api
    
    dv = vars[0]
    iv = vars[1] 
    
    y = df[dv]    
    x = df[iv]
    
    if len(y.unique()) == 2:
        y = pd.get_dummies(y, drop_first=True).iloc[:, 0]
    else:
        raise ValueError("Now, figure making not works in Multinominal Regression. It will be ready soon")
    
    
    x = pd.get_dummies(data=x, drop_first=True, dtype='int', prefix='dummy_', prefix_sep='_')
    x = api.add_constant(x)

    model = api.Logit(y, x).fit()

    y_score = model.predict(x)

    thresholds = np.linspace(0, 1, 100)

    tpr = []
    fpr = []

    for thresh in thresholds:
        tp = np.sum((y_score > thresh) & (y == 1))
        fn = np.sum((y_score <= thresh) & (y == 1))
        fp = np.sum((y_score > thresh) & (y == 0))
        tn = np.sum((y_score <= thresh) & (y == 0))

        tpr.append(tp / (tp + fn) if (tp + fn) != 0 else 0)
        fpr.append(fp / (fp + tn) if (fp + tn) != 0 else 0)

    auc = np.trapz(tpr, fpr)

    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, color='Red')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])

    ax.text(0.6, 0.2, f'AUC = {auc:.3f}')
    ax.grid(False)
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curve')
    ax.figure.set_size_inches(10, 8)
    
    return ax
