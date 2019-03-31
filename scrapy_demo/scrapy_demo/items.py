# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    keyWord = scrapy.Field()
    courseId = scrapy.Field()
    productName = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    descriptionSize = scrapy.Field()
    lessonCount = scrapy.Field()
    learnerCount = scrapy.Field()
    # time = scrapy.Field()
    # productDifficultyLevel = scrapy.Field()
    # num_reviews = scrapy.Field()
    # published_time = scrapy.Field()


