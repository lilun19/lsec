import requests

#路由推送
sUrl = "https://partner-sit.sf-express.com/hotwheels/route/push"
mailno = "SF1011639535563"
orderid="20200409935707907"
data_before = '''<?xml version='1.0' encoding='UTF-8'?><Request service="RoutePushService" lang="zh-CN"><Body><WaybillRoute 
        id="200493564547309" mailno="{mailno}" orderid="{orderid}" acceptTime="2020-04-09 09:01:01" acceptAddress="深圳市" 
        remark="已收件(派件人:张益达,电话:18012345678)" opCode="50"/></Body></Request>'''.format(mailno= mailno,orderid= orderid)
data = data_before.encode('utf-8')
headers = {"Content-Type" :"application/xml; charset=UTF-8"}
response = requests.request("POST" ,sUrl ,data=data ,headers=headers)
print(response.text)