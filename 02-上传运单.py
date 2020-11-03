from daihuoguanjia_stress import *

# 上传运单号并发测试
threads = []
#多少个用户数并发(-1)
user_num = 81
#存放token
token = []
for i in range(1,user_num):
    if i>102:
        print("最多只支持101的并发用户数量")
    else:
        print('xncs%s'%i+"用户登录操作！")
        #获取商户端token
        sh_token = login('xncs%s'%i)
        token.append(sh_token)
        #获取订单列表1000单(平台为快手小店同步订单)
        order_list = list_order(sh_token,0,1000,8)
        # 查询快递模板
        expressTemplateId = list_expressTemplate(sh_token)
        # 设置快递模板
        orderTemplate(sh_token, order_list, expressTemplateId, i)
        # 审核订单
        audit_order(sh_token, order_list, i)
        #获取运单
        get_waybill(sh_token,order_list,i)
        #获取运单列表1000单
        waybill_list = list_waybill(sh_token,1000)
        print(waybill_list)
        # sync(sh_token, waybill_list, i)
        # 创建线程（上传运单号）
        t = threading.Thread(target=sync, args=(sh_token, waybill_list, i))
        threads.append(t)
print(threads,len(threads))
#开始时间
start_time = time.strftime('%Y%m%d%H%M%S')
print("开始时间{}".format(start_time))
#启动线程
for i in range(user_num-1):
    threads[i].start()
for i in range(user_num-1):
    threads[i].join()
#退出登录
for i in range(user_num-1):
    logout(token[i],i+1)
#结束时间
end_time = time.strftime('%Y%m%d%H%M%S')
print("开始时间{}".format(start_time))
print("结束时间{}".format(end_time))
print("运行时间{}".format(int(end_time)-int(start_time)))