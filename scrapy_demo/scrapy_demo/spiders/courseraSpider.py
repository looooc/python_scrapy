import datetime
import json
import re

import requests
import scrapy
import time

class courseraSpider(scrapy.Spider):
    def __init__(self):
        self.source = 'coursera.org'
        self.keyWord = 'ai'
        self.pageCount = 1


    name = "coursera"
    allowed_domains = ['coursera.org']


    def start_requests(self):
        start_url = 'https://lua9b20g37-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.30.0%3Breact-instantsearch%205.2.3%3BJS%20Helper%202.26.1&x-algolia-application-id=LUA9B20G37&x-algolia-api-key=dcc55281ffd7ba6f24c3a9b18288499b'

        # self.get_totalTime()

        for i in range(0, 30):
            yield scrapy.Request(url=start_url, method="POST", meta={'download_timeout': 20},body=json.dumps({
                "requests":[
                    {
                        "indexName":"DO_NOT_DELETE_PLACEHOLDER_INDEX_NAME",
                        "params":"query=ai&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="
                    },
                    {
                        "indexName":"test_degrees_keyword_only",
                        "params":"query=ai&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="
                    },
                    {
                        "indexName":"test_all_products",
                        "params":"query=ai&hitsPerPage=10&maxValuesPerFacet=1000&page={i}&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%22language%22%2C%22productDifficultyLevel%22%2C%22partners%22%2C%22skills%22%5D&tagFilters=".format(i=i)
                    },
                    {
                        "indexName":"test_suggestions",
                        "params":"query=ai&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="
                    }
                ]
            }), headers={'Content-Type': 'application/json'}, callback=self.parse_json)


    # def get_totalTime(self):
    #     time_stamp = self.now_to_timestamp()
    #     url = "https://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?%s" % (time_stamp)
    #     print("-----------------url:" + url)
    #     payload = "callCount=1&scriptSessionId=${scriptSessionId}190&httpSessionId=96974c93c84449c7abfb2e1075bdfaed&c0-scriptName=PlanNewBean&c0-methodName=getPlanCourseDetail&c0-id = 0&c0-param0=string:1208894818&c0-param1=number:0&c0-param2=null:null&batchId=%s" % (
    #         self.now_to_timestamp())
    #     headers = {'content-type': 'text/plain'}
    #     r = requests.post(url, data=payload, headers=headers)
    #     print("--------------------r" + r.text)
    #
    #
    # # 13位时间戳
    # def now_to_timestamp(self):
    #     datetime_object = datetime.datetime.now()
    #     now_timetuple = datetime_object.timetuple()
    #     now_second = time.mktime(now_timetuple)
    #     mow_millisecond = now_second * 1000 + datetime_object.microsecond / 1000
    #     print("timetuple-- " + str(now_timetuple))
    #     print("datimeobject-- " + str(datetime_object))
    #
    #     print("second-- " + str(now_second))
    #
    #     print("millisecond-- " + str(mow_millisecond))
    #     return round(time.time() * 1000)
    #     # print("非准确------"+str())
    def get_descriptionSize(self, objectUrl):
        url = "https://www."+self.source+objectUrl
        r = requests.get(url=url,headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"})
        #print(r.text)
        desc = re.search(r'<div class="content-inner".*', r.text)
        description = re.split('>',desc[0])
        description = description[1]
        print(len(description))
        return len(description)



    def parse_json(self, response):
        res = json.loads(response.text)
        # if res['code'] == 0:
        data = res['results'][2]['hits']
        print("第 %s 页" % (res['result'][2]['page']))
        for l_data in data:
            item = {
                'source': self.source,
                'keyWord': self.keyWord,
                #'courseId': l_data['courseId'],
                'courseId': l_data['objectID'],
                'productName': l_data['name'],
                #'price': l_data['originalPrice'],
                'score': l_data['avgProductRating'],
                'descriptionSize': self.get_descriptionSize(l_data['objectUrl']),
                #'lessonCount': l_data['lessonCount'],
                'time': l_data['avgLearningHours'],
                'learnerCount': l_data['enrollments'],
                'productDifficultyLevel': l_data['productDifficultyLevel']
            }
            #print(item)
            yield item
