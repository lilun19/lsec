# coding=utf-8
import requests, time, threading, json, random
import traceback
from mysql_db import DB
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 志军
# op_url='http://100.119.78.116:8080/'
# 压测环境
op_url = 'http://op-erp-pet.sf-express.com/api'

# 志军
# user_url = 'http://100.119.78.116:8088/'
# 压测环境
# user_url = 'http://10.211.16.36/api'
user_url = 'http://erp-pet.sf-express.com/api'
now = time.strftime('%Y%m%d%H%M')


# 登录运营端,并取出token值
def op_login(op_user):
    r = requests.post(op_url + "/manager/logintest?username={}".format(op_user))
    print(r.text)
    op_token = r.headers['token']
    # print(op_token)
    return op_token


# 运营端创建用户
def op_create_user(op_token, i):
    params = {"name": "自动性能测试店铺{}_{}".format(now, i), "isTestAccount": 0, "contactMan": "", "contactAddress": "",
              "supportedExpressIds": "1", "businessAreaCode": "755Y", "sfmarketCode": "",
              "expectedAmountMonthly": "2000", "joinType": 1, "customerFrom": 1, "joinMan": "曾祥卫", "creatorId": 86,
              "versionId": 7, "username": "xncs{}_{}".format(now, i), "contactPhone": "13048843947", "status": 0}
    headers = {"Content-Type": "application/json",
               "token": op_token}
    requests.post(op_url + "/manager/merchantinfo", headers=headers, json=params, timeout=30000)


# 运营端创建用户
def op_user(op_token, i):
    params = {"name": "自动性能测试店铺{}".format(i), "isTestAccount": 0, "contactMan": "", "contactAddress": "",
              "supportedExpressIds": "1", "businessAreaCode": "755Y", "sfmarketCode": "",
              "expectedAmountMonthly": "2000", "joinType": 1, "customerFrom": 1, "joinMan": "曾祥卫", "creatorId": 86,
              "versionId": 7, "username": "xncs{}".format(i), "contactPhone": "13048843947", "status": 0}
    headers = {"Content-Type": "application/json", "token": op_token}
    r = requests.post(op_url + "/manager/merchantinfo", headers=headers, json=params, timeout=30000)
    print(r.text)


# 登录商家端,并取出token值
def user_login(i):
    r = requests.post(user_url + "/sys/user/logintest?username=xncs{}_{}".format(now, i))
    print(r.text)
    user_token = r.headers['token']
    print(user_token)
    return user_token


def login(username):
    LoginUrl = user_url + "/sys/user/logintest?username=" + username
    # print(LoginUrl+'\n'+username)
    response = requests.request("POST", LoginUrl, timeout=30000)
    # print(response.text)
    print(response.headers['token'])
    return response.headers['token']


# 退出登录
def logout(token, i=None):
    headers = {'Content-Type': 'application/json', 'token': token}
    requests.post(user_url + "/sys/user/logout", headers=headers, timeout=30000)
    # resCode = response.status_code
    # resBody = response.json()
    # if resCode == 200:
    #     if 'ok' in resBody.get('code'):
    #         print("退出登录成功{}".format(i))
    #     else:
    #         print("退出登录失败{}".format(i))
    # else:
    #     print("退出登录失败{}".format(i))


# 查询月结
def get_monthlyCard(user_token):
    headers = {'token': user_token}
    res = requests.get(user_url + "/waybill/expressproduct/monthlycard/get", headers=headers, timeout=30000)
    result = json.loads(res.text)
    expressCompanyMerchantId = result["result"][0]["expressCompanyMerchantId"]
    expressCompanyName = result["result"][0]["expressCompanyName"]
    expressProductId = result["result"][0]["expressProductId"]
    expressProductName = result["result"][0]["expressProductName"]
    id = result["result"][0]["id"]
    monthlyCard = result["result"][0]["monthlyCard"]
    month = {"expressCompanyMerchantId": expressCompanyMerchantId, "expressCompanyName": expressCompanyName,
             "expressProductId": expressProductId, "expressProductName": expressProductName, "id": id,
             "monthlyCard": monthlyCard}
    return month


