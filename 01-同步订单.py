from daihuoguanjia_stress import *

# 同步订单并发测试
threads = []
#多少个用户数并发
user_num = 100
#存放token
token = []
for i in range(user_num):
    # 1、新建商家
    op_token = op_login('zxw01')
    op_create_user(op_token, i)
    # 3、每个商家新建店铺
    user_token = user_login(i)
    token.append(user_token)
    user_create_shop(user_token,i)
    # 4、数据库授权
    auth_shop(i)
    # 5、多线程开始100个商家同时拉单，统计从拉单开始到拉单结束
    shopcode = get_shopcode(i)
    # 创建线程
    t = threading.Thread(target=sys_order, args=(user_token, shopcode, i))
    threads.append(t)
print(threads,len(threads))
#开始时间
start_time = time.strftime('%Y%m%d%H%M%S')
print("开始时间{}".format(start_time))
#启动线程
for i in range(user_num):
    threads[i].start()
for i in range(user_num):
    threads[i].join()
#退出登录
for i in range(user_num):
    logout(token[i])
#结束时间
end_time = time.strftime('%Y%m%d%H%M%S')
print("开始时间{}".format(start_time))
print("结束时间{}".format(end_time))
print("运行时间{}".format(int(end_time)-int(start_time)))