import time
import sqlite3
import os.path


class DB(object):

    def __init__(self,db_name):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_name)
        # 创建数据库连接
        self.dbconn = sqlite3.connect(db_path)

        # 创建字典型游标(返回的数据是字典类型)
        self.dbcur = self.dbconn.cursor()

        # __enter__() 和 __exit__() 是with关键字调用的必须方法
        # with本质上就是调用对象的enter和exit方法

    def __enter__(self):

        # 返回游标
        return self.dbcur

    def __exit__(self, exc_type, exc_value, exc_trace):

        # 提交事务
        self.dbconn.commit()

        # 关闭游标
        self.dbcur.close()

        # 关闭数据库连接
        self.dbconn.close()


def getSqlHead(head=None):
    if head == None:
        return 'select count(*)'
    elif head == '*':
        return 'select rowid, *'
    else:
        return 'select ' + head


def getSqlTablename(tablename):
    return ' from ' + tablename


def getQueryCondition(where_para=None, group_para=None, order_para=None, limit_para=None, offset_para=None):
    queryCondition = ''
    if where_para != None and type(where_para) == type(""):
        queryCondition += ' where ' + where_para
    if where_para != None and type(where_para) == type([]):
        where_para_new = []
        for date in where_para:
            where_para_new.append(list(date.keys())[0] + ' = ' + list(date.values())[0])
        where_para = " and ".join(where_para_new)
        queryCondition += ' where ' + where_para
    if group_para != None:
        queryCondition += ' group by ' + group_para
    if order_para != None:
        queryCondition += ' order by ' + order_para
    if limit_para != None:
        queryCondition += ' limit ' + str(limit_para)
    if offset_para != None:
        queryCondition += ' offset ' + str((int(offset_para)-1) * int(limit_para))
    return queryCondition



def getMachineTable(head=None, where_para=None, group_para=None, order_para=None, limit_para=None, offset_para=None):
    #一个DTO里只能有一次数据库查询
    with DB("machine.db") as db:
        sqlHead = getSqlHead(head)
        sqlTable = getSqlTablename('machine_info')
        if order_para == 'true':
            order_para = 'usage_status ASC'
        if order_para == 'false':
            order_para = 'usage_status DESC'
        queryCondition = getQueryCondition(where_para,group_para,order_para,limit_para,offset_para)

        sql = sqlHead + sqlTable + queryCondition
        query_result = db.execute(sql)

        datalist = []
        for detail in query_result:
            datalist.append(detail)

    return datalist





#初始化函数，建表
def createMachineTable():
    with DB("machine.db") as db:
        sql = 'CREATE TABLE IF NOT EXISTS machine_info(hdm_ip varchar(255), ' \
              'manage_ip varchar(255), password varchar(255), machine_type varchar(255), ' \
              'usage_status int, booking_status int, solution_id int,  owner varchar(255), ' \
              'useage_start_time varchar(255), useage_end_time varchar(255), city int, ' \
              'location varchar(255), booking_start_time varchar(255), booking_end_time varchar(255), is_delete int)'

        db.execute(sql)


def insertMachineTable(hdm_ip_value, manage_ip_value, password_value, machine_type_value, usage_status_value,
                              booking_status_value, solution_id_value, owner_value, useage_start_time_value,
                              useage_end_time_value, city_value, location_value, booking_start_time_value,
                              booking_end_time_value, is_delete_value):

    with DB("machine.db") as db:
        sql = 'INSERT INTO machine_info(hdm_ip, manage_ip, password, ' \
              'machine_type, usage_status, booking_status, solution_id, owner, useage_start_time, useage_end_time, ' \
              'city, location, booking_start_time, booking_end_time, is_delete) VALUES' \
              '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        db.execute(sql, [hdm_ip_value, manage_ip_value, password_value, machine_type_value, usage_status_value,
                         booking_status_value, solution_id_value, owner_value, useage_start_time_value,
                         useage_end_time_value, city_value, location_value, booking_start_time_value,
                         booking_end_time_value, is_delete_value])
        return {"msg": "ok"}


def modifyMachineTable(rowid,update_sql):

    with DB("machine.db") as db:
        sql = "UPDATE machine_info SET%s WHERE rowid = %s"%(update_sql,rowid)
        db.execute(sql)
        return {"msg": "ok"}


def delMachineTable(rowid):

    with DB("machine.db") as db:
        sql = "DELETE FROM machine_info WHERE rowid=%s"%rowid
        db.execute(sql)
        return {"msg": "ok"}


#初始化函数，建表
def createSolutionTable():
    with DB("machine.db") as db:
        sql = 'CREATE TABLE IF NOT EXISTS solution_info(solution_name varchar(255), tc_name varchar(255))'

        db.execute(sql)

def insertSolutionTable(solution_name_value, tc_name_value):

    with DB("machine.db") as db:
        sql = 'INSERT INTO solution_info(solution_name, tc_name) VALUES(?, ?)'
        db.execute(sql, [solution_name_value, tc_name_value])
        return {"msg": "ok"}


def getSolutionTable(head=None, where_para=None, group_para=None, order_para=None, limit_para=None, offset_para=None):
    #一个DTO里只能有一次数据库查询
    with DB("machine.db") as db:
        sqlHead = getSqlHead(head)
        sqlTable = getSqlTablename('solution_info')
        queryCondition = getQueryCondition(where_para,group_para,order_para,limit_para,offset_para)

        sql = sqlHead + sqlTable + queryCondition
        query_result = db.execute(sql)

        datalist = []
        for detail in query_result:
            datalist.append(detail)

    return datalist


def modifySolutionTable(rowid,update_sql):

    with DB("machine.db") as db:
        sql = "UPDATE solution_info SET%s WHERE rowid = %s"%(update_sql,rowid)
        db.execute(sql)
        return {"msg": "ok"}


def delSolutionTable(rowid):

    with DB("machine.db") as db:
        sql = "DELETE FROM solution_info WHERE rowid=%s"%rowid
        db.execute(sql)
        return {"msg": "ok"}


#初始化函数，建表
def createCityTable():
    with DB("machine.db") as db:
        sql = 'CREATE TABLE IF NOT EXISTS city_info(city_name varchar(255))'

        db.execute(sql)


def insertCityTable(city_name_value):

    with DB("machine.db") as db:
        sql = 'INSERT INTO city_info(city_name) VALUES(?)'
        db.execute(sql, [city_name_value])
        return {"msg": "ok"}


def modifyCityTable(rowid,update_sql):

    with DB("machine.db") as db:
        sql = "UPDATE city_info SET%s WHERE rowid = %s"%(update_sql,rowid)
        db.execute(sql)
        return {"msg": "ok"}


def getCityTable(head=None, where_para=None, group_para=None, order_para=None, limit_para=None, offset_para=None):
    #一个DTO里只能有一次数据库查询
    with DB("machine.db") as db:
        sqlHead = getSqlHead(head)
        sqlTable = getSqlTablename('city_info')
        queryCondition = getQueryCondition(where_para,group_para,order_para,limit_para,offset_para)

        sql = sqlHead + sqlTable + queryCondition
        query_result = db.execute(sql)

        datalist = []
        for detail in query_result:
            datalist.append(detail)

    return datalist

def delCityTable(rowid):

    with DB("machine.db") as db:
        sql = "DELETE FROM city_info WHERE rowid=%s"%rowid
        db.execute(sql)
        return {"msg": "ok"}

# if __name__ == '__main__':
#     query_result = createCityTable()



