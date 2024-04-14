import colorsys, os, sys, subprocess, time, sqlite3
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QProgressBar
from threading import Thread
from queue import Queue
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QLabel
from functools import partial
from typing import List, Optional

def ping(self, ip):
    output = os.popen(f"ping {ip} -w 100").read()
    timeout_ch = "请求超时"
    timeout_en = "Request timed out"
    noloss = "(0%"
    count_timeout_ch = output.count(timeout_ch)
    count_timeout_en = output.count(timeout_en)

    if count_timeout_ch == 0 and count_timeout_en != 0:
        count_timeout = count_timeout_en
    else:
        count_timeout = count_timeout_ch

    count_noloss = output.count(noloss)
    if count_timeout == 1:  
        return f"😟,{ip},1 loss,Something wrong."
    elif count_timeout == 2:
        return f"🤯,{ip},2 loss,Try again!"
    elif count_timeout == 3:
        return f"😈,{ip},3 loss,Bad!!"
    elif count_timeout == 4:
        return f"💀,{ip},4 loss,Fail!!!"
    elif count_timeout == 0 and count_noloss == 0:
        return f"😔,{ip},ahhh,It's Nothing!!!"
    elif count_timeout == 0:
        return f"⭐,{ip},ohhh,Successful!!!"

def get_ping_result(ips):
    threads = []
    ping_result_list = [None] * len(ips)
    for index, ip in enumerate(ips):
        thread = Thread(target=lambda i=index: ping_result_list.__setitem__(i, function_pingtool.Worker.ping(self, ip)))
        thread.start()
        threads.append(thread)
    for index, thread in enumerate(threads):
        thread.join()
        self.progressChanged.emit(index + 1)
    result_queue.put(ping_result_list)

def get_ping_results(ips):
    start = time.time()
    result_queue = Queue()
    worker = function_pingtool.Worker()
    worker.progressChanged.connect(progressBar.setValue)
    ping_thread = Thread(target=worker.get_ping_result, args=(ips, result_queue))
    ping_thread.start()
    ping_thread.join()
    now = time.time()
    running_time = now-start
    dt_now = datetime.fromtimestamp(now)
    print('完成！耗时:%.3f秒' %running_time)
    print('现在时间:%s' %dt_now)
    return result_queue.get()

def get_ip_db(sheet_name, ip_column_name='IP', tips_column_name='Tips', db_url='d:\SQLite\IP-Data.db'):
    with sqlite3.connect(db_url) as conn:
        ip_cursor = conn.cursor()
        tips_cursor = conn.cursor()

        ip_query = f'SELECT {ip_column_name} FROM {sheet_name}'
        tips_query = f'SELECT {tips_column_name} FROM {sheet_name}'

        ip_cursor.execute(ip_query)
        tips_cursor.execute(tips_query)

        ip_rows = ip_cursor.fetchall()  # 读取所有行
        tips_rows = tips_cursor.fetchall()

        ip_list = [row[0] for row in ip_rows]  # 使用列表推导快速创建列表
        tips_list = [row[0] for row in tips_rows]

    return ip_list, tips_list
    
ips, tips = get_ip_db("LOCAL_IP")
print(ips)
print(tips)

ping_result_list = get_ping_results(ips)