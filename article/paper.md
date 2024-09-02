---
title: 'Statmanager-kr: A User-friendly Statistical Package for Python in Pandas'
tags:
  - Python
  - statistical analysis
  - social science
  - null-hypothesis
  - user-friendly
authors:
  - name: Changseok Lee
    orcid: 0000-0002-8825-5571
    affiliation: 1
affiliations:
 - name: DYPHI Research Institute, DYPHI Inc., Daejeon, Republic of Korea
   index: 1
date: 15 January 2024
bibliography: paper.bib
---

# Summary

Python is one of the most accessible and adaptable programming languages, utilized in various research domains, including statistics. However, few statistical packages inherit these characteristics of Python, leaving researchers unfamiliar with programming languages dependent on other expensive software. To address this gap, `Statmanager-kr` has been developed to provide non-programmers with convenient access to statistical functions. `Statmanager-kr` is designed to be compatible with `Pandas.DataFrame` and enables statistical analyses using a single method with a relatively small number of parameters. With `Scipy` and `Statsmodels` ensuring the validity of analyses, `Statmanager-kr` offers functions for hypothesis testing, comparing between-group and within-group differences, regression, correlations, data visualization, and more.

# Statement of need

`Statmanager-kr` is a statistical package for Python in `Pandas`. This package provides methods commonly used for null hypothesis significance testing (NHST), which is of interest to researchers in various fields [@Moon2020]. It is also possible to test for normality or equivariance using the Shapiro-Wilk, Levene, or F<sub>max</sub> tests. 

Most of the statistical software available today is difficult to use, as a previous study reported that one of the challenges students face in statistics courses was "using software" [@Murtonen:2003]. Although there are basic statistical libraries in Python, such as Scipy [@seabold:2010] and Statsmodels [@Virtanen:2020], they are quite complex. While some studies require complex and detailed statistical modeling and analysis, there are also many studies that require only a few hypothesis tests. Therefore, the development of an easy-to-use statistical package would be of great benefit to these researchers. 

To achieve this, `Statmanager-kr` has been designed to run analyses with only three lines of code: 1. read data as a `Pandas.DataFrame`, 2. create a `Stat_Manager` object, 3. execute the `.progress()` method. Therefore, users can use `Statmanager-kr` as long as they know `Pandas` methods to read the data, such as `.read_csv()` or `.read_excel()`. It also includes functions to visualize the results depending on the analysis method.


# Related Work

Recent advances in the field of statistics have been achieved through the emergence of user-friendly packages, such as `Pingouin` [@vallat2018]. Pingouin is an easy-to-use statistics package that offers a wide range of analytical functions. Like `Pingouin`, `Statmanager-kr` is similar in that it aims to be a user-friendly statistics package. 

However, `Statmanager-kr` and `Pingouin` differ in their target users. Since `Statmanager-kr` is designed for researchers with limited programming experience, it focuses on keeping the workflow short and concise; therefore, `Statmanager-kr` was designed to allow users to apply analyses and obtain results by always running a single method, `.progress()`, in a similar way. On the other hand, `Pingouin` was developed for users with a relatively high level of programming knowledge and experience; therefore, in terms of workflow, `Pingouin` offers more comprehensive and fine-tunable analysis methods and provides more detailed analysis results. Also, `Statmanager-kr` only works with `Pandas.DataFrame`, while `Pingouin` has the advantage of being compatible with a wider range of datasets. 

Another difference is related to visualization and post-hoc. `Statmanager-kr` performs post-hoc by adding the parameter `posthoc` to the `.progress()`. In addition, it is possible to visualize the results by using `.figure()` as a method chaining. Although `Pingouin` does not provide the ability to directly visualize the results of an analysis, it does support the generation of graphs that are very useful from a statistical perspective, such as paired plots, shift plots, and circular mean plots. In addition, Pingouin has the advantage of supporting a wider range of post-hoc tests. 

In conclusion, depending on the researcher's programming experience and the purpose of the study, `Statmanager-kr` and `Pingouin` can be used differently. Researchers who are familiar with programming may be better suited to use `Pingouin` as it supports more analysis methods and customization. On the other hand, `Statmanager-kr` is designed to be used by researchers who are not familiar with programming and coding, but want to get quick results.

# Features

`Statmanager-kr` was designed to be compatible with the wide range form of `Pandas.DataFrame`.  

## User-friendly Features

### Setting the Language

It is possible to change the language by adjusting the `language` parameter when creating an object of the Stat_Manager class. The supported languages are Korean ("kor") and English ("eng"), and the default is Korean.

```python
sm = Stat_Manager(df, language = 'eng')
```

### Other Methods

Users can search for a specific usage by calling the `.howtouse()` method. It can also change the language with `.set_language()`, or change the dataframe by running `.change_dataframe()`.  


## Statistical Test

The implementation of analysis in `Statmanager-kr` can be summarized as follows.

