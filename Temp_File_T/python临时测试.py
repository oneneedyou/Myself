# import uvicorn
# from fastapi import FastAPI
# print(dir(FastAPI))
# app = FastAPI() # 创建 api 对象
#
# # @app.get("/") # 根路由
# @app.api_route(path="/",methods=["get", "post"])
# def root():
#     return {"武汉": "加油！！！"}
#
# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=52000)
import requests;import urllib3
urllib3.disable_warnings()
from Myself_Python.water_for_life.myself_class_file import *
import requests
########################################################################################################################
i = [1,2,3,4,5,6,7,8,9,10]
j = 0
@loop_(num=10)
def aaa():
    global j
    print(i[j])
    j += 1
    print("哈哈哈", j)
    return j

a = aaa()
print(a)





