import interface_spring as app
########################################################################################################################
client = app.client()
username = app.client_para_.username
password = app.client_para_.password
# client.login(username, password)
# client.updata_server_Message(server_ip="192.168.222.202", server_port=9882, server_cache_dir=None)

# client.set_one_plan(username, password, plan_name="327测试", plan_time="", plan_file_path=r"D:\Users\Administrator\Desktop\Myself\》》》测试文件《《《")
# client.execute_plan_instantly(username, password, plan_name="327测试")
app.client_para_.password = "Push@123.com1"
# client.set_one_plan(username, password, plan_name="视频分析", plan_time="", plan_file_path=r"D:\Users\Administrator\Desktop\Myself\Myself_Python\TEST_FILE\正常\正常文件\文件类型\图片\归档客户端图标200x200")
client.execute_plan_instantly(username, password, plan_name="视频分析")

# client.unlogin(username, password)

########################################################################################################################
server = app.server()
# server.updata_passwd(username, password, new_password="Push@123.com")
# server.login(username, password)
# server.logout(username, password)
# server.search_()
