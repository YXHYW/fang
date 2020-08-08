# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NewHouseItem(scrapy.Item):
    """新房信息类"""
    # 省份、城市
    province = Field()
    city = Field()
    # 小区的名字
    name = Field()
    # 价格
    price = Field()
    # 几居，这个是个列表
    rooms = Field()
    # 面积
    area = Field()
    # 地址
    address = Field()
    # 行政区
    district = Field()
    # 是否在售
    sale = Field()
    # 详情页面
    origin_url = Field()

class EsfHouseItem(scrapy.Item):
    """二手房信息类"""
    # 省份、城市
    province = Field()
    city = Field()
    # 小区的名字
    name = Field()
    # 房间数
    rooms = Field()
    # 楼层
    floor = Field()
    # 朝向
    towards = Field()
    # 年代
    year = Field()
    # 地址
    address = Field()
    # 面积
    area = Field()
    # 总价
    price = Field()
    # 单价
    unit = Field()
    # 详情页面
    origin_url = Field()