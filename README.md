# Bilibili爬虫开源

### 项目介绍：

Bilibili是中国的一家视频网站，其有相当多的数据可供研究，因此我开发了这个爬虫项目，旨在收集B站数据用于科学研究，如果各位有兴趣自行运行，还请大家遵守爬虫规则，不要给官方服务器造成太大压力。


***当然，如果您觉得有用的话，还请各位大佬动动小手，给孩子点个小星星，孩子现在大三，想要在保研的时候能多说点东西，在这里先行跪谢大家了！***

### 关于数据：

本项目可以根据txt文件中预存的用户uid来对这些用户的每个视频数据进行批量爬取，每个用户的所有视频数据全部存储在一个json文件当中，json结构示例如下：

{
        "用户名": "丸子",
        "粉丝数": 1321912,
        "bv": "BV1xV411c7j1",
        "链接": "https://www.bilibili.com/video/BV1xV411c7j1/",
        "标题": "【世界弹射物语/丸子】云水土偶嘉年华活动攻略. 奖励&武器一览/Boss解析/队伍推荐",
        "播放量": "5995",
        "时长（秒）": 131,
        "发布日期": "2023-09-23",
        "当前时间": "2023-09-24 17:21:48",
        "弹幕": "92",
        "点赞数": "904",
        "硬币数": "45",
        "收藏数": "37",
        "分享数": "13",
        "标签": "游戏",
        "回复": "27"
    }

除此之外，本项目还提供数据处理算法，可以对json进行批量处理，以用户为单位导出数据，具体可得到的变量有：

平均视频更新时间、视频平均时长（秒）、视频总数、视频平均点赞数、视频平均硬币数、视频平均转发数、视频平均弹幕数、视频平均收藏数、视频平均播放量、视频平均评论数、视频推荐指数（旧版B站推流算法，具体请见代码）、点赞/播放量超过4%的视频数、粉丝数、UP主所在分区（默认发布视频最多的分区为视频作者所在分区）



**本项目爬取到的原始数据、处理结束的数据均已开源(由于github一次最多上传100份文件，故1500份json文件过大，如有需要请联系我的微信：wxid_5acoeqkneahp22)，可直接取用，注意：处理算法方面删除了预处理部分，比如如何去除异常值，但不影响数据真实性**

### 简单分析：

爬取到的数据的分布：

<img src="image\image-20231007202705023.png" alt="image-20231007202705023"  width="500px">

粉丝数与其他变量的关系：

<img src="image\image-20231007203007965.png" alt="image-20231007203007965"  width="400px"><img src="image\image-20231007203043943.png" alt="image-20231007203043943"  width="400px">

<img src="image\image-20231007203104474.png" alt="image-20231007203104474"  width="400px"><img src="image\image-20231007203127629.png" alt="image-20231007203127629"  width="400px">

<img src="image\image-20231007203151553.png" alt="image-20231007203151553"  width="400px"><img src="image\image-20231007203211418.png" alt="image-20231007203211418"  width="400px">

<img src="image\image-20231007203229848.png" alt="image-20231007203229848"  width="400px"><img src="image\image-20231007203259301.png" alt="image-20231007203259301"  width="400px">

更多分析敬请自行探索

### 项目演示：

B站：https://www.bilibili.com/video/BV1BG411m76w/?spm_id_from=333.999.0.0&vd_source=0ab930fe0115c428541edbd7c102b6b4   

抖音：https://www.douyin.com/user/self?modal_id=7288262331803405631


### 项目结构：

```
C:.
│  bili_uid_scraper.py：通过接入b站接口批量爬取某个用户的关注列表，用于批量获取高质量uid
│  data_preprocessing.py：数据处理，把原始数据以用户为单位生成信息，存储为csv
│  main.py：主函数
│  result.csv：处理结果
│  target_id.txt：所有想要获取的uid，包括爬取成功和放弃爬取的
│  remove_duplicate_string.py：对字符串进行去重
│
├─json：存放爬取到的json文件
├─open source base data：开源的已爬取到的数据
└─utils
        bilibili_spider.py：爬虫主代码
        tools.py：工具类
```

### 依赖准备：

- selenium
- bs4
- geckodriver：https://github.com/mozilla/geckodriver/releases
- firefox

以上内容均有相关教程，在此不再赘述，可能仍需其他依赖，如有报错可以根据报错再调整

### 快速使用：

##### 1.安装依赖：

​	参考“依赖准备”

##### 2.批量爬取用户uid：

在b站随便找一个关注量较大的博主，或者是自己也可以，在TA的主页找到uid：    

<img src="image\image-20231007192131657.png" alt="image-20231007192131657"  width="500px">

然后打开bili_uid_scraper.py，把uid写在vmids里面

<img src="image\image-20231007194337712.png" alt="image-20231007194337712"  width="500px">

运行程序，接着从输出文件当中获取uid，再放入vmids中，重复操作直到你认为uid数量已经足够，然后把uid都放入target_id.txt中，注意格式，一个uid占一行

##### 3.运行爬虫程序：

打开文件夹，在路径栏中输入cmd

<img src="image\image-20231007195111603.png" alt="image-20231007195111603"  width="500px">

在命令提示行中输入python main.py

<img src="image\image-20231007195302581.png" alt="image-20231007195302581"  width="500px">

##### 4.处理数据：

在文件夹中的json文件夹里，就会出现刚刚爬取成功的json串，接下来按照相同步骤运行代码

（python data_preprocessing.py），会输出your_result.csv



##### 另：

爬到的uid可能会有重复的，因为可能会有多个人同时关注TA，可以自行选择是否运行remove_duplicate_string.py文件（把两个目标路径替换成自己的路径），这段代码可以对txt文件中的字符串进行去重

### 改进方向：

B站中有很多非正常格式，比如说拜年祭和综艺，这些网页结构和正常视频的很不相同，会导致爬取失败，不过这种视频很少，且大多集中在官方号之中，所以不必担心，另外，有些时候视频标签会爬取失败，不稳定，日后可以查找原因，不过我设置了爬取错误的内容超过20%就放弃存储，会保证数据质量。
