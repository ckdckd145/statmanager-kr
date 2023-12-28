
LINK_DOC ={
    'kor' : '*****\n↓↓ 상세한 정보는 Documentation link를 확인하세요! ↓↓\nhttps://cslee145.notion.site/fd776d4f9a4f4c9db2cf1bbe60726971?v=3b2b237555fc4cd3a41a8da337d80c01&pvs=4 \n*****\n',
    'eng' : '*****\n↓↓ Check for the more details in documentation! ↓↓\nhttps://cslee145.notion.site/60cbfcbc90614fe990e02ab8340630cc?v=4991650ae5ce4427a215d1043802f5c0&pvs=4 \n*****\n'
}


TRIM_REFERENCE = "Reference:\n[1] Guo, J. H., & Luh, W. M. (2009). Optimum sample size allocation to minimize cost or maximize power for the two‐sample trimmed mean test. British Journal of Mathematical and Statistical Psychology, 62(2), 283-298.\n[2] Yuen, K. K. (1974). The two-sample trimmed t for unequal population variances. Biometrika, 61(1), 165-170.\n\n"

index_column_for_figure_for_howtouse = { 
    'kor' : '구분',
    'eng' : 'Index',
}

keyerror_message_for_languageset = "Language must be choosen between 'kor' and 'eng'. Default set is 'kor'. If you want to set the language to English, enter 'eng'. "

message_for_change_languageset = {
    'kor' : '*****\n언어 설정이 한글로 변경되었습니다.\n*****\n',
    'eng' : '*****\nThe Language is set to ENGLISH.\n*****\n'
}

keyerror_message_for_bootstrap = {
    'kor' : "부트스트랩핑을 진행하기 위한 리샘플링 횟수가 잘못 입력되었습니다. method 파라미터에 제공된 인자의 형식이 bootstrap2000, bootstrap894 혹은 bootstrap894_df, bootstrap2000_df 등과 일치하는지 확인하십시오. 리샘플링 횟수는 반드시 0보다 큰 양수여야 합니다. ",
    'eng' : "The number of resamples to proceed with bootstrapping was entered incorrectly. Make sure the format of the argument provided in the method parameter matches bootstrap2000, bootstrap894, or bootstrap894_df, bootstrap2000_df, etc. The number of resamples must be a positive number greater than 0.",
}

keyerror_message_for_trim = {
    'kor' : f'Trim ratio가 잘못 입력되었습니다. method 파라미터에 제공된 인자의 형식이 ttest_ind_trim0.2, ttest_ind_trim0.1 등과 일치하는지 확인하십시오. Trim ratio는 반드시 0 초과 0.5 미만의 값이어야 합니다. 자세한 내용은 아래 논문을 참고하십시오. {TRIM_REFERENCE}',
    'eng' : f"The trim ratio to proceed with Yuen's t-test was entered incorrectly. Make sure the format of the argument provided in the method parameter matches ttest_ind_trim0.2, or ttest_ind_trim0.1. The trim ratio shoule be a value ranging from 0 to 0.5. If you want to get more information, see the references. {TRIM_REFERENCE}",
}

valueerror_message_for_bootstrap ={
    'kor' : "부트스트랩핑을 진행하기 위해 제공되는 그룹 변수는 반드시 2분할이어야 합니다. 2분할보다 많은 그룹 변수를 포함하고자 하는 경우, group_names 파라미터를 통해 두 개의 그룹을 특정하십시오. ",
    'eng' : "The group variables provided for bootstrapping must be bipartite. If you want to include group variables with more than two unique categories, please specify two groups using the group_names parameter.",
}

