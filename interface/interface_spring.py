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
    def print_info(self, res, des):
        print(f"{des}==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.json())

    def get_labes_id(self, *args, **kwargs):
        """贴标签的请求中，labes键值需要标签id列表"""
        labels_id = []
        for i in kwargs["labels"]:
            a = mysql_.MYSQL_1().DB_object(host="192.168.222.202", sql_do=f"select id from labels where name='{i}'")
            b = int(a["查询结果数(内容)"][0][0])
            labels_id.append(b)
        return labels_id

    def get_task_id(self, *args, **kwargs):
        """根据计划名称获取计划id"""
        text = mysql_().MYSQL_1().DB_object(host="192.168.222.202", port=56788, user="Niord", password="hardwork",
                                            database="docmanager",
                                            sql_do="select PlanID from plan_info where PlanName='" + str(
                                                kwargs["plan_name"]) + "';")
        sql_task_id = text["查询结果数(内容)"][0][0]
        return sql_task_id

    def updata_server_Message(self, *args, **kwargs):
        """更新客户端的服务指向"""
        # 客户端更新服务端接口
        methond = "get"
        url = f"https://{client_para_.ip}:{client_para_.port}/api/system_config/_by_server"
        data = {
            "server_host": kwargs["server_ip"],
            "server_port": kwargs["server_port"],
            "samba_dir": kwargs["server_cache_dir"]
        }
        res = requests.get(url=url, params=data, headers=None, verify=False)
        print("更新客户端的服务指向==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.json())

    def login(self, *args, **kwargs):
        """获取token, 客户端登录"""
        # 客户端登录接口        #客户端获取token
        client_login_methond = "post"
        client_login_url = f"https://{client_para_.ip}:{client_para_.port}/api/authenticate"
        client_login_data = {
            "username": client_para_.username,
            "password": md5_().md5(client_para_.password),
            "verify_code": "code",
            "rememberMe": True,
            "isArchive": True
        }
        res = requests.post(url=client_login_url, json=client_login_data, headers=None, verify=False)
        print("获取token, 客户端登录==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.json())
        return {"Authorization": "Bearer " + res.json()["id_token"]}

    def unlogin(self, *args, **kwargs):
        """客户端登出"""
        # 客户端登出接口
        client_unlogin_methond = "post"
        client_unlogin_url = f"https://{client_para_.ip}:{client_para_.port}/api/logout"
        client_unlogin_data = {
            "username": client_para_.username,
            "password": md5_().md5(client_para_.password),
            "verify_code": "code"
        }

        headers = self.login(*args, **kwargs)
        res = requests.post(url=client_unlogin_url, json=client_unlogin_data, headers=headers, verify=False)
        print("客户端登出==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))

    def set_one_plan(self, *args, **kwargs):
        """添加计划信息, 客户端建立计划接口"""
        method = "post"
        planid = str(uuid_().uuid())
        url = f"https://{client_para_.ip}:{client_para_.port}/api/plan_info"
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
                    "IsCompress": 0,
                    "IsSetClear": 0,
                    "ClearDays": 0,
                    "PluginDesc": None,
                    "RaidType": None,
                    "RaidNum": 0
                },
                "PlanLevel": 0,
                "PlanName": "千万---文件",
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

        headers = self.login(*args, **kwargs)
        res = requests.post(url=url, json=data, headers=headers, verify=False)
        print("添加计划信息, 客户端建立计划接口==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        print("响应体: ", res.content.decode(res.apparent_encoding))

    def execute_plan_instantly(self, is_all: int = 1, *args, **kwargs):
        """客户端立即执行接口"""
        text = mysql_().MYSQL_1().DB_object(host="192.168.222.202", port=56788, user="Niord", password="hardwork",
                                     database="docmanager", sql_do="select PlanID from plan_info where PlanName='" + str(kwargs["plan_name"]) + "';")
        sql_task_id = text["查询结果数(内容)"][0][0]

        methond = "post"
        url = f"https://{client_para_.ip}:{client_para_.port}/api/plan_task/immediately"
        data = {
            "planid": sql_task_id,
            "is_all": is_all#1全量，0增量; 默认全量
        }

        headers = self.login(*args, **kwargs)
        res = requests.post(url=url, json=data, headers=headers, verify=False)
        print("客户端立即执行接口==============================================")
        print("状态码: ", res.status_code)
        print("响应头: ", res.headers)
        # if res.json()["status"] and res.json()["status"] == "INTERNAL_SERVER_ERROR":
        #     print("ERROR >>> : \n\t", res.json()["message"])
        # else:
        #     print("响应体: ", res.content.decode(res.apparent_encoding))
        print("响应体: ", res.content.decode(res.apparent_encoding))

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

    def get_all_plan_info(self, *args, **kwargs):
        method = "post"
        url = "https://localhost:9881/api/plan_info/_search"
        para = {
            "page": 0,
            "size": 100,
            "sort": ["addtime", "desc"]
        }
        data = {"where": {"bool_and": []}}

        res = requests.post(url=url, params=para, json=data, headers=client.login(), verify=False)
        self.print_info(res, des="客户端计划信息检索接口---检索全部计划")
        return res

    def from_planname_search_info(self, *args, **kwargs):
        """根据计划名称检索计划信息，后边贴标签要用到它"""
        method = "post"
        url = "https://localhost:9881/api/plan_info/_search"
        para = {
            "page": 0,
            "size": 100,
            "sort": ["addtime", "desc"]
        }
        data = {"where": {"bool_and": [{"planname.contains": kwargs["plan_name"]}]}}

        res = requests.post(url=url, params=para, json=data, headers=client.login(), verify=False)
        self.print_info(res, des="客户端计划信息检索接口---检索计划名称")
        return res

    def labes(self, *args, **kwargs):
        """计划名称，标签名称列表"""
        method = "put"
        url = "https://localhost:9881/api/plan_info"
        # data = {
        #     "planid": "f7bcb53b-a05e-4000-9a23-482c8c05342d",
        #     "planname": "视频分析",
        #     "plandescription": "",
        #     "plantype": "0",
        #     "plancontent": {
        #         "Burn": 0,
        #         "CheckPlan": 0,
        #         "IsDup": 1,
        #         "IsRun": 1,
        #         "IsRunAdmin": 1,
        #         "IsWithCD": 0,
        #         "IsoFormat": 0,
        #         "MachineCode": "",
        #         "PlanID": "f7bcb53b-a05e-4000-9a23-482c8c05342d",
        #         "PlanInfo": {
        #             "FilePath": [
        #                 "D:/Users/Administrator/Desktop/Myself/Myself_Python/TEST_FILE/正常/正常文件/文件类型/视频"
        #             ],
        #             "Filter": [],
        #             "FilterOut": [],
        #             "IsAll": 0,
        #             "IsCompress": 0,
        #             "IsSetClear": 0,
        #             "ClearDays": 0,
        #             "PluginDesc": None,
        #             "RaidType": None,
        #             "RaidNum": None
        #         },
        #         "PlanLevel": 2,
        #         "PlanName": "视频分析",
        #         "PlanType": 0,
        #         "TaskSourceValue": None,
        #         "UserID": "",
        #         "WriteSytle": 0,
        #         "Times": [
        #             {
        #                 "Month": 2,
        #                 "Year": 2023,
        #                 "Minute": "00",
        #                 "Hour": "00",
        #                 "DataType": "单次",
        #                 "index": 0,
        #                 "Time": "2023-02-19T16:00:00.000Z",
        #                 "Day": 20,
        #                 "TimeName": "",
        #                 "IsAll": True
        #             }
        #         ]
        #     },
        #     "planstate": 0,
        #     "planisonce": 1,
        #     "planisexcute": 1,
        #     "labels": [
        #         14,
        #         15
        #     ],
        #     "id": 3
        # }
        data = {}
        res = self.from_planname_search_info(plan_name="视频分析").json()[0]
        list = ["planid", "planname", "plandescription", "plantype", "planstate", "planisonce", "planisexcute", "id"]
        for i in list:
            data[i] = res[i]
        data["labels"] = self.get_labes_id(*args, **kwargs)

        a = res["plancontent"];print("》》》》》》》》》》》》》》", a)

        data["plancontent"] = ""
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", a.content.decode(a.encoding))

        # res = requests.put(url=url, data=data, headers=client.login(), verify=False)
        # self.print_info(res=res, des="计划贴标签")

########################################################################################################################
if __name__ == "__main__":
    client = client();server = server()
    # server.login()
    client_para_.password = "Push@123.com1"
    client.labes(planname="视频分析", labels=[1,2,22])