# 查询用户月结物流
def get_expressMessage(user_token):
    headers = {'token': user_token}
    res = requests.get(user_url + "/sys/user/monthlycard/get/expandproandcard?isSpecialMonthly=0&shopCode=",
                       headers=headers, timeout=30000)
    result = json.loads(res.text)
    expressCompanyMerchantId = result["result"]["expressProductVoList"][0]["expressCompanyMerchantId"]
    userMonthlyId = result["result"]["monthlyCardVoList"][0]["userMonthlyId"]
    expressProductId = result["result"]["expressProductVoList"][0]["expressProductId"]
    express = {"expressCompanyMerchantId": expressCompanyMerchantId, "userMonthlyId": userMonthlyId,
               "expressProductId": expressProductId, }
    return express


# 批量设置物流
def setLogistic(user_token, express, order_list, i):
    Logistic_headers = {"Content-Type": "application/json", "token": user_token}
    order_list = ','.join(order_list)
    Logistic_params = {"isSpecialMonthly": 0, "expressCompanyMerchantId": express["expressCompanyMerchantId"],
                       "expressProductId": express["expressProductId"],
                       "expressPayMethod": 1, "userMonthlyId": express["userMonthlyId"],
                       "collectionCardNumber": "9999999999", "parcelWeight": 0, "freshServices": "", "selfPickup": "",
                       "orderNos": order_list}
    print(Logistic_params)
    response = requests.put(user_url + "/order/sale/list", json=Logistic_params, headers=Logistic_headers,
                            timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("设置物流成功{}".format(i))
        else:
            print("设置物流失败{}".format(i))
    else:
        print("设置物流失败{}".format(i))


# 查询用户列表-获取用户id
def list_user(user_token):
    headers = {'Content-Type': 'application/json', 'token': user_token}
    params = {"truename": "", "username": "", "organId": "", "creatorId": "", "current": 1, "size": 50}
    res = requests.post(user_url + "/sys/user/list", headers=headers, json=params, timeout=30000)
    result = json.loads(res.text)
    user_id = result["result"]["records"][0]["userId"]
    return user_id


# 根据id查询用户详情
def user_detail(user_token, user_id):
    headers = {'Content-Type': 'application/json', 'token': user_token}
    res = requests.get(user_url + "/sys/user/" + str(user_id), headers=headers, timeout=30000)
    result = json.loads(res.text)
    detail = {}
    detail["organId"] = result["result"]["organId"]
    detail["roleIds"] = result["result"]["roleIds"]
    detail["merchantUsername"] = result["result"]["merchantUsername"]
    detail["username"] = result["result"]["username"]
    return detail


# 修改用户绑定月结
def modify_user(user_token, user_id, month, detail, i):
    headers = {'Content-Type': 'application/json', 'token': user_token}
    data = {"userMonthlyCardVOList": [
        {"id": month["id"], "monthlyCard": "9999999999", "expressCompanyMerchantId": month["expressCompanyMerchantId"],
         "expressCompanyName": month["expressCompanyName"], "expressProductId": month["expressProductId"],
         "expressProductName": month["expressProductName"]}],
            "organId": detail["organId"], "roleIds": detail["roleIds"], "truename": "", "email": "",
            "merchantUsername": detail["merchantUsername"], "username": detail["username"],
            "phone": "13048843947", "defaultMonthlyCard": month["id"], "defaultSpecialMonthlyCard": "",
            "directorFlag": 0}
    r = requests.put(user_url + "/sys/user/" + str(user_id) + "/update", headers=headers, json=data, timeout=30000)
    resCode = r.status_code
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("绑定月结卡号成功{}".format(i))
        else:
            print("绑定月结卡号失败{}".format(i))
    else:
        print("绑定月结卡号失败{}".format(i))


# 商家新建店铺
def user_create_shop(user_token, i):
    headers = {'Content-Type': 'application/json', 'token': user_token}
    params = {"platformType": 7, "childPlatformType": 8, "name": "性能测试店铺{}_{}".format(now, i), "remark": "",
              "addressVos": {"addressId": '', "phone": "15623548956", "telephone": "",
                             "contact": "季玉恒", "province": "北京", "provinceId": 2, "city": "北京市", "cityId": 3,
                             "district": "海淀区", "districtId": 9, "detailAddress": "上园村3号",
                             "senderAddress": "季玉恒  15623548956 北京北京市海淀区上园村3号"}}
    res = requests.post(user_url + "/order/shop", headers=headers, json=params, timeout=30000)
    # print(res.status_code,res.json())


# 给商家店铺授权
def auth_shop(i):
    db = DB()
    table_name = "o_shop"
    db.update(table_name, "`authorize`=1", "`name` = '性能测试店铺{}_{}'".format(now, i))
    # a = db.selcet_data("code", table_name, "`name` = '性能测试店铺'")
    # print(a)
    db.close()


# 查询商家店铺的shopcode
def get_shopcode(i):
    db = DB()
    table_name = "o_shop"
    a = db.selcet_data("code", table_name, "`name` = '性能测试店铺{}_{}'".format(now, i))
    # print(a)
    db.close()
    # print(a[0].get('code'))
    return a[0].get('code')


def shopcode(i):
    db = DB()
    table_name = "o_shop"
    print('获取性能测试店铺{}的shopcode'.format(i))
    a = db.selcet_data("code", table_name, "`name` = '快手性能测试店铺{}'".format(i))
    db.close()
    print(a[0].get('code'))
    return a[0].get('code')


# 商家同步订单
def sys_order(user_token, shopcode, i):
    headers1 = {"Content-Type": "application/json",
                "token": user_token}
    params = {"childPlatformType": 8, "shopCode": shopcode, "isQueryTotalRequest": 0, "isArrowDeleteOldData": 1,
              "synTimeStart": 1599926400, "synTimeEnd": 1600012799}
    r = requests.post(user_url + "/order/sale/integrateLubanSaleOrder", json=params, headers=headers1, timeout=30000)
    resCode = r.status_code
    print(r)
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("同步成功{}".format(i))
        else:
            print("同步失败{}".format(i))
    else:
        print("同步失败{}".format(i))


# 订单列表获取1000条订单(待审核：verifyStatus=0，已审核未发货：verifyStatus=1，sendStatus=0)
def list_order(user_token, verifyStatus, size, childPlatformType=None):
    list_headers = {"Content-Type": "application/json", "token": user_token}
    list_params = {"current": 1, "size": size, "dateTimeType": "1", "organId": "", "creatorId": "", "oddNumber": "",
                   "oddNumberType": "originalOrderNo",
                   "status": "0", "sendStatus": "", "waybillStatus": "", "childPlatformType": "", "shopCode": "",
                   "originalOrderNo": "", "exceptionFlagStr": "",
                   "consigneeName": "", "consigneePhone": "", "expressPayMethod": "", "isDocall": "",
                   "userMonthlyId": "", "collectionCardNumber": "",
                   "verifyStatus": "0", "stockOutStatus": "", "warehouseCode": "", "customerCode": "",
                   "flowDirection": "", "remark": "", "buyerMessage": "",
                   "sellerMessage": "", "productName": "", "productNameType": "1", "merchantCode": "",
                   "expressCompanyMerchantId": "", "expressProductId": "",
                   "orderPayMethod": "", "minCollectingMoney": "", "maxCollectingMoney": "", "minConsignmentNumber": "",
                   "maxConsignmentNumber": "",
                   "minNumber": "", "maxNumber": "", "consignment": "", "consignmentType": "1", "selfPickup": "",
                   "attributeNames": "", "minProductNumber": "",
                   "maxProductNumber": "", "codeType": "1", "productCodeOrSkuCodes": "", "createTimeStart": "",
                   "createTimeEnd": ""}
    if verifyStatus == 0:
        response = requests.post(user_url + "/order/sale/page", json=list_params, headers=list_headers, timeout=30000)
        result = json.loads(response.text)
        orders = result["result"]["page"]["records"]
        order_list = [order["orderNo"] for order in orders]
    elif verifyStatus == 1:
        list_params["verifyStatus"] = 1
        list_params["sendStatus"] = 0
        response = requests.post(user_url + "/order/sale/page", json=list_params, headers=list_headers, timeout=30000)
        result = json.loads(response.text)
        orders = result["result"]["page"]["records"]
        order_list = [order["orderNo"] for order in orders]
    return order_list


# 审核订单
def audit_order(user_token, order_list, i):
    audit_headers = {"Content-Type": "application/x-www-form-urlencoded", "token": user_token}
    audit_params = "orderNos=" + ','.join(order_list)
    response = requests.put(user_url + "/order/sale/batch/audit", data=audit_params, headers=audit_headers,
                            timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("审核成功{}".format(i))
        else:
            print("审核失败{}".format(i))
    else:
        print("审核失败{}".format(i))


# 获取运单
def get_waybill(user_token, order_list, i):
    waybill_headers = {"Content-Type": "application/x-www-form-urlencoded", "token": user_token}
    waybill_params = "orderNos=" + ','.join(order_list)
    # print(waybill_params)
    response = requests.post(user_url + "/order/sale/transport", data=waybill_params, headers=waybill_headers,
                             timeout=30000)
    print(response)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("获取运单成功{}".format(i))
        else:
            print("获取运单失败{}".format(i))
    else:
        print("获取运单失败{}".format(i))


# 运单列表获取1000条运单（未上传）
def list_waybill(user_token, size):
    list_headers = {"Content-Type": "application/json", "token": user_token}
    list_params = {"current": 1, "size": size, "dateTimeType": "1", "organId": "", "creatorId": "", "oddNumber": "",
                   "oddNumberType": "mailNo", "waybillStatus": "",
                   "printStatus": "", "printNumber": "", "alterpriceStatus": "", "childPlatformType": "",
                   "shopCode": "", "expressCompanyMerchantId": "",
                   "expressProductId": "", "expressPayMethod": "", "consigneeName": "", "consigneePhone": "",
                   "isDocall": "", "isCanceldocall": 0, "userMonthlyId": "",
                   "collectionCardNumber": "", "customerCode": "", "flowDirection": "", "remark": "",
                   "buyerMessage": "", "sellerMessage": "", "productName": "",
                   "productNameType": "1", "merchantCode": "", "consignment": "", "consignmentType": "1",
                   "exceptionFlagStr": "", "orderPayMethod": "",
                   "minCollectingMoney": "", "maxCollectingMoney": "", "minConsignmentNumber": "",
                   "maxConsignmentNumber": "", "minNumber": "", "maxNumber": "",
                   "selfPickup": "", "exceptionFlag": 0, "attributeNames": "", "createTimeStart": "",
                   "createTimeEnd": "", "uploadMailnoStatusStr": ""}
    response = requests.post(user_url + "/waybill/page", json=list_params, headers=list_headers, timeout=30000)
    result = json.loads(response.text)
    mailnos = result["result"]["records"]
    print("mailnos={}".format(mailnos))
    mailno_list = [mailno["mailNo"] for mailno in mailnos]
    print("mailno_list={}".format(mailno_list))
    return mailno_list


# 上传运单号
def sync(user_token, mailno_list, i):
    sync_headers = {"Content-Type": "application/x-www-form-urlencoded", "token": user_token}
    sync_params = "mailNos=" + ','.join(mailno_list) + "&syncType=0"
    # print(sync_params)
    response = requests.post(user_url + "/order/sale/sync", data=sync_params, headers=sync_headers, timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("上传运单号成功{}".format(i))
        else:
            print("上传运单号失败{}".format(i))
    else:
        print("上传运单号失败{}".format(i))


# 查询商品类别
def list_category(user_token):
    headers = {'token': user_token}
    res = requests.get(user_url + "/inventory/category/all", headers=headers, timeout=30000)
    result = json.loads(res.text)
    categorylist = {}
    categorylist["categoryId"] = result["result"]["list"][0]["categoryId"]
    categorylist["categoryName"] = result["result"]["list"][0]["categoryName"]
    categorylist["attributeIds"] = result["result"]["list"][0]["attributeIds"]
    return categorylist


# 获取规格id
def get_attributeIds(user_token, categorylist):
    headers = {'token': user_token}
    res = requests.get(user_url + "/inventory/attribute/all?categoryId=%s&organId=" % categorylist["categoryId"],
                       headers=headers, timeout=30000)
    result = json.loads(res.text)
    attributeIds = result["result"]["list"][0]["attributeDetailVoList"][0]["id"]
    return attributeIds


# 增加商品
def add_goods(user_token, categorylist, attributeIds, i):
    headers = {"Content-Type": "application/json",
               "token": user_token}
    params = {"productCode": "x%s" % now, "productName": "性能测试产品", "categoryName": categorylist["categoryName"],
              "categoryId": categorylist["categoryId"],
              "purchaseDecimal": 0, "unitsId": "", "status": 0, "remark": "", "shortName": "",
              "productSkuList": [{"merchantCode": "", "skuCode": "sku000", "barcode": "", "volume": "", "netWeight": "",
                                  "roughWeight": "", "primePrice": "",
                                  "wholesalePrice": "", "retailPrice": "",
                                  "attributeIds": str(categorylist["attributeIds"]) + ":" + str(attributeIds),
                                  "attributeNames": "通用:通用"}]}
    r = requests.post(user_url + "/inventory/product/insert", json=params, headers=headers, timeout=30000)
    resCode = r.status_code
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("新增商品成功{}".format(i))
        else:
            print("新增商品失败{}".format(i))
    else:
        print("新增商品失败{}".format(i))


# 新增寄件人
def add_adress(user_token, i):
    headers = {"Content-Type": "application/json", "token": user_token}
    params = {"receivingSenderNo": "JJR200727737322%s" % random.randint(0, 999999999999),
              "receivingSenderName": "性能测试寄件人", "receivingSenderPhone": "13048843947",
              "receivingSenderTelphone": "", "company": "", "remark": "", "province": "广东省", "provinceId": 2077,
              "city": "深圳市", "cityId": 2101,
              "district": "宝安区", "districtId": 2105, "detailAddress": "茶树新村7巷2号"}
    r = requests.post(user_url + "/order/sale/address/sender", json=params, headers=headers, timeout=30000)
    resCode = r.status_code
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("新增寄件人成功{}".format(i))
        else:
            print("新增寄件人失败{}".format(i))
    else:
        print("新增寄件人失败{}".format(i))


# 获取寄件人id
def get_adress(user_token):
    headers = {'token': user_token}
    res = requests.get(user_url + "/order/sale/address/sender/list", headers=headers, timeout=30000)
    print("获取寄件人接口返回" + str(res))
    result = json.loads(res.text)
    addressId = result["result"]["list"][0]["addressId"]
    return addressId


# 导入订单
def import_order(user_token, addressId, i):
    headers1 = {"token": user_token}
    multipart_encoder = MultipartEncoder(
        fields={
            # 这里根据服务器需要的参数格式进行修改
            'file': (
                'file.xlsx', open(r"E:\lsec_csv\导入订单标准模板.xlsx", 'rb'),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),

            'templateCode': 'OrderTemplate',
            'isSelection': '1',
            'addressId': str(addressId)
        },
        boundary='------' + str(random.randint(1e28, 1e29 - 1)))
    headers1['Content-Type'] = multipart_encoder.content_type
    try:
        r = requests.post(user_url + "/order/sale/import", data=multipart_encoder, headers=headers1, timeout=30000)
        print(r)
        resCode = r.status_code
        resBody = r.json()
        if resCode == 200:
            if 'ok' in resBody.get('code'):
                print("导入订单成功{}".format(i))
            else:
                print("导入订单失败{}".format(i))
                print(resBody)
        else:
            print("导入订单失败{}".format(i))
            print(resBody)
    except Exception as e:
        print(time.strftime('%Y%m%d%H%M%S') + "--xncs%s用户导入失败" % (i))
        print('traceback.format_exc():\n%s' % traceback.format_exc())


# 导出订单
def export_order(user_token, i):
    headers = {"Content-Type": "application/json", "token": user_token}
    params = {"dateTimeType": "1", "organId": "", "creatorId": "", "oddNumber": "", "oddNumberType": "originalOrderNo",
              "status": "", "sendStatus": "", "waybillStatus": "",
              "childPlatformType": "", "shopCode": "", "originalOrderNo": "", "exceptionFlagStr": "",
              "consigneeName": "", "consigneePhone": "", "expressPayMethod": "",
              "isDocall": "", "userMonthlyId": "", "collectionCardNumber": "", "verifyStatus": "", "stockOutStatus": "",
              "warehouseCode": "", "customerCode": "",
              "flowDirection": "", "remark": "", "buyerMessage": "", "sellerMessage": "", "productName": "",
              "productNameType": "1", "merchantCode": "",
              "expressCompanyMerchantId": "", "expressProductId": "", "orderPayMethod": "", "minCollectingMoney": "",
              "maxCollectingMoney": "",
              "minConsignmentNumber": "", "maxConsignmentNumber": "", "minNumber": "", "maxNumber": "",
              "consignment": "", "consignmentType": "1", "selfPickup": "",
              "attributeNames": "", "minProductNumber": "", "maxProductNumber": "", "codeType": "1",
              "productCodeOrSkuCodes": "", "createTimeStart": "",
              "createTimeEnd": "", "fileName": "销售订单%s" % now, "code": ""}
    r = requests.post(user_url + "/order/sale/export", json=params, headers=headers, timeout=30000)
    resCode = r.status_code
    if resCode == 200:
        print("导出订单成功{}".format(i))
    else:
        print("导出订单失败{}".format(i))


# 批量配置打印机
def independentprint(user_token, i):
    headers = {"Content-Type": "application/json", "token": user_token}
    params = {"independentPrintId": 0, "printer": "ZDesigner GK888d (EPL)", "printPluginType": 1, "isPreview": 1,
              "printTemplate": 1, "formatType": 1,
              "isExpressTypecodeSensitive": 1, "templateCode": ""}
    r = requests.post(user_url + "/waybill/independentprint", json=params, headers=headers, timeout=30000)
    resCode = r.status_code
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("配置打印机成功{}".format(i))
        else:
            print("配置打印机失败{}".format(i))
    else:
        print("配置打印机失败{}".format(i))


# 批量打印运单
def batchprint(user_token, mailno_list, i):
    batchprint_headers = {"Content-Type": "application/x-www-form-urlencoded", "token": user_token}
    batchprint_params = "mailNos=" + ','.join(mailno_list)
    # print(batchprint_params)
    response = requests.post(user_url + "/waybill/batchprint", data=batchprint_params, headers=batchprint_headers,
                             timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("批量打印成功{}".format(i))
        else:
            print("批量打印失败{}".format(i))
    else:
        print("批量打印失败{}".format(i))


# 导出运单
def batchexport(user_token, i):
    headers = {"Content-Type": "application/json", "token": user_token}
    params = {"dateTimeType": "1", "organId": "", "creatorId": "", "oddNumber": "", "oddNumberType": "mailNo",
              "waybillStatus": "", "printStatus": "", "printNumber": "",
              "alterpriceStatus": "", "childPlatformType": "", "shopCode": "", "expressCompanyMerchantId": "",
              "expressProductId": "", "expressPayMethod": "",
              "consigneeName": "", "consigneePhone": "", "isDocall": "", "isCanceldocall": 0, "userMonthlyId": "",
              "collectionCardNumber": "", "customerCode": "",
              "flowDirection": "", "remark": "", "buyerMessage": "", "sellerMessage": "", "productName": "",
              "productNameType": "1", "merchantCode": "", "consignment": "",
              "consignmentType": "1", "exceptionFlagStr": "", "orderPayMethod": "", "minCollectingMoney": "",
              "maxCollectingMoney": "", "minConsignmentNumber": "",
              "maxConsignmentNumber": "", "minNumber": "", "maxNumber": "", "selfPickup": "", "exceptionFlag": 0,
              "attributeNames": "", "createTimeStart": "",
              "createTimeEnd": "", "uploadMailnoStatusStr": "", "fileName": "运单列表%s" % now, "excelType": 2, "code": ""}
    r = requests.post(user_url + "/waybill/batchexport", json=params, headers=headers, timeout=30000)
    resCode = r.status_code
    if resCode == 200:
        print("导出运单成功{}".format(i))
    else:
        print("导出运单失败{}".format(i))


# 运单列表获取1000个运单id
def get_waybillid(user_token, size):
    list_headers = {"Content-Type": "application/json", "token": user_token}
    list_params = {"current": 1, "size": size, "dateTimeType": "1", "organId": "", "creatorId": "", "oddNumber": "",
                   "oddNumberType": "mailNo", "waybillStatus": "",
                   "printStatus": "", "printNumber": "", "alterpriceStatus": "", "childPlatformType": "",
                   "shopCode": "", "expressCompanyMerchantId": "",
                   "expressProductId": "", "expressPayMethod": "", "consigneeName": "", "consigneePhone": "",
                   "isDocall": "", "isCanceldocall": 0, "userMonthlyId": "",
                   "collectionCardNumber": "", "customerCode": "", "flowDirection": "", "remark": "",
                   "buyerMessage": "", "sellerMessage": "", "productName": "",
                   "productNameType": "1", "merchantCode": "", "consignment": "", "consignmentType": "1",
                   "exceptionFlagStr": "", "orderPayMethod": "",
                   "minCollectingMoney": "", "maxCollectingMoney": "", "minConsignmentNumber": "",
                   "maxConsignmentNumber": "", "minNumber": "", "maxNumber": "",
                   "selfPickup": "", "exceptionFlag": 0, "attributeNames": "", "createTimeStart": "",
                   "createTimeEnd": "", "uploadMailnoStatusStr": ""}
    response = requests.post(user_url + "/waybill/page", json=list_params, headers=list_headers, timeout=30000)
    result = json.loads(response.text)
    mailnos = result["result"]["records"]
    print("mailnos={}".format(mailnos))
    waybillId_list = [mailno["waybillId"] for mailno in mailnos]
    print(waybillId_list)
    return waybillId_list


# 取消运单
def batchcancel_waybill(user_token, waybillId_list, i):
    waybill_headers = {"Content-Type": "application/x-www-form-urlencoded", "token": user_token}
    waybill_params = "waybillIds="
    for waybillId in waybillId_list:
        waybill_params = waybill_params + str(waybillId).strip() + ','
    waybill_params = waybill_params[:-1]
    print(waybill_params)
    response = requests.post(user_url + "/waybill/batchcancel", data=waybill_params, headers=waybill_headers,
                             timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("取消运单成功{}".format(i))
        else:
            print("取消运单失败{}".format(i))
    else:
        print("取消运单失败{}".format(i))


# 新建快递模板
def add_expressTemplate(user_token, i):
    template_headers = {"Content-Type": "application/json", "token": user_token}
    # 顺丰-BSP-顺丰标快
    template_params = {"expressCompanyCode": "SF", "expressCompanyId": 44, "templateCode": "SF002",
                       "templateName": "顺丰-BSP-标快%s" % (i), "expressCompanyName": "顺丰速运",
                       "templateType": 2, "pddTemplateUrl": "", "printPluginType": 2, "printerName": "ZDesigner GK888t",
                       "printPreview": 1, "codeFormat": "img",
                       "expressLanguage": "zh-CN",
                       "addressVo": {"addressType": 2, "receivingSenderName": "性能测试寄件人", "city": "深圳市", "cityId": 2101,
                                     "district": "宝安区", "districtId": 2105, "receivingSenderPhone": "13048843947",
                                     "receivingSenderTelphone": "", "company": "", "detailAddress": "茶树新村7巷2号",
                                     "country": "", "province": "广东省", "addressId": "", "provinceId": 2077},
                       "signBack": "",
                       "payType": 1, "platformExpressProductCode": "1", "expressProductName": "顺丰标快",
                       "platformExpressCompanyCode": "SF", "insuredPrice": "",
                       "insuredType": "", "overweightServiceFee": "", "packingFee": "", "collectingMoney": "",
                       "electronicSign": "", "freshServices": "",
                       "commandServices": "", "monthlyCard": "9999999999", "isDocall": 0, "selfPickup": 0,
                       "expressProductId": 38, "expressProductCode": "1"}
    response = requests.post(user_url + "/order/expressTemplate/save", json=template_params, headers=template_headers,
                             timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("新建模板成功{}".format(i))
        else:
            print("新建模板失败{}".format(i))
    else:
        print("新建模板失败{}".format(i))


# 查询列表快递模板第一个
def list_expressTemplate(user_token):
    headers = {'token': user_token}
    res = requests.get(user_url + "/order/expressTemplate/page?current=1&size=50", headers=headers, timeout=30000)
    result = json.loads(res.text)
    expressTemplateId = result["result"]["records"][0]["id"]
    print(expressTemplateId)
    return expressTemplateId


# 设置默认模板
def default_expressTemplate(user_token, expressTemplateId, i):
    headers = {"Content-Type": "application/json", "token": user_token}
    r = requests.post(
        user_url + "/order/expressTemplate/setDefault?templateId=%s&updateOrder=false" % (expressTemplateId),
        headers=headers, timeout=30000)
    resCode = r.status_code
    resBody = r.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("设置默认模板成功{}".format(i))
        else:
            print("设置默认模板失败{}".format(i))
    else:
        print("设置默认模板失败{}".format(i))


# 设置快递模板
def orderTemplate(user_token, order_list, expressTemplateId, i):
    Logistic_headers = {"Content-Type": "application/json", "token": user_token}
    order_list = ','.join(order_list)
    Logistic_params = {"isSpecialMonthly": 0, "collectionCardNumber": "9999999999", "parcelWeight": 0,
                       "freshServices": "", "selfPickup": "", "templateId": expressTemplateId,
                       "orderNos": order_list}
    print(Logistic_params)
    response = requests.post(user_url + "/order/sale/orderTemplate", json=Logistic_params, headers=Logistic_headers,
                             timeout=30000)
    resCode = response.status_code
    resBody = response.json()
    print(resCode, resBody)
    if resCode == 200:
        if 'ok' in resBody.get('code'):
            print("设置快递模板成功{}".format(i))
        else:
            print("设置快递模板失败{}".format(i))
    else:
        print("设置快递模板失败{}".format(i))

    # #测试


token = login('pet00')
# logout(token)
