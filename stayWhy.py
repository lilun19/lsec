import json,requests,hashlib,base64,xmltodict,time

#制造异常件
str = '''SF1030293368735
SF1030293368701
SF1030293368566
SF1030293368541
SF1011811020208
SF1030293368574'''
mailNos = str.split('\n')
print(mailNos)
for mailNo in mailNos:
     KUrl = "http://10.202.43.6:8080/shiva-oms-ht-web/barCreate/simpleCreate"
     K = {"waybillNo": mailNo, "opCode": "50", "zoneCode": "755A", "courierCode": "000212",
          "barScanTm": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "barOprCode": "000212",
          "objTypeCode": "20", "barSn": "sgs-core", "weightQty": "1", }
     headers = {"Cookie":"JSESSIONID=272178A4BA63E9296DA7D7EAAC84DAA6","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
     #requests.request("POST",KUrl,data=K,headers=headers)
     # time.sleep(5)
     K["opCode"] = "70"
     K["stayWhyCode"]=1
     response2 = requests.request("POST", KUrl, data=K, headers=headers)
     print(mailNo+' 已成为异常件！')

