import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import statsmodels.api as sm
import sklearn.metrics as metrics
import scipy

def regression_results(y_true, y_pred):

    # Regression metrics
    explained_variance=metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred)
    mse=metrics.mean_squared_error(y_true, y_pred)
    mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
    r2=metrics.r2_score(y_true, y_pred)

    print('explained_variance: ', round(explained_variance,4))
    print('mean_squared_log_error: ', round(mean_squared_log_error,4))
    print('r2: ', round(r2,4))
    print('MAE: ', round(mean_absolute_error,4))
    print('MSE: ', round(mse,4))
    print('RMSE: ', round(np.sqrt(mse),4))

data = pd.read_csv('./final_data/final_data_3.csv', encoding=None)
data = data.dropna()

# most_shared
data['most_shared'] = data['chosun_article_most_shared']

# 기사 단어 분석
data['positivity'] = data['num_good_words'] / data['num_all_words'] - data['num_bad_words'] / data['num_all_words']
data['emotionality'] =data['num_good_words'] / data['num_all_words'] + data['num_bad_words'] / data['num_all_words']
data['complexity'] = 1.043 * np.sqrt(data['num_long_words'] * 30 / data['num_sentences']) + 3.1291

# 조선 자체 데이터
data['chosun_comments'] = data["chosun_num_comments"]
data['chosun_likes'] = data["chosun_num_likes"]

# 기사 감성 평가
data['good'] = data['final_naver_num_good']
data['warm'] = data['final_naver_num_warm']
data['sad'] = data['final_naver_num_sad']
data['angry'] = data['final_naver_num_angry']
data['want'] = data['final_naver_num_want']

data['cheer'] = data['final_naver_num_cheer']
data['congrats'] = data['final_naver_num_congrats']
data['expect'] = data['final_naver_num_expect']
data['surprise'] = data['final_naver_num_surprise']

# 기사 추천 및 댓글
data['practical_utility'] = data['final_naver_num_recommend']
data['comments'] = data['final_naver_comment_num']

# 위치별 노출 시간
data['Top'] = data['sum_chosun_Top']
data['Headline_Thum02'] = data['sum_chosun_Headline_Thum02']
data['Headline_Thum03'] = data['sum_chosun_Headline_Thum03']
data['Headline_Thum04'] = data['sum_chosun_Headline_Thum04']
data['Headline_Txt'] = data['sum_chosun_Headline_Txt']
data['Headline_Txt02'] = data['sum_chosun_Headline_Txt02']
data['Headline_Txt03'] = data['sum_chosun_Headline_Txt03']
data['Headline_Txt04'] = data['sum_chosun_Headline_Txt04']
data['location_economy'] = data['sum_chosun_economy']
data['location_National_Issue'] = data['sum_chosun_National_Issue']
data['location_editorial'] = data['sum_chosun_editorial']
data['location_rank'] = data['sum_chosun_rank']

# 지면 위치, page
data['paper_A'] = data['paper_location_A']
data['paper_B'] = data['paper_location_B']
data['paper_D'] = data['paper_location_D']
data['online'] = data['paper_location_online']
# online

#page_0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 38, 39

# time of day
data['daytime'] = data['chosun_time_daytime']
# weekday_0, 1, 2, 3, 4, 5, 6

# category
# 'section_opinion', 'section_politics', 'section_social', 'section_economy', '   section_world', 'section_entertain', 'section_domestic', 'section_culture', 'section_life

# intercept
data['intercept'] = 1.0

# 변수 지정

# x_values = ['positivity', 'emotionality', 'complexity',
#           'chosun_comments', 'chosun_likes',
#           'good', 'warm', 'sad', 'angry', 'want', 'cheer', 'congrats', 'expect', 'surprise',
#           'practical_utility', 'comments',
#            'Top', 'Headline_Thum02', 'Headline_Thum03', 'Headline_Thum04', 'Headline_Txt', 'Headline_Txt02',
#            'Headline_Txt03', 'Headline_Txt04', 'location_economy', 'location_National_Issue', 'location_editorial', 'location_rank']
#
# x_dummies =['paper_A', 'paper_B', 'paper_D', 'online',
#           'daytime',
#           'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', #'weekday_6',
#           'section_opinion', 'section_politics', 'section_social', 'section_economy', 'section_world', 'section_entertain', 'section_domestic', 'section_culture', 'section_life']

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
x_values = [ 'chosun_likes','chosun_comments','chosun_time_laps', 'good', 'warm', 'sad', 'angry', 'want']

x_dummies =['daytime', 'paper_A', 'paper_B', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'section_opinion', 'section_politics', 'section_social', 'section_economy', 'section_world', 'section_entertain', 'section_domestic', 'section_culture','intercept'] #'section_life',

y_list = ['most_shared']
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# normalize and load
try:
    try:
        values_not_normalized = data[x_values].replace({',':''},regex=True).apply(pd.to_numeric,1)
    except:
        values_not_normalized = data[x_values]
    std_scaler = StandardScaler()
    fitted = std_scaler.fit(values_not_normalized)
    values_normalized = std_scaler.transform(values_not_normalized)
    values_normalized = pd.DataFrame(values_normalized, columns=data[x_values].columns)

    data_dummies = data[x_dummies]

    # load data
    x = pd.concat([values_normalized,data_dummies],axis=1)
except:
    data_dummies = data[x_dummies]
    x = data_dummies
y = data[y_list]
print(x.head())
print(y.head())


#로지스틱 회귀분석 시행
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
# model = LogisticRegression()
# model.fit(x_train, y_train)
#
# #모델의 정확도 확인
# print('학습용 데이터셋 정확도 : %.2f' % model.score(x_train, y_train))
# print('검증용 데이터셋 정확도 : %.2f' % model.score(x_test, y_test))
#
# y_pred=model.predict(x_test)
# print(classification_report(y_test, y_pred))
#
# print(model.coef_)
# print(regression_results(y_test, y_pred))

# #로지스틱 회귀분석 시행
logit = sm.Logit(y,x)
result = logit.fit()
print()
print('--------------------Result--------------------')
print()
print(result.summary2())
print()
print('--------------------Odds Ratio--------------------')
print()
print(np.exp(result.params))