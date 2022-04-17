# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class CrawlspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # cookies = 'JSESSIONID=ABAAAECAAEBABII2ADCB36FA829C26C152FBEAE602015DE; WEBTJ-ID=20220415155651-1802c3990f8536-03b0d10c8ed423-48667e53-2073600-1802c3990f91045; RECOMMEND_TIP=true; PRE_UTM=; PRE_LAND=https://www.lagou.com/; user_trace_token=20220415155652-c8e8a0ed-5947-4df7-8ca3-e69dec06205c; LGUID=20220415155652-0b9ce059-83f2-4e43-8e0a-637e25468649; _ga=GA1.2.974368334.1650009412; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009412; sajssdk_2015_cross_new_user=1; sensorsdata2015session={}; privacyPolicyPopup=false; LGSID=20220415155652-55426a34-08a9-4e2d-a5fa-05220f6037b2; PRE_HOST=www.baidu.com; PRE_SITE=https://www.baidu.com/link?url=ywb5h_oqWYEP6qvIYGT2Mc4a63uNgkaVb2gBkKa4lIS&wd=&eqid=b18edc100002785c0000000462592541; _gid=GA1.2.951458541.1650009413; index_location_city=杭州; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009485; gate_login_token=571081e1310ecfb4767ecf15a3099f105ba6341472c27f38e3e2ab6734c40744; _putrc=66010CEE1F7E84CF123F89F2B170EADC; login=true; unick=郭江斌; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; TG-TRACK-CODE=index_search; __lg_stoken__=b5e5712dd34f4bb4a52f272ea19e0d905f0a3688a56b1c40122f2845f9be6b40300a1498bc1cad1464732c6db0c1231aa3269e12da784957cfbed22a64fc0917de31332b3d2e; X_MIDDLE_TOKEN=1c8bea253978dd49cc04efaee7707170; LGRID=20220415160659-04abbf9f-a3b0-4f09-8e7f-9de0888db47e; X_HTTP_TOKEN=af6a6f0ead13f7db2600100561a0924f86d873e1b1; hasDeliver=4; sensorsdata2015jssdkcross={"distinct_id":"1802c39932215eb-0ed351f2dcbf7a-48667e53-2073600-1802c399323e69","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$os":"Windows","$browser":"Chrome","$browser_version":"100.0.4896.75"},"$device_id":"1802c39932215eb-0ed351f2dcbf7a-48667e53-2073600-1802c399323e69"}'  # 复制自己的cookie
        # cookies = {i.split("=")[0].strip(): i.split("=")[1].strip() for i in cookies.split(";")}
        # request.headers["cookie"] = 'JSESSIONID=ABAAAECAAEBABII2ADCB36FA829C26C152FBEAE602015DE; WEBTJ-ID=20220415155651-1802c3990f8536-03b0d10c8ed423-48667e53-2073600-1802c3990f91045; RECOMMEND_TIP=true; PRE_UTM=; PRE_LAND=https://www.lagou.com/; user_trace_token=20220415155652-c8e8a0ed-5947-4df7-8ca3-e69dec06205c; LGUID=20220415155652-0b9ce059-83f2-4e43-8e0a-637e25468649; _ga=GA1.2.974368334.1650009412; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009412; sajssdk_2015_cross_new_user=1; sensorsdata2015session={}; privacyPolicyPopup=false; LGSID=20220415155652-55426a34-08a9-4e2d-a5fa-05220f6037b2; PRE_HOST=www.baidu.com; PRE_SITE=https://www.baidu.com/link?url=ywb5h_oqWYEP6qvIYGT2Mc4a63uNgkaVb2gBkKa4lIS&wd=&eqid=b18edc100002785c0000000462592541; _gid=GA1.2.951458541.1650009413; index_location_city=杭州; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009485; gate_login_token=571081e1310ecfb4767ecf15a3099f105ba6341472c27f38e3e2ab6734c40744; _putrc=66010CEE1F7E84CF123F89F2B170EADC; login=true; unick=郭江斌; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; TG-TRACK-CODE=index_search; __lg_stoken__=b5e5712dd34f4bb4a52f272ea19e0d905f0a3688a56b1c40122f2845f9be6b40300a1498bc1cad1464732c6db0c1231aa3269e12da784957cfbed22a64fc0917de31332b3d2e; X_MIDDLE_TOKEN=1c8bea253978dd49cc04efaee7707170; LGRID=20220415160659-04abbf9f-a3b0-4f09-8e7f-9de0888db47e; X_HTTP_TOKEN=af6a6f0ead13f7db2600100561a0924f86d873e1b1; hasDeliver=4; sensorsdata2015jssdkcross={"distinct_id":"1802c39932215eb-0ed351f2dcbf7a-48667e53-2073600-1802c399323e69","first_id":"","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":"","$os":"Windows","$browser":"Chrome","$browser_version":"100.0.4896.75"},"$device_id":"1802c39932215eb-0ed351f2dcbf7a-48667e53-2073600-1802c399323e69"}'

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):

        # response.text.encode('utf-8')
        # print(response.text.encode('utf-8'))
        # div_list = response.xpath('/html/body/div/div[1]/div/div[2]/div[3]/div/div[1]/div')
        # for div in div_list:
        #     job_name = div.xpath('./div[1]/div[1]/div[1]/a/text()')[0]
        #     company = div.xpath('./div[1]/div[2]/div[1]/a/text()')[0]
        #     money = div.xpath('./div[1]/div[1]/div[2]/span/text()')[0]
        #     size = div.xpath('./div[1]/div[2]/div[2]/text()')[0]
        #     benefit = div.xpath('./div[2]/div[2]/text()')[0]
        #     position = div.xpath('./div[1]/div[1]/div[1]/a/text()')[1]
        #     print(job_name, position, money)
        #     print(company, size, benefit)
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
