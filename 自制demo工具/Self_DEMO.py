from fastapi import FastAPI, Header, Body, Form, Request  # 接收请求体json数据模型
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse  # 返回数据的模型
from fastapi.templating import Jinja2Templates  # 前端渲染引擎
import uvicorn  # 运行框架
from typing import Optional
from pydantic import BaseModel  # 发送请求体模型
from enum import Enum

app = FastAPI()  # 实例化fastapi对象


# 根路径，首页
@app.get("/")
def root(q: int = 123456):
    return "哈哈"


class post_request_class(BaseModel):
    test_data_0: str = "post"
    test_data_1: str = "请求"
    test_data_2: str = "类"


@app.get("/test/")
def post_request(id: int = 1314520):
    return {'id': id}


@app.post("/login")
def login(data=Body(None)):
    """
    接收post请求
    :param data:
    :return:
    """
    return {"body": data}


# 创建请求体数据模型
class Item(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    tax: float = None


@app.post("/items/")
async def create_item(item: Item):
    return item


# json数据的返回
@app.get("/user")
def user():
    return {"爱": "Love", "生命": "live", "自由": "haha"}


# 列表数据的返回
@app.get("/users")
def users():
    return ["我", "爱", "你"]


# post请求
@app.post("/post")
def post_():
    return {"post": 1314520}


# 接口同时支持多种请求方法
@app.api_route("/api_route", methods=("get", "post", "put"))
def api_route_():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# 获取URL路径参数
@app.get("/user_url/{id_1}")
def URL_parameter(id_1):
    print(id_1)
    return {"ID:": id_1}


# 查询字符串参数
@app.get("/user_url")
def URL_parameter(id_1: int):
    print(id_1)
    return {"ID:": id_1}


# 请求头
@app.get("/header_para")
def header_para(token=Header(1314520)):
    print(token)
    return [token]


# 获取请求体，导入body方法
@app.get("/body")
def body_(data=Body(None)):
    return [data]


# 接收Form表单格式数据,导入Form方法
@app.get("/form_")
def form_(username=Form(None), password=Form(None)):
    print(username, password)
    return {"data": {"username": username, "password": password}}


# 修改响应状态码，导入JSONResponse方法
@app.get("/response")
def response_():
    return JSONResponse(content={"a": "爱你一万年"})
