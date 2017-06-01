# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

# from utils.common import extract_num
# from settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
# from w3lib.html import remove_tags



class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):
    return value+"-sunwenke"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime ( value, "%Y/%m/%d" ).date ()
    except Exception as e:
        create_date = datetime.datetime.now ().date ()

    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def return_value(value):
    return value


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

class ArticleItemLoader(ItemLoader):
    #自定义itemloader，调用takefist
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose (date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field () #让url的长度变成固定的长度
    front_image_url = scrapy.Field(
        output_processor=MapCompose ( return_value )
    )
    front_image_path = scrapy.Field() #封面在本地存放的路径
    praise_nums = scrapy.Field(
        input_processor=MapCompose ( get_nums )
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose ( get_nums )
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose ( get_nums )
    )
    tags = scrapy.Field(
        input_processor=MapCompose ( remove_comment_tags ),
        output_processor=Join(",")
    )
    content = scrapy.Field()