notation_for_bootstrap_when_zero = {
    'kor' : "NOTE : 부트스트랩핑을 진행하기 위한 리샘플링 횟수가 입력되지 않았습니다. 자동으로 1000번의 리샘플링이 진행됩니다.\n\n리샘플링 횟수를 조정하려면 method 파라미터에 제공된 인자의 형식이 bootstrap2000, bootstrap894 혹은 bootstrap894_df, bootstrap2000_df 등과 일치하는지 확인하십시오.\n리샘플링 횟수는 반드시 0보다 큰 양수여야 합니다. \n",
    'eng' : "NOTE : No resampling times was entered to proceed with bootstrapping. 1000 resamplings are automatically performed.\n\nTo adjust the number of resamples, make sure that the format of the argument provided in the method parameter matches bootstrap2000, bootstrap894, or bootstrap894_df, bootstrap2000_df, etc.\nThe number of resamples must be a positive number greater than 0. \n",
}

typeerror_message_for_indexsetting = "데이터프레임에 Index가 설정되어 있지 않습니다. Stat_Manager() 생성시 id를 지정하거나, index가 설정된 df를 인자로 제공하십시오.\nIndex is not set on the dataframe. Specify id when creating Stat_Manager(), or provide a df with index set as an argument."

keyerror_message_for_fisherexact = {
    'kor' : "Fisher's Exact Test는 2 x 2인 경우에만 작동합니다. ",
    'eng' : "Fisher's Exact Test only works if it is 2 x 2 table. ",
    }

warning_message_for_frequency_analysis = {
    'kor' : "Warning: 기대빈도 5미만의 cell이 차지하는 비율이 25% 이상입니다. Fisher's Exact Test 수행을 권고합니다. .progress(method = 'fisher')",
    'eng' : "Warning: The percentage of cells with an expected frequency of less than 5 is greater than 25%. It is recommended to perform a Fisher's Exact Test.. .progress(method = 'fisher')"
    }

keyerror_message_for_cronbach = {
    'kor' : "크론바흐의 알파를 계산하기 위해서는 적어도 두 개 이상의 컬럼이 제공되어야 합니다. ",
    'eng' : "At least two columns must be provided to calculate Cronbach's alpha. ",
}

percentage_of_under_five_values_word = {
    'kor' : '기대빈도 5 미만의 cell이 차지하는 비율',
    'eng' : 'Percentage of cells with expected frequency less than 5',
    }

percentage_df_word = {
    'kor' : '기대빈도 분할표: ',
    'eng' : 'Expected frequency contingency table: ',
}

warning_message_for_normality = {
    'kstest' : {
        'kor' : "주의: 적어도 하나 이상의 경우에서 표본 수가 30보다 적습니다. 정규성 가정 충족 여부를 확인하기 위해 다른 분석을 고려하십시오. ",
        'eng' : "Warning: at least one case, the sample size is less than 30. Consider another analysis to check the normality assumption. ",
                },
    'shapiro' : {
        'kor' : "주의: 적어도 하나 이상의 경우에서 표본 수가 30보다 많습니다. 정규성 가정 충족 여부를 확인하기 위해 다른 분석을 고려하십시오. ",
        'eng' : "Warning: at least one case, the sample size is more than 30. Consider another analysis to check the normality assumption. ",
    },
}

conclusion_for_normality_assumption = {
    'kor' : {
        'under' : '정규성 가정 미충족',
        'up' : '정규성 가정 충족',
        },
    'eng' : {
        'under' : 'The normality assumption is not met.',
        'up' : 'The normality assumption is met.',
        }
}

conclusion_for_homoskedasticity_assumption = {
    'kor': {
        'under' : '결론: 등분산성 가정 미충족',
        'up' : '결론: 등분산성 가정 충족' ,
        },
    'eng': {
        'under' : 'Conclusion : The homoskedasticity assumption is not met',
        'up' : 'Conclusion : The homoskedasticity assumption is met',
        },
}

notation_meesage_for_multinominal = {
    'kor' : "Note: 다항로지스틱회귀(Multinominal Logistic Regression)가 진행됩니다. ",
    'eng' : "Note: Multinominal Logistic Regression is performed "
}

notation_message_for_correlation = {
    'kor' : "Note: 입력된 모든 변수에서 결측값이 없는 데이터만 포함됩니다.\n",
    'eng' : "Note: Missing values are automatically deleted. \n",
}

