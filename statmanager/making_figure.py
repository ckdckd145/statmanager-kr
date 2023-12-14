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

# make sure that all function should be finished with returning FigureInStatmanager object... Don't forget...


TODAY = dt.datetime.now().strftime('%Y-%m-%d')
NOW_TIME = dt.datetime.now().strftime("%H:%M:%S")

class StatmanagerResult:
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
    
    def save(self, filename, file_format ='txt'):

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

            for i, item in enumerate(self.result):
                if isinstance(item, pd.DataFrame):
                    item.to_excel(writer, sheet_name=f'result_{i + 1}')

            writer.close()

        else:
            raise ValueError("Unsupported fileformat. You must choose 'txt' or 'xlsx'.")        
    
    
    def figure(self, method = 'auto'):

        if method == 'auto':
            if self.method == 'kstest':
                result = plot_cdf(df = self.df, dv = self.vars, language_set = self.language_set)
                return result
            
            elif self.method == 'shapiro' or self.method == 'z_normal':
                result = qq_plot(self.df[self.vars], language_set = self.language_set)
                return result
            
            elif self.method == 'levene' or self.method == 'fmax':
                result = boxplot_homoskedasticity(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set)
                return result
            
            elif self.method == 'pearsonr' or self.method == 'spearmanr' or self.method == 'kendallt':
                result = correlation_heatmap(self.df_results[1], language_set = self.language_set, testname = self.method)
                return result
            
            elif self.method == 'ttest_rel' or self.method == 'f_oneway_rm':
                result = point_within(df = self.df, vars = self.vars, language_set = self.language_set, parametric = True)
                return result
            
            elif self.method == 'wilcoxon' or self.method == 'friedman':
                result = point_within(df = self.df, vars = self.vars, language_set = self.language_set, parametric = False)
                return result
            
            elif self.method == 'ttest_ind' or self.method == 'f_oneway': # or self.method == 'oneway_ancova'  --> should be different
                result = bar_between(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set, parametric = True)
                return result
            
            elif self.method == 'mannwhitneyu' or self.method == 'brunner' or self.method == 'kruskal':# or self.method == 'rm_ancova'  --> should be different
                result = bar_between(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set, parametric = False)
                return result                
            
            elif self.method == 'f_nway':
                result = f_nway_plot(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set)
                return result
            
            elif self.method == 'f_nway_rm':
                result = f_nway_rm_plot(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set)
                return result
            
            elif self.method == 'linearr':
                result = residual_plot(df = self.df, vars = self.vars, language_set = self.language_set)
                return result
            
            elif self.method == 'logisticr':
                result = roc_curve (df = self.df, vars = self.vars, language_set = self.language_set)
                return result
        
        else:
            from .menu_for_howtouse import figure_functions
            testfunc = figure_functions[method]['testfunc']
            n = len(self.df)
            
            if method == 'pp_plot' or method == 'qq_plot':
                
                figure_object = testfunc(series = self.df[self.vars], language_set = self.language_set)
                return figure_object
            
            if 'hist' in method:
                
                figure_object = testfunc(df = self.df, var = self.vars, n = n, language_set = self.language_set)
                return figure_object

            if 'boxplot' in method:
                
                figure_object = testfunc(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set)
                return figure_object
            
            if method == 'point_within':
                
                figure_object = testfunc(df = self.df, vars = self.vars, language_set = self.language_set, parametric = True)
                return figure_object
            
            if method == 'bar_between':
                figure_object = testfunc(df = self.df, vars = self.vars, group_vars = self.group_vars, language_set = self.language_set, parametric = True)
                return figure_object

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
        
        try:
            self.ax.set_xlabel(self.xlabel, fontdict = self.font_properties)
            
            self.ax.set_ylabel(self.ylabel, fontdict = self.font_properties)
            
            self.ax.set_title(self.title, fontdict = self.font_properties)
            
            if self.xticks is not None:
                self.ax.set_xticks(self.xticks)
            
            if self.yticks is not None:
                self.ax.set_yticks(self.yticks)
        except:
            pass
    
    def show(self):
        plt.show(False)
        
        return self
    
    def save():
        pass


def pp_plot(series: pd.Series, language_set = 'kor'):
    sorted_data = series.sort_values()
    cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
    
    theoretical_cdf = stats.norm.cdf(sorted_data, np.mean(series), np.std(series))
    slope, intercept, r_value, _, _ = stats.linregress(theoretical_cdf, cdf)
    
    ax = plt.subplot()
    ax.plot(theoretical_cdf, cdf, marker='o', linestyle = '', markersize=6)
    ax.plot([0, 1], [0, 1], color='red', linestyle='-', linewidth=2)
    ax.text(x= 0.7, y= 0.2, s = f"R\u00B2 = {r_value:.4f}", style = 'italic', fontdict = font_properties[language_set])
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
    ax.grid(False)
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
    plt.grid(False)
    return result_ax


