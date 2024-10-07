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

Python is one of the most accessible and adaptable programming languages, utilized in various research domains, including statistics. However, few statistical packages inherit these characteristics of Python, leaving researchers unfamiliar with programming languages dependent on other expensive software. To address this gap, `Statmanager-kr` has been developed to provide non-programmers with convenient access to statistical functions. `Statmanager-kr` is designed to be compatible with `Pandas.DataFrame` and enables statistical analyses using a single method with a relatively small number of parameters. With `SciPy` and `statsmodels` ensuring the validity of analyses, `Statmanager-kr` offers functions for hypothesis testing, comparing between-group and within-group differences, regression, correlations, data visualization, and more.

# Statement of need

`Statmanager-kr` is a statistical package for Python in `Pandas`. This package provides methods commonly used for null hypothesis significance testing (NHST), which is of interest to researchers in various fields [@Moon2020]. It is also possible to test for normality or equivariance using the Shapiro-Wilk, Levene, or F<sub>max</sub> tests. 

Most of the statistical software available today is difficult to use, as a previous study reported that one of the challenges students face in statistics courses was "using software" [@Murtonen:2003]. Although there are basic statistical libraries in Python, such as `SciPy` [@Virtanen:2020] and `statsmodels` [@seabold:2010], they are quite complex. While some studies require complex and detailed statistical modeling and analysis, there are also many studies that require only a few hypothesis tests. Therefore, the development of an easy-to-use statistical package would be of great benefit to these researchers. 

To achieve this, `Statmanager-kr` has been designed to run analyses with only three lines of code: 1) read data as a `Pandas.DataFrame`, 2) create a `Stat_Manager` object, 3) execute the `progress()` method. Therefore, users can use `Statmanager-kr` as long as they know `Pandas` functions to read the data, such as `read_csv()` or `read_excel()`. It also includes functions to visualize the results depending on the analysis method.


# Related Work

Recent advances in the field of statistics have been achieved through the emergence of user-friendly packages, such as `Pingouin` [@vallat2018]. Pingouin is an easy-to-use statistics package that offers a wide range of analytical functions. Like `Pingouin`, `Statmanager-kr` is similar in that it aims to be a user-friendly statistics package. 

However, `Statmanager-kr` and `Pingouin` differ in their target users. Since `Statmanager-kr` is designed for researchers with limited programming experience, it focuses on keeping the workflow short and concise; therefore, `Statmanager-kr` was designed to allow users to apply analyses and obtain results by always running a single method, `progress()`, in a similar way. On the other hand, `Pingouin` was developed for users with a relatively high level of programming knowledge and experience; therefore, in terms of workflow, `Pingouin` offers more comprehensive and fine-tunable analysis methods and provides more detailed analysis results. Also, `Statmanager-kr` only works with `Pandas.DataFrame`, while `Pingouin` has the advantage of being compatible with a wider range of date types. 

Another difference is related to post-hoc analysis and visualiztion. When running an analysis that allows post-hoc analysis, such as ANOVA, in `Statmanager-kr`, post-hoc analysis like Bonferroni correction can be performed by adding the `posthoc` parameter to the `progress` method. It is possible to visualize the results by using `figure()` as a method chaining in `Statmanager-kr`. Although `Pingouin` does not provide the functions to directly visualize the results of an analysis, it does support the generation of graphs that are very useful from a statistical perspective, such as paired plots, shift plots, and circular mean plots. `Pingoin` also has the advantage of supporting a wider range of post-hoc analyses, although it requires a separate method.  

In conclusion, depending on the researcher's programming experience and the purpose of the study, `Statmanager-kr` and `Pingouin` can be used differently. Researchers who are familiar with programming may be better suited to use `Pingouin` as it supports more analysis methods and customization. On the other hand, `Statmanager-kr` is designed to be used by researchers who are not familiar with programming and coding, but want to get quick results.

# Features

Learn more about the features in the *[official documentation](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0)*. The instructions for running each analysis are also described in *[the manual section of the official documentation](https://cslee145.notion.site/Statmanager-kr-Official-Documentation-74a610c12881402d96dc5d1654f97433#be93db7f4159419fa73eb324d6567793)*. *[Korean versions of the official documenation](https://cslee145.notion.site/fd776d4f9a4f4c9db2cf1bbe60726971?v=3b2b237555fc4cd3a41a8da337d80c01)* are also available.



# Acknowledgements

Author declares no conflicts of interests.

# References