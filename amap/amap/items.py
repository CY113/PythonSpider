# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    parent = scrapy.Field()
    childtype = scrapy.Field()
    name = scrapy.Field()
    tag = scrapy.Field()
    type = scrapy.Field()
    typecode = scrapy.Field()
    biz_type = scrapy.Field()
    address = scrapy.Field()
    location = scrapy.Field()
    tel = scrapy.Field()
    postcode = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    pcode = scrapy.Field()
    pname = scrapy.Field()
    citycode = scrapy.Field()
    cityname = scrapy.Field()
    adcode = scrapy.Field()
    adname = scrapy.Field()
    importance = scrapy.Field()
    shopid = scrapy.Field()
    shopinfo = scrapy.Field()
    poiweight = scrapy.Field()
    gridcode = scrapy.Field()
    distance = scrapy.Field()
    entr_location = scrapy.Field()
    business_area = scrapy.Field()
    exit_location = scrapy.Field()
    match = scrapy.Field()
    recommend = scrapy.Field()
    timestamp = scrapy.Field()
    alias = scrapy.Field()
    indoor_map = scrapy.Field()
    groupbuy_num = scrapy.Field()
    discount_num = scrapy.Field()
    event = scrapy.Field()
    children = scrapy.Field()
    photos = scrapy.Field()
    belong = scrapy.Field()
