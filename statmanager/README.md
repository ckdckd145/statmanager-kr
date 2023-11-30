# STAT MANAGER KR
## 개발자 정보
이창석 (Changseok Lee)
이메일: ckdckd145@gmail.com   
Linkedin: www.linkedin.com/in/cslee0052   
버그가 발생하거나 제안사항은 언제든지 이메일로 연락주시면 감사하겠습니다.   

## Documentaion Link
https://cslee145.notion.site/statmanager-kr-Manual-c277749fe94b4e08a836236b409642b3?pvs=4

## Ver 1.7.2 : Update 내용은 위 Documentation Link를 확인하십시오. 

#
지원하는 통계방법은 지속적으로 업데이트할 예정입니다.   
* 현재까지 지원하는 통계종류
    * 정규성 검정
        * Kolmogorov-Sminrnov Test
        * Shapiro-Wilks Test
        * Z-Skewness & Z-Kurtosis Test
    * 등분산성 검정
        * Levene Test
        * Fmax Test
    * 빈도분석
        * 카이제곱검정 (Chi-square Test)
        * Fisher's Exact Test (1.4.0 ver 추가)(임시 구현)
    * 상관분석
        * Pearson's r
        * Spearman's rho
        * Kendall's tau-h (1.4.0 ver 추가)
    * 차이비교 (2)
        * 모수검정법
            * 독립표본 T-Test (Independent Samples T-Test)
            * 대응표본 T-Test (Dependent Samples T-Test)
        * 비모수검정법
            * Mann-Whitney U Test (2집단 간 차이를 검정하는 비모수 기법)
            * Wilcoxon-Signed Ranksum Test (집단 내 두 변수의 차이를 검정하는 비모수 기법)
            * Brunner-Munzel Test (2집단 간 차이를 검정하는 또 다른 비모수 기법)
        * Bootstrap
            * Bootstrap percentile method (1.1.0 ver 추가)
            * Bootstrap resampling : Bootstrap된 데이터프레임을 반환합니다. (1.2.0 ver 추가)
    * 차이비교 (3)
        * 모수검정법
            * One-way ANOVA
            * One-way Repeated Measures ANOVA (1.1.0 ver 추가)
            * N-way ANOVA (1.3.0 ver 추가)
            * N-way Repeated Measures ANOVA (1.3.0 ver 추가)
            * One-way ANCOVA
            * Repeated Measures ANCOVA
            * N-way ANCOVA
            * N-way Repeated Measures ANCOVA 
        * 비모수검정법
            * Kruskal Wallis Test
            * Friedman Test (1.1.0 ver 추가)
        * 사후검증 (Post-hoc)
            * Bonferroni correction 
            * Tukey HSD (1.2.0 ver 추가)
    * 회귀
        * 선형회귀 (Linear Regression)  (1.2.0 ver 추가)
        * 로지스틱회귀 (Logistic Regression) (1.2.0 ver 추가)
        * 다항로지스틱회귀 (Multinomial Logistic Regression) (1.2.0 ver 추가)


### 개발 목적
해당 프로그램은 python에서 pandas를 활용하여 데이터 분석을 주로 하시는 분들을 위한 패키지입니다.SPSS와 같이 손쉬운 통계를 제공하는 툴이 시중에 출시되어 있지만, 가격이 비싸다는 단점이 있습니다. pandas를 주로 사용하시는 분들이 사용하기에 번거롭다는 것도 단점입니다.   
하지만, 그렇다고 scipy나 statmodels와 같은 패키지를 사용하기에는 요구되는 코딩 방식과 데이터프레임의 방식이 상이한 부분이 많아 어려움이 큽니다. 이를 상쇄하고자 하나의 통일된 방식의 코딩을 통해 통계분석을 진행할 수 있게끔 패키지를 만들고 있습니다.   

#
### 활용
#### 필요 라이브러리
* pandas
* statsmodels
* scipy
* numpy
* matplotlib
* seaborn

#### 안내
jupyter notebook 사용을 강력하게 권고합니다. (.py 환경에서도 문제없이 동작합니다.)

#### 설치
    pip install statmanager-kr

#### Import
    from statmanager import Stat_Manager

#### 객체 생성
    sm = Stat_Manager(df, id)
* df = pandas.DataFrame
* id = index column