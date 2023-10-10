#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 打开txt文件，读取所有的字符串
with open("C:\\Users\\puppy\\Desktop\\开源\\target_id.txt", "r") as f:
    strings = f.readlines()

# 创建一个空的集合，用来存储不重复的字符串
unique_strings = set()

# 遍历所有的字符串，如果不在集合中，就添加到集合中
for s in strings:
    s = s.strip() # 去掉字符串两端的空白字符
    if s not in unique_strings:
        unique_strings.add(s)

# 打开输出文件，写入不重复的字符串
with open("C:\\Users\\puppy\\Desktop\\开源\\target_id.txt", "w") as f:
    for s in unique_strings:
        f.write(s + "\n")

