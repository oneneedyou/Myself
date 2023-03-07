#<-*- coding: UTF-8 -*->
from Myself_Python.water_for_life.myself_class_file import *
import requests;import urllib3;import time;import uuid
from requests import utils
urllib3.disable_warnings()
# -*- coding: UTF-8 -*-
import locale;print(locale.getpreferredencoding())# 查看本地编码'cp936'
import pymysql;import time

########################################################################################################################
class server_para_:
    username: str = "secadmin"
    password: str = "Push@123.com"
    ip: str = "192.168.222.202"
    port: int = 8443

class server():
    def updata_passwd(self, *args, **kwargs):
        method = "post"
        url = f"https://{server_para_.ip}:{server_para_.port}/api/user/password-rest"
        data = {
            "userId": args[0],
            "originalPassword": md5_().md5(args[1]),
            "newPassword": md5_().md5(kwargs["new_password"]),
            "newPasswordAgain": md5_().md5(kwargs["new_password"]),
            "newPasswordBase64": base64_().base64(kwargs["new_password"])
        }

        headers = self.login(*args, **kwargs)
        res = requests.post(url=url, json=data, headers=headers, verify=False)
        print("更新客户端的服务指向==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.json())

    def login(self, *args, **kwargs):
        method = "post"
        url = f"https://{server_para_.ip}:{server_para_.port}/api/authenticate"
        data = {
            "username": server_para_.username,
            "password": md5_().md5(server_para_.password),
            "verify_code": "code",
            "rememberMe": True,
            "isArchive": False,
            "type": 1
        }

        res = requests.post(url=url, json=data, verify=False)
        print("服务端登录接口==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))
        return {"Authorization": "Bearer " + res.json()["id_token"]}

    def logout(self, *args, **kwargs):
        pass

    def search_(self, *args, **kwargs):
        method = "post"
        url = f"https://{server_para_.ip}:{server_para_.port}/api/search/simple"
        para = {
            "page": 100,
            "size": 10,
            "paged": True,
            "sort": ["timestamp", "desc"]
        }
        data = {
            "category": "word",
            "search": None,
            "all": True
        }

        headers = self.login(*args, **kwargs)
        res = requests.post(url=url,params=para, json=data,headers=headers, verify=False)
        print("服务端全文检索接口==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))


########################################################################################################################
class client_para_:
    username: str = "secadmin"
    password: str = "Push@123.com"
    ip: str = "192.168.1.200"
    port: int = 9881

class client():
    def print_info(self, des, res, *args, **kwargs):
        print(f"{des}==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))
        if res.status_code == 200:
            return ["success", f"{des} 接口通讯成功"]
        else:
            return ["fail", f"{des} 接口通讯失败"]

    def url_(self, para, *args, **kwargs):
        return f"https://{client_para_.ip}:{client_para_.port}/{para}"

    def planname_to_taskid(self, *args, **kwargs):
        text = mysql_().MYSQL_1().DB_object(host="192.168.222.202", port=56788, user="Niord", password="hardwork",
                                            database="docmanager",
                                            sql_do="select PlanID from plan_info where PlanName='" + str(
                                                kwargs["plan_name"]) + "';")
        return text["查询结果数(内容)"][0][0]

    def updata_server_Message(self, *args, **kwargs):
        """更新客户端的服务指向"""
        # 客户端更新服务端接口
        methond = "get"
        url = self.url_("api/system_config/_by_server")
        data = {
            "server_host": kwargs["server_ip"],
            "server_port": kwargs["server_port"],
            "samba_dir": kwargs["server_cache_dir"]
        }
        return self.print_info(des="更新客户端的服务指向", res=requests.get(url=url, params=data, headers=None, verify=False))

    def login(self, *args, **kwargs):
        """获取token, 客户端登录"""
        # 客户端登录接口        #客户端获取token
        client_login_methond = "post"
        client_login_data = {
            "username": client_para_.username,
            "password": md5_().md5(client_para_.password),
            "verify_code": "code",
            "rememberMe": True,
            "isArchive": True
        }
        res = requests.post(url=self.url_("/api/authenticate"), json=client_login_data, headers=None, verify=False)
        print("获取token, 客户端登录==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))
        return {"Authorization": "Bearer " + res.json()["id_token"]}

    def unlogin(self, *args, **kwargs):
        """客户端登出"""
        # 客户端登出接口
        client_unlogin_methond = "post"
        data = {
            "username": client_para_.username,
            "password": md5_().md5(client_para_.password),
            "verify_code": "code"
        }
        return self.print_info(des="客户端登出", res=requests.post(url=self.url_("api/logout"), json=data, headers=self.login(*args, **kwargs), verify=False))

    def set_one_plan(self, *args, **kwargs):
        """添加计划信息, 客户端建立计划接口
            计划名称、归档问价路径、是否压缩、
        """
        method = "post"
        planid = str(uuid_().uuid())
        data = {
            "planid": planid,
            "planname": kwargs["plan_name"],
            "plandescription": "",
            "plantype": "0",
            "plancontent": {
                "Burn": 0,
                "CheckPlan": 0,
                "IsDup": 1,
                "IsRun": 0,
                "IsRunAdmin": 1,
                "IsWithCD": 0,
                "IsoFormat": 0,
                "MachineCode": "",
                "PlanID": planid,
                "PlanInfo": {
                    "FilePath": [
                        str(kwargs["plan_file_path"])
                    ],
                    "Filter": [],
                    "FilterOut": [],
                    "IsAll": 0,
                    "IsCompress": kwargs["is_zip"],
                    "IsSetClear": 0,
                    "ClearDays": 0,
                    "PluginDesc": None,
                    "RaidType": None,
                    "RaidNum": 0
                },
                "PlanLevel": 0,
                "PlanName": kwargs["plan_name"],
                "PlanType": 0,
                "TaskSourceValue": None,
                "UserID": "",
                "WriteSytle": 0,
                "Times": [
                    {
                        "DataType": "单次",
                        "Year": 2023,
                        "Month": 2,
                        "Day": 20,
                        "Hour": "00",
                        "Minute": "00",
                        "Time": "2023-02-19T16:00:00.000Z",
                        "IsAll": True,
                        "TimeName": "",
                        "index": 0
                    }
                ]
            },
            "planstate": 0,
            "planisonce": 1,
            "planisexcute": 0,
            "labels": []
        }
        return self.print_info(des="添加计划信息, 客户端建立计划接口", res=requests.post(url=self.url_("api/plan_info"), json=data, headers=self.login(*args, **kwargs), verify=False))

    def execute_plan_instantly(self, is_all: int = 1, *args, **kwargs):
        """客户端立即执行接口"""
        methond = "post"
        data = {
            "planid": self.planname_to_taskid(),
            "is_all": is_all
        }
        return self.print_info(des="客户端立即执行接口", res=requests.post(url=self.url_("api/plan_task/immediately"), json=data, headers=self.login(*args, **kwargs), verify=False))

    def mysql_test_link(self):
        pass
    #数据库链接测试
        method = "post"
        url = f"https://{client_para_.ip}:{client_para_.port}/api/database/databaseConnectionNew"
        data = {
            "BKPath": "F:/迅雷下载",
            "BasePath": "",
            "DBName": "docmanager",
            "DBType": 3,
            "Host": "192.168.222.202",
            "MysqlDump": "D:/Users/Administrator/Desktop/归档客户端/mysqldump.exe",
            "PassWord": "hardwork",
            "PluginDesc": None,
            "Port": "56788",
            "UserName": "Niord"
        }

    def mysql_archive_plan(self):
        method = "post"
        url = f"https://{client_para_.ip}:{client_para_.port}/api/plan_info"
        data = {
            "planid": "a6457c0d-452e-1556-5fc8-e5c393d6fac3",
            "planname": "数据库归档",
            "plandescription": "",
            "plantype": 1,
            "plancontent": {
                "Burn": 0,
                "CheckPlan": 0,
                "IsDup": 1,
                "IsRun": 0,
                "IsRunAdmin": 1,
                "IsWithCD": 0,
                "IsoFormat": 0,
                "MachineCode": "",
                "PlanID": "a6457c0d-452e-1556-5fc8-e5c393d6fac3",
                "PlanInfo": {
                    "BKPath": "F:/迅雷下载",
                    "BasePath": "",
                    "DBName": "docmanager",
                    "DBType": 3,
                    "Host": "192.168.222.202",
                    "MysqlDump": "D:/Users/Administrator/Desktop/归档客户端/mysqldump.exe",
                    "PassWord": "hardwork",
                    "PluginDesc": None,
                    "Port": "56788",
                    "UserName": "Niord",
                    "RaidType": None,
                    "RaidNum": None
                },
                "PlanLevel": 0,
                "PlanName": "数据库归档",
                "PlanType": 1,
                "TaskSourceValue": None,
                "UserID": "",
                "WriteSytle": 0,
                "Times": [
                    {
                        "DataType": "单次",
                        "Year": 2023,
                        "Month": 2,
                        "Day": 24,
                        "Hour": "00",
                        "Minute": "00",
                        "Time": "2023-02-23T16:00:43.000Z",
                        "IsAll": True,
                        "TimeName": "",
                        "index": 0
                    }
                ]
            },
            "planstate": 0,
            "planisonce": 1,
            "planisexcute": 0,
            "labels": []
        }

########################################################################################################################
# if __name__ == "__main__":
#     client = client();server = server()
#     server.login()
