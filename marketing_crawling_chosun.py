# -*- coding: utf-8 -*-
import pandas as pd
import requests, bs4
import re
import time
from selenium import webdriver
from datetime import datetime
import json
from konlpy.tag import Okt
import numpy as np
import threading


def crawl_chosun():

    crawl_time = datetime.today().strftime("%Y%m%d_%H-%M")

    #---------------------------------------------------------------------------------------
    okt=Okt()
    #---------------------------------------------------------------------------------------
    class KnuSL():
        def data_list(wordname):
            with open('./data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
                data = json.load(f)
            result = ['None', 'None']
            for i in range(0, len(data)):
                if data[i]['word'] == wordname:
                    result.pop()
                    result.pop()
                    result.append(data[i]['word_root'])
                    result.append(data[i]['polarity'])
            r_word = result[0]
            s_word = result[1]
            return r_word, s_word
    ksl = KnuSL
    # ---------------------------------------------------------------------------------------


    # by BeautifulSoup
    article_urls = []

    article_types = [] #news

    article_location_1 = []
    article_location_2 = []

    article_onclick_others = []

    # by selenium

    article_most_shared = []

    article_titles = []
    article_reporter = []

    article_time_daytime = []
    article_time_access = []
    article_time_uploaded = []
    article_time_reviesed = []
    article_time_laps = []

    article_sections = [] #정치 일반

    article_num_facebook_share = []
    article_num_comments = []
    article_num_likes = []

    article_contents = []
    article_num_good_words = []
    article_num_bad_words = []
    article_num_neutral_words = []
    article_num_none_words = []

    article_num_all_words = []
    article_num_long_words = []
    # ---------------------------------------------------------------------------------------

    open_main_url = ('https://www.chosun.com/')

    driver0 = webdriver.Chrome('./chromedriver')
    driver0.set_window_position(10,10)
    driver0.set_window_size(900,800)

    driver0.get(open_main_url)
    time.sleep(10)

    p = re.compile('^https://news.chosun.com/')

    for element in driver0.find_elements_by_css_selector('#tab-2 > div > dl > dt > a'):
        try:
            if p.match(element.get_attribute('href')):

                article_most_shared.append(1)

                article_urls.append(element.get_attribute('href'))
                #print(element.get_attribute('href'))
                article_location_1.append(element.get_attribute('onclick').replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[2])
                article_location_2.append(element.get_attribute('onclick').replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[4])

                article_types.append(element.get_attribute('onclick').replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[3])
                article_onclick_others.append(element.get_attribute('onclick').replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[0:2])
                print('Success: Most shared')
        except:
            print('Error: Most shared')
    driver0.close()

    main_resp = requests.get(open_main_url)
    #print(main_resp.encoding)
    main_resp.encoding='utf-8'
    #main_resp.encoding=None
    main_bs = bs4.BeautifulSoup(main_resp.text, 'html.parser')
    elements = main_bs.find_all('dl', 'news_item')

    number_of_article = 0
    for element in elements:
        try:
            if p.match(element.find('a')['href']):
                article_most_shared.append(0)
                article_urls.append(element.find('a')['href'])
                article_location_1.append(element.find('a')['onclick'].replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[2])
                article_location_2.append(element.find('a')['onclick'].replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[4])

                article_types.append(element.find('a')['onclick'].replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[3])
                article_onclick_others.append(element.find('a')['onclick'].replace("ga(\'","").replace(');',"").replace("\'","").replace(" ","").split(',')[0:2])
                number_of_article +=1
        except:
            pass

    # print(article_urls)
    print('--------------------------')
    print('Number of article: {}'.format(number_of_article))
    print('--------------------------')

    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_position(10,10)
    driver.set_window_size(900,800)

    progress = 0
    for article_url in article_urls:
        try:
            driver.get(article_url)
            time.sleep(10)

            words = okt.morphs(driver.find_element_by_css_selector('#news_body_id > div.par').text)
            article_contents.append(driver.find_element_by_css_selector('#news_body_id > div.par').text.split())
            tmp_good=0
            tmp_bad=0
            tmp_neutral=0
            tmp_none=0
            tmp_long_word=0

            for word in words:
                if len(word)>=3:
                    tmp_long_word += 1

                if ksl.data_list(word)[1] == 'None':
                    tmp_none += 1
                else:
                    sentiment = int(ksl.data_list(word)[1])
                    if sentiment > 0:
                        tmp_good += 1
                    elif sentiment < 0:
                        tmp_bad += 1
                    else:
                        tmp_neutral += 1

            article_num_good_words.append(tmp_good)
            article_num_bad_words.append(tmp_bad)
            article_num_neutral_words.append(tmp_neutral)
            article_num_none_words.append(tmp_none)

            article_num_all_words.append(len(words))
            article_num_long_words.append(tmp_long_word)
            #-----------------------------------------------------------------

            article_titles.append(driver.find_element_by_css_selector('#news_title_text_id').text)
            try:
                article_reporter.append(driver.find_element_by_css_selector('#csContent > header > div > div > ul > li > a').text)
            except:
                article_reporter.append(np.NaN)

            tmp=0
            for a in driver.find_element_by_css_selector('#news_body_id > div.news_date').text.replace('입력 ','').replace('수정 ','').split(' | '):
                tmp_article_time_access = datetime.now()
                if tmp==0:
                    tmp_article_time_uploaded = datetime.strptime(a, '%Y.%m.%d %H:%M')
                    tmp_article_time_reviesed = np.NaN
                    tmp_article_time_laps = (tmp_article_time_access - tmp_article_time_uploaded).total_seconds()/60
                else:
                    tmp_article_time_reviesed = datetime.strptime(a, '%Y.%m.%d %H:%M')
                tmp += 1

            article_time_access.append(tmp_article_time_access.strftime('%Y-%m-%d %H:%M'))
            article_time_uploaded.append(tmp_article_time_uploaded.strftime('%Y-%m-%d %H:%M'))
            if 5<tmp_article_time_uploaded.hour<18:
                article_time_daytime.append(1)
            else:
                article_time_daytime.append(0)

            if pd.isna(tmp_article_time_reviesed):
                article_time_reviesed.append(tmp_article_time_reviesed)
            else:
                article_time_reviesed.append(tmp_article_time_reviesed.strftime('%Y-%m-%d %H:%M'))
            article_time_laps.append(tmp_article_time_laps)

            article_sections.append(driver.find_element_by_css_selector('#news_cat_trig_id').text)

            article_num_facebook_share.append(driver.find_element_by_css_selector('#news_left_aside_id > ul > li:nth-child(3) > a > span').get_attribute('innerHTML'))
            article_num_comments.append(driver.find_element_by_css_selector('#BBSCNT').get_attribute('innerHTML'))
            article_num_likes.append(driver.find_element_by_css_selector('#CSCNT').get_attribute('innerHTML'))
            progress += 1
            print('Success, {}/{}'.format(progress,len(article_urls)))
        except:
            progress += 1
            print('Fail, {}/{}'.format(progress,len(article_urls)))

    driver.close()

    df_chosun = pd.DataFrame()

    df_chosun['url'] = pd.Series(article_urls)
    df_chosun['title'] = pd.Series(article_titles)

    df_chosun['time_access'] = pd.Series(article_time_access)
    df_chosun['time_uploaded'] = pd.Series(article_time_uploaded)
    df_chosun['time_reviesed'] = pd.Series(article_time_reviesed)
    df_chosun['time_laps'] = pd.Series(article_time_laps)
    df_chosun['time_daytime'] = pd.Series(article_time_daytime)


    df_chosun['types'] = pd.Series(article_types)
    df_chosun['sections'] = pd.Series(article_sections)
    df_chosun['location_1'] = pd.Series(article_location_1)
    df_chosun['location_2'] = pd.Series(article_location_2)

    df_chosun['article_most_shared'] = pd.Series(article_most_shared)

    df_chosun['num_facebook_share'] = pd.Series(article_num_facebook_share)
    df_chosun['num_comments'] = pd.Series(article_num_comments)
    df_chosun['num_likes'] = pd.Series(article_num_likes)

    df_chosun['num_good_words'] = pd.Series(article_num_good_words)
    df_chosun['num_bad_words'] = pd.Series(article_num_bad_words)
    df_chosun['num_neutral_words'] = pd.Series(article_num_neutral_words)
    df_chosun['num_none_words'] = pd.Series(article_num_none_words)

    df_chosun['num_long_words'] = pd.Series(article_num_long_words)
    df_chosun['num_all_words'] = pd.Series(article_num_all_words)

    df_chosun['reporter'] = pd.Series(article_reporter)
    df_chosun['contents'] = pd.Series(article_contents)

    df_chosun['onclick_others'] = pd.Series(article_onclick_others)

    #print(df_chosun.head())

    df_chosun.to_csv('./result/chosun_{}.csv'.format(crawl_time),encoding='utf-8-sig')
    print('--------------------  Crawled at: {}  --------------------'.format(crawl_time))

def crawling():
    threading.Timer(7200, crawling).start()
    crawl_chosun()

crawling()