notation_message_for_cronbach_alpha = {
    'kor' : "Note: 입력된 모든 변수에서 결측값이 없는 데이터만 계산에 포함됩니다. \n",
    'eng' : "Note: Missing values are automatically deleted. \n",
}

NOTATION_FOR_HOWTOUSE = {
    'kor' : '.howtouse()에 분석과 관련해 검색할 키워드를 입력하세요.\n\n예시 1. ANOVA의 적용 방법이 궁금한 경우 sm.howtouse("ANOVA")\n예시 2. 정규성 검정이 궁금한 경우 sm.howtouse("정규성")\n예시 3. 비모수 검정이 궁금한 경우 sm.howtouse("비모수")\n\n데이터 필터링 방법을 확인하고 싶다면 sm.howtouse("selector")를 입력하세요! \n\n아래 표는 statmanager-kr에 구현된 통계분석 방법별로 구현 방법을 요약한 것입니다. \n통계분석 방법 외, 그림이나 그래프를 그리는 기능을 확인하려면 sm.howtouse("fgiure")를 검색하세요! ',
    'eng' : 'In .howtouse(), enter the keywords you want to search for the analysis:\n\nExample 1. If you want to know how to apply ANOVA, sm.howtouse("ANOVA")\nExample 2. If you want to know how to test normality, sm.howtouse("normality")\nExample 3. If you want to know how to test nonparametric, sm.howtouse("Non-parametric")\n\nIf you want to know how to filter your data, enter sm.howtouse("selector")! \n\nThe table below summarizes the implementation methods for each statistical analysis method applied to statmanager-kr. \n Search sm.howtouse("fgiure") for the function to draw pictures and graphs! '
}

NOTATION_FOR_HOWTOUSE_SELECTOR = {
    'kor' : '\n아래 표는 .progress()에서 데이터 필터링에 활용되는 selector 파라미터의 활용 방법을 설명합니다. \n',
    'eng' : '\nThe table below describes how selector parameters are utilized to filter data in .progress(). \n',
}

notation_message_for_calculating_eta_squared  = {
    'kor' : '효과크기: Eta-squared (η2)가 계산됩니다. : ',
    'eng' : 'Effectsize: Eta-squared (η2) is calculated: ',
}


def success_message_for_creating_object (ver, doclink):
    
    success_message = {
        'kor' :  f"Stat_Manager 객체 생성 완료! (Version {ver})\n\n사용법 설명 메소드: .howtouse()\n분석 메소드: .progress()\n언어 세팅 변경 메소드: .set_language()\n데이터프레임 변경 메소드 .change_dataframe()\nNote: To change the language, provide 'eng' as an argument to the 'language' parameter when creating the Stat_Manager() object.\nOr just run .set_language('eng')\n\n{doclink}",
        'eng' : f"Stat_Manager object created successfully! (Version {ver})\n\nMethod to check how to use: .howtouse()\nMethod for statistical analysis: .progress()\nMethod for changing language: .set_language()\nMethod for changing dataframe .change_dataframe()\n\n{doclink}",
            }
    
    return success_message
success_message_for_changing_dataframe = {
    'kor' : f'데이터프레임 변경에 성공했습니다.\n',
    'eng' : f'Dataframe change was successful. \n'
    }

def error_message_for_selector_type (doclink):
    
    error_message = {
        'kor' : f"selector 인자는 반드시 dictionary 형태여야 합니다.\nsm.howtouse('selector') 를 실행해보세요.\n{doclink}",
        'eng' : f"The 'selector' argument must be in the form of a dictionary: try \nsm.howtouse('selector').\n{doclink}",
            }
    
    return error_message

def selector_notification (condition_texts, test):
    
    message = {
        'kor' : f"*****\nNote: 아래 조건에 부합하는 데이터에 한해서만 분석이 진행됩니다.\n{condition_texts}\n*****\n\n{test}",
        'eng' : f"*****\nNote: Only data that meets the following conditions will be analyzed.\n{condition_texts}\n*****\n\n{test}",
            }
    
    return message

