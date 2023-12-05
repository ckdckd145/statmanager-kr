import os
import pandas as pd

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