#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[1]:


# 导入requests库和csv库
import requests
import csv
import random
import time

# 定义一个函数，根据用户ID和页码获取关注列表
def get_followings(vmid, pn):
    # 构造请求URL
    url = f"https://api.bilibili.com/x/relation/followings?vmid={vmid}&pn={pn}&ps=20"
    # 定义请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        "Cookie": "buvid3=75A035EA-F55B-3ADD-3068-C6D4CD47AA1D50610infoc; b_nut=1686101150; _uuid=1B310101105-23AB-F766-1F7A-6ED4A99A375C54739infoc; buvid4=00D0918C-DB93-BE61-5360-0CEF57E4E43C53036-023060709-bK5ysmawZ6U3gC0F76rRLg%3D%3D; home_feed_column=4; rpdid=|(u)Ylmuu~uJ0J'uY)Ykklml); buvid_fp_plain=undefined; FEED_LIVE_VERSION=undefined; DedeUserID=442926799; DedeUserID__ckMd5=1b064f969c58e0c9; header_theme_version=CLOSE; browser_resolution=1280-643; fingerprint=ff3b9fcd54df7ecbf1c2a7a562d93c75; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; SESSDATA=7cbf4f5a%2C1710144461%2Cac9b3%2A92CjDhv-RBcV0l5uMuRajpadUzgAzSX7qPnfScXtDD7i4HfUqzZ5MMSMocGJmR1v_V-UQSVnVXbjlNM1V2blk0Vk9JUlJMNWdsY3JtYTNkb3VDeWo5RWR2YW5WU3VvZnFQeW01Z1hzdDY3Uld6Mk5aWFhSM005ODZYOFFEZDQ5NVNQTE5mbUNBLWx3IIEC; bili_jct=62ca242c9674f04a2a886b28ae5e79ce; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ4NTE2NjMsImlhdCI6MTY5NDU5MjQ2MywicGx0IjotMX0.RPkTTGfSkPEk248qaz45tWxIxnD2vlWDNbEg_aBI6fk; bili_ticket_expires=1694851663; PVID=1; bp_video_offset_442926799=840817179101233289; buvid_fp=ff3b9fcd54df7ecbf1c2a7a562d93c75; b_lsid=4A4D4489_18A926C1A20; sid=77sq3mhr",
        "Referer": f"https://space.bilibili.com/{vmid}/fans/follow"
    }
    # 发送GET请求，并获取响应内容
    response = requests.get(url, headers=headers)
    # 将响应内容转换为JSON格式
    data = response.json()
    # 返回关注列表
    # 使用try-except块来捕获和处理KeyError异常
    try:
        # 尝试从字典中获取"data"键的值
        return data["data"]["list"]
    except KeyError:
        # 处理异常
        print(f"KeyError: 'data' not found in {data}")
        return []



# 定义一个函数，根据用户ID获取所有关注列表，并保存到CSV文件中
# 添加一个参数writer，表示CSV写入器对象
def save_followings(vmid, writer):
    # 初始化页码为1
    pn = 1
    # 循环获取关注列表，直到没有数据为止
    while True:
        # 调用get_followings函数，获取一页关注列表
        followings = get_followings(vmid, pn)
        # 如果关注列表为空，说明已经到达最后一页，退出循环
        if not followings:
            break
        # 否则，遍历关注列表中的每个用户
        for user in followings:
            # 获取用户的ID、昵称和签名
            mid = user["mid"]
            # 写入一行数据到CSV文件中
            writer.writerow([mid])
        # 递增页码
        pn += 1

# 定义一个列表，存储多个用户ID
vmids = [442926799, 9618426, 1197454103, 28880583, 3493094345410926]
# 打开一个CSV文件，例如"all_followings.csv"
with open("followings.csv", "w", encoding="utf-8", newline="") as f:
    # 创建一个CSV写入器对象
    writer = csv.writer(f)
    # 写入表头
    writer.writerow(["mid"])
    # 遍历每个用户ID
    for vmid in vmids:
        # 调用save_followings函数，爬取该用户的所有关注列表，并保存到CSV文件中
        save_followings(vmid, writer) # 传递writer对象作为参数


# In[ ]:




