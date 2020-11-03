#coding=utf-8
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os, time
import configparser as cparser


# ======== 读取db_config.ini文件设置 ===========
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = r"E:\tem\lsec\db_config.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

# host = cf.get("mysqlconf", "host")
# port = cf.get("mysqlconf", "port")
# db   = cf.get("mysqlconf", "db_name")
# user = cf.get("mysqlconf", "user")
# password = cf.get("mysqlconf", "password")

host = cf.get("lsecpetmysqlconf", "host")
port = cf.get("lsecpetmysqlconf", "port")
db   = cf.get("lsecpetmysqlconf", "db_name")
user = cf.get("lsecpetmysqlconf", "user")
password = cf.get("lsecpetmysqlconf", "password")


# ======== 封装MySql基本操作 ===================
class DB:

    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(host=host,
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表中所有数据
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()
        print("delete table:%s success!"%table_name)

    # 根据条件，清除表中数据
    def clear_condition(self, table_name, condition):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + " where " + condition + ";"
        # print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.conn.commit()
        print("delete table:%s where %s success!"%(table_name,condition))

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ");"
        #print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        print("insert table:%s values:%s"%(table_name,table_data))

    # 更新表数据
    def update(self, table_name, data, condition):
        real_sql = "update " + table_name + " set " + data + " where " + condition + ";"
        # print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()
        # print(real_sql)

    #查询表数据--返回查询结果
    def selcet_data(self, column_name, table_name, condition):
        real_sql = "select " + column_name + " from "+ table_name + " where " + condition + ";"
        # print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
            pnlist = []
            alldata = cursor.fetchall()
            for singl_company in alldata:
                pnlist.append(singl_company)
        self.conn.commit()
        return pnlist
        # print(real_sql)


    # 关闭数据库连接
    def close(self):
        self.conn.close()

if __name__ == '__main__':

    # db = DB()
    # table_name = "sign_event"
    # data = {'id':1,'name':'iphone X','`limit`':2000,'status':1,'address':'shenzhen','start_time':'2017-12-25 12:00:00','create_time':'2017-10-9 15:15:00'}
    #
    # db.clear(table_name)
    # db.insert(table_name, data)
    # db.clear_condition(table_name, "id=2")
    # db.close()

    # table_name = "sign_guest"
    # data = {'id':1,'realname':'alen','phone':13511001100,'email':'alen@mail.com','sign':0,'event_id':1,'create_time':'2017-10-9 15:15:00'}
    # db.clear(table_name)
    # db.insert(table_name, data)
    # db.close()
    #




    # table_name = "sign_guest"
    # db.clear(table_name)
    # for i in range(1,3001):
    #     id = i
    #     realname = 'zeng'+ str(i)
    #     phone = 13811000000+i
    #     email = 'zeng0' + str(i) + "@mail.com"
    #     data = {'id':id,'realname':realname,'phone':phone,'email':email,'sign':0,'event_id':1,'create_time':'2017-12-25 15:00:00'}
    #
    #
    #
    #     db.insert(table_name, data)
    # db.close()


    # #############进销存系统---创建订单
    # db = DB()
    # table_name = "oms_o_waybill"
    # #
    # # data = {'order_no':'CBA1001919888842','mail_no':'4441590246508328',
    # #         'express_name': '顺丰速运', 'express_code': 'sf',
    # #         'd_contact':'郭美美','d_address':'北京东城区东城大道3栋7楼','d_tel':'123321',
    # #         'j_contact':'曾祥卫','j_tel':'123232','j_address':'广东深圳软件产业基地1栋C座7楼',
    # #         '`number`':2,'collecting_money':0,'`status`':3,'tenant_id':'zxw-oms','batch_no':2,'create_time':'2020-04-08 10:00:00'}
    # # db.insert(table_name, data)
    # # db.close()
    #
    # # #######db.clear(table_name)
    # for i in range(0,100):
    #     data = {'order_no': 'CBA10019198888'+time.strftime("%H%M%S"), 'mail_no': '4441590246508888'+time.strftime("%H%M%S"),
    #             'express_name': '自提', 'express_code': 'other',
    #         'd_contact':'郭美美','d_address':'北京东城区东城大道3栋7楼','d_tel':'123321',
    #         'j_contact':'曾祥卫','j_tel':'123232','j_address':'广东深圳软件产业基地1栋C座7楼',
    #         '`number`':2,'collecting_money':0,'`status`':65,'tenant_id':'zxw-oms','batch_no':2,'create_time':'2020-04-07 10:00:00'}
    #
    #
    #     # time.sleep(1)
    #     db.insert(table_name, data)
    # db.close()

    #############进销存系统---商品类别
    # db = DB()
    # table_name = "p_category"
    # # #
    # # # data = {'order_no':'CBA1001919888842','mail_no':'4441590246508328',
    # # #         'express_name': '顺丰速运', 'express_code': 'sf',
    # # #         'd_contact':'郭美美','d_address':'北京东城区东城大道3栋7楼','d_tel':'123321',
    # # #         'j_contact':'曾祥卫','j_tel':'123232','j_address':'广东深圳软件产业基地1栋C座7楼',
    # # #         '`number`':2,'collecting_money':0,'`status`':3,'tenant_id':'zxw-oms','batch_no':2,'create_time':'2020-04-08 10:00:00'}
    # # # db.insert(table_name, data)
    # # # db.close()
    # # #INSERT INTO `p_category_tenant` (`p_category_id`, `tenant_id`) VALUES ('286', 'lc-oms');
    # #
    # # # #######db.clear(table_name)
    # for i in range(510, 1100):
    #     data = {'`category_code`':'LB88800{}'.format(1+i),'`category_name`':"自动类别"+str(i)}
    #
    #     # time.sleep(1)
    #     db.insert(table_name, data)
    # db.close()



    # db = DB()
    # table_name = "p_category_tenant"
    # for i in range(801, 1391):
    #     data = {'`p_category_id`':str(i),'`tenant_id`':'lc-oms'}
    #
    #     # time.sleep(1)
    #     db.insert(table_name, data)
    # db.close()


    ############进销存系统---计量单位
    # db = DB()
    # table_name = "p_units"
    # # #
    # # # data = {'order_no':'CBA1001919888842','mail_no':'4441590246508328',
    # # #         'express_name': '顺丰速运', 'express_code': 'sf',
    # # #         'd_contact':'郭美美','d_address':'北京东城区东城大道3栋7楼','d_tel':'123321',
    # # #         'j_contact':'曾祥卫','j_tel':'123232','j_address':'广东深圳软件产业基地1栋C座7楼',
    # # #         '`number`':2,'collecting_money':0,'`status`':3,'tenant_id':'zxw-oms','batch_no':2,'create_time':'2020-04-08 10:00:00'}
    # # # db.insert(table_name, data)
    # # # db.close()
    # # #INSERT INTO `p_category_tenant` (`p_category_id`, `tenant_id`) VALUES ('286', 'lc-oms');
    # #
    # # # #######db.clear(table_name)
    # for i in range(600, 1101):
    #     data = {'`units_name`':"自动"+str(i)}
    #
    #     # time.sleep(1)
    #     db.insert(table_name, data)
    # db.close()


    # db = DB()
    # table_name = "p_units_tenant"
    # for i in range(678, 1179):
    #     data = {'`p_units_id`':str(i),'`tenant_id`':'lc-oms'}
    #
    #     # time.sleep(1)
    #     db.insert(table_name, data)
    # db.close()


    ###########直播电商--店铺管理
    db = DB()
    table_name = "o_shop"
    # db.update(table_name,"`authorize`=1","`name` = '性能测试店铺'")
    a = db.selcet_data("code", table_name, "`name` = '性能测试店铺'")
    print(a)
    db.close()






