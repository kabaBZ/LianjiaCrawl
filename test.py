import copy

import requests
from lxml import etree

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36',
    # 'Host': 'www.lagou.com',
    # 'Referer': 'https://www.lagou.com/wn/jobs?pn=3&cl=false&fromSearch=true',
    'cookie' : 'JSESSIONID=ABAAAECAAEBABII2ADCB36FA829C26C152FBEAE602015DE; WEBTJ-ID=20220415155651-1802c3990f8536-03b0d10c8ed423-48667e53-2073600-1802c3990f91045; RECOMMEND_TIP=true; PRE_UTM=; PRE_LAND=https://www.lagou.com/; user_trace_token=20220415155652-c8e8a0ed-5947-4df7-8ca3-e69dec06205c; LGUID=20220415155652-0b9ce059-83f2-4e43-8e0a-637e25468649; _ga=GA1.2.974368334.1650009412; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009412; sajssdk_2015_cross_new_user=1; sensorsdata2015session={}; privacyPolicyPopup=false; LGSID=20220415155652-55426a34-08a9-4e2d-a5fa-05220f6037b2; PRE_HOST=www.baidu.com;_gid=GA1.2.951458541.1650009413; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1650009485; gate_login_token=571081e1310ecfb4767ecf15a3099f105ba6341472c27f38e3e2ab6734c40744; _putrc=66010CEE1F7E84CF123F89F2B170EADC; login=true; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; TG-TRACK-CODE=index_search; __lg_stoken__=b5e5712dd34f4bb4a52f272ea19e0d905f0a3688a56b1c40122f2845f9be6b40300a1498bc1cad1464732c6db0c1231aa3269e12da784957cfbed22a64fc0917de31332b3d2e; X_MIDDLE_TOKEN=1c8bea253978dd49cc04efaee7707170; LGRID=20220415160659-04abbf9f-a3b0-4f09-8e7f-9de0888db47e; X_HTTP_TOKEN=af6a6f0ead13f7db2600100561a0924f86d873e1b1; hasDeliver=4;}',
}
url = 'https://hz.lianjia.com/ershoufang/pg1'
response = requests.get(url , headers = headers)
tree = etree.HTML(response.text)
page_num = tree.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()')[0]
# re.match(r'pg1',url)
page_num = int(page_num)
i = page_num//30 +1
print(i)
for pg in range (1,i+1):
    url = url.replace('pg%d'%(pg-1),'pg%d'%pg)
    print(url)
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    li_list = tree.xpath('/html/body/div[4]/div[1]/ul/li')
    for li in li_list:
        house_id = li.xpath('./@data-lj_action_housedel_id')[0]
        print(house_id)