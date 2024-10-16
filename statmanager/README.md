 
[![PyPI version](https://badge.fury.io/py/statmanager-kr.svg)](https://badge.fury.io/py/statmanager-kr)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ckdckd145/statmanager-kr/blob/main/LICENSE)
[![status](https://joss.theoj.org/papers/d88c1a10e30fbfc39104534970afcd23/status.svg)](https://joss.theoj.org/papers/d88c1a10e30fbfc39104534970afcd23)
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=Pandas&logoColor=white">
<img src="https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=Jupyter&logoColor=white">
<img src="https://img.shields.io/badge/Scipy-8CAAE6?style=flat&logo=Scipy&logoColor=white">


![logo](../doc/logo.png)

### Available Operating Systems

<img src="https://img.shields.io/badge/Windows_10-00adef">
<img src="https://img.shields.io/badge/Windows_11-0078d4">
<img src="https://img.shields.io/badge/Mac_OS-000000">
<img src="https://img.shields.io/badge/Linux-FCC624">

### Availabe Python Versions

<img src="https://img.shields.io/badge/Python_3.10-3776AB">
<img src="https://img.shields.io/badge/Python_3.11-3776AB">
<img src="https://img.shields.io/badge/Python_3.12-3776AB">

<br>

<b>Statmanager-kr</b> is open-source statistical package for researchers, data scientists, psychologist, studends, and anyone who need statistical analysis. <b>Statmanager-kr</b> aims to be a user-friendly statistical package that can be easily used by people who unfamiliar with programming language.

Currently, <b><u>KOREAN</u></b> and <b><u>ENGLISH</u></b> are supported.   


## Documentaion

[Official documentation - Korean](https://cslee145.notion.site/fd776d4f9a4f4c9db2cf1bbe60726971?v=3b2b237555fc4cd3a41a8da337d80c01)   
[Official Documentation - English](https://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4)

## Source Code & Dependency
Source codes are available in the [Github respository](https://github.com/ckdckd145/statmanager-kr)

#### Dependency
* pandas
* statsmodels
* scipy
* numpy
* matplotlib
* seaborn
* XlsxWriter

It is recommended to use the <b>latest versions</b> of these libraries and packages to avoid unexpected errors.

## Contribution Guidelines

Please check the [guidelines](https://www.notion.so/cslee145/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4#96a4e9547ae54a41928ff4114729f6c2) in official documentation.   

Please use [Github Discussion](https://github.com/ckdckd145/statmanager-kr/discussions) to let me know the questions, bugs, suggestions or anything. 


# Quick Start

[If you want to start with sample file, click this](https://github.com/ckdckd145/statmanager-kr/blob/main/test.ipynb)
[Read manual in documentation](https://www.notion.so/cslee145/Documentation-74a610c12881402d96dc5d1654f97433?pvs=4#be93db7f4159419fa73eb324d6567793)  | 


### Installation
```python
pip install statmanager-kr
```

### Update
```python
pip install statmanager-kr --upgrade
```

### Import 

```Python
import pandas as pd
from statmanager import Stat_Manager

# use your data file instead of 'testdf.csv'
df = pd.read_csv('testdf.csv', index_col = 'id') 
sm = Stat_Manager(df, language = 'eng')
```

### Independent Samples T-test

```python
sm.progress(method = 'ttest_ind', vars = 'age', group_vars = 'sex').figure()
```

<details markdown="1">
  <summary><b>Output (Click to See)</b></summary>

|  | female | male |
| --- | --- | --- |
| n | 15.00 | 15.00 |
| mean | 27.33 | 28.00 |
| median | 26.00 | 26.00 |
| sd | 4.88 | 6.94 |
| min | 21.00 | 20.00 |
| max | 39.00 | 39.00 |

| dependent variable | t-value | degree of freedom | p-value | 95% CI | Cohen'd |
| --- | --- | --- | --- | --- | --- |
| height | -0.304 | 28 | 0.763 | [-5.153,  3.820] | -0.111 |

![figure](./doc/output_ttest_ind.png)

</details>

### Dependent Samples T-test

```python
sm.progress(method = 'ttest_rel', vars = ['prescore', 'postscore']).figure()
```

<details markdown="1">
  <summary><b>Output (Click to See)</b></summary>

|  | prescore | postscore |
| --- | --- | --- |
| n | … | … |
| mean | 5.13 | 4.23 |
| median | 5.50 | 4.00 |
| sd | 2.85 | 2.91 |
| min | … | … |
| max | … | … |

| variables | t-value | degree of freedom | p-value | 95% CI | Cohen's d |
| --- | --- | --- | --- | --- | --- |
| ['prescore', 'postscore'] | 1.198 | 29 | 0.24 | [-0.636, 2.436] | 0.313 |

![figure](./doc/output_ttest_rel.png)

</details>

### Pearson's Correlation

```python
sm.progress(method = 'pearsonr', vars = ['income', 'prescore', 'age']).figure()
```

<details markdown="1">
  <summary><b>Output (Click to See)</b></summary>

|  | n | Pearson's r | p-value | 95%_confidence_interval |
| --- | --- | --- | --- | --- |
| income & prescore | 30 | -0.103 | 0.588 | [-0.447, 0.267] |
| income & age | 30 | -0.051 | 0.789 | [-0.404, 0.315] |
| prescore & age | 30 | -0.044 | 0.816 | [-0.398, 0.321] |

|  | income | prescore | age |
| --- | --- | --- | --- |
| income | 1.000 | -0.103 | -0.051 |
| prescore | -0.103 | 1.000 | -0.044 |
| age | -0.051 | -0.044 | 1.000 |

![figure](./doc/output_pearsonr.png)

</details>

### One-way ANOVA with Post-hoc test

```python
sm.progress(method = 'f_oneway', vars = 'age', group_vars = 'condition', posthoc = True).figure()
```

<details markdown="1">
  <summary><b>Output (Click to See)</b></summary>

|  | test_group | sham_group | control_group |
| --- | --- | --- | --- |
| n | 10 | 10 | 10 |
| mean | 28.5 | 28.3 | 26.2 |
| median | 27 | 29 | 25.5 |
| sd | 6.57 | 5.56 | 5.88 |
| min | … | … | … |
| max | … | … | … |

|  | sum_sq | df | F | p-value | partial eta  squared |
| --- | --- | --- | --- | --- | --- |
| Intercept | 6864.4 | 1 | 189.469 | 0 | 0.872 |
| C(condition) | 32.467 | 2 | 0.448 | 0.644 | 0.004 |
| Residual | 978.2 | 27 | NaN | NaN | 0.124 |

|Test  Multiple Comparison ttest_ind FWER=0.05 method=bonf alphacSidak=0.02,  alphacBonf=0. | | | | | | 
| --- | --- | --- | --- | --- | --- |

| group1 | group2 | stat | pval | pval_corr | reject |
| --- | --- | --- | --- | --- | --- |
| control_group | sham_group | -0.8204 | 0.4227 | 1 | FALSE |
| control_group | test_group | -0.8246 | 0.4204 | 1 | FALSE |
| sham_group | test_group | -0.0735 | 0.9422 | 1 | FALSE |


![figure](./doc/output_f_oneway.png)

</details>

### One-way Repeated Measure ANOVA with Post-hoc test

```python
sm.progress(method = 'f_oneway_rm', vars = ['prescore','postscore','fupscore'], posthoc = True).figure()
```

<details markdown="1">
  <summary><b>Output (Click to See)</b></summary>

|  | prescore | postscore | fupscore |
| --- | --- | --- | --- |
| n | 30.00 | 30.00 | 30.00 |
| mean | 5.13 | 4.23 | 4.37 |
| median | 5.50 | 4.00 | 4.00 |
| sd | 2.85 | 2.91 | 2.62 |
| min | … | … | … |
| max | … | … | … |

|  | F Value | Num DF | Den DF | p-value | partial etq  squared |
| --- | --- | --- | --- | --- | --- |
| variable | 1.079 | 2 | 58 | 0.347 | 0.02 |


|Test  Multiple Comparison ttest_ind FWER=0.05 method=bonf alphacSidak=0.02,  alphacBonf=0. | | | | | | 
| --- | --- | --- | --- | --- | --- |

| group1 | group2 | stat | pval | pval_corr | reject |
| --- | --- | --- | --- | --- | --- |
| fupscore | postscore | 0.1866 | 0.8526 | 1 | FALSE |
| fupscore | prescore | -1.0849 | 0.2824 | 0.8473 | FALSE |
| postscore | prescore | -1.2106 | 0.231 | 0.6929 | FALSE |


![figure](./doc/output_f_oneway_rm.png)

</details>

<br>

# Related Software

As mentioned earlier, `Statmanager-kr` was developed to provide a user-friendly way to perform statistical analysis methods to test hypotheses, even if the researcher is not familiar with programming languages such as Python. As such, a related software that provides similar user-friendly features is [`Pingouin`](https://pingouin-stats.org/build/html/index.html). 

The main difference is that `Statmanager-kr` was developed with the goal of being a package that can be used by researchers who lack programming knowledge or experience. To this end, rather than implementing independent methods for each analysis, `Statmanager-kr` is designed to allow users to enter code in the same way at any time to perform statistical analysis and obtain the results. Of course, [`Pingouin`](https://pingouin-stats.org/build/html/index.html) also has user-friendly characteristics, but it is a package that is better suited for users with more programming experience and knowledge than `Statmanager-kr`. Due to this difference in characteristics, `Statmanager-kr` does not support the ability to fine-tune analysis methods by adjusting parameters, whereas [`Pingouin`](https://pingouin-stats.org/build/html/index.html) is useful for adjusting parameters to obtain more careful and suitable results. 

In conclusion, `Statmanager-kr` is a good package for researchers who lack programming experience and knowledge and want to see results quickly. [`Pingouin`](https://pingouin-stats.org/build/html/index.html), on the other hand, is a more suitable package for researchers with more programming experience and knowledge, who need a fine-tuned approach to each analysis method. 


## How to cite? 

For inserting the citations, please use this:
* Lee, C., (2024). Statmanager-kr: A User-friendly Statistical Package for Python in Pandas. Journal of Open Source Software, 9(102), 6642, https://doi.org/10.21105/joss.06642


## Development: Changseok Lee

<a href="https://www.github.com/ckdckd145" target="_blanck">
  <img src="https://img.shields.io/badge/Github-github?style=flat&logo=Github&color=black"
</a>
<a href="https://www.linkedin.com/in/cslee0052" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn%20Profile-kakao?style=flat&logo=LinkedIn&logoColor=white&color=black">
</a>
</a>
<a href="mailto:ckdckd145@gmail.com" target="_blank">
    <img src="https://img.shields.io/badge/Gmail-gmail?style=flat&logo=Gmail&logoColor=white&color=black">
</a>
</center>



#
### Copyright (C) 2023 Changseok Lee