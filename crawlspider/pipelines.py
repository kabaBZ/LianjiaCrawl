# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlspiderPipeline:
    def process_item(self, item, spider):
        # print(item['job_name'], item['position'], item['money'])
        # print(item['company'], item['size'], item['benefit'])
        print(item['job_name'])
        return item
