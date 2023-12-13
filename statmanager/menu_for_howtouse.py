import os
import pandas as pd

from .messages_for_reporting import *
from .making_figure import *

from .normality_functions import *
from .frequency_functions import *
from .homoskedasticity_functions import *
from .reliability_functions import *
from .bootstrap_functions import *
from .correlation_functions import *
from .regression_functions import *
from .within_group_functions import *
from .between_group_functions import *
from .ways_anova_functions import *
from .ancova_functions import *

from .posthoc_functions import *
from .effectsize_functions import *


current_filepath = os.path.abspath(__file__)
current_directory = os.path.dirname(current_filepath)

menu_for_howtouse_eng_path = os.path.join(current_directory, 'menu_for_howtouse_eng.csv')
menu_for_howtouse_kor_path = os.path.join(current_directory, 'menu_for_howtouse_kor.csv')
selector_for_howtouse_eng_path = os.path.join(current_directory, 'selector_for_howtouse_eng.csv')
selector_for_howtouse_kor_path = os.path.join(current_directory, 'selector_for_howtouse_kor.csv')
figure_for_howtouse_eng_path = os.path.join(current_directory, 'figure_for_howtouse_eng.csv')
figure_for_howtouse_kor_path = os.path.join(current_directory, 'figure_for_howtouse_kor.csv')

menu_for_howtouse_eng = pd.read_csv(menu_for_howtouse_eng_path)
menu_for_howtouse_kor = pd.read_csv(menu_for_howtouse_kor_path)

selector_for_howtouse_kor = pd.read_csv(selector_for_howtouse_kor_path, index_col='python 식')
selector_for_howtouse_eng = pd.read_csv(selector_for_howtouse_eng_path, index_col='python operator')

figure_for_howtouse_eng = pd.read_csv(figure_for_howtouse_eng_path)
figure_for_howtouse_kor = pd.read_csv(figure_for_howtouse_kor_path)


menu = {
    'kstest' : {
        'name' : 'Kolmogorov-Smirnov Test',
        'type' : 'normality',
        'testfunc' : kstest, #normality_fuctions
    },
    'shapiro' : {
        'name' : 'Shapiro-Wilks Test',
        'type' : 'normality',
        'testfunc' : shapiro,
    },
    'levene' : {
        'name' : 'Levene Test',
        'type' : 'homoskedasticity',
        'testfunc' : levene,
    },
    'ttest_ind' : {
        'name' : 'Indenpendent Samples T-test',
        'type' : 'between_group',
        'testfunc' : ttest_ind,
    },
    'ttest_rel' : {
        'name' : 'Dependent Samples T-test',
        'type' : 'within_group',
        'testfunc' : ttest_rel,
    },
    'mannwhitneyu' : {
        'name' : 'Mann-Whitney U Test (Wilcoxon Rank Sum Test)',
        'type' : 'between_group',
        'testfunc' : mannwhitneyu,
    },
    'brunner' :{
        'name' : 'Brunner-Munzel Test',
        'type' : 'between_group',
        'testfunc' : brunner,
    },        
    'wilcoxon' : {
        'name' : 'Wilcoxon-Signed Rank Test',
        'type' : 'within_group',
        'testfunc' : wilcoxon,    
    },
    'f_oneway' : {
        'name' : 'One-way ANOVA',
        'type' : 'between_group',
        'testfunc' : f_oneway,
    },
    'kruskal' : {
        'name' : 'Kruskal-Wallis Test',
        'type' : 'between_group',
        'testfunc' : kruskal,
    },
    'chi2_contingency' : {
        'name' : 'Chi-Squared Test',
        'type' : 'frequency_analysis',
        'testfunc' : chi2,
        },
    'fisher' : {
        'name' : "Fisher's Exact Test",
        'type' : 'frequency_analysis',
        'testfunc' : fisher,
    },
    'z_normal' : {
        'name' : 'z-skeweness & z-kurtosis test',
        'type' : 'normality',
        'testfunc' : z_normal,
        },
    'fmax' : {
        'name' : 'F-max Test',
        'type' : 'homoskedasticity',
        'testfunc' : fmax,
        },
    'pearsonr' : {
        'name' : "Correlation analysis: Pearson's r (Pearson correlation coefficient)",
        'type' : 'correlation',
        'testfunc' : pearson,
    },
    'spearmanr' : {
        'name' : "Correlation analysis: Spearman's rho (Spearman's rank correlation coefficient)",
        'type' : 'correlation',
        'testfunc' : spearman,
    },
    'kendallt' : {
        'name' : "Correlation analysis: Kendall's tau (Kendall's tau correlation coefficient)",
        'type' : 'correlation',
        'testfunc' : kendall,  
    },
    'friedman' : {
        'name' : 'Friedman Test',
        'type' : 'within_group',
        'testfunc' : friedman,
    },
    'f_oneway_rm' : {
        'name' : 'One-way Repeated Measures ANOVA',
        'type' : 'within_group',
        'testfunc' : rm_anova,
    },
    'bootstrap' : {
        'name' : 'Bootstrap percentile method: Resampling No. =',
        'type' : 'bootstrap',
        'testfunc' : percentile_method,
    },
    'linearr' : {
        'name' : 'Linear Regression',
        'type' : 'regression',
        'testfunc' : linear,
    },
    'logisticr' : {
        'name' : 'Logistic Regression',
        'type' : 'regression',
        'testfunc' : logistic,
    },
    'f_nway' : {
        'name' : "-way ANOVA",
        'type' : 'anova_nways',
        'testfunc' : f_nway,
    },
    'f_nway_rm' : {
        'name' : "-way Mixed Repeated Measures ANOVA",
        'type' : 'anova_nways',
        'testfunc' : f_nway_rm,
    },
    'oneway_ancova' : {
        'name' : 'One-way ANCOVA',
        'type' : 'compare_ancova',
        'testfunc' : oneway_ancova,
    },
    'rm_ancova' : {
        'name' : 'Repeated-Measures ANCOVA',
        'type' : 'compare_ancova',
        'testfunc' : rm_ancova,
    },
    'cronbach' : {
        'name' : "Calculating Cronbach's Alpha",
        'type' : 'reliability',
        'testfunc' : cronbach,
    },}


figure_functions = {
    'pp_plot' : {
        'name' : "Making p-p plot",
        'type' : 'making_figure',
        'testfunc' : pp_plot,
        },
    'qq_plot' : {
        'name' : "Making q-q plot",
        'type' : 'making_figure',
        'testfunc' : qq_plot,
        },
    'hist' : {
        'name' : "Making histogram",
        'type' : 'making_figure',
        'testfunc' : hist,
        },
    'hist_cumulative' : {
        'name' : "Making cumulative histogram",
        'type' : 'making_figure',
        'testfunc' : hist_cumulative,
        },
    'boxplot_variance' : {
        'name' : "Making boxplot for checking variance among groups",
        'type' : 'making_figure',
        'testfunc' : boxplot_homoskedasticity,
        },
    "point_within" : {
        'name' : "Making pointplot for repeated variables",
        'type' : 'making_figure',
        'testfunc' : point_within,
        },
    "bar_between" : {
        'name' : "Making bar graph among groups",
        'type' : 'making_figure',
        'testfunc' : bar_between,
        },
    }