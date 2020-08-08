# fang
使用Scrapy爬取房天下网站

## 0. 简介

年轻人在Git上写的第一个爬虫。

**还没写完。。。**

大致就是爬取房天下网站，不确定是否能爬成。QAQ

### 工具

- python
- scrapy

## 1. 分析 URL

新房的url：https://hf.newhouse.fang.com/house/s/，https:// + 城市缩写 + newhouse + fangcom + house/s

二手房的url：https://hf.esf.fang.com/，https:// + 城市缩写 + esf + ……

北京是个例外

## 2. 分析页面元素

## 其它笔记

- 修改Scrapy的日志等级：
  - `LOG_LEVEL = 'ERROR'`