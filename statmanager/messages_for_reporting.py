
LINK_DOC ={
    'kor' : '*****\n↓↓ 상세한 정보는 Documentation link를 확인하세요! ↓↓\nhttps://cslee145.notion.site/statmanager-kr-Documentation-c9d0886f29ea461d9d0f44449a145f8a?pvs=4 \n*****\n',
    'eng' : '*****\n↓↓ Check for the more details in documentation! ↓↓\nhttps://cslee145.notion.site/statmanager-kr-Documentation-c9d0886f29ea461d9d0f44449a145f8a?pvs=4 \n*****\n'
}

keyerror_message_for_languageset = "Language must be choosen between 'kor' and 'eng'. Default set is 'kor'. If you want to set the language to English, enter 'eng'. "

message_for_change_languageset = {
    'kor' : '언어 설정이 한글로 변경되었습니다. ',
    'eng' : 'The Language is set to English. '
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
            
percentage_of_under_five_values_word = {
    'kor' : '기대빈도 5 미만의 cell이 차지하는 비율',
    'eng' : 'Percentage of cells with expected frequency less than 5',
    }

warning_message_for_normality = {
    'kstest' : {
        'kor' : "주의: 표본 수가 30보다 적습니다. 정규성 가정 충족 여부를 확인하기 위해 다른 분석을 고려하십시오. ",
        'eng' : "Warning: The sample size is less than 30. Consider another analysis to check the normality assumption. ",
                },
    'shapiro' : {
        'kor' : "주의: 표본 수가 30보다 많습니다. 정규성 가정 충족 여부를 확인하기 위해 다른 분석을 고려하십시오. ",
        'eng' : "Warning: The sample size is more than 30. Consider another analysis to check the normality assumption. ",
    },
}

conclusion_for_normality_assumption = {
    'kor' : {
        'under' : '결론: 정규성 가정 미충족',
        'up' : '결론: 정규성 가정 충족',
        },
    'eng' : {
        'under' : 'Conclusion: The normality assumption is not met.',
        'up' : 'Conclusion: The normality assumption is met.',
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


NOTATION_FOR_HOWTOUSE = {
    'kor' : '.howtouse()에 분석과 관련해 검색할 키워드를 입력하세요.\n\n예시 1. ANOVA의 적용 방법이 궁금한 경우 sm.howtouse("ANOVA")\n예시 2. 정규성 검정이 궁금한 경우 sm.howtouse("정규성")\n예시 3. 비모수 검정이 궁금한 경우 sm.howtouse("비모수")\n\n데이터 필터링 방법을 확인하고 싶다면 sm.howtouse("selector")를 입력하세요! \n\n아래 표는 statmanager-kr에 구현된 통계분석 방법별로 구현 방법을 요약한 것입니다. ',
    'eng' : 'In .howtouse(), enter the keywords you want to search for the analysis:\n\nExample 1. If you want to know how to apply ANOVA, sm.howtouse("ANOVA")\nExample 2. If you want to know how to test normality, sm.howtouse("normality")\nExample 3. If you want to know how to test nonparametric, sm.howtouse("Non-parametric")\n\nIf you want to know how to filter your data, enter sm.howtouse("selector")! \n\nThe table below summarizes the implementation methods for each statistical analysis method applied to statmanager-kr.'
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
        'kor' :  f"Stat_Manager 객체 생성 완료! (Version {ver})\n\n사용법 설명 메소드: .howtouse()\n분석 메소드: .progress()\nNote: To change the language, provide 'eng' as an argument to the 'language' parameter when creating the Stat_Manager() object. \n\n{doclink}",
        'eng' : f"Stat_Manager object created successfully! (Version {ver})\n\nMethod to check how to use: .howtouse()\nMethod for statistical analysis: .progress()\n\n{doclink}",
            }
    
    return success_message


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

def ttest_rel_and_wilcoxon_result_reporting_two (s, degree_of_freedom, p):
    
    reporting_result_two = {
        'kor' : f'\n검정통계치 = {s:.3f}, df(자유도) = {degree_of_freedom}, p = {p:.3f}\n',
        'eng' : f'\nTest statistic = {s:.3f}, df(degree of freedom) = {degree_of_freedom}, p = {p:.3f}\n',
    }
    
    return reporting_result_two

def f_nway_rm_result_reporting_one (vars, group_vars):
    reporting_result = {
        'kor' : f"종속변수 : {vars} \n독립변인 : {group_vars}\n\n",
        'eng' : f"Dependent variables : {vars} \nIndependent variables : {group_vars}\n\n",
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
        'eng' : f"\Dependent variable: {dv}\Group variable : {group_vars}\Comparision groups : {group_names}\Covariates: {covars}\nDescriptive analysis: ",
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


def compare_btwgroup_result_reporting_one (dv, group_vars, group_names):
    
    reporting_result_one = {
        'kor' : f"변수 : {dv}\n집단변수 : {group_vars}\n비교집단 : {group_names}\n기술통계치: ",
        'eng' : f"Variable : {dv}\nGroup variable : {group_vars}\nComparison group : {group_names}\nDecriptive analysis: ",
        }
    
    return reporting_result_one

def compare_btwgroup_result_reporting_two (s, p):
    
    reporting_result_two = {
        'kor' : f"검정통계치 = {s:.3f}, p = {p:.3f}",
        'eng' : f"Test statistic = {s:.3f}, p = {p:.3f}"
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


def fmax_result_reporting(group_n, group_names, max_variance, min_variance, f_max):
    reporting_result = {
        'kor' : f"\n집단 수 = {group_n}\n집단 구분 : {group_names}\n집단 중 최대 분산 = {max_variance}\n집단 중 최소 분산 = {min_variance}\nF-max statistic = {f_max}\n",
        'eng' : f"\nNo. of groups = {group_n}\nIncluded groups : {group_names}\nMax variance among groups = {max_variance}\nMin variance among groups = {min_variance}\nF-max statistic = {f_max}\n",
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
        'kor' : f"\n변수 = {dv}\n\n왜도 = {skewness}\n왜도의 표준오차 = {skewness_se}\nZ-왜도 = {z_skewness}\n\n첨도 = {kurtosis}\n첨도의 표준오차 = {kurtosis_se}\nZ-첨도 = {z_kurtosis}\n\nn= {n}, Z-왜도 및 Z-첨도의 절단값 (절대값) = {cutoff}",
        'eng' : f"\nvariables = {dv}\n\nskewness = {skewness}\nstandard error of skewness = {skewness_se}\nz-skewness = {z_skewness}\n\nkurtosis = {kurtosis}\nstandard error of kurtosis = {kurtosis_se}\nz-kurtosis = {z_kurtosis}\n\nsample n = {n}, corresponding absolute cutoff score of z-skewenss and z-kurtosis = {cutoff}",
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


def frequency_analysis_result_reporting_two (s, p):
    result = {
        'kor' : f"\n카이제곱 χ² = {s:.3f}, p = {p:.3f}\n분할표: ",
        'eng' : f"\nχ² = {s:.3f}, p = {p:.3f}\nContingency Table: ",
    }
    
    return result


def logistic_regression_result_reporting_one(dv, mapper):
    result = {
        'kor' : f"종속변수: {dv}\n더미코딩됨: {mapper}\n",
        'eng' : f"\nDependent variable: {dv}\nDummy-coded as : {mapper}\n",
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
        'kor' : f"독립변수: {iv}\n",
        'eng' : f"Independent variable: {iv}\n",
    }
    
    return result