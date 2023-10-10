import re
import os
import os.path as osp
import sys
import json
import time
import argparse
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from urllib import parse as url_parse
import random
import sys
from selenium.webdriver.chrome.service import Service
from .tools import mkdir_if_missing, write_json, read_json
import win32api


class Bilibili_Spider():

    def __init__(self, uid, save_dir_json='json', save_by_page=False, t=0):
        self.t = t
        self.uid = uid
        self.user_url = 'https://space.bilibili.com/{}'.format(uid)
        gecko_driver_path = 'C:\\Users\puppy\\.cache\\selenium\\geckodriver\\win64\\0.33.0\\geckodriver.exe'
        service = Service(executable_path=gecko_driver_path)
#         driver = webdriver.Firefox(service=service)
        self.save_dir_json = save_dir_json
        self.save_by_page = save_by_page
        options = webdriver.FirefoxOptions()
#         加上这行代码则不会开启浏览器，容易会被监测为爬虫
#         options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=options,service=service)
        print('spider init done.')

    def close(self):
        # 关闭浏览器驱动
        self.browser.quit()

        
    def show_error_message(self):
        # 使用win32api.MessageBox函数来创建弹窗
        # 参数分别是：父窗口句柄（None表示没有父窗口），消息内容，标题，按钮类型（0表示OK按钮）
        win32api.MessageBox(None, "爬虫程序遇到了错误，请输入验证码", "错误提示", 0)
        
    #把视频播放时长改成以秒来计算
    def time_convert(self, time_str):
        time_item = time_str.split(':')
        assert 1 <= len(time_item) <= 3, 'time format error: {}, x:x expected!'.format(time_str)
        if len(time_item) == 1:
            seconds = int(time_item[0]) # 修改了这里
        elif len(time_item) == 2:
            seconds = int(time_item[0])*60 + int(time_item[1])
        else:
            seconds = int(time_item[0])*60*60 + int(time_item[1])*60 + int(time_item[2])
        return seconds

    #把发布时间改为标准时间记录方式
    def date_convert(self, date_str):
        date_item = date_str.split('-')
        assert len(date_item) == 2 or len(date_item) == 3, 'date format error: {}, x-x or x-x-x expected!'.format(date_str)
        if len(date_item) == 2:
            year = datetime.datetime.now().strftime('%Y')
            date_str = '{}-{:>02d}-{:>02d}'.format(year, int(date_item[0]), int(date_item[1]))
        else:
            date_str = '{}-{:>02d}-{:>02d}'.format(date_item[0], int(date_item[1]), int(date_item[2]))
        return date_str

    # 获取从主页获取视频页数以及用户名
    def get_page_num(self):
        page_url = self.user_url + '/video?tid=0&pn={}&keyword=&order=pubdate'.format(1)
        self.browser.get(page_url)
        time.sleep(self.t+1*random.random())
        while len(self.browser.page_source) == 0:
#             self.show_error_message()
            self.browser.get(page_url)
            time.sleep(self.t*3+1*random.random())
            print("视频页数信息获取失败，重新尝试")
        count = 0
        while True:
            try:
                html = BeautifulSoup(self.browser.page_source, features="html.parser")
                time.sleep(0.5+1*random.random())
                page_number = html.find('span', attrs={'class':'be-pager-total'}).text
            except Exception as e: 
                count = count +1
                print("视频页数信息匹配失败，第"+str(count)+"次尝试")
#                 self.show_error_message()
                self.browser.get(page_url)
                time.sleep(10+1*random.random())
                continue # 继续循环
            else: # 如果没有错误，就执行 else 子句
                break # 跳出循环

            
        user_name = html.find('span', id = 'h-name').text
        
        url = "https://api.bilibili.com/x/relation/stat"
        params = {
            "vmid": self.uid,
            "w_rid": "c974deec0b4cfb1e3e35734038bc5686",
            "wts": 1694779465,
            "web_location": "333.999"
        }

        # 发送GET请求并获取响应
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
        response = requests.get(url, params=params, headers = header)

        # 检查响应状态码是否为200（成功）
        if response.status_code == 200:
            # 解析响应为JSON格式
            data = json.loads(response.text)

            # 从data字典中提取follower的值
            follower = data["data"]["follower"]
        else:
            follower = ""

        return int(page_number.split(' ')[1]), user_name, follower
    
    # 爬取某一页的所有视频
    def get_videos_by_page(self, idx):
        # 获取第 page_idx 页的视频信息
        # 网址、标题、播放量、播放时长、发布日期
        urls_page, titles_page, plays_page, dates_page, durations_page = [], [], [], [], []
        page_url = self.user_url + '/video?tid=0&pn={}&keyword=&order=pubdate'.format(idx+1)
        self.browser.get(page_url)
        time.sleep(self.t+1*random.random())
        while len(self.browser.page_source) == 0:
            self.browser.get(page_url)
            time.sleep(self.t+1*random.random())
            print("视频页信息获取失败，重新尝试")
