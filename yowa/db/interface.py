import time
import datetime

import cx_Oracle

from yowa.settings import DB_CONF
from yowa.utils import cs
from yowa.db.oracle_engine import Oracle_Connection

class Session(object):
    
    def __init__(self, config = None):
        self.config = DB_CONF
        if config:
            self.config = config
        self._conn = Oracle_Connection(self.config['USERNAME'], self.config['PASSWORD'], dsn = self.config['SERVICE_NAME'])

    def getMission(self, **kwargs):
        cursor = self._conn.cursor()
        
        where_cluster = ' and '.join(["%s = '%s'" % s for s in kwargs.items()])
        stmt = 'select * from mission_t where ' + where_cluster
        
        query = cursor.execute(stmt)
        rs = query.fetchall()
        return rs

    def addContent(self, item):
        cursor = self._conn.cursor()
        cursor.setinputsizes(content = cx_Oracle.CLOB)

        clob_var = cursor.var(cx_Oracle.CLOB)
        clob_var.setvalue(0, item['content'])

        try:
            climb_switch_time = datetime.datetime.fromtimestamp(item['release_switch_time'])
        except:
            climb_switch_time = None
        
        if item["child_mark"] == "jr":
            stmt = "insert into news_recommand_t (title, source, release_time, pic_url, content, url, climb_time) "\
                   "values (:title, :source, :release_time, :pic_url, :content, :child_url, :climb_time)"

            query = cursor.execute(stmt,
                                   title = item['title'],
                                   source = item['source'], 
                                   release_time = item['release_time'],
                                   pic_url = item['pic_url'],
                                   content = clob_var,
                                   child_url = item['child_url'],
                                   climb_time = datetime.datetime.fromtimestamp(item['climb_time']))
        else:
            stmt = "insert into v2_content_7_t (father_url_number, title, content, source, "\
                   "climb_time, climb_switch_time, release_time, child_url, pic_url, price, "\
                   "city, deadline, category_code, section_type, merchant, author) "\
                   "values (:father_url_number, :title, :content, :source, :climb_time, "\
                   ":climb_switch_time, :release_time, :child_url, :pic_url, :price, :city, "\
                   ":deadline, :child_mark, :sum_mark, :merchant, :author)"

            query = cursor.execute(stmt,
                                   father_url_number = item['father_url_number'],
                                   title = item['title'],
                                   content = clob_var,
                                   source = item['source'],
                                   climb_time = datetime.datetime.fromtimestamp(item['climb_time']),
                                   climb_switch_time = climb_switch_time,
                                   release_time = item['release_time'],
                                   child_url = item['child_url'],
                                   pic_url = item['pic_url'],
                                   price = item['price'],
                                   city = item['city'],
                                   deadline = item['deadline'],
                                   child_mark = item['child_mark'],
                                   sum_mark = item['sum_mark'],
                                   merchant = item['merchant'],
                                   author = item['author'])
            
        self._conn.commit()
        return query

    def close(self):
        self._conn.close()
