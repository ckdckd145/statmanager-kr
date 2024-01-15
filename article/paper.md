---
title: 'Statmanager-kr: A user-friendly statistical package for python in pandas'
tags:
  - Python
  - statistic analysis
  - social science
  - null-hypothesis
  - user-friendly
authors:
  - name: Changseok
    surname: Lee
    orcid: 0000-0002-8825-5571
    equal-contrib: true
    affiliation: 1
affiliations:
 - name: DYPHI Research Institute, DYPHI Inc., Daejeon, Korea
   index: 1
date: 15 January 2024
bibliography: paper.bib
---

# Summary

Python is one of the most popular and easiest programming languages to learn and use. 
However, despite many people using Python for statistical analysis, it is difficult to find a statistical package that can match Python's user-friendly nature within the context of statistical analysis. 
Consequently, people who possess statistical knowledge but lack familiarity with programming languages continue to rely on other costly and inconvenient software. 
The `statmanager-kr` was designed to provide easy-to-use statistical functions, even for people with little knowledge of programming languages. 
Because many people are already familiar with data in table format, such as that in Microsoft Excel, `statmanager-kr` was designed to be compatible with `Pandas.DataFrame`. 
Additionally, statmanager-kr relies on `scipy` and `statsmodels` for accurate and valid statistical analysis. 
The `statmanager-kr` provides functions related to testing for normality and homoscedasticity assumptions, comparing between-group and within-group differences, conducting regression analysis, and data visualization.


# Statement of need

The `statmanager-kr` is an statistical package for Python in `Pandas`. 
This package provides functions that have commonly used for null hypothesis significance testing (NHST), which is of interest to researchers in various research fields [@Moon2020]. The `statmanager-kr` provides statistical analysis functions to test for significant differences between groups in specific data or within groups in data collected multiple times, based on the researcher's or student's hypothesis. 
Before applying a specific analysis, it is possible to check whether the normality assumption or the equivariance assumption is met, depending on the distribution of the data. For example, the Shapiro-Wilk test can be used to assess the assumption of normality. To verify the assumption of equality of variances, either the Levene test or the Fmax test can be utilized. Based on these results, the hypothesis of interest can be tested by conducting an independent samples T-test or Mann-Whitney U test. This function helps researchers determine whether the hypothesis formulated by the researcher is acceptable or not. 

Most statistical software available to date is difficult to use, inconvenient, and comes with a high cost. 
In fact, a previous study reported that one of the difficulties university students face in methodological courses like statistics was the "hands-on" exercises, which involve using software [@Murtonen:2003]. Although the inherent difficulty of statistics may be unavoidable, the low usability of the software can be addressed. 
To achieve this goal, the `statmanager-kr` was designed to enable the application of all analysis with just three lines of codes: 1. reading data as a `Pandas.DataFrame`, 2. creating a `Stat_Manager` object, 3. running `.progress()` method. Therefore, users can use the `statmanager-kr` as long as they learn a minimum of `Pandas` methods to read the data, such as `.read_csv()`, or `.read_excel()`. In addition, it includes additional functions like `.figure()` to visualize results in commonly used ways depending on the analysis method. 

# Features

The `statmanager-kr` was designed to be compatible with the wide range form of `pandas.DataFrame`.
The implementation of analysis methods and purposes in statmanager-en can be summarized as follows.

Objective | Analysis
-- | --
Check the normality assumption | Kolmogorov-Smirnov Test, Shapiro-Wilks Test, Z-Skeweness & Z-Kurtosis Test
Check the homoskedasticity assumption | Levenve Test, Fmax Test
Frequency analysis | Chi-Squared Test, Fisher’s Exact Test
Check the reliability of the scale | Calculating Cronbach’s Alpha
Correlation analysis | Pearson’s r, Spearman’s rho, Kendall’s tau
Comparison between groups | Independent Samples T-test, Yuen’s T-test, Welch’s T-test, Mann-whitney U test, Brunner-Munzel Test, One-way ANOVA, Kruskal Wallis Test, One-way ANCOVA
Comparison within group | Dependent Samples T-test, Wilcoxon-Signed Rank Test, One-way Repeated Measures ANOVA, Friedman Test, Repeated Measures ANCOVA,
Comparison by multiple ways | N-way ANOVA, N-way Mixed Repeated Measures ANOVA
Regression analysis | Linear Regression, Logistic Regression
etc | Bootstrapping percentile method

<br>All analysis method has its own <b>"key"</b> that enables its application in the `.progress()` method. 
The analysis is conducted by providing the "key" for each analysis method to the `method` parameter in the `.progress()`, the variables to be analyzed to `vars` parameter, and the group variables to `group_vars` parameter. 

```python
import pandas as pd
from stamanager import Stat_Manager

df = pd.read_csv(r'../testdata.csv', index_col = 'name')               # 1. Reading the data
sm = Stat_Manager(df)                                                  # 2. Creating object
sm.progress(method = 'ttest_ind', vars = 'weight', group_vars = 'sex') # 3. Running: check the difference in weight by sex
```
<br>Also, if a post-hoc test is required, as in the case of a one-way ANOVA (key of one-way ANOVA is `f_oneway`), it can be conducted by simply providing `True` to the `posthoc` parameter.

```python
#Omit the import syntax

sm = Stat_Manager(df)

# check the differences in income by condition 
sm.progress(method = 'f_oneway', vars = 'income', group_vars = 'condition', posthoc = True) 
```

# Acknowledgements

Author declares no conflicts of interests.

# References