def normality_test_result_reporting (dv, n, s, p):
    
    reporting_result = {
        'kor' : f"변수: {dv}\nn = {n}\n검정통계치 = {s:.3f}, p = {p:.3f}\n",
        'eng' : f"Variable : {dv}\nn = {n}\nTest statistics = {s:.3f}, p = {p:.3f}\n"
    }
    
    return reporting_result

def homoskedasticity_test_result_reporting (group_vars, group_names, s, p):
    
    reporting_result = {
        'kor' : f"집단변수 : {group_vars}\n비교집단 : {group_names}\n검정통계치 = {s:.3f}, p = {p:.3f}\n",
        'eng' : f"Group variable : {group_vars}\nComparison groups : {group_names}\nTest statistics = {s:.3f}, p = {p:.3f}\n",
    }
    
    return reporting_result


def friedman_and_f_oneway_rm_result_reporting (vars):
    
    reporting_result = {
        'kor' : f"변수: {vars}, 시점 = {len(vars)}\n변수별 기술통계치: \n",
        'eng' : f"Variables: {vars}, No. of time-point = {len(vars)}\nDescriptive anaylsis by variables: \n",
    }
    
    return reporting_result

def friedman_result_reporting_two(s, p):
    result = {
        'kor' : f"검정 통계치 = {s:.3f}, p = {p:.3f}",
        'eng' : f"Test statistic = {s:.3f}, p = {p:.3f}",   
    }
    
    return result

def ttest_rel_and_wilcoxon_result_reporting_one (vars, n):
    
    reporting_result_one = {
        'kor' : f"변수 : {vars[0]}, {vars[1]}\nn = {n}\n기술통계치: \n",
        'eng' : f"Variables : {vars[0]}, {vars[1]}\nn = {n}\nDescriptive analysis: \n",
    }
    
    return reporting_result_one

def ttest_rel_result_reporting_two (s, degree_of_freedom, p, ci, d):
    
    reporting_result_two = {
        'kor' : f"\n검정통계치 = {s:.3f}, df(자유도) = {degree_of_freedom}, p = {p:.3f}\n95% 신뢰구간 = [{ci.low:.3f}, {ci.high:.3f}]\nCohen's d = {d:.3f}",
        'eng' : f"\nTest statistic = {s:.3f}, df(degree of freedom) = {degree_of_freedom}, p = {p:.3f}\n95% Confidence interval = [{ci.low:.3f}, {ci.high:.3f}]\nCohen's d = {d:.3f}",
    }
    
    return reporting_result_two

def wilcoxon_result_reporting_two (s, z, p, e):
    
    reporting_result_two = {
        'kor' : f'\n검정통계치 = {s:.3f}, z = {z:.3f}, p = {p:.3f}\n랭크-비즈 상관계수(Rank-biserial correlation) = {e:.3f}',
        'eng' : f'\nTest statistic = {s:.3f}, z = {z:.3f}, p = {p:.3f}\nRank-biserial correlation = {e:.3f}',
    }
    
    return reporting_result_two

def f_nway_rm_result_reporting_one (vars, group_vars):
    reporting_result = {
        'kor' : f"반복측정 변인 : {vars} (time) \n집단변인 : {group_vars}\n\n",
        'eng' : f"Repeated measures factor : {vars} (time) \nGroup factors : {group_vars}\n\n",
    }
    return reporting_result



def f_nway_result_reporting_one (dv, group_vars):
    
    reporting_result = {
        'kor' : f"종속변수 : {dv} \n독립변인 : {group_vars}\n\n",
        'eng' : f"Dependent variables : {dv} \nIndependent variables : {group_vars}\n\n",
    }
    
    return reporting_result

def f_nway_result_reporting_two (dv, n): # also applied in f_nway_rm
    reporting_result = {
        'kor' : f"기술통계치: {n}에 따른 {dv}",
        'eng' : f"Descripitive analysis: {dv} by {n}",
    }
    
    return reporting_result

