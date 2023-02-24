# -*- coding: UTF-8 -*-
import locale;print(locale.getpreferredencoding())# 查看本地编码'cp936'
import pymysql;import time
class MYSQL:
    def Print_Test(self):
        """sql函数参数为空，导致没有DB_object函数没有接收到sql语句时"""
        print("mysql语句参数为空，跳过，执行默认函数 MYSQL.Print_Test() ！！！")

    def sql(self, *args, **kwargs):
        """用来生成不同的sql语句"""
        try:
            ############################归档
            # sql = {
            #     "a": "SELECT TaskId FROM tasktable where TaskState=1000;",
            #     "b": "select add_time from task_life_cycle where task_id=" + '"' + str(kwargs["taskid"]) + '"' + " and content like " + f'"%{kwargs["test"]}%";',
            #     "c": "select ArchiveFileSize from tasktable where TaskId=" + '"' + str(kwargs["taskid"]) + '";',
            # }
            # return str(sql[kwargs["key"]])

            ############################盘点
            # sql = {
            #     "a": "SELECT TaskId FROM check_task_table where CheckState=1000;",
            #     "b": "select add_time from task_life_cycle where task_id=" + '"' + str(kwargs["taskid"]) + '"' + " and content like " + f'"%{kwargs["test"]}%";'
            # }
            # return str(sql0[kwargs["key"]])
            ############################还原
            sql = {
                "a": "",
                "b": ""
            }
            return str(sql[kwargs["key"]])
        except:
            print("error: sql()函数缺少参数")
            return 0

    def DB_object(self,
                host: str = '192.168.199.165',
                port: int = 56788,
                user: str = 'Niord',
                password: str = 'hardwork',
                database: str = 'docmanager',
                charset: str = 'utf8',
                *args, **kwargs):
        """mysql链接对象，返回查询结果数，和查询结果全部内容"""
        try:
            """如果mysql语句不为空，就用sql_do接收sql语句"""
            sql_do = self.sql(*args, **kwargs)
            print("DB_object函数: ", args, kwargs, sql_do)
        except:
            """如果没有mysql语句，就直接退出当前函数，执行后面的内容"""
            self.Print_Test()
            return
        try:
            db_object = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset).cursor()
            data0 = db_object.execute(sql_do); print("查询结果数量: ", data0)
            data1 = db_object.fetchall(); print("查询结果内容: ", data1)
            # 操作写入数据库
            # pymysql.connect().commit()
            db_object.close()
            return {"查询结果数(数字)": data0,
                    "查询结果数(内容)": data1}
        except:
            print("查询失败")
            return 0
def log_print(log_conten):
    f = open("aaaaaaaaaaaa.txt", mode="a+", encoding='utf-8')
    print(str(time.time()) + ">>>>>>>", str(log_conten), sep="\t", end="\t<<<<<<<\n", file=f)
    f.close()
def report(list):
    import csv
    with open(r"b.csv", "a+", newline='') as b:
        b_csv = csv.writer(b)  # 创建csv 对象
        b_csv.writerow(list)
        b.close()
def time2_time1(time_start, time_end):
    """计算时间差，单位秒"""
    start_time1 = time.strptime(time_start, "%Y-%m-%d %H:%M:%S")
    end_time1 = time.strptime(time_end, "%Y-%m-%d %H:%M:%S")
    start_time2 = int(time.mktime(start_time1))
    end_time2 = int(time.mktime(end_time1))
    print(end_time2 - start_time2)
    return (end_time2 - start_time2)
##############################################################################归档
# #symbol = (("客户端开始进行文件归档计算处理", "客户端文件归档计算处理执行完成"),
#          ("开始上传文件", "结束上传文件"),
#          ("开始更新缓存文件", "更新缓存文件成功"),
#          ("开始调度归档任务", "下发归档任务"),
#          ("worker任务开始执行拷贝", "已结束,结束状态(归档成功)"),
#          ("worker执行阶段已结束", "已结束,结束状态(归档成功), 修改任务状态(1000)"))
##############################################################################盘点
# symbol = (("调度服务开始调度【任务盘点】盘点任务", "结果整理完成"),
#          ("worker任务开始执行拷贝", "worker任务执行结束"))
##############################################################################还原
symbol = (("调度服务开始调度【任务盘点】盘点任务", "结果整理完成"),
         ("worker任务开始执行拷贝", "worker任务执行结束"))

content = MYSQL().DB_object(key="a", table_name="0", taskid="0", test="0")
print("----------------------------------------------------------------------------------------------------------")
headers = ["任务ID", "客户端文件处理时间(秒)", "客户端文件上传时间(秒)", "客户端更新缓存文件时间(秒)", "调度流程时间(秒)", "worker使用时间(秒)", "插入ES元信息时间(秒)", "任务文件总大小(Byte)"]
report(headers)
i = 0
while i < content["查询结果数(数字)"]:
    print("----------------------------------------------------------------------------------------------------------")
    print(f"第{i}次")
    result = []
    taskid = content["查询结果数(内容)"][i][0]
    result.append(taskid)
    j = 0
    while j < 2:
        print(f"第{j}次")
        try:
            time0 = MYSQL().DB_object(key="b", table_name="0", taskid=taskid, test=symbol[j][0])
            time1 = str(time0["查询结果数(内容)"][0][0])
            time0 = MYSQL().DB_object(key="b", table_name="0", taskid=taskid, test=symbol[j][1])
            time2 = str(time0["查询结果数(内容)"][0][0])
            a = time2_time1(time1, time2)
        except:
            a = 0
        result.append(a)
        print(a, "秒")
        j = j + 1
    # filesize = MYSQL().DB_object(key="c", table_name="0", taskid=taskid, test="0")
    # print(filesize["查询结果数(内容)"][0][0])
    # result.append(filesize["查询结果数(内容)"][0][0])
    report(result)
    i = i + 1
