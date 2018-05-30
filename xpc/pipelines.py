# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='47.100.185.114',
            port=3306,
            user='root',
            password='sunxr1996',
            db='xpc',
            charset='utf8mb4'
        )
        self.cur = self.conn.cursor()

    # def process_item(self, item, spider):
    #     if not hasattr(item, "table_name"):
    #         return item
    #     # cols = item.keys()
    #     # values = item.values()
    #     cols, values = zip(*item.items())
    #     spl = "INSERT INTO '{}' ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {};".format(
    #             item.table_name,
    #             ','.join(cols),
    #             ','.join(['%s'] * len(values)),
    #             ','.join(['{}=%s'.format(k) for k in cols])
    #             )
    #     self.cur.execute(spl, values * 2)
    #     print(self.cur._last_executed)
    #     self.conn.commit()
    #     # sql = 'show tables;'
    #     # self.cur.execute(sql)
    #     # self.conn.commit()
    #
    #     return item

    def process_item(self, item, spider):
        if not hasattr(item, 'table_name'):
            return item
        # cols = list(item.keys())
        # values = [item[k] for k in cols]
        cols, values = zip(*item.items())
        sql = "INSERT INTO `{}` ({}) VALUES ({}) " \
              "ON DUPLICATE KEY UPDATE {}".format(
            item.table_name,
            ','.join(cols),
            ','.join(['%s'] * len(values)),
            ','.join(['{}=%s'.format(k) for k in cols])
        )
        self.cur.execute(sql, values * 2)
        # print(self.cur._last_executed)
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