#         html = BeautifulSoup(self.browser.page_source, features="html.parser")
#         print(html)
        count = 0
        while True:
            try:
                html = BeautifulSoup(self.browser.page_source, features="html.parser")
                ul_data = html.find('div', id = 'submit-video-list').find('ul', attrs= {'class': 'clearfix cube-list'})
                # 遍历每一个视频信息
                for li in ul_data.find_all('li'):
                    # url & title
                    a = li.find('a', attrs = {'target':'_blank', 'class':'title'})
                    a_url = 'https:{}'.format(a['href'])
                    a_title = a.text
                    # pub_date & play
                    date_str = li.find('span', attrs = {'class':'time'}).text.strip()

                    # 获取前一天的日期
                    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
                    # yesterday_date是一个date对象
                    yesterday_date = yesterday.date()
                    # 尝试用原来的方法解析日期字符串
                    try:
                        pub_date = self.date_convert(date_str)
                    # 如果失败了，就用前一天的日期替代
                    except:
                        pub_date = yesterday_date.strftime('%Y-%m-%d')

                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    play = li.find('span', attrs = {'class':'play'}).text.strip()
                    time_str = li.find('span', attrs = {'class':'length'}).text
                    duration = self.time_convert(time_str)

                    urls_page.append(a_url)
                    titles_page.append(a_title)
                    dates_page.append((pub_date, now))
                    plays_page.append(play)
                    durations_page.append(duration)
            except Exception as e: 
                count = count +1
                print("视频页信息获取失败，第"+str(count)+"尝试")
                if count == 1:
                    time.sleep(self.t+1*random.random())
                else:
                    time.sleep(self.t+1*random.random())
                if count == 3:
                    print("错误太多，请稍后重试")
                    break
                continue # 继续循环
            else: # 如果没有错误，就执行 else 子句
                break # 跳出循环
        return urls_page, titles_page, plays_page, dates_page, durations_page
    
    #把数据进行保存
    def save(self, json_path, bvs, urls, titles, plays, durations, dates, barrages_count, like_count, coins_count, collections_count, forwards_count, tag_count, reply_count):
        data_list = []
        for i in range(len(barrages_count)):
            result = {}
            result['用户名'] = self.user_name
            result['粉丝数'] = self.follower
            result['bv'] = bvs[i]
            result['链接'] = urls[i]
            result['标题'] = titles[i]
            result['播放量'] = plays[i]
            result['时长（秒）'] = durations[i]
            result['发布日期'] = dates[i][0]
            result['当前时间'] = dates[i][1]
            result['弹幕'] = barrages_count[i]
            result['点赞数'] = like_count[i]
            result['硬币数'] = coins_count[i]
            result['收藏数'] = collections_count[i]
            result['分享数'] = forwards_count[i]
            result['标签'] = tag_count[i]
            result['回复'] = reply_count[i]
            data_list.append(result)
        
        print('write json to {}'.format(json_path))
        write_json(data_list, json_path) # 写入数据到json文件
        print('dump json file done. total {} urls. \n'.format(len(urls)))
        
    def get_video_url(self, video_id_or_url):
        if self.is_url(video_id_or_url):
            return video_id_or_url
        else:
            return f"https://www.bilibili.com/video/{video_id_or_url}"
        
    def is_url(self, video_id_or_url):
        return video_id_or_url.startswith("http") or video_id_or_url.startswith("https")

    # 主函数，爬取所有内容，并打印
    def get(self):
        # 获取该 up 主的所有基础视频信息
        print('Start ... \n')
        self.page_num, self.user_name, self.follower = self.get_page_num()
        time.sleep(self.t+1*random.random())
        count_failed = 0
        while self.page_num == 0:
            if count_failed == 3:
                print(f"{self.uid}可能是没有视频，记得检查！")
                break
            print('视频界面数目获取失败，网络不佳，重新尝试 ... ')
            count_failed = count_failed + 1
            self.page_num, self.user_name, self.follower = self.get_page_num()
        
        if self.page_num < 1000000 and self.page_num > 0:
            print('Pages Num {}, User Name: {}'.format(self.page_num, self.user_name))

            bvs = []
            urls = []
            titles = []
            plays = []
            dates = []
            durations = []   # by seconds
            barrages_count, like_count, coins_count, collections_count, forwards_count, tag_count, reply_count = [], [], [], [], [], [], []
            
            wrong_num = 0
            
            for idx in range(self.page_num):
                print('>>>> page {}/{}'.format(idx+1, self.page_num))
                urls_page, titles_page, plays_page, dates_page, durations_page = self.get_videos_by_page(idx)
                stop = 0
                while len(urls_page) == 0:
                    print('failed, try again page {}/{}'.format(idx+1, self.page_num))
                    time.sleep(self.t+1*random.random())
                    urls_page, titles_page, plays_page, dates_page, durations_page = self.get_videos_by_page(idx)
                    stop = stop + 1
                    if stop >= 10:
                        time.sleep(300+1*random.random())
                bvs_page = [x.split('/')[-2] for x in urls_page]
                assert len(urls_page) == len(titles_page), '{} != {}'.format(len(urls_page), len(titles_page)) 
                assert len(urls_page) == len(plays_page), '{} != {}'.format(len(urls_page), len(titles_page)) 
                assert len(urls_page) == len(dates_page), '{} != {}'.format(len(urls_page), len(dates_page))  
                assert len(urls_page) == len(durations_page), '{} != {}'.format(len(urls_page), len(durations_page))
                print('successfully get {}_{} ,'.format(self.user_name, self.uid), '{} in total'.format(len(urls_page)))
                sys.stdout.flush()

                i = 0
                for video_id_or_url in bvs_page:
                    i += 1
                    url = self.get_video_url(video_id_or_url.strip())
                    try:
                        tag = ""
                        match_view = ""
                        match_danmaku = ""
                        match_reply = ""
                        match_favorite = ""
                        match_coin = ""
                        match_share = ""
                        match_like = ""
                        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                        response = requests.get(url,headers = header)
                        soup = BeautifulSoup(response.text, "html.parser")

                        # 视频 aid、视频时长和作者 id
                        initial_state_script = soup.find("script", text=re.compile("window.__INITIAL_STATE__"))
                        initial_state_text = initial_state_script.string

                        # 提取标题
                        title_raw = soup.find("title").text
                        title = re.sub(r"_哔哩哔哩_bilibili", "", title_raw).strip()
                        # 提取标签
                        # 定义正则表达式模式
                        pattern1 = "<div class=\"firstchannel-tag\" data-v-934a50f8><a href=\"//www.bilibili.com/.*?\" target=\"_blank\" class=\"tag-link\">(.*?)</a></div>"
                        
                        pattern_view = "\"view\":(.*?),"
                        pattern_danmaku = "\"danmaku\":(.*?),"
                        pattern_reply = "\"reply\":(.*?),"
                        pattern_favorite = "\"favorite\":(.*?),"
                        pattern_coin = "\"coin\":(.*?),"
                        pattern_share = "\"share\":(.*?),"
                        pattern_like = "\"like\":(.*?),"
                            
                        #赋值区：
                        match_view = re.search(pattern_view,response.text).group(1)
                        match_danmaku = re.search(pattern_danmaku,response.text).group(1)
                        match_reply = re.search(pattern_reply,response.text).group(1)
                        match_favorite = re.search(pattern_favorite,response.text).group(1)
                        match_coin = re.search(pattern_coin,response.text).group(1)
                        match_share = re.search(pattern_share,response.text).group(1)
                        match_like = re.search(pattern_like,response.text).group(1)
                        matches1 = re.search(pattern1,response.text).group(1)
                        tag = matches1
                        if match_view:
                            views = match_view
                            danmaku = match_danmaku
                            reply = match_reply
                            favorites = match_favorite
                            coins = match_coin
                            shares = match_share
                            likes = match_like
                            
                            plays.append(views)
                            barrages_count.append(danmaku)
                            like_count.append(likes)
                            coins_count.append(coins)
                            collections_count.append(favorites)
                            forwards_count.append(shares)
                            tag_count.append(tag)
                            reply_count.append(reply)
