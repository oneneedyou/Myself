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
    taskid = None

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
                                            sql_do="select PlanID from plan_info where PlanName='" + str(kwargs["plan_name"]) + "';")
        return text["查询结果数(内容)"][0][0]

    def get_task_status(self, taskid, *args, **kwargs):
        status = mysql_.MYSQL_1().DB_object(host=server_para_.ip, sql_do=f"select TaskState from tasktable where TaskId='{taskid}';")
        print(f"select TaskState from tasktable where TaskId='{taskid}';")
        if status["查询结果数(内容)"][0][0] == 1000:
            return True
        else:
            return False
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
        res = requests.post(url=self.url_("api/authenticate"), json=client_login_data, headers=None, verify=False)
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

    def execute_plan_instantly(self, is_all, *args, **kwargs):
        """客户端立即执行接口"""
        methond = "post"
        data = {
            "planid": self.planname_to_taskid(*args, **kwargs),
            "is_all": is_all
        }

        res = requests.post(url=self.url_("api/plan_task/immediately"), json=data, headers=self.login(*args, **kwargs), verify=False)
        client_para_.taskid = res.json()["taskid"]
        return self.print_info(des="客户端立即执行接口", res=res)

    def mysql_test_link(self, *args, **kwargs):
        #数据库链接测试
        method = "post"
        data = {
            "BKPath": "F:/迅雷下载",
            "BasePath": "",
            "DBName": "docmanager",
            "DBType": 3,
            "Host": server_para_.ip,
            "MysqlDump": "D:/Users/Administrator/Desktop/归档客户端/mysqldump.exe",
            "PassWord": "hardwork",
            "PluginDesc": None,
            "Port": "56788",
            "UserName": "Niord"
        }
        return self.print_info(des="数据库链接测试", res=requests.post(url=self.url_("api/database/databaseConnectionNew"), json=data, headers=self.login(), verify=False))

    def mysql_archive_plan(self, *args, **kwargs):
        method = "post"
        planid = uuid_().uuid()
        data = {
            "planid": planid,
            "planname": kwargs["plan_name"],
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
                "PlanID": planid,
                "PlanInfo": {
                    "BKPath": "F:/迅雷下载",
                    "BasePath": "",
                    "DBName": "docmanager",
                    "DBType": 3,
                    "Host": server_para_.ip,
                    "MysqlDump": "D:/Users/Administrator/Desktop/归档客户端/mysqldump.exe",
                    "PassWord": "hardwork",
                    "PluginDesc": None,
                    "Port": "56788",
                    "UserName": "Niord",
                    "RaidType": None,
                    "RaidNum": None
                },
                "PlanLevel": 0,
                "PlanName": kwargs["plan_name"],
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
        return self.print_info(des="建立数据库归档计划接口", res=requests.post(url=self.url_("api/plan_info"), headers=self.login(), json=data, verify=False))

    def restore(self, *args, **kwargs):
        method = "post"
        data = {
            "applyname": kwargs["applyname"],
            "path": kwargs["path"],
            "planid": self.planname_to_taskid(*args, **kwargs),
            "taskid": kwargs["taskid"]
        }
        return self.print_info(des="客户端还原接口", res=requests.post(url=self.url_("api/plan_task/version_restore"), headers=self.login(), json=data, verify=False))

    def get_all_plan_info(self, *args, **kwargs):
        method = "post"
        para = {
            "page": 0,
            "size": 100,
            "sort": ["addtime", "desc"]
        }
        data = {"where": {"bool_and": []}}
        return self.print_info(des="客户端计划信息检索接口---检索全部计划", res=requests.post(url=self.url_("api/plan_info/_search"), params=para, json=data, headers=self.login(), verify=False))

    def from_planname_search_info(self, *args, **kwargs):
        """根据计划名称检索计划信息，后边贴标签要用到它"""
        method = "post"
        para = {
            "page": 0,
            "size": 100,
            "sort": ["addtime", "desc"]
        }
        data = {"where": {"bool_and": [{"planname.contains": kwargs["plan_name"]}]}}
        return self.print_info(des="客户端计划信息检索接口---检索计划名称", res=requests.post(url=self.url_("api/plan_info/_search"), params=para, json=data, headers=self.login(), verify=False))

    def labes(self, plan_name,labels_list, *args, **kwargs):
        """计划名称，标签名称列表"""
        def get_labels_id(labels_list):
            res = []
            for i in labels_list:
                a = mysql_.MYSQL_1().DB_object(host=server_para_.ip, sql_do=f"select id from labels where name='{i}';")
                res.append(a["查询结果内容"][0][0])
            return res

        method = "put"
        data = {}
        result0 = mysql_.MYSQL_1().DB_object(host=server_para_.ip,
                                   sql_do=f"select id,PlanID,PlanName,PlanDescription,PlanType,PlanContent,PlanState,PlanIsOnce,PlanIsExcute from plan_info where PlanName='{plan_name}';")
        result = result0["查询结果内容"]
        data["id"] = result[0][0]
        data["planid"] = result[0][1]
        data["planname"] = result[0][2]
        data["plandescription"] = result[0][3]
        data["plantype"] = result[0][4]
        data["plancontent"] = result[0][5]; data["plancontent"]["PlanInfo"]["PluginDesc"] = None; data["plancontent"]["PlanInfo"]["RaidType"] = None; data["plancontent"]["PlanInfo"]["RaidNum"] = None; data["plancontent"]["TaskSourceValue"] = None
        data["planstate"] = result[0][6]
        data["planisonce"] = result[0][7]
        data["planisexcute"] = result[0][8]
        data["labels"] = get_labels_id(labels_list)
        self.print_info(des="计划贴标签", res=requests.put(url=self.url_("api/plan_info"), data=data, headers=self.login(), verify=False))

########################################################################################################################
# if __name__ == "__main__":
#     client = client();server = server()
#     server.login()
