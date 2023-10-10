#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 导入需要的模块
import json
import os
import pandas as pd
import datetime

# 定义一个函数，计算两个日期之间的天数差
def date_diff(date1, date2):
    # 将日期字符串转换为datetime对象
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
    if date1 == date2:
        return 365
    # 计算两个日期之间的天数差
    diff = (date2 - date1).days
    # 返回天数差
    return diff

# 定义一个函数，计算视频推荐指数
def video_score(video):
    # 从视频字典中提取各项数据
    coin = int(video["硬币数"])
    fav = int(video["收藏数"])
    danmu = int(video["弹幕"])
    reply = int(video["回复"])
    play = int(video["播放量"])
    like = int(video["点赞数"])
    share = int(video["分享数"])
    # 根据公式计算视频推荐指数
    score = coin * 0.4 + fav * 0.3 + danmu * 0.4 + reply * 0.4 + play * 0.25 + like * 0.4 + share * 0.6
    # 返回视频推荐指数
    return score

# 定义一个空的数据框，用于存储最终结果
df = pd.DataFrame(columns=["id", "平均视频更新时间", "UP主所在分区", "视频平均时长", "视频总数", "视频平均点赞数", "视频平均硬币数", "视频平均转发数", "视频平均弹幕数", "视频平均收藏数", "视频平均播放量", "视频平均评论数", "视频推荐指数", "点赞/播放量超过4%的视频数", "粉丝数"])

# 读取txt文件中的所有id
with open("target_id.txt", "r") as f:
    ids = f.read().splitlines()

# 遍历每个id
for id in ids:
    # 拼接json文件的路径
    json_file = os.path.join("json", id + ".json")
    # 判断json文件是否存在，如果不存在，跳过该id
    if not os.path.exists(json_file):
        continue
    # 打开json文件，读取所有视频字符串，并转换为字典列表
#     with open(json_file, "r", encoding="utf-8") as f:
#         videos = json.load(f)

    with open(json_file, "r", encoding="utf-8") as f:
        total_data = json.load(f) # 将文件内容转换为Python列表
#         videos = total_data
        if len(total_data) > 1:
            videos = total_data[:len(total_data)//2] # 取列表的前一半
        else:
            videos = total_data
        
    # 初始化各项变量，用于存储该id的统计结果
    avg_update_time = 0 # 平均视频更新时间（天）
    zone = "" # UP主所在分区（出现次数最多的视频标签）
    avg_duration = 0 # 视频平均时长（秒）
    video_count = len(videos) # 视频总数
    total_like = 0 # 总点赞数
    total_coin = 0 # 总硬币数
    total_share = 0 # 总转发数
    total_danmu = 0 # 总弹幕数
    total_fav = 0 # 总收藏数
    avg_play = 0 # 视频平均播放量
    total_reply = 0 # 总评论数
    video_score_sum = 0 # 视频推荐指数之和
    high_like_rate_count = 0 # 点赞/播放量超过4%的视频数

    # 定义一个空的字典，用于存储各个分区的出现次数
    zone_count = {}

    # 遍历每个视频字典，进行统计分析
    for video in videos:
        # 判断视频的"播放量"是否为空，如果是，跳过该视频，继续处理下一个视频
        if video["播放量"] == "" or video["点赞数"] == "" or video["硬币数"] == "" or video["收藏数"] == "" or video["分享数"] == "":
            continue
        # 累加各项数据到对应变量中
        total_like += int(video["点赞数"])
        total_coin += int(video["硬币数"])
        total_share += int(video["分享数"])
        total_danmu += int(video["弹幕"])
        total_fav += int(video["收藏数"])
        avg_play += int(video["播放量"])
        total_reply += int(video["回复"])

        # 计算视频推荐指数，并累加到对应变量中
        score = video_score(video)
        video_score_sum += score

        # 计算视频时长，并累加到对应变量中
        duration = int(video["时长（秒）"])
        avg_duration += duration

        # 判断点赞/播放量是否超过4%，如果是，累加到对应变量中
        like_rate = int(video["点赞数"]) / int(video["播放量"])
        if like_rate > 0.04:
            high_like_rate_count += 1

        # 获取视频标签，并更新分区字典中的计数
        tag = video["标签"]
        zone_count[tag] = zone_count.get(tag, 0) + 1

    # 计算平均视频更新时间，需要用到最新视频发布时间和最早发布日期
    current_time = videos[0]["发布日期"] 
    earliest_date = videos[0]["发布日期"] # 初始化最早发布日期为第一个视频的发布日期
    # 遍历所有视频的发布日期，找出最早的一个
    for video in videos:
        date = video["发布日期"]
        if date < earliest_date:
            earliest_date = date
    # 调用date_diff函数，计算当前时间和最早发布日期之间的天数差
    diff = date_diff(earliest_date, current_time)
    # 计算平均视频更新时间，即天数差除以视频总数
    avg_update_time = diff / video_count
    
    # 记录UP主粉丝数
    fan = int(videos[0]["粉丝数"])
    if fan > 0 and fan <= 100000 :
        fans = "0-100000"
    if fan > 100000 and fan <= 1000000 :
        fans = "100000-1000000"
    if fan > 1000000 and fan <= 3000000 :
        fans = "100000-3000000"
    if fan > 3000000:
        fans = "3000000-∞"
        
    max_count = 0 # 初始化最大计数为0
    for tag, count in zone_count.items():
        if count > max_count:
            max_count = count
            zone = tag

    # 计算视频平均时长，即总时长除以视频总数
    avg_duration = avg_duration / video_count
    
    # 计算视频平均播放量
    avg_play = avg_play / video_count
    
    # 计算视频平均点赞数
    avg_like = total_like / video_count
    
    # 计算视频平均分享数
    avg_share = total_share / video_count
    
    # 计算视频平均弹幕
    avg_danmu = total_danmu / video_count
    
    # 计算视频平均收藏数
    avg_fav = total_fav / video_count
    
    # 计算视频平均回复
    avg_reply = total_reply / video_count
    
    # 计算视频平均硬币数
    avg_coin = total_coin / video_count

    # 计算视频推荐指数，即推荐指数之和除以视频总数
    video_score_avg = video_score_sum / video_count
    
    df.loc[len(df)] = [id, avg_update_time, zone, avg_duration, video_count, avg_like, avg_coin, avg_share, avg_danmu, avg_fav, avg_play, avg_reply, video_score_avg, high_like_rate_count, fans]

# 将数据框保存为csv文件
df.to_csv("your_result.csv", index=False, encoding="utf_8_sig")