| Objective                             | Analysis                                                                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Check the normality assumption        | Kolmogorov-Smirnov Test, Shapiro-Wilks Test, Z-Skewness & Z-Kurtosis Test                                                                              |
| Check the homoskedasticity assumption | Levene's Test, F<sub>max</sub> Test                                                                                                                                 |
| Frequency analysis                    | Chi-Squared Test, Fisher’s Exact Test                                                                                                                   |
| Check the reliability of the scale    | Calculating Cronbach’s Alpha                                                                                                                            |
| Correlation analysis                  | Pearson’s r, Spearman’s rho, Kendall’s tau                                                                                                              |
| Comparison between groups             | Independent Samples T-test, Yuen’s T-test, Welch’s T-test, Mann-whitney U test, Brunner-Munzel Test, One-way ANOVA, Kruskal Wallis Test, One-way ANCOVA |
| Comparison within group               | Dependent Samples T-test, Wilcoxon-Signed Rank Test, One-way Repeated Measures ANOVA, Friedman Test, Repeated Measures ANCOVA,                          |
| Comparison by multiple ways           | N-way ANOVA, N-way Mixed Repeated Measures ANOVA                                                                                                        |
| Regression analysis                   | Linear Regression, Logistic Regression                                                                                                                  |
| etc                                   | Bootstrapping percentile method                                                                                                                         |

<br>Each analysis method has its own <b>"key"</b> that allows it to be used in the `.progress()` method. The analysis is performed by passing the key for each analysis method to the `method` parameter in the `.progress()` method, the variables to be analyzed to the `vars` parameter, and the group variables to the `group_vars` parameter.

```python
import pandas as pd
from statmanager import Stat_Manager

# 1. Reading the data
df = pd.read_csv(r'testdata.csv', index_col = 'name')

# 2. Creating object of Stat_Manager class
sm = Stat_Manager(df)

# 3. Running: check the difference in weight by sex
sm.progress(method = 'ttest_ind', vars = 'weight', group_vars = 'sex') 
```


<br>Also, if a post-hoc test is required, as in the case of a one-way ANOVA (key of one-way ANOVA is `f_oneway`), it can be conducted by simply providing `True` to the `posthoc` parameter.

```python
sm.progress(method = 'f_oneway', vars = 'income', group_vars = 'condition', posthoc = True) 
```

### Keys and Related Informations
The method-specific information needed to use the `.progress()` method can be found by using the `.howtouse()` method. The detailed information is summarized in the table below:

| Key                | Analysis                            | Required Parameters  | Optional Parameters         |
| ------------------ | ----------------------------------- | -------------------- | --------------------------- |
| `kstest`           | Kolmogorov-Smirnov Test             | `vars`               | `group_vars`                |
| `shapiro`          | Shapiro-Wilks Test                  | `vars`               | `group_vars`                |
| `z_normal`         | Z-Skewness & Z-Kurtosis test        | `vars`               | `group_vars`                |
| `levene`           | Levene Test                         | `vars`, `group_vars` |
| `fmax`             | F<sub>max</sub> Test                | `vars`, `group_vars` |
| `chi2_contingency` | Chi-squared Test                    | `vars`               |
| `fisher`           | Fisher's Exact Test                 | `vars`               |
| `pearsonr`         | Pearson's r                         | `vars`               |
| `spearmanr`        | Spearman's rho                      | `vars`               |
| `kendallt`         | Kendall's tau                       | `vars`               |
| `ttest_ind`        | Independent Samples T-test          | `vars`, `group_vars` |
| `ttest_rel`        | Dependent Samples T-test            | `vars`               |
| `ttest_ind_trim`   | Yuen's Two Samples T-test           | `vars`, `group_vars` |
| `ttest_ind_welch`  | Welch's Two Samples T-test          | `vars`, `group_vars` |
| `mannwhitneyu`     | Mann-Whitney U Test                 | `vars`, `group_vars` |
| `brunner`          | Brunner-Munzel Test                 | `vars`, `group_vars` |
| `wilcoxon`         | Wilcoxon-Signed Rank Test           | `vars`               |
| `bootstrap`        | Boostrap Percentile Method          | `vars`               | `group_vars`                |
| `f_oneway`         | One-way ANOVA                       | `vars`, `group_vars` | `posthoc`, `posthoc_method` |
| `f_oneway_rm`      | One-way Repeated Measures ANOVA     | `vars`               | `posthoc`, `posthoc_method` |
| `kruskal`          | Kruskal-Wallis Test                 | `vars`, `group_vars` | `posthoc`, `posthoc_method` |
| `friedman`         | Friedman Test                       | `vars`               | `posthoc`, `posthoc_method` |
| `f_nway`           | N-way ANOVA                         | `vars`, `group_vars` | `posthoc`, `posthoc_method` |
| `f_nway_rm`        | N-way Mixed Repeated Measures ANOVA | `vars`, `group_vars` | `posthoc`, `posthoc_method` |
| `linearr`          | Linear Regression                   | `vars`               |
| `hier_linearr`     | Hierarchical Linear Regression      | `vars`               |
| `logisticr`        | Logistic Regression                 | `vars`               |
| `oneway_ancova`    | One-way ANCOVA                      | `vars`, `group_vars` |
| `rm_ancova`        | One-way Repeated Measures ANCOVA    | `vars`               |
| `cronbach`         | Calculating Cronbach's Alpha        | `vars`               |

Also `Statmanager-kr` provides two post-hoc methods. It can be run by providing the key of the `posthoc_method` parameter as follows:

| Key of `posthoc_method` | Method                |
| ----------------------- | --------------------- |
| `bonf`                  | Bonferroni Correction |
| `tukey`                 | Tukey HSD             |


## Visualization 

A figure is automatically generated for the results of the analysis when a `.figure()` is run as a chain method against a `.progress()`. 

```python
# Running: check the difference in weight by sex with figure
sm.progress(method = 'ttest_ind', vars = 'weight', group_vars = 'sex').figure()
```

# Acknowledgements

Author declares no conflicts of interests.

# References