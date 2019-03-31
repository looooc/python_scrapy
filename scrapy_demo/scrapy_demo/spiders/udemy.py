import datetime
import json
import pymongo

import requests
import scrapy
import time

class udemy(scrapy.Spider):

    def __init__(self):
        self.source = 'udemy.com'
        self.keyWord = 'ai'
        self.pageCount = 1

    name = "udemy"
    allowed_domains = ['udemy.com']

    # start_urls = [
    #     'https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=ai&p={}'.format(
    #         i) for i in range(1, 30)]


    def start_requests(self):
        # self.get_pageCount()
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        db = client['udemy']
        r = db['repost']
        start_url = ['https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=ai&p={}'.format(i) for i in range(1, 50)]

        # for url in start_url:
        #     yield scrapy.Request(url=url,headers={
        #         "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        #         "referer": "https://www.udemy.com/courses/search/?src=ukw&q=ai"
        #     }, callback=self.parse_json)

        for url in start_url:
            res = requests.get(url=url,headers={
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                "referer": "https://www.udemy.com/courses/search/?src=ukw&q=big+data"
            })
            res = json.loads(res.text)
            print("-----------当前地 {} 页".format(res['pagination']['current_page']))
            data = res['courses']
            for l_data in data:
                item = {
                    'source': self.source,
                    'keyWord': self.keyWord,
                    'courseId': l_data['id'],
                    'productName': l_data['title'],
                    'time': l_data['content_info'],
                    'descriptionSize': l_data['estimated_content_length'],
                    'productDifficultyLevel': l_data['instructional_level'],  # 难度
                    'lessonCount': l_data['num_published_lectures'],
                    'learnerCount': l_data['num_subscribers'],
                    'price': l_data['price'],
                    'published_time': l_data['published_time'],  # 发布时间
                    'num_reviews': l_data['num_reviews'],  # 评分人数
                    'score': l_data['rating']  # 评分
                }
                print(item)
                result = r.update({'courseId': item['courseId']}, {'$set': item}, upsert=True)
                print(result)


    #
    # def get_pageCount(self):
    #     res = requests.get(url='https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=ai&p=2', headers={
    #         "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    #         "referer": "https://www.udemy.com/courses/search/?src=ukw&q=ai"
    #     })
    #     res = json.loads(res.text)
    #     data = res['courses']
    #     # for l_data in data:
    #     #     item = {
    #     #         'productName': l_data['title']
    #     #     }
    #     #     print(item)
    #
    #     self.pageCount = res['pagination']['total_page']
    #     print("---------------------pagecount"+str(self.pageCount))

    # def pars(self, response):
    #     res = json.loads(response.text)
    #     print(res)
    #     data = res['courses']
    #     for l_data in data:
    #         item = {
    #             'source': self.source,
    #             'keyWord': self.keyWord,
    #             'courseId': l_data['id'],
    #             'productName': l_data['title'],
    #             'time': l_data['content_info'],
    #             'descriptionSize': l_data['estimated_content_length'],
    #             'productDifficultyLevel': l_data['instructional_level'],  # 难度
    #             'lessonCount': l_data['num_published_lectures'],
    #             'learnerCount': l_data['num_subscribers'],
    #             'price': l_data['price'],
    #             'published_time': l_data['published_time'],  # 发布时间
    #             'num_reviews': l_data['num_reviews'],  # 评分人数
    #             'score': l_data['rating']  # 评分
    #         }
    #         yield item
    #         print(item)

        # for url in start_urls:
        #     scrapy.Request(url=url,headers={
        #         "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        #         "referer": "https://www.udemy.com/courses/search/?src=ukw&q=ai"
        #     }, callback=self.parse)