def plot_cdf(df, dv, language_set): # 'kstest'
    plt.style.use('grayscale')
    data_sorted = np.sort(df[dv])
    cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
    norm_cdf = stats.norm.cdf(data_sorted, np.mean(data_sorted), np.std(data_sorted))

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.lineplot(x=data_sorted, y=cdf, label='Empirical CDF', ax=ax, linewidth=3, errorbar = None)
    sns.lineplot(x=data_sorted, y=norm_cdf, label='Normal CDF', ax=ax, linewidth=3, errorbar = None)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]) # CDF Yticks
    ax.grid(False)
    return FigureInStatmanager(xlabel = dv,
                               ylabel = 'CDF',
                               title = 'Kolmogorov-Smirnov Test: CDF Comparison',
                               figure = ax,
                               language_set = language_set)
    
    
def boxplot_homoskedasticity(df, vars, group_vars, language_set = 'kor'):
    plt.style.use('grayscale')
    ax = sns.boxplot(x = group_vars, y = vars, data = df, hue = group_vars)    
    ax.grid(False)
    return FigureInStatmanager(xlabel = group_vars,
                               ylabel = vars,
                               title = f'Box plot for "{vars}"',
                               figure = ax,
                               language_set = language_set)    
    
    
def correlation_heatmap(df_result:pd.DataFrame, testname, language_set = 'kor'):
    plt.style.use('grayscale')
    
    coefficient_name = {
        'pearsonr' : "Pearson's r",
        'spearmanr' : "Spearman's r",
        'kendallt' : "Kendall's tau"
    }
    
    ax = sns.heatmap(df_result.abs(), annot=df_result, fmt = '.3f', cmap ='gray')
    ax.grid(False)
    return FigureInStatmanager(xlabel = None,
                               ylabel = None,
                               title = f'Heatmap for correlation coefficients ({coefficient_name[testname]})',
                               figure = ax,
                               language_set= language_set)

def point_within (df, vars, language_set, parametric):
    plt.style.use('grayscale')
    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars = index_col, value_vars = vars)
    
    if parametric:
        stat = np.mean
        stat_value = 'Mean'
    else:
        stat = np.median
        stat_value = 'Median'
    
    ax = sns.pointplot(data = melted_df, x = 'variable', y = 'value', errorbar = 'ci', estimator = stat)
    
    min_value = melted_df['value'].min()
    max_value = melted_df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.grid(False)
    return FigureInStatmanager(xlabel = None,
                               ylabel = None,
                               title = f'{stat_value} difference between {", ".join(vars)}',
                               figure = ax,
                               language_set = language_set)

def bar_between (df, vars, group_vars, parametric, language_set):
    
    plt.style.use('grayscale')
    
    if parametric:
        stat = np.mean
        stat_value = 'Mean'
    else:
        stat = np.median
        stat_value = 'Median'
        
    ax = sns.barplot(data = df, y = vars, x = group_vars, estimator = stat, hue = group_vars)
    
    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)    
    ax.grid(False)
    return FigureInStatmanager(xlabel = group_vars,
                               ylabel = vars,
                               title = f'{stat_value} differences in {vars} by {group_vars}',
                               figure = ax,
                               language_set = language_set)
    
def point_between_twogroup (df, vars, group_vars, language_set):
    
    plt.style.use('grayscale')
    
    ax = sns.pointplot(data = df, y = vars, x = group_vars[0], hue = group_vars[1], errorbar = 'ci')
    
    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)  
    ax.grid(False)
    return FigureInStatmanager(xlabel = group_vars[0],
                               ylabel = vars,
                               title = 'title',
                               figure = ax,
                               language_set = language_set)
    
def mulitway_interaction_plot (df, vars, group_vars, language_set):
    if len(group_vars) < 3:
        raise ValueError("group_vars should contain at least three variables for multi-way interaction plot.")
    
    plt.style.use('grayscale')
    point_vars = group_vars[:2]
    facet_vars = group_vars[2:]       

    min_value = df[vars].min()
    max_value = df[vars].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
        
    g = sns.FacetGrid(df, col=facet_vars[0], row=facet_vars[1] if len(facet_vars) > 1 else None, margin_titles=True, palette='Greys')
    g.map_dataframe(sns.pointplot, point_vars[0], vars, point_vars[1], palette = 'Greys')

    # Adding plot title and labels
    g.set_axis_labels(point_vars[0], vars)
    g.add_legend()
    
    for ax in g.axes.flatten():
        ax.set_yticks(ticks)
    
    g.fig.subplots_adjust(top=0.8)
    g.fig.suptitle(f'Interaction Plot for {", ".join(group_vars)}')
    plt.grid(False)
    return FigureInStatmanager(xlabel = None,
                               ylabel = vars,
                               title = 'title',
                               figure = g,
                               language_set = language_set)
    
