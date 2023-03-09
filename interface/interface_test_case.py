import json
import interface_spring as app; import time
from Myself_Python.water_for_life.myself_class_file import *
########################################################################################################################
client = app.client()
app.client_para_.password = "Push@123.com1"

#修改服务器指向，登录退出
# client.updata_server_Message(server_ip="192.168.222.202", server_port=9882, server_cache_dir=None)
# client.login()
# client.unlogin()

# #文件全量
# client.set_one_plan(plan_name="文件全量-1", is_zip=0, plan_file_path=r"D:\Users\Administrator\Desktop\TEST_FILE\新版\正常\正常文件\文件类型")
client.execute_plan_instantly(plan_name="文件全量-1", is_all=1)
taskid_0 = app.client_para_.taskid
result = mysql_.MYSQL_1().DB_object(host=app.server_para_.ip, sql_do=f"select TaskContent from tasktable where TaskId='{taskid_0}';")
if json.loads(result["查询结果数(内容)"][0][0])["TaskContent"]["TaskInfo"]["IsAll"] == 1:
    while True:
        if client.get_task_status(taskid=taskid_0):
            client.restore(applyname="文件全量-1" + "-客户端还原流程", path="", plan_name="文件全量-ceshi", taskid=taskid_0)
            break
        else:
            print("等待15秒")
            time.sleep(15)
            print("。。。。。。")
    print("结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束结束")
else:
    print(taskid_0, "是增量归档，放弃执行还原流程")
# 文件增量
# client.set_one_plan(plan_name="文件增量", is_zip=0, plan_file_path=r"D:\Users\Administrator\Desktop\TEST_FILE\新版\正常\正常文件\文件类型")
# client.execute_plan_instantly(plan_name="文件增量", is_all=0)
# taskid_1 = app.client_para_.taskid
# # #文件全量压缩
# # client.set_one_plan(plan_name="文件全量压缩", is_zip=1, plan_file_path=r"D:\Users\Administrator\Desktop\TEST_FILE\新版\正常\正常文件\文件类型")
# # client.execute_plan_instantly(plan_name="文件全量压缩", is_all=1)
# taskid_2 = app.client_para_.taskid
# #数据库归档
# client.mysql_archive_plan(plan_name="数据库归档")
# client.execute_plan_instantly(plan_name="数据库归档", is_all=1)
# #还原
# while True:
#     if client.get_task_status(taskid=taskid_0):
#         client.restore(applyname="还原测试", path="", plan_name="文件全量", taskid=taskid_0)
#         break
# #盘点（清理cache）

#带标签归档
#标签检索
#清理cache
#预览
#自动还原
#预览success
########################################################################################################################
server = app.server()
# server.updata_passwd(username, password, new_password="Push@123.com")
# server.login(username, password)
# server.logout(username, password)
# server.search_()

