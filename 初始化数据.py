import json,requests,hashlib,base64,xmltodict,time
from daihuoguanjia_stress import *

# #新增100个商户
# for i in range(1,102):
#     op_token = op_login('zxw01')
#     op_user(op_token, i)

# #添加导入的订单-每个商户5000条
# for i in range(1,102):
#     token = login('xncs%s'%i)
#     addressId = get_adress(token)
#     import_order(token, addressId, i)
#     logout(token,i)
#
# #添加同步的订单-每个商户1000条
# for i in range(1,102):
#     token = login('xncs%s'%i)
#     scode = shopcode(i)
#     sys_order(token,scode,i)
#     logout(token, i)
#
# # 新建快手店铺
# for n in range(1,102):
#     user_token = login('xncs%s'%n)
#     user_create_shop(user_token,n)
#     logout(user_token,n)
#
# #新建bsp快递模板-设置为默认
# for n in range(1,102):
#     user_token = login('xncs%s'%n)
#     add_expressTemplate(user_token,n)
#     templateId = list_expressTemplate(user_token)
#     default_expressTemplate(user_token, templateId, n)
#     logout(user_token,n)
#     time.sleep(2)


