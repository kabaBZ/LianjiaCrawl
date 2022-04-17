import copy
import scrapy
import requests
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlspider.items import CrawlspiderItem
from scrapy_redis.spiders import RedisSpider
from redis import Redis
from selenium import webdriver
import time

class LagouwangSpider(RedisSpider):
    name = 'lagouwang'
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': 'lianjia_ssid=82c0666f-124e-476b-bbcf-8e8d4c3dc6e2; lianjia_uuid=10dde14e-356c-461b-b1da-2d1cb291bc00; UM_distinctid=1802d409266de1-0b2c6250bf775f-48667e53-1fa400-1802d409267cc5; _smt_uid=62596898.306df5a5; sajssdk_2015_cross_new_user=1; _ga=GA1.2.1406946909.1650026652; _gid=GA1.2.1216006085.1650026652; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1650026670; select_city=330100; CNZZDATA1254525948=73055294-1650016899-|1650016899; CNZZDATA1255633284=1256213122-1650017174-|1650017174; CNZZDATA1255604082=1754692427-1650020501-|1650020501; sensorsdata2015jssdkcross={"distinct_id":"1802d40947bc-042d3a810f6be6-48667e53-2073600-1802d40947c116e","$device_id":"1802d40947bc-042d3a810f6be6-48667e53-2073600-1802d40947c116e","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开"}}; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1650026943; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYWY4MjM0MWQ4MTQ5ZGZhZjQxYzNmODczZGE0OGJkZWU0OGJhYWQ2MjFkN2RkMDIxOTBkYzlmMDVhNjQxY2ViYTM5ZDU3NzZhYTZhOTI2NjAwZmRmOWQyZWFhNDE1YTU5Nzc0MGVjMDRkMmE5ZDY0YTI3ZDlhMTU2N2NkOGVmZDM0NjNlNTNjOTFhNjhkZDc4YzkzMjUzYmY0OTc5N2MwMmQxNTIzNmY2NGIzOTc5ZmNkYmUwNGE1NTA2Nzg4Yjk3N2ZhZDMzN2U3ZTc2YmIwNzgwMjgyMTc1MTAzMTljYTFmZGY5YjRiNWY2NGZmY2FjNjQzY2Y4NTA0Mzk5ODc3ZFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI0Zjc4Y2JkM1wifSIsInIiOiJodHRwczovL2h6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcGcyLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
            'Host': 'hz.lianjia.com',
            'Origin': 'hz.lianjia.com',
            'Referer': 'hz.lianjia.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }
    conn = Redis(host='1.15.233.110',port=6379,password='kaba5643')
    start_urls = ['https://hz.lianjia.com/ershoufang/']
    redis_key = 'Queue'
    # link = LinkExtractor(allow=r'ershoufang\/pg\d\d$')
    # rules = (
    #     Rule(link, callback='parse_item',follow=False),
    # )
    # url = 'https://hz.lianjia.com/ershoufang/'

    def parse_p(self,response):
        page_num = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract_first()
        print(page_num)
        url_list = response.meta['url_list']
        item = response.meta['item']
        page_num = int(page_num)
        # 售价：p  房型：l  面积：a
        p = response.meta['p']
        a = 0
        url = response.meta['url']
        # 售价>3000 添加房型标签
        if page_num > 3000:
            for l in range(1,6):
                # 链接加l标签
                url = 'https://hz.lianjia.com/ershoufang/pg1p%dl%d/' % (p,l)
                yield scrapy.Request(url,callback=self.parse_l,meta={'url_list':url_list,'url':url,'p':p,'l':l,'a':a,'item':item},encoding = 'utf-8')
        elif page_num > 0:
            page_num = int(page_num)
            i = page_num // 30 + 1
            print(i)
            for pg in range(1, i + 1):
                url = url.replace('pg%d' % (pg - 1), 'pg%d' % pg)
                print(url)
                self.conn.lpush('Queue', url)
            li_list = response.xpath('/html/body/div[4]/div[1]/ul/li')
            for li in li_list:
                house_id = li.xpath('./@data-lj_action_housedel_id').extract_first()
                item['house_id'] = house_id
                url = 'https://hz.lianjia.com/ershoufang/' + house_id + '.html'
                yield scrapy.Request(url, callback=self.parse_data,
                                     meta={'url_list': url_list, 'url': url, 'p': p, 'l': l, 'a': a, 'item': item},encoding = 'utf-8')

    def parse_l(self, response):
        page_num = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract_first()
        print(page_num)
        url_list = response.meta['url_list']
        item = response.meta['item']
        page_num = int(page_num)
        # 售价：p  房型：l  面积：a
        p = response.meta['p']
        l = response.meta['l']
        a = response.meta['a']
        url = response.meta['url']
        # 售价>3000 添加面积标签
        if page_num > 3000:
            for a in range(1, 6):
                # 链接加a标签
                url = 'https://hz.lianjia.com/ershoufang/pg1p%dl%da%d/' % (p, l,a)
                yield scrapy.Request(url, callback=self.parse_a, meta={'url_list':url_list,'url':url,'p':p,'l':l,'a':a,'item':item},encoding = 'utf-8')
        elif page_num > 0:
            page_num = int(page_num)
            i = page_num // 30 + 1
            print(i)
            for pg in range(1, i + 1):
                url = url.replace('pg%d' % (pg - 1), 'pg%d' % pg)
                print(url)
                self.conn.lpush('Queue', url)
            li_list = response.xpath('/html/body/div[4]/div[1]/ul/li')
            for li in li_list:
                house_id = li.xpath('./@data-lj_action_housedel_id').extract_first()
                item['house_id'] = house_id
                url = 'https://hz.lianjia.com/ershoufang/' + house_id + '.html'
                yield scrapy.Request(url, callback=self.parse_data,
                                     meta={'url_list': url_list, 'url': url, 'p': p, 'l': l, 'a': a, 'item': item},encoding = 'utf-8')


    def parse_a(self, response):
        page_num = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract_first()
        print(page_num)
        url_list = response.meta['url_list']
        item = response.meta['item']
        page_num = int(page_num)
        # 售价：p  房型：l  面积：a
        p = response.meta['p']
        l = response.meta['l']
        a = response.meta['a']
        url = response.meta['url']
        # 链接加location标签
        # url = url + 'a%d' % a
        # 售价>3000 添加location标签
        if page_num > 3000:
            # 进入区域循环
            parse_location = 1
            print(url)
            print('进入区域循环')
            # self.conn.lpush('Queue',url)
            # yield item
        elif page_num > 0:
            page_num = int(page_num)
            i = page_num // 30 + 1
            print(i)
            for pg in range(1, i + 1):
                url = url.replace('pg%d' % (pg - 1), 'pg%d' % pg)
                print(url)
                self.conn.lpush('Queue', url)
            li_list = response.xpath('/html/body/div[4]/div[1]/ul/li')
            for li in li_list:
                house_id = li.xpath('./@data-lj_action_housedel_id').extract_first()
                item['house_id'] = house_id
                url = 'https://hz.lianjia.com/ershoufang/' + house_id + '.html'
                yield scrapy.Request(url, callback=self.parse_data,meta={'url_list': url_list, 'url': url, 'p': p, 'l': l, 'a': a, 'item': item},encoding = 'utf-8')


    def parse_data(self,response):
        item = response.meta['item']
        price = response.xpath('/html/body/div[5]/div[2]/div[3]/div/span[1]/text()').extract_first() + response.xpath('/html/body/div[5]/div[2]/div[3]/div/span[2]/span/text()').extract_first()
        item['price'] = price
        yield item

    def parse(self, response):
        page_num = response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract_first()
        item = CrawlspiderItem()
        print(page_num)
        page_num = int(page_num)
        pg = 1
        # 售价：p  房型：l  面积：a
        p, l, a = 0, 0, 0
        url_list = []
        if page_num > 3000:
            print('大于3000添加p')
            for p in range(1,6):
                #添加p标签
                url = 'https://hz.lianjia.com/ershoufang/pg1p%d/' % p
                #城市>3000 添加售价标签
                yield scrapy.Request(url,callback=self.parse_p,meta={'url_list':url_list,'url':url,'p':p,'l':l,'a':a,'item':item},encoding = 'utf-8')
        elif page_num > 0:
            print('小于3000大于0')
            li_list = response.xpath('/html/body/div[4]/div[1]/ul/li')
            for li in li_list:
                house_id = li.xpath('./@data-lj_action_housedel_id').extract_first()
                item['house_id'] = house_id
                url = 'https://hz.lianjia.com/ershoufang/' + house_id + '.html'
                yield scrapy.Request(url,encoding = 'utf-8',callback=self.parse_data,meta={'url_list':url_list,'url':url,'p':p,'l':l,'a':a,'item':item})