#                             print(f"第{i}个视频{url}已完成爬取")
                        else:
                            print(f"第{i}行视频 {url}未找到相关数据，可能为分集视频")
                            
                    except Exception as e:
                        print(e)
                        plays.append(match_view)
                        barrages_count.append(match_danmaku)
                        like_count.append(match_like)
                        coins_count.append(match_coin)
                        collections_count.append(match_favorite)
                        forwards_count.append(match_share)
                        tag_count.append(tag)
                        reply_count.append(match_reply)
                        wrong_num = wrong_num + 1
                        print(f"第{i}行发生错误，出错数据为{video_id_or_url}")

                bvs.extend(bvs_page)
                urls.extend(urls_page)
                titles.extend(titles_page)
                dates.extend(dates_page)
                durations.extend(durations_page)
            json_path = os.path.join(".", "json", "{}.json".format(self.uid)) # 获取当前文件夹中的json文件夹里的json文件路径
            if wrong_num/len(barrages_count) < 0.2:
                self.save(json_path, bvs, urls, titles, plays, durations, dates, barrages_count, like_count, coins_count, collections_count, forwards_count, tag_count, reply_count)
            else :
                print(f"{wrong_num}/ {len(barrages_count)}，太多错误了！！放弃收集")
            self.close()
        elif self.page_num >= 30:
            print(self.uid + "超过1800个视频，放弃爬取")
#         elif self.page_num == 0:
#             print(f"{self.uid}可能是没有粉丝，或者网络不佳导致获取失败，记得检查！")
        else :
            print(f"{self.uid}未知错误")
            self.close()