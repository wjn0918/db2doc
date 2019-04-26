
"""
连接数据库获取表结构
"""
from configparser import ConfigParser

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor

cf = ConfigParser()
cf.read('conf/db.ini')

class DB():
    def __init__(self,db_name="mysql"):
        """默认为mysql"""
        self.db_name = db_name


    def conn(self):
        """获取数据库连接对象"""
        if self.db_name == 'mysql':
            return self.__conn_mysql__()

    def cursor(self):
        """获取游标"""


    def executeSql(self, sql, args=None, returnDict=False):
        """
        执行sql语句
        :param sql:sql 语句
        :param args: sql 中的参数
        :param returnDict: 是否创建返回字典类型游标
        :return: 查询的所有结果
        """
        if self.db_name == 'mysql':
            return self.__executeMysqlSql__(sql, args, returnDict)


    def __conn_mysql__(self):
        """
        通过线程池，创建MySQL连接对象，线程数设为5
        :return:
        """
        items = dict(cf.items('mysql'))
        host = items['host']
        user_name = items['user_name']
        password = items['password']
        db = items['db']
        pool = PooledDB(pymysql, 5, host=host, user=user_name, passwd=password, db=db, port=3306,
                        setsession=['SET AUTOCOMMIT = 1'])
        # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        conn = pool.connection()
        return conn
        pass

    def __executeMysqlSql__(self, sql, args=None, returnDict=False):
        """
        执行sql
        :param sql:sql 语句
        :param args: sql 中的参数
        :param returnDict: 是否创建返回字典类型游标
        :return: 查询的所有结果
        """
        conn = self.__conn_mysql__()
        if returnDict:
            cursor = conn.cursor(DictCursor)
        else:
            cursor = conn.cursor()
        cursor.execute(sql, args)
        r = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return r
        pass

if __name__ == '__main__':
    db = DB()
    sql = 'select * from t_1'
    db.executeSql(sql)