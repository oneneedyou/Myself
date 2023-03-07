#数据类型
class data_class():
    def dictionary(self):
        a = {}


#测试函数，异常报错函数
class error_():
    def NOT_fuc(self):
        print(">>>>>>>>>>>>>>ERROR:", "函数不存在")

#发送http请求
class request_():
    def get_(self):
        import requests
        resp = requests.get("http://127.0.0.1:52000/")
        print(resp.status_code)  # HTTP 状态码
        print(resp.headers)  # 响应头
        print(resp.cookies)  # 响应的 cookies
        print(resp.content.decode("utf-8"))  # 响应内容

    def post_(self):
        import requests
        resp = requests.post("http://127.0.0.1:52000/", data=b"Hello World")
        print(resp.status_code)
        print(resp.content.decode("utf-8"))

    def form_(self):
        import requests
        file1 = open("临时测试文件/json.json", "rb")
        resp = requests.post("http://httpbin.org/post", data={"key1": "value1"}, files={"file_key1": file1})
        print(resp.content.decode("utf-8"))
        print("+++++aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa+++++++++++++")
        print(resp.text)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(type(resp.headers))
        print(type(resp.content))
        print(type(resp.status_code))
        print(type(resp.ok))
        print(resp.cookies)
        file1.close()

    def apparent_(self):
        import requests
        resp = requests.get("http://httpbin.org/get")
        # 响应内容编码
        print(resp.apparent_encoding)
        # 解码字节类型的响应内容
        print(resp.content.decode(resp.apparent_encoding))
        # 直接使用已解码的响应内容
        print(resp.text)

    def download_file(self):
        import requests
        # 文件保存位置
        file = open("aa.jpg", "wb")
        # 发出请求
        resp = requests.get(
            "https://img1.baidu.com/it/u=1552107944,1918856320&fm=253&fmt=auto&app=138&f=JPEG?w=670&h=447", stream=True)
        # 逐块读取响应数据
        for bs in resp.iter_content(1024):
            # 数据写入文件
            file.write(bs)
        # 关闭文件
        file.close()

    def cookies_(self):
        import requests
        # 发送请求（响应中将会设置一个cookie: hello=world）
        resp = requests.get("http://httpbin.org/cookies/set/hello/world", allow_redirects=False)
        # 响应的 resp.cookies 为 RequestsCookieJar 类型
        resp.cookies.get("hello")
        'world'
        resp.cookies["hello"]
        'world'
        resp.cookies.items()
        [('hello', 'world')]
        resp.cookies.keys()
        ['hello']

#socket服务端
class socket_():

    def socket_(self):
        import socket
        ipaddress = "192.168.1.200"
        port = 52000
        address = (ipaddress, port)
        server = socket.socket()
        server.bind(address)
        server.listen(5)
        print(">>>创建监听套接字成功")
        while True:
            content, address = server.accept()
            print(">>>本次socket套接字为：", address)
            content_0 = content.recv(1024).decode('utf-8')
            print(">>>接收到客户端数据：", content_0)
            txt = "server接收到消息>>>" + content.recv(1024).decode('utf-8')
            print(txt)
            content.close()

#Fastapi
class fastapi_():
    def fastapi_(self):
        import uvicorn
        from fastapi import FastAPI

        app = FastAPI()  # 创建 api 对象

        @app.get("/")  # 根路由
        def root(self):
            return {"武汉": "加油！！！"}

        @app.get("/say/{data}")
        def say(data: str, q: int):
            return {"data": data, "item": q}

        @app.get("/syslog/get")
        def get_syslog(self):
            return "success"

        @app.post("/syslog/post")
        def post_syslog(self):
            return "ssss"

        if __name__ == '__main__':
            uvicorn.run(app, host="127.0.0.1", port=52000)

#mysql增删改查
class mysql_():

    class MYSQL_0:
        """填写数据库链接信息，选择key确定不同sql语句"""
        def Print_Test(self):
            """sql函数参数为空，导致没有DB_object函数没有接收到sql语句时"""
            print("mysql语句参数为空，跳过，执行默认函数 MYSQL.Print_Test() ！！！")

        def sql(self, *args, **kwargs):
            """用来生成不同的sql语句"""
            try:
                ############################根据实际情况写入sql语句
                sql = {
                    "a": f"select PlanID from plan_info where PlanName='" + str(kwargs["plan_name"]) + "';",
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
            import pymysql
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
                db_object = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                            charset=charset).cursor()
                data0 = db_object.execute(sql_do)
                print("查询结果数量: ", data0)
                data1 = db_object.fetchall()
                print("查询结果内容: ", data1)
                # 操作写入数据库
                # pymysql.connect().commit()
                db_object.close()
                return {"查询结果数(数字)": data0,
                        "查询结果数(内容)": data1}
            except:
                print("查询失败")
                return 0

    class MYSQL_1():
        """执行一条sql语句，返回结果数和内容"""
        def DB_object(self,
                      host: str = '192.168.199.165',
                      port: int = 56788,
                      user: str = 'Niord',
                      password: str = 'hardwork',
                      database: str = 'docmanager',
                      charset: str = 'utf8',
                      *args, **kwargs):
            import pymysql
            """mysql链接对象，返回查询结果数，和查询结果全部内容"""
            try:
                db_object = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                            charset=charset).cursor()
                data0 = db_object.execute(kwargs["sql_do"])
                print("查询结果数量: ", data0)
                data1 = db_object.fetchall()
                print("查询结果内容: ", data1)
                # 操作写入数据库
                # pymysql.connect().commit()
                db_object.close()
                return {"查询结果数(数字)": data0,
                        "查询结果数(内容)": data1}
            except:
                print("查询失败")
                return 0

#密码MD5加密
class md5_():
    def md5(self, str):
        import hashlib
        m = hashlib.md5()
        m.update(str.encode("utf8"))
        print(">>>>>>>>>>", m.hexdigest())
        return m.hexdigest()

    def md5GBK(self, str1):
        import hashlib
        m = hashlib.md5(str1.encode(encoding='gb2312'))
        print(m.hexdigest())
        return m.hexdigest()

#生成uuid
class uuid_():
    def uuid(self):
        import uuid;return uuid.uuid4()

#base64加密
class base64_():
    def base64(self, str):
        import base64
        bs64 = base64.b64encode(str.encode('utf-8'))
        print("bs64 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", bs64)
        return base64

#类装饰器，循环执行N次被装饰的函数
class loop_(object):
    def __init__(self, num):
        """接收装饰器参数，在这是是循环次数"""
        self.level = num

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("[循环{0}次]: enter {1}()".format(self.level, func.__name__))
            i = 0
            a = {}
            while i < self.level:
                i += 1
                print(f"第{i}次")
                a[f"第{i}次"] = func(*args, **kwargs)
            print(">>>{0}次循环结束<<<")
            return a
        return wrapper






