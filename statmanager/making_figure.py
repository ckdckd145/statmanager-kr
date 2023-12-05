import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

font_properties = {
    'kor' : {'family' : 'Gulim', 'color': 'Black', 'weight': 'normal', 'size': 16},
    'eng' : {'family': 'Times New Roman', 'color': 'Black', 'weight': 'normal', 'size': 16},
}


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
        
        self.ax.set_xlabel(self.xlabel, fontdict = self.font_properties)
        
        self.ax.set_ylabel(self.ylabel, fontdict = self.font_properties)
        
        self.ax.set_title(self.title, fontdict = self.font_properties)
        
        if self.xticks is not None:
            self.ax.set_xticks(self.xticks, fontdict = self.font_properties)
        
        if self.yticks is not None:
            self.ax.set_yticks(self.yticks, fontdict = self.font_properties)


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

def hist():
    pass

def hist_cumulative():
    pass

