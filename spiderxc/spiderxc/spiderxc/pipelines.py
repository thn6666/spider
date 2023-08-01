# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import openpyxl
import pymysql
class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost',port=3306,
                                    user='root',password='15303869923hao',
                                    database='spiderxc1',charset='utf8mb4')
        self.cursor = self.conn.cursor()
    def close_spider(self, spider):
        # if len(self.data) > 0:
        #     self.write_to_db()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        url = item.get('url', '')
        update_at = item.get('update_at', '')
        data = item.get('data', '')
        #批处理
        # if len(self.data) == 100:
        #     self.write_to_db()
        #     self.data.clear()
        self.cursor.execute(
            'insert into collection_content(url, title, update_at,data) values (%s, %s,%s, %s)',
            (url, title, update_at, data)
        )
        return item