def f_nway_result_reporting_three (dv): # also applied in f_nway_rm
    reporting_result = {
        'kor' : f"기술통계치: 상호작용에 따른 {dv}",
        'eng' : f"Descripitive analysis: {dv} by Interaction",
    }
    
    return reporting_result

def f_nway_result_reporting_four (testname): # also applied in f_nway_rm
    result = {
        'kor' : f"{testname} 통계치:\n",
        'eng' : f"{testname} Statistics:\n",
    }
    
    return result


def posthoc_message_for_main_effect (n):
    
    posthoc_messages = {
        'kor' : f"\n{n}의 주효과에 대한 사후 검정",
        'eng' : f"\nPosthoc test for main effect of {n}",
    }
    
    return posthoc_messages

posthoc_message_for_interaction = {
    "kor" : "상호작용에 대한 사후검정",
    "eng" : "Posthoc test for interaction effect",
    }

ancova_model_result_reporting = {
    'kor' : 'OLS 모형 결과: ',
    'eng' : 'OLS Model Result: ',
}

ancova_statistic_result_reporting = {
    'kor' : '\nANCOVA 통계치: ',
    'eng' : '\nANCOVA statistics: ',
}

ancova_coef_result_reporting = {
    'kor' : '비교쌍-회귀계수 결과표: ',
    'eng' : 'Pair-Coef Result Table: ',
}

def ancova_coef_interpreting_message (covars):
    
    coef_interpreting_message = {
        'kor' : f"Note: pair의 회귀계수(coef)가 p < .05 수준에서 유의한 경우 공변량({covars})을 통제하였음에도 집단 간 차이가 유의함을 의미합니다.\n회귀계수(coef)는 조정된 평균 값의 차이를 반영합니다. ",
        'eng' : f"Note: If the regression coefficient (coef) of a pair is significant at the p < .05 level, it means that the difference between groups is significant despite controlling for covariates ({covars}).\nThe regression coefficient (coef) reflects the difference in EMMeans. "
    }
    
    return coef_interpreting_message


warning_message_for_ancova_posthoc = {
    'kor' : "*****\nWarning: 추정 주변 평균(EMMeans)이 아닌, 현재 데이터 세트의 평균 값을 토대로 posthoc이 진행됩니다. 공변량의 영향력이 고려되지 않았으므로, 해석에 주의하십시오.\nPair-Coef Result Table을 참고하여 집단 간 공변량을 고려하였을 때의 평균차를 확인하시기 바랍니다.\n*****",
    'eng' : "*****\nWarning: The post hoc results are based on the mean value of the current dataset, not EMMeans. Be careful with interpretation, as the influence of covariates is not taken into account.\nRefer to the Pair-Coef Result Table to see the difference in means when calculating the effects of covariates are taken into account.\n*****"
}


def oneway_ancova_result_reporting (dv, group_vars, group_names, covars):
    
    reporting_result = {
        'kor' : f"\n종속변수: {dv}\n집단변수 : {group_vars}\n비교집단 : {group_names}\n공변량: {covars}\n기술통계치: ",
        'eng' : f"\nDependent variable: {dv}\nGroup variable : {group_vars}\nComparision groups : {group_names}\nCovariates: {covars}\nDescriptive analysis: ",
    }
    
    return reporting_result


def rm_ancova_result_reporting (repeated_vars, covars):
    
    reporting_result = {
        'kor' : f"변수: {repeated_vars}, 시점 = {len(repeated_vars)}\n공변량: {covars}\n기술통계치: ",
        'eng' : f"Variables: {repeated_vars}, No. of time-point = {len(repeated_vars)}\nCovariate: {covars}\nDescriptive analysis: ",
    }

    return reporting_result

def nway_ancova_result_reporting (dv, group_vars, covars):
    
    reporting_result = {
        'kor' : f"\n종속변수 : {dv} \n독립변인: {group_vars}\n공변량: {covars}\n기술통계치 : \n",
        'eng' : f"Dependent variables : {dv} \Independent variables : {group_vars}\Covariates: {covars}\nDescriptive analysis : \n",
    } 
    
    return reporting_result

