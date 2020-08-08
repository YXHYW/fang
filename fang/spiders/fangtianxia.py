# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.http import request
from fang.items import NewHouseItem,EsfHouseItem
from scrapy_redis.spiders import RedisSpider

class FangtianxiaSpider(RedisSpider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls"

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            # 第一个td标签没有内容
            # 因为只有第一个td标签有class属性，所以使用not筛掉即可
            tds = tr.xpath(".//td[not(@class)]")
            
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            # 删掉第二行的空白字符
            province_text = re.sub(r"\s","",province_text)
            # 如果有省份名了，就赋值给province
            if province_text:
                province = province_text
            if province == "其它":
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # 构建新房的url链接
                scheme = city_url.split("//")[0]
                domain = city_url.split("//")[1]
                # 处理北京这个例外
                if "bj." in domain:
                    newhouse_url = "https://newhouse.fang.com/house/s/"
                    esf_url = "https://esf.fang.com"
                else:
                    city_suoxie = domain.split(".")[0]
                    newhouse_url = scheme + "//" + city_suoxie + ".newhouse" + ".fang.com/house/s/"
                    # 构建二手房的url链接
                    esf_url = scheme + "//" + city_suoxie + ".esf" + ".fang.com"
                # 通过 meta 传递province、city给 parse_newhouse()、parse_esf()
                # yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})

    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li[not(@style)]")
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            name = re.sub(r"\s",'',name)

            house_type_text = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            rooms = list(map(lambda x:re.sub(r'\s','',x),house_type_text))

            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/","",area)

            # 地址
            address = li.xpath(".//div[@class='address']/a/@title").get()

            # 行政区
            district_text = "".join(li.xpath(".//div[@class='address']/a/span/text()").getall())
            district = re.search(r".*\[(.+)\].*",district_text).group(1)

            sale = li.xpath(".//div[@class='fangyuan']/span/text()").get()

            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s","",price)

            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            origin_url = "https:" + origin_url[1:-1]
            
            item = NewHouseItem(name=name,rooms=rooms,price=price,area=area,address=address,sale=sale,district=district,origin_url=origin_url,province=province,city=city)

            yield item

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        # 如果urljoin没用就手动改url
        # next_url = response.url + next_url

        # 如果存在下一页就循环调用自身，继续解析网页
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={"info":(province,city)})

    def parse_esf(self,response):
        province,city = response.meta.get('info')
        dls = response.xpath("//div[contains(@class,'shop_list')]/dl[not(@data-bgcomare)]")
        item = EsfHouseItem(province=province,city=city)
        for dl in dls:
            item['name'] = dl.xpath(".//p[@class='add_shop']/a/@title").get()
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x:re.sub(r"\s","",x),infos))

            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['towards'] = info
                elif "建" in info:
                    item['year'] = info.replace("年建","")
            item['price'] = dl.xpath(".//dd[@class='price_right']/span[@class='red']/b/text()").get()
            item['unit'] = dl.xpath(".//dd[@class='price_right']/span[last()]/text()").get().replace("元/㎡","")
            origin_url = dl.xpath(".//dt/a/@href").get()
            item['origin_url'] = response.urljoin(origin_url)
            yield item
        
        next_url = response.xpath("//div[@class='page_al']/p[1]/@href").get()
        
        # 如果存在下一页就循环调用自身，继续解析网页
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={"info":(province,city)})