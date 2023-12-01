# STATMANAGER KR

# STATUS : NOW ON WORK (TEMPORARY)
Open-source statistical package for Python based on the Pandas.    
Especially for researchers, data scientists, psychologist, students, and anyone who interested in conducting hypothesis testing. The statmanager-kr aims to organize packages that are "convenient to use", "uncompliated to use", and "convenient to see results".   
Currently, Korean and English are supported. 


Python 오픈소스 통계 패키지입니다.   
Pandas를 사용하며, 가설 검증에 대해 관심을 갖는 연구원, 데이터분석가, 심리학자, 학생 등을 위합니다. statmanager-kr은 사용하기 쉽고, 사용이 복잡하지 않으며, 결과를 확인하기에 편리한 패키지 구성을 목표로 개발됩니다.  
현재 지원하는 언어 세팅은 한글과 영어입니다. 


## Documentaion
https://cslee145.notion.site/statmanager-kr-Manual-c277749fe94b4e08a836236b409642b3?pvs=4

## Current Ver 1.7.2 : 
Please see documentation for the update history.    
업데이트 내역은 정식 문서에서 확인하시기 바랍니다. 


#
* Available functions | 현재 사용 가능한 분석
    1. Normality assumption | 정규성 가정
        * Kolmogorov-Sminrnov Test
        * Shapiro-Wilks Test
        * Z-Skewness & Z-Kurtosis Test   
    2. Homoskedasticity assumption | 등분산성 가정
        * Levene Test
        * Fmax Test
    3. Frequency analysis  | 빈도분석
        * Chi-squared Test
        * Fisher's Exact Test (temporary)
    4. Correlation analysis | 상관분석
        * Pearson's r
        * Spearman's rho
        * Kendall's tau
    5. Comparison (2) | 차이비교 (2)
        * Parametric | 모수검정법
            * Independent Samples T-Test
            * Dependent Samples T-Test
        * Non-parametric | 비모수검정법 | 비모수검정법
            * Mann-Whitney U Test 
            * Wilcoxon-Signed Ranksum Test 
            * Brunner-Munzel Test 
        * Bootstrap
            * Bootstrap percentile method 
            * Bootstrap resampling
    6. Comparison (3) | 차이비교 (3)
        * Parametric | 모수검정법
            * One-way ANOVA
            * One-way Repeated Measures ANOVA 
            * N-way ANOVA 
            * N-way Repeated Measures ANOVA 
            * One-way ANCOVA
            * Repeated Measures ANCOVA
            * N-way ANCOVA (temporary)
        * Non-parametric | 비모수검정법
            * Kruskal Wallis Test
            * Friedman Test 
        * Post-hoc | 사후검증 
            * Bonferroni correction 
            * Tukey HSD 
    * Regression
        * Linear Regression
        * Multiple linear regression
        * Logistic Regression
        * Multinomial Logistic Regression


#### INSTALLATION
* pandas
* statsmodels
* scipy
* numpy
* matplotlib
* seaborn

#### Recommendation
Using "Jupyter Notebook" is strongly RECOMMENDED (Of course, statmanager-kr works just as well in a Python environment)   
"주피터 노트북(Jupyter Notebook)" 사용을 강력하게 권고합니다. 물론, Python 환경에서도 statmanager-kr은 문제없이 작동합니다.  

#### Installing statmanager-kr
    pip install statmanager-kr

#### Updating statmanager-kr
    pip install statmanager-kr --upgrade




# Development

* Contributor   
    * Changseok Lee   
      * Email: ckdckd145@gmail.com   
      * Linkedin: www.linkedin.com/in/cslee0052   
      * Github : https://github.com/ckdckd145