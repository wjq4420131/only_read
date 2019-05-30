# 作者：wjq   
# 创建时间: 2019/5/24  
# 文件: only_read.py   
# 软件名称: PyCharm

import paramiko
import os
import datetime
import threading
import csv
import xlsxwriter
import json
import xlwt

# 读取当前路径
base_dir = os.getcwd()
# 命令开始执行时间
starttime = datetime.datetime.now()
print(" -------------------------------------------------------------")
print("|                                                             |")
print("  startime:        ", starttime)
print("|                                                             |")
print(" -------------------------------------------------------------")

# 按日期创建巡检结果
dayTime = datetime.datetime.now().strftime('%Y-%m-%d')
pwd_file = os.getcwd() + '\\' + 'result' + '\\' + dayTime + '\\'
isExists = os.path.exists(pwd_file)
if not isExists:
    os.makedirs(pwd_file)


def only_read():
    # 注意路径前面的r，否则有些文件会当作转义字符处理
    # 读取命令脚本
    cmd_filepath = base_dir + r"\file\cmd.txt"
    ip_filepath = base_dir + r"\file\ip.txt"
    cmd_file = open(cmd_filepath, "r", encoding='utf-8')
    cmd = cmd_file.read()
    # print(cmd)

    # print(cmd)
    # 读取IP地址列表
    ip_file = open(ip_filepath, "r", encoding='utf-8')
    while 1:
        ipinfo = ip_file.readline()
        if not ipinfo:
            break
        else:
            # 读取IP，用户名，密码
            infos = ipinfo.split(',')
            name = infos[0]
            host = infos[1]
            port = infos[2]
            username = infos[3]
            pwd = infos[4].strip()
            pwd = pwd.strip('\n')
            print(name, host)
            # 远程连接服务器
        try:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, pwd, timeout=20)
            stdin, stdout, stderr = client.exec_command(cmd)

            list = []
            for i in stdout:
                list.append(i.strip('\n'))
            title = [name, host]
            jieguo = title + list

            file = open(pwd_file + '\data.txt', 'a+')
            file.write(str(jieguo).replace('\'', '') + '\n');
            file.close()

        except Exception as  e:
            file = open(pwd_file + '\error.txt', 'a+')
            file.write(name + ":"+ host + '\n')
            file.close()
            print(host)


def raid():
    # 注意路径前面的r，否则有些文件会当作转义字符处理
    # 读取命令脚本
    cmd_filepath = base_dir + r"\file\raid.txt"
    ip_filepath = base_dir + r"\file\ip.txt"
    cmd_file = open(cmd_filepath, "r", encoding='utf-8')
    cmd = cmd_file.read()
    print(cmd)

    # print(cmd)
    # 读取IP地址列表
    ip_file = open(ip_filepath, "r", encoding='utf-8')
    while 1:
        ipinfo = ip_file.readline()
        if not ipinfo:
            break
        else:
            # 读取IP，用户名，密码
            infos = ipinfo.split(',')
            name = infos[0]
            host = infos[1]
            port = infos[2]
            username = infos[3]
            pwd = infos[4].strip()
            pwd = pwd.strip('\n')
            print(name, host)
            # 远程连接服务器
        try:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, pwd, timeout=20)
            stdin, stdout, stderr = client.exec_command(cmd)

            with open(pwd_file + r'\get_disk_info.txt', 'a+') as file_txt:
                file_txt.write(
                    "===================================================================================================================" + '\n')
                file_txt.write("                                                      " + host + "      " + '\n')
                file_txt.write(
                    "===================================================================================================================" + '\n')
                for i in stdout:
                    file_txt.write(i.strip('\n') + '\n')
                    print(i.strip('\n'))
                endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file_txt.write(endtime)
            file_txt.close()

        except Exception as  e:
            file = open(pwd_file + '\disk_error.txt', 'a+')
            file.write(name + ":" +  host + '\n')

            file.close()
            print(host)

# print(host)
# for i in range(2):
#     t =threading.Thread(target=only_read)
#     t.start()

if __name__ == '__main__':

    # 获取当前执行代码的线程
    current_thread = threading.current_thread()
    print("main:", current_thread)
    # 获取程序活动线程的列表
    thread_list = threading.enumerate()
    #print("111:", thread_list)
    # 创建跳舞的线程
    dance_thread = threading.Thread(target=only_read)
    #print("dance_thread:", dance_thread)
    # 创建唱歌的线程
    sing_thread = threading.Thread(target=raid)
    #print("sing_thread:", sing_thread)
    thread_list = threading.enumerate()
    #print("222:", thread_list)
    # 启动线程执行对应的任务
    dance_thread.start()
    sing_thread.start()
    # 提示:线程执行完成任务以后该线程就会销毁
    thread_list = threading.enumerate()
    #print("333:", thread_list, len(thread_list))
    # 扩展-获取活动线程的个数
    active_count = threading.active_count()
