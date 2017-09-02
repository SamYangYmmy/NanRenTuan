 #coding:utf-8
import MySQLdb
from scrapy.utils.project import get_project_settings

class DBOperator():
    # 初始化，得到setting 中的数据库设置：
    def __init__(self):
        self.settings=get_project_settings()
        self.host=self.settings['MYSQL_HOST']
        self.port=self.settings['MYSQL_PORT']
        self.user=self.settings['MYSQL_USER']
        self.passwd=self.settings['MYSQL_PASSWD']
        self.db=self.settings['MYSQL_DBNAME']
        self.conn=self.connectDatabase()
        self.cur=self.conn.cursor()

    #链接数据库
    def connectDatabase(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.db,
                             charset='utf8')
        return conn

    def createDatabase(self):
        conn=self.connectDatabase()

        sql="create database if not exists "+self.db
        cur=conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def createTable(self):
        conn = self.connectDatabase()
        sql= """create table tbl_movie(
                id int unsigned not null auto_increment primary key,
                actress_name char(32) not null,
                movie_id char(16) not null,
                movie_name char(128)  ,
                movie_date char(32) );"""
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def insert(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            self.conn.rollback()

    def update(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
        except:
            conn.rollback()
        conn.close()

    def delete(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
        except:
            conn.rollback()
        conn.close()