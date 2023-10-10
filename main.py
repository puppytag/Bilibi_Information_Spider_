import os
import os.path as osp
import sys

from utils.bilibili_spider import Bilibili_Spider


def main(target_uid):
    bilibili_spider = Bilibili_Spider(target_uid, 'json', False, 0.5)
    bilibili_spider.get()


if __name__ == '__main__':
    # 定义一个字典来存储参数
    args = {
        'uid': '442926799',
    }
    
    with open("./target_id.txt", "r") as f:
        strings = f.readlines()

    uids = list()

    for s in strings:
        s = s.strip() # 去掉字符串两端的空白字符
        uids.append(s)
    # 将字典作为参数传递给main函数
    
#     main('317127781')
    
    i = 0
    for target_uid in uids:
        main(target_uid)
        i = i+1
        if i == 101:
            sys.exit("程序已终止")