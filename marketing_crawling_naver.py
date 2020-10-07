import requests, bs4
import time
from urllib.parse import quote
from datetime import datetime
from selenium import webdriver
import pandas as pd
import numpy as np
import threading
import re

def crawl_naver():

    crawl_time = datetime.today().strftime("%Y%m%d_%H-%M")

    article_urls = []

    article_titles = []
    article_chosun_url = []

    article_summary = []

    article_time_daytime = []
    article_time_access = []
    article_time_uploaded = []
    article_time_reviesed = []
    article_time_laps = []

    article_paper_page = []
    article_paper_location = []

    num_good = []
    num_warm = []
    num_sad = []
    num_angry = []
    num_want = []
    num_cheer = []
    num_congrats = []
    num_expect = []
    num_surprise = []

    num_recommend = []

    comment_num = []
    comment_num_deleted = []
    comment_num_violation = []

    sort_lists = []

    sort_recent = []
    sort_like = []
    sort_ratio = []

    open_main_url = ('https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=023&listType=title&date={}'.format(datetime.today().strftime("%Y%m%d")))
    main_resp = requests.get(open_main_url)
    main_bs = bs4.BeautifulSoup(main_resp.text, 'html.parser')
    page_urls = main_bs.find_all('div', 'paging','a')
    print(page_urls)
    last_page = int(str(page_urls).split('</a>')[-2][-1])

    for page in range(1,last_page+1):
        print('page {} crawling'.format(page))

        open_page_url = ('https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=023&listType=title&date={}&page={}'.format(datetime.today().strftime("%Y%m%d"),page))
        page_resp = requests.get(open_page_url)
        page_bs = bs4.BeautifulSoup(page_resp.text, 'html.parser')
        url_groups = page_bs.find_all('ul', 'type02')
        for url_group in url_groups:
            urls = url_group.find_all('li')
            for url in urls:
                article_urls.append(url.find('a')['href'])
        time.sleep(5)

    driver = webdriver.Chrome('./chromedriver')
    driver.set_window_position(920,10)
    driver.set_window_size(900,800)

    progress = 0
    for url in article_urls:
        try:
            driver.get(url)
            time.sleep(7)
            try:
                article_titles.append(driver.find_element_by_css_selector('#articleTitle').text)
            except:
                try:
                    article_titles.append(driver.find_element_by_css_selector('#content > div > div.content > div > div.news_headline > h4').text)
                except:
                    article_titles.append('No_title')

            try:
                article_chosun_url.append(driver.find_element_by_css_selector(
                    '#main_content > div.article_header > div.article_info > div > a').get_attribute('href'))
            except:
                try:
                    article_chosun_url.append(
                        driver.find_element_by_css_selector('#content > div.end_ct > div > div.article_info > a').get_attribute('href'))
                except:
                    article_chosun_url.append(np.NaN)

            try:
                driver.find_element_by_css_selector('#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_right > div.media_end_head_autosummary._auto_summary_wrapper > a').click()
                time.sleep(3)
                article_summary.append(driver.find_element_by_css_selector(
                    '#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_right > div.media_end_head_autosummary._auto_summary_wrapper > div > div.media_end_head_autosummary_layer_body > ._contents_body').text)
            except:
                article_summary.append(np.NaN)


            p = re.compile('^2020')

            tmp = 0
            tmp_article_time_access = datetime.now()
            tmp_article_time_uploaded = np.NaN
            tmp_article_time_reviesed = np.NaN
            tmp_article_time_laps = np.NaN

            for a in driver.find_elements_by_css_selector('#main_content > div.article_header > div.article_info > div > span'):
                if p.match(a.text):
                    if tmp==0:
                        tmp_article_time_uploaded = datetime.strptime(a.text.replace('오전', 'AM').replace('오후', 'PM'), '%Y.%m.%d. %p %I:%M')
                        tmp_article_time_reviesed = np.NaN
                        tmp_article_time_laps = (tmp_article_time_access - tmp_article_time_uploaded).total_seconds()/60

                    else:
                        tmp_article_time_reviesed = datetime.strptime(a.text.replace('오전', 'AM').replace('오후', 'PM'), '%Y.%m.%d. %p %I:%M')
                    tmp += 1
                else:
                    pass

            if pd.isna(tmp_article_time_access):
                article_time_access.append(tmp_article_time_access)
            else:
                article_time_access.append(tmp_article_time_access.strftime('%Y-%m-%d %H:%M'))

            if pd.isna(tmp_article_time_uploaded):
                article_time_uploaded.append(tmp_article_time_uploaded)
            else:
                article_time_uploaded.append(tmp_article_time_uploaded.strftime('%Y-%m-%d %H:%M'))

            if pd.isna(tmp_article_time_uploaded):
                article_time_daytime.append(np.NaN)
            else:
                if 5 < tmp_article_time_uploaded.hour < 18:
                    article_time_daytime.append(1)
                else:
                    article_time_daytime.append(0)


            if pd.isna(tmp_article_time_reviesed):
                article_time_reviesed.append(tmp_article_time_reviesed)
            else:
                article_time_reviesed.append(tmp_article_time_reviesed.strftime('%Y-%m-%d %H:%M'))
            article_time_laps.append(tmp_article_time_laps)

            try:
                article_paper_location.append(driver.find_element_by_css_selector(
                    '#main_content > div.article_header > div.article_info > div > span.sponsor_newspaper').text.replace('신문',''))
            except:
                article_paper_location.append('online')
            try:
                num_good.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.good > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                num_warm.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.warm > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                num_sad.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.sad > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                num_angry.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.angry > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                num_want.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.want > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                num_cheer.append(0)
                num_congrats.append(0)
                num_expect.append(0)
                num_surprise.append(0)
            except:
                try:
                    num_good.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.good > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                    num_warm.append(0)
                    num_sad.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.sad > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                    num_angry.append(0)
                    num_want.append(0)
                    num_cheer.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.cheer > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                    num_congrats.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.congrats > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                    num_expect.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.expect > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                    num_surprise.append(driver.find_element_by_css_selector('div._reactionModule.u_likeit > ul > li.u_likeit_list.surprise > a > span.u_likeit_list_count._count').get_attribute('innerHTML'))
                except:
                    num_good.append(0)
                    num_warm.append(0)
                    num_sad.append(0)
                    num_angry.append(0)
                    num_want.append(0)
                    num_cheer.append(0)
                    num_congrats.append(0)
                    num_expect.append(0)
                    num_surprise.append(0)
            try:
                num_recommend.append(driver.find_element_by_css_selector('#toMainContainer > a > em.u_cnt._count').get_attribute('innerHTML'))
            except:
                num_recommend.append(np.NaN)

            try:
                comment_num.append(driver.find_element_by_css_selector('#cbox_module > div.u_cbox_wrap.u_cbox_ko > div.u_cbox_comment_count_wrap > ul > li:nth-child(1) > span').text)
                comment_num_deleted.append(driver.find_element_by_css_selector('#cbox_module > div.u_cbox_wrap.u_cbox_ko > div.u_cbox_comment_count_wrap > ul > li:nth-child(2) > span').text)
                comment_num_violation.append(driver.find_element_by_css_selector('#cbox_module > div.u_cbox_wrap.u_cbox_ko > div.u_cbox_comment_count_wrap > ul > li:nth-child(3) > span').text)

                tmp_sort_lists=[]
                tmp_sort_like = 0
                tmp_sort_recent = 0
                tmp_sort_ratio = 0
                for a in driver.find_elements_by_css_selector('.u_cbox_sort_label'):
                    if a.text == '최신순':
                        tmp_sort_recent += 1
                    elif a.text == '순공감순':
                        tmp_sort_like += 1
                    elif a.text == '공감비율순':
                        tmp_sort_ratio += 1
                    tmp_sort_lists.append(a.text)

                sort_recent.append(tmp_sort_recent)
                sort_like.append(tmp_sort_like)
                sort_ratio.append(tmp_sort_ratio)

                sort_lists.append(tmp_sort_lists)
            except:
                comment_num.append(0)
                comment_num_deleted.append(0)
                comment_num_violation.append(0)

                sort_recent.append(0)
                sort_like.append(0)
                sort_ratio.append(0)

                sort_lists.append(np.NaN)

            progress += 1
            print('Success, {}/{}'.format(progress,len(article_urls)))
        except:
            progress += 1
            print('Fail, {}/{}'.format(progress,len(article_urls)))

    driver.close()

    df_naver = pd.DataFrame()

    df_naver['url'] = pd.Series(article_urls)
    df_naver['chosun_url'] = pd.Series(article_chosun_url)

    df_naver['title'] = pd.Series(article_titles)

    df_naver['time_access'] = pd.Series(article_time_access)
    df_naver['time_uploaded'] = pd.Series(article_time_uploaded)
    df_naver['time_reviesed'] = pd.Series(article_time_reviesed)
    df_naver['time_laps'] = pd.Series(article_time_laps)
    df_naver['time_daytime'] = pd.Series(article_time_daytime)

    df_naver['paper_page'] = pd.Series(article_paper_page)
    df_naver['paper_location'] = pd.Series(article_paper_location)

    df_naver['num_good'] = pd.Series(num_good)
    df_naver['num_warm'] = pd.Series(num_warm)
    df_naver['num_sad'] = pd.Series(num_sad)
    df_naver['num_angry'] = pd.Series(num_angry)
    df_naver['num_want'] = pd.Series(num_want)
    df_naver['num_cheer'] = pd.Series(num_cheer)
    df_naver['num_congrats'] = pd.Series(num_congrats)
    df_naver['num_expect'] = pd.Series(num_expect)
    df_naver['num_surprise'] = pd.Series(num_surprise)

    df_naver['num_recommend'] = pd.Series(num_recommend)

    df_naver['comment_num'] = pd.Series(comment_num)
    df_naver['comment_num_deleted'] = pd.Series(comment_num_deleted)
    df_naver['comment_num_violation'] = pd.Series(comment_num_violation)

    df_naver['summary'] = pd.Series(article_summary)

    df_naver['sort_lists'] = pd.Series(sort_lists)
    df_naver['sort_recent'] = pd.Series(sort_recent)
    df_naver['sort_like'] = pd.Series(sort_like)
    df_naver['sort_ratio'] = pd.Series(sort_ratio)

    #print(df_naver.head())

    df_naver.to_csv('./result/naver_{}.csv'.format(crawl_time), encoding='utf-8-sig')
    print('--------------------  Crawled at: {}  --------------------'.format(crawl_time))

def crawling():
    threading.Timer(7200, crawling).start()
    crawl_naver()

crawling()