def notation_for_trim_ttest(trim):
    result ={
        'kor' : f"Note: 백분율을 기준으로 상위 및 하위 {(trim * 100):.2f}% 데이터를 자르고 분석이 진행됩니다.\n",
        'eng' : f"Note: The analysis will trim the top and bottom {(trim * 100):.2f}% data based on percentage.\n",
    }

    return result

notation_for_not_trim = {
    'kor' : '\nWarning: 제공된 trim ratio를 적용하였을 때 잘리는 데이터가 없습니다.\n기존 데이터 세트에 대한 독립표본 t검정이 적용됩니다.\n',
    'eng' : '\nWarning: No data is truncated when the provided trim ratio is applied.\nAn independent sample t-test on the existing data set is conducted.\n'
}

def compare_btwgroup_result_reporting_one (dv, group_vars, group_names):
    
    reporting_result_one = {
        'kor' : f"변수 : {dv}\n집단변수 : {group_vars}\n비교집단 : {group_names}\n기술통계치: ",
        'eng' : f"Variable : {dv}\nGroup variable : {group_vars}\nComparison group : {group_names}\nDecriptive analysis: ",
        }
    
    return reporting_result_one

def ttest_ind_result_reporting_two (s, p, dof, ci, d):
    reporting_result_two = {
        'kor' : f"검정통계치 = {s:.3f}, 자유도(degree of freedom) = {dof},  p = {p:.3f}\n95% 신뢰구간 = [{ci.low:.3f}, {ci.high:.3f}]\nCohen's d = {d:.3f}",
        'eng' : f"Test statistic = {s:.3f}, degree of freedom = {dof}, p = {p:.3f}\n95% Confidence interval = [{ci.low:.3f}, {ci.high:.3f}]\nCohen's d = {d:.3f}"
    }
    
    return reporting_result_two    

def brunner_result_reporting_two(s, p):
    
    reporting_result_two = {
        'kor' : f"검정통계치 = {s:.3f}, p = {p:.3f}",
        'eng' : f"Test statistic = {s:.3f}, p = {p:.3f}"
    }
    
    return reporting_result_two


def kruskal_result_reporting_two(s, p, dof):
    
    reporting_result_two = {
        'kor' : f"H = {s:.3f}, 자유도 = {dof}, p = {p:.3f}",
        'eng' : f"H = {s:.3f}, degree of freedom = {dof}, p = {p:.3f}"
    }
    
    return reporting_result_two

def compare_btwgroup_result_reporting_two (s, p, z, e):
    
    reporting_result_two = {
        'kor' : f"검정통계치 = {s:.3f}, p = {p:.3f}\nz-statistic = {z:.3f}\n랭크-비즈 상관계수(Rank-biserial correlation) = {e:.3f}",
        'eng' : f"Test statistic = {s:.3f}, p = {p:.3f}\nz-statistic = {z:.3f}\nRank-biserial correlation = {e:.3f}"
    }
    
    return reporting_result_two

def f_oneway_df_reporting(degree_of_freedom_between_group, degree_of_freedom):
    
    result = {
        'kor' : f"집단 간 자유도 = {degree_of_freedom_between_group}, 집단 내 자유도 = {degree_of_freedom}",
        'eng' : f"Degree of freedom (between groups) = {degree_of_freedom_between_group}, Degree of freedom (within groups) = {degree_of_freedom}",
    }
    
    return result

notation_message_for_returning_bootstrap_df = {
    'kor' : "\nbootstrap된 DataFrame이 반환되었습니다.\n특정 변수에 선언한 후 활용하세요.\n",
    'eng' : "\nA bootstrapped DataFrame was returned.\nDeclare it in a specific variable and utilize it."
}