def f_nway_plot(df, vars, group_vars, language_set):
    
    plt.style.use('grayscale')
    
    if len(group_vars) == 2:
        result = point_between_twogroup(df = df, vars = vars, group_vars = group_vars, language_set = language_set)
        return result
    
    elif len(group_vars)>= 3:
        result = mulitway_interaction_plot(df = df, vars = vars, group_vars = group_vars, language_set = language_set)
        return result
    


def plot_rm_onegroup(df, vars, group_vars, language_set):
    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars=index_col, value_vars=vars, var_name='time').set_index(index_col)
    df = df.drop(columns = vars).merge(melted_df, how = 'outer', on = index_col)
    # Create a line plot with interaction effect
    ax = sns.pointplot(data=df, x='time', y='value', hue=group_vars)

    min_value = df['value'].min()
    max_value = df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)
    ax.set_yticks(ticks)  
    
    # Enhancing the plot
    plt.legend(title=group_vars)
    ax.grid(False)
    return FigureInStatmanager(xlabel = 'time',
                               ylabel = 'value',
                               title = f'Interaction Plot for {group_vars}',
                               figure = ax,
                               language_set = language_set)

def plot_rm_twogroup(df, vars, group_vars, language_set):
    if len(group_vars) < 2:
        raise ValueError("group_vars should contain at least two variables for interaction plot.")

    # Melt the DataFrame for easier plotting
    index_col = df.index.name
    melted_df = df.reset_index().melt(id_vars=index_col, value_vars=vars, var_name='time').set_index(index_col)
    df = df.drop(columns=vars).merge(melted_df, how='outer', on=index_col)

    # Setting the first two group_vars for pointplot and the rest for FacetGrid
    point_vars = group_vars[:2]
    facet_vars = group_vars[2:] if len(group_vars) > 2 else None

    min_value = df['value'].min()
    max_value = df['value'].max()
    ideal_ticks = 6
    
    ticks = np.linspace(min_value, max_value, ideal_ticks)

    # Creating the FacetGrid
    if facet_vars:
        g = sns.FacetGrid(df, col=facet_vars[0], row=facet_vars[1] if len(facet_vars) > 1 else None, margin_titles=True, palette='Greys')
    else:
        g = sns.FacetGrid(df, col=point_vars[0], margin_titles=True, palette='Greys')

    g.map_dataframe(sns.pointplot, point_vars[0] if facet_vars else 'time', 'value', point_vars[1], errorbar = 'ci', palette='Greys')

    # Adding plot title and labels
    g.set_axis_labels(point_vars[0] if facet_vars else 'time', 'Value')
    g.add_legend()
    
    for ax in g.axes.flatten():
        ax.set_yticks(ticks)
        
    g.fig.subplots_adjust(top=0.8)
    g.fig.suptitle(f'Interaction Plot for {", ".join(group_vars)}', fontsize=16)
    plt.grid(False)
    return FigureInStatmanager(xlabel = None,
                               ylabel = None,
                               title = None,
                               figure = g,
                               language_set = language_set)

def f_nway_rm_plot(df, vars, group_vars, language_set):
    plt.style.use('grayscale')
    
    if isinstance(group_vars, list) and len(group_vars) >= 2:
        result = plot_rm_twogroup (df = df, vars = vars, group_vars = group_vars, language_set = language_set)
        return result
    else:
        result = plot_rm_onegroup (df = df, vars = vars, group_vars = group_vars, language_set = language_set)
        return result        
    
def residual_plot (df, vars, language_set):
    from statsmodels import api
    plt.style.use('grayscale')
    dv = vars[0]
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
    return FigureInStatmanager(xlabel = 'Predicted Values',
                               ylabel = 'Residuals',
                               title = 'Residual plot',
                               figure = ax,
                               language_set=language_set)
    
def roc_curve(df, vars, language_set):
    from statsmodels import api
    
    plt.style.use('grayscale')

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

    ax.text(0.6, 0.2, f'AUC = {auc:.3f}', fontdict = font_properties[language_set])
    ax.grid(False)
    return FigureInStatmanager(xlabel = 'False Positive Rate',
                               ylabel = 'True Positive Rate',
                               title = 'ROC curve',
                               figure = ax,
                               language_set=language_set)