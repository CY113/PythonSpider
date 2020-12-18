import json
import math
import re

import scrapy
from scrapy.utils.project import get_project_settings

from amap.items import AmapItem
from amap.tools.process_area import get_area_list, getCeil


class PolygonSpider(scrapy.Spider):
    name = 'polygon'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = get_project_settings()['KEY']
        self.base_url = "https://restapi.amap.com/v3/place/polygon?key={}&polygon={}&keywords=&types=010000|020000|030000|040000|040000|050000|060000|070000|080000|090000|100000|110000|120000|130000|140000|150000|160000|170000|180000|190000|200000|220000|970000|990000&offset=20&page={}&extensions=all".format(
            self.key, {}, {})

    def start_requests(self):
        area_list = get_area_list()
        for area in area_list:
            city = area['city']
            lat_min, lat_max, lng_min, lng_max = float(area["lat_min"]), float(area["lat_max"]), float(area["lng_min"]), float(area["lng_max"])
            ceil = getCeil(lat_min, lat_max, lng_min, lng_max)
            for c in ceil:
                start_url = self.base_url.format(c, 1)
                yield scrapy.Request(start_url, callback=self.parse, meta={'polygon': ceil, "city": city})

    def parse(self, response):
        data = json.loads(response.body.decode())
        if data['status'] != '0':
            count = int(data['count'])
            if count >= 800:
                print("poi数据大于800")
                lng_min, lat_max = response.meta['polygon'].split('|')[0].split(',')
                lng_min, lat_min = response.meta['polygon'].split('|')[1].split(',')
                lat_mid = round(((float(lat_min) + float(lat_max)) / 2), 6)
                params1 = str(lng_min) + ',' + str(lat_max) + '|' + str(lng_min) + ',' + str(lat_mid)
                params2 = str(lng_min) + ',' + str(lat_mid) + '|' + str(lng_min) + ',' + str(lat_min)
                url1 = self.base_url.format(params1, 1)
                url2 = self.base_url.format(params2, 1)
                yield scrapy.Request(url1, callback=self.parse, meta={'polygon': params1, "city": response.meta["city"]})
                yield scrapy.Request(url2, callback=self.parse, meta={'polygon': params2, "city": response.meta["city"]})

            else:
                item = AmapItem()
                pages = self.parse_pages(response)
                info = json.loads(response.body.decode())
                pois = info['pois']
                for poi in pois:
                    item["id"] = poi['id']  # ID    str
                    item["parent"] = poi['parent']  # 父节点   list
                    item["childtype"] = poi['childtype']  # 子节点 list
                    item["name"] = poi['name']  # 名称    str
                    item["tag"] = poi['tag']  # 标签  list
                    item["type"] = poi['type']  # 类型    str
                    item["typecode"] = poi['typecode']  # 类型代码  str
                    item["biz_type"] = poi['biz_type']  # biz_type  list
                    item["address"] = poi['address']  # 地址  str
                    item["location"] = poi['location']  # 经纬度   str
                    item["tel"] = poi['tel']  # 电话  list
                    item["postcode"] = poi['postcode']  # postcode  list
                    item["website"] = poi['website']  # 网址  list
                    item["email"] = poi['email']  # email   list
                    item["pcode"] = poi['pcode']  # 邮政编码    str
                    item["pname"] = poi['pname']  # 省份  str
                    item["citycode"] = poi['citycode']  # 城市代码  str
                    item["cityname"] = poi['cityname']  # 城市名称  str
                    item["adcode"] = poi['adcode']  # 地区代码  str
                    item["adname"] = poi['adname']  # 地区名   str
                    item["importance"] = poi['importance']  # 重要性   list
                    item["shopid"] = poi['shopid']  # 商店ID  list
                    item["shopinfo"] = poi['shopinfo']  # shopinfo  str
                    item["poiweight"] = poi['poiweight']  # poiweight   list
                    item["gridcode"] = poi['gridcode']  # gridcode  str
                    item["distance"] = poi['distance']  # distance  list
                    item["entr_location"] = poi['entr_location']  # entr_location   str
                    item["business_area"] = poi['business_area']  # business_area   list
                    item["exit_location"] = poi['exit_location']  # exit_location   list
                    item["match"] = poi['match']  # match   str
                    item["recommend"] = poi['recommend']  # recommend   str
                    item["timestamp"] = poi['timestamp']  # timestamp   str
                    item["alias"] = poi['alias']  # alias   list
                    item["indoor_map"] = poi['indoor_map']  # indoor_map    str
                    item["groupbuy_num"] = poi['groupbuy_num']  # groupbuy_num  str
                    item["discount_num"] = poi['discount_num']  # discount_num  str
                    item["event"] = poi['event']  # indoor_map  list
                    item["children"] = poi['children']  # indoor_map    list
                    item["photos"] = poi['photos']  # indoor_map    list
                    item["belong"] = response.meta["name"]
                    yield item
                if pages > 1:
                    for i in range(2, pages + 1):
                        next_url = re.sub("page=(\d+)", "page=" + str(i),
                                          response.url)  # 得到下一页
                        yield scrapy.Request(next_url, callback=self.parse, meta={"name": response.meta["name"]})
        else:
            raise ValueError('高德key出现问题')

    @staticmethod
    def parse_pages(response):
        """
        计算总页数
        :return:
        """
        content = json.loads(response.body.decode())
        total_count = int(content["count"])
        return int(math.ceil(total_count / 20))
