
from sql2doc.db import DB
import numpy as np

from sql2doc.pen import MyPen
from configparser import ConfigParser

cf = ConfigParser()
cf.read('conf/conf.ini')


def getTablesNameComment(db_obj,schema_name):
    """
    获取库中所有表名和表注释
    :@param db_obj:数据库连接对象
    :@param shcama_name:数据库名称
    :return: ([name1,name2,],[com1,com2])
    """
    sql = 'select ' \
          'table_name,' \
          'table_rows,' \
          'table_comment ' \
          'from ' \
          'information_schema.`TABLES` ' \
          'where ' \
          'table_schema = %s '
    r = db_obj.executeSql(sql=sql, args=schema_name, returnDict=True)
    table_names = []
    table_comments = []
    for i in r:
        table_names.append(i['table_name'])
        table_comments.append(i['table_comment'])
    return table_names,table_comments

    pass


def getColumnsInfo(db_obj, schema_name, table_name):
    """
    获取表中的字段名,字段类型，字段注释。。。
    :param db_obj: 数据库连接对象
    :param schema_name: 数据库名
    :param table_name: 表名
    :return: （[colName1,colName2,],[dataType1,dataType2,],[com1,com2,]）
    """
    sql = 'select ' \
          'table_name,' \
          'column_name, ' \
          'column_type, ' \
          'column_comment ' \
          'from ' \
          'information_schema.`COLUMNS` ' \
          'where ' \
          'table_schema = %s and table_name = %s '
    args = (schema_name, table_name)
    # print(db_obj.executeSql(sql,args,True))
    columns_name = []
    columns_type = []
    columns_comment = []
    for i in db_obj.executeSql(sql,args,True):
        columns_name.append(i['column_name'])
        columns_type.append(i['column_type'])
        columns_comment.append(i['column_comment'])
    # 添加序列数
    columns_index = np.linspace(1, len(columns_name), len(columns_name), dtype=int)
    return columns_index, columns_name, columns_type, columns_comment

    pass


def getTableInfo():
    """
    获取表信息
    :return: table_info = {table_name:[t1,t2,],table_comments:"表注释",
            column_name:[col1,col2,],column_type:[type1,type2],
            column_comment:[com1,com2]}
    """
    table_info = {}
    db_obj = DB()

    # 读取配置文件
    items = dict(cf.items('mysql'))
    schema_name = items['db_name']
    print("你需要导出的是：%s 库" %(schema_name))
    table_names,comments = getTablesNameComment(db_obj,schema_name)
    table_info['table_name'] = table_names
    table_info['table_comment'] = comments
    # print(table_info
    column_index = []
    column_name = []
    column_type = []
    column_comment = []
    for table_name in table_info['table_name']:
        columns_index, columns_name, columns_type, columns_comment = getColumnsInfo(db_obj, schema_name, table_name)
        column_index.append(columns_index)
        column_name.append(columns_name)
        column_type.append(columns_type)
        column_comment.append(columns_comment)
    table_info['column_index'] = column_index
    table_info['column_name'] = column_name
    table_info['column_type'] = column_type
    table_info['column_comment'] = column_comment
    return table_info
    pass



def write2word(table_info):
    """
    将数据输出到word中
    :param table_info_reduced:处理后的表结构信息
    :return:
    """
    pen = MyPen(file_path)
    pen.draw(table_info)



    pass


def main():
    """程序入口"""
    table_info = getTableInfo()
    write2word(table_info)

    pass

if __name__ == '__main__':
    file_path = 'cs.doc'
    main()