notation_for_trim_ratio_when_zero = {
    'kor' : f"trim ratio가 입력되지 않아, 기본 값인 0.2로 분석이 진행됩니다.\ntrim ratio는 0 ~ 0.5 사이의 수치가 권고됩니다.\n자세한 내용은 아래 레퍼런스를 참고하십시오.\n\n{TRIM_REFERENCE}",
    'eng' : f"The trim ratio wasn't entered, so the analysis proceeds with set the trim ratio as 0.2.\nThe trim ratio is recommended to be set ranging from 0 to 0.5\nSee the reference below for more information.\n\n{TRIM_REFERENCE}",
}

valueerror_message_for_trim_ratio = {
    'kor' : f'Trim ratio는 0 초과, 0.5 미만의 값으로 설정되어야 합니다.자세한 내용은 아래 레퍼런스를 참고하십시오.{TRIM_REFERENCE}',
    'eng' : f'The trim ratio sholdbe set to a value greater than 0 and less than 0.5.\n\nSee the reference below for more information.{TRIM_REFERENCE}',
}


def fmax_result_reporting(dv, group_vars, group_n, group_names, max_variance, min_variance, f_max):
    reporting_result = {
        'kor' : f"변수: {dv}\n집단 변수: {group_vars}\n집단 수 = {group_n}\n집단 구분 : {group_names}\n\n집단 중 최대 분산 = {max_variance:.3f}\n집단 중 최소 분산 = {min_variance:.3f}\nF-max statistic = {f_max:.3f}\n",
        'eng' : f"Variable: {dv}\nGroup variable : {group_vars}\nNo. of groups = {group_n}\nIncluded groups : {group_names}\n\nMax variance among groups = {max_variance:.3f}\nMin variance among groups = {min_variance:.3f}\nF-max statistic = {f_max:.3f}\n",
    }
    return reporting_result


def percentile_method_result_reporting(a_var, confidence_level, a_lower_bound, a_upper_bound, b_var, b_lower_bound, b_upper_bound):
    reporting_result_for_percentile_method = {
        'kor' : f"{a_var} 의 {confidence_level * 100:.0f}% 신뢰구간 = [{a_lower_bound:.3f}, {a_upper_bound:.3f}]\n{b_var} 의 {confidence_level * 100:.0f}% 신뢰구간 = [{b_lower_bound:.3f}, {b_upper_bound:.3f}]\n",
        'eng' : f"{confidence_level * 100:.0f}% confidence interval of {a_var} = [{a_lower_bound:.3f}, {a_upper_bound:.3f}]\n{confidence_level * 100:.0f}% confidence interval of {b_var} = [{b_lower_bound:.3f}, {b_upper_bound:.3f}]\n",
    }
    
    return reporting_result_for_percentile_method


conclusion_for_percentile_method = {
    'kor' : {
        'under': "두 분포의 신뢰구간이 중복되지 않습니다. \n두 분포 간 차이가 유의합니다.",
        'up' : "두 분포의 신뢰구간이 중복됩니다. \n두 분포 간 차이가 유의하지 않습니다."
        },
    'eng' : {
        'under' : "The confidence intervals for the two distributions do not overlap. Therefore, the difference between the two distributions is significant.",
        'up' : "The confidence intervals for the two distributions overlap. Therefore, the difference between the two distributions is not significant.",
        }
}

grade_for_cohen_d = {
    'kor' : {
        'under_2' : '해석 불가능',
        'under_5' : '작은 효과크기',
        'under_8' : '중간 효과크기',
        'upper_8' : '큰 효과크기',
        },
    'eng' : {
        'under_2' :  '',
        'under_5' : '',
        'under_8' : '',
        'upper_8' : '',
        },
}


def z_normal_result_reporting (dv, skewness, skewness_se, z_skewness, kurtosis, kurtosis_se, z_kurtosis, n, cutoff):
    
    reporting_result = {
        'kor' : f"\n변수 = {dv}\n\n왜도 = {skewness:.3f}\n왜도의 표준오차 = {skewness_se:.3f}\nZ-왜도 = {z_skewness:.3f}\n\n첨도 = {kurtosis:.3f}\n첨도의 표준오차 = {kurtosis_se:.3f}\nZ-첨도 = {z_kurtosis:.3f}\n\nn= {n}, Z-왜도 및 Z-첨도의 절단값 (절대값) = {cutoff:.3f}",
        'eng' : f"\nvariables = {dv}\n\nskewness = {skewness:.3f}\nstandard error of skewness = {skewness_se:.3f}\nz-skewness = {z_skewness:.3f}\n\nkurtosis = {kurtosis:.3f}\nstandard error of kurtosis = {kurtosis_se:.3f}\nz-kurtosis = {z_kurtosis:.3f}\n\nsample n = {n}, corresponding absolute cutoff score of z-skewenss and z-kurtosis = {cutoff:.3f}",
    }
    
    return reporting_result

reference_of_z_normal = "\nReferences:\n[1] Ghasemi, A., & Zahediasl, S. (2012). Normality tests for statistical analysis: a guide for non-statisticians. International journal of endocrinology and metabolism, 10(2), 486. \n[2] Moon, S. (2019). Statistics for the Social Sciences: Moving Toward an Integrated Approach. Cognella Academic Publishing."

reference_of_fmax = "\nReference:\n[1] Fidell, L. S., & Tabachnick, B. G. (2003). Preparatory data analysis. Handbook of psychology: Research methods in psychology, 2, 115-141.\n"


def frequency_analysis_result_reporting_one (vars):
    
    result = {
        'kor' : f"변수 : {vars[0]}, {vars[1]}",
        'eng' : f"Variables : {vars[0]}, {vars[1]}",
    }
    
    return result


def frequency_analysis_result_reporting_two (s, p, dof):
    result = {
        'kor' : f"\n카이제곱 χ² = {s:.3f}, p = {p:.3f}, 자유도 = {dof}\n분할표: ",
        'eng' : f"\nχ² = {s:.3f}, p = {p:.3f}, 자유도 = {dof}\nContingency Table: ",
    }
    
    return result

def frequency_analysis_result_reporting_two_fisher (s, p):
    result ={ 
        'kor' : f"\n검정 통계치 = {s:.3f}, p = {p:.3f}\n분할표: ",
        'eng' : f"\nTest Statistic = {s:.3f}, p = {p:.3f}\nContingency Table: ",
    }
    
    return result


def logistic_regression_result_reporting_one(dv):
    result = {
        'kor' : f"종속변수: {dv}\n",
        'eng' : f"\nDependent variable: {dv}\n",
    }
    
    return result
    
def linear_regression_result_reporting_one (dv):
    result = {
        'kor' : f"\n종속변수: {dv}",
        'eng' : f"\nDependent variable: {dv}",
    }
    
    return result

def regression_result_reporting_ivs (iv):
    result = {
        'kor' : f"독립변수: {iv}\nNote: 범주형 독립변수는 자동으로 더미코딩됩니다. ",
        'eng' : f"Independent variable: {iv}\nNote: Categorical independent variables are automatically dummy-coded. ",
    }
    
    return result

warning_message_for_negative_cronbach_alpha = {
    'kor' : 'Warning: 크론바흐의 알파가 음수입니다.\n이러한 결과는 일반적이지 않으며, 포함된 항목 간 공분산이 음수이거나, 부적 상관관계를 이루고 있음을 반영하는 것일 수 있습니다.\n계산에 포함된 항목에 대해 전반적으로 재검토할 것을 권고합니다. ',
    'eng' : "Warning: Cronbach's alpha is negative.\nThis result is not typical and may reflect negative covariance between the included items, or that they are corrleated in negative ways.\nA general reexamination of the items included in the calculation should be recommended.",
}

def cronbach_alpha_result_reporting(n, test_items, cronbach):
    number_of_test_items = len(test_items)
    test_items = ", ".join(test_items)
    
    result = {
        'kor' : f"n = {n}\n포함된 항목: {test_items} ({number_of_test_items})\n\n크론바흐의 알파 = {cronbach:.3f}\n",
        'eng' : f"n = {n}\nIncluded items: {test_items} ({number_of_test_items})\n\nCronbach's alpha = {cronbach:.3f}\n",
    }
    
    return result