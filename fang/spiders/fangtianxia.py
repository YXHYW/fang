# -*- coding: utf-8 -*-
import scrapy
import re

class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

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
                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})

    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        pass

    def parse_esf(self,response):
        province,city = response.meta.get('info')
        pass