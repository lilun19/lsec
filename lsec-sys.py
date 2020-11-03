# -*- coding: UTF-8 -*-
import requests,json,time

erp_url = "http://erp-sit.sf-express.com"
op_url = "http://op-erp-sit.sf-express.com"

class lesc_sys:
    # 基础相关
    def __init__(self,url):
        self.url = url

    def login(self,username):
        #登录商户端
        LoginUrl = self.url + "/api/sys/user/logintest?username=" + username
        response = requests.post(LoginUrl)
        self.token = response.headers['token']
        # self.token = erp_token
        print(self.token)
        return self.token


lesc = lesc_sys(erp_url)
token = lesc.login("yypdc")