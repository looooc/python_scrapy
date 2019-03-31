import datetime
import json

import requests
import scrapy
import time

class Spider(scrapy.Spider):

    def __init__(self):
        self.source = 'study.163.com'
        self.keyWord = '区块链'
        self.pageCount = 1

    name = "wangyiyun"
    allowed_domains = ['study.163.com']

    def start_requests(self):
        start_url = 'https://study.163.com/p/search/studycourse.json'

        #self.get_totalTime()

        for i in range(1,15):
            yield scrapy.Request(url=start_url, method="POST", body=json.dumps({
                "pageSize":50,
                "pageIndex":i,
                "relativeOffset":0,
                "searchTimeType":-1,
                "orderType":5,
                "priceType":-1,
                "activityId":0,
                "qualityType":0,
                "keyword":self.keyWord
            }), headers={'Content-Type': 'application/json'},callback=self.parse_json)

    # def get_totalTime(self):
    #     time_stamp = self.now_to_timestamp()
    #     url = "https://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?%s"%(time_stamp)
    #     print("-----------------url:"+url)
    #     payload = "callCount=1&scriptSessionId=${scriptSessionId}190&httpSessionId=96974c93c84449c7abfb2e1075bdfaed&c0-scriptName=PlanNewBean&c0-methodName=getPlanCourseDetail&c0-id = 0&c0-param0=string:1208894818&c0-param1=number:0&c0-param2=null:null&batchId=%s"%(self.now_to_timestamp())
    #     headers = {'content-type': 'text/plain'}
    #     r = requests.post(url, data=payload, headers=headers)
    #     print("--------------------r"+r.text)
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
    #     #print("非准确------"+str())




    def parse_json(self, response):
        res = json.loads(response.text)
        if res['code'] == 0:
            data = res['result']['list']
            print("第 %s 页"%(res['result']['query']['pageIndex']))
            for l_data in data:
                item = {
                    'source': self.source,
                    'keyWord': self.keyWord,
                    'courseId': l_data['courseId'],
                    'productName': l_data['productName'],
                    'price': l_data['originalPrice'],
                    'score': l_data['score'],
                    'descriptionSize': len(l_data['description']) if l_data['description'] != None else 0,
                    'lessonCount': l_data['lessonCount'],
                    'learnerCount': l_data['learnerCount']
                }
                yield item
