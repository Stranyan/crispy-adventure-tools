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

app = QtWidgets.QApplication(sys.argv) # 创建一个QApplication对象
layout: QVBoxLayout
ping_result_list: List[Optional[str]] = []
#tab_widget = QTabWidget() # 创建一个QTabWidget对象

# 创建第一个页面
class function_pingtool():
    class Worker(QObject):
        progressChanged = pyqtSignal(int)
        def __init__(self):
            super().__init__()
            self.table = QtWidgets.QTableWidget(10, 10)

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

        def get_ping_result(self, ips, result_queue):
            self.progressChanged.emit(0)
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

        def get_ping_results(self, ips, progressBar):
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
    
        def display_data_in_treeview(self, ping_result_list, tips, table):
            table.setRowCount(len(ping_result_list))
            for row, data in enumerate(ping_result_list):
                data_get = data.split(',')
                tip = tips[row] if row < len(tips) else ''
                for column, text in enumerate(data_get + [tip]):
                    item = QtWidgets.QTableWidgetItem(text)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    table.setItem(row, column, item)

            for row in range(table.rowCount()):
                item_for_color = table.item(row, 0)
                if item_for_color is not None:
                    text = item_for_color.text()
                    def change_color(BColor):
                        for column in range(table.columnCount()):
                            item_for_color = table.item(row, column)
                            if item_for_color is not None:
                                item_for_color.setBackground(QtGui.QColor(BColor))
    
                                BColor_RGB_16 = BColor[1:]
                                BColor_RGB = [int(BColor_RGB_16[:2], 16), int(BColor_RGB_16[2:4], 16), int(BColor_RGB_16[4:], 16)]
                                BColor_HSV = colorsys.rgb_to_hsv(BColor_RGB[0]/255.0, BColor_RGB[1]/255.0, BColor_RGB[2]/255.0)
                                V = BColor_HSV[2]
                                if V > 0.5:
                                    TColor = "#000000"
                                else:
                                    TColor = "#FFFFFF"
    
                                item_for_color.setForeground(QtGui.QColor(TColor))
    
                    if text == '💀':
                        change_color("#681313")
                    elif text == '⭐':
                        change_color("#367E18")
                    elif text == '😈':
                        change_color("#FF8400")
                    elif text == '🤯':
                        change_color("#F7D060")
                    elif text == '😟':
                        change_color("#5C9E58")
                    elif text == '😔':
                        change_color("#98D8AA")

        def ping_button(self, progressBar, entry):
            text1 = entry.text()
            ip_get1 = text1.split(',')
            ips1 = []
            tips1 = []
            for ip in ip_get1:
                self.ping(ip)
                ips1.append(ip)

            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips1))

            ping_result_list = self.get_ping_results(ips1, progressBar)
            self.display_data_in_treeview(ping_result_list, tips1, self.table)

        def ping_custom_button(self, progressBar, entry_any_1, entry_any_2, entry_any_3, entry_any_4):
            ip_1 = entry_any_1.text()
            ip_2 = entry_any_2.text()
            ip_3 = entry_any_3.text()
            ip_4 = entry_any_4.text()

            def if_ip(ip):
                ip_list = []
                if "-" in ip:
                    ip_start, ip_end = ip.split('-', 1)
                    ip_range = [str(i) for i in range(int(ip_start), int(ip_end) + 1)]
                    ip_list.extend(ip_range)
                else:
                    ip_list.append(ip)
                return ip_list
            def if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4):
                ip_lists = [ip_list_1, ip_list_2, ip_list_3, ip_list_4]
                result = []
                for ip_list in ip_lists:
                    if len(ip_list) > 1:
                        for i in ip_lists[0]:
                            for j in ip_lists[1]:
                                for k in ip_lists[2]:
                                    for l in ip_lists[3]:
                                        combined = f"{i}.{j}.{k}.{l}"
                                        result.append(combined)
                        break
                return result
            ip_list_1 = if_ip(ip_1)
            ip_list_2 = if_ip(ip_2)
            ip_list_3 = if_ip(ip_3)
            ip_list_4 = if_ip(ip_4)
            result = if_list(ip_list_1, ip_list_2, ip_list_3, ip_list_4)
            #print("result",result)

            #ips = [f"192.168.20.{i}" for i in range(1, 101)]
            ips = result
            tips = []

            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))

            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)

        def ping_local_button(self, progressBar):
            ips = ["192.168.20.254",
                   "192.168.20.204",
                   "192.168.20.203",
                   "192.168.20.201",
                   "192.168.20.200",
                   "192.168.20.101",
                   "192.168.20.11",
                   "192.168.20.1"
                ]
            tips = ["路由器",
                    "人脸识别",
                    "数据库服务器",
                    "通信管理机",
                    "NVR",
                    "101",
                    "11",
                    "1",
                ]

            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))

            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)

        def ping_local_camera_1_100_button(self, progressBar):
            ips = [f"192.168.20.{i}" for i in range(1, 101)]
            tips = []
            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))
    
            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)
    
        def ping_local_camera_101_199_button(self, progressBar):
            ips = [f"192.168.20.{i}" for i in range(101, 200)]
            tips = []
            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))
    
            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)
    
        def ping_lan_button(self, progressBar):
            name = 'LAN_IP'
            ips, tips = self.get_ip_db(name)
            print(ips)

            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))
    
            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)
    
        def ping_internet_button(self, progressBar):
            ips = ["baidu.com",
                   "bing.com",
                   "163.com",
                   "google.com",
                   "github.com",
                   "csdn.net",
                   "sketchfab.com",
                   "notion.so",
                ]
            tips = ["百度",
                    "必应",
                    "网易",
                    "Google",
                    "Github",
                    "CSDN",
                    "Sketchfab",
                    "Notion",
                ]
    
            progressBar = QProgressBar()
            progressBar.setMinimum(0)
            progressBar.setMaximum(len(ips))
    
            ping_result_list = self.get_ping_results(ips, progressBar)
            self.display_data_in_treeview(ping_result_list, tips, self.table)

class pingtool(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Let's Ping Tool"))
        progressBar = QProgressBar()
        entry1 = QtWidgets.QLineEdit()
        entry_any_1 = QtWidgets.QLineEdit()
        entry_any_2 = QtWidgets.QLineEdit()
        entry_any_3 = QtWidgets.QLineEdit()
        entry_any_4 = QtWidgets.QLineEdit()
        self.layout.addWidget(progressBar)
        fp = function_pingtool()
        f = fp.Worker()
        ping_button = partial(f.ping_button, progressBar, entry1)
        ping_custom_button = partial(f.ping_custom_button, progressBar, entry_any_1, entry_any_2, entry_any_3, entry_any_4)
        ping_local_button = partial(f.ping_local_button, progressBar)
        ping_lan_button = partial(f.ping_lan_button, progressBar)
        ping_internet_button = partial(f.ping_internet_button, progressBar)
        ping_local_camera_1_100_button = partial(f.ping_local_camera_1_100_button, progressBar)
        ping_local_camera_101_199_button = partial(f.ping_local_camera_101_199_button, progressBar)

        # 第一行：输入框和按钮
        hbox1 = QtWidgets.QHBoxLayout()
        ping_button_real = QtWidgets.QPushButton('Ping')
        ping_button_real.clicked.connect(ping_button)
        entry1.returnPressed.connect(ping_button_real.click)
        hbox1.addWidget(entry1)
        hbox1.addWidget(ping_button_real)
        self.layout.addLayout(hbox1)
        # 五个按钮
        buttons1 = [("Ping Local", ping_local_button),
            ("Ping Lan", ping_lan_button),
            ("Ping Internet", ping_internet_button)
            ]
        buttons2 = [("Ping Camera 1-100", ping_local_camera_1_100_button),
            ("Ping Camera 101-199", ping_local_camera_101_199_button)
            ]
        hbox2 = QtWidgets.QHBoxLayout()
        for text, slot in buttons1:
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(slot)
            hbox2.addWidget(button)
        hbox3 = QtWidgets.QHBoxLayout()
        for text, slot in buttons2:
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(slot)
            hbox3.addWidget(button)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.layout.addLayout(vbox)

        #Custom Ping
        hbox4 = QtWidgets.QHBoxLayout()
        costom_ping_button_real = QtWidgets.QPushButton('Ping Any')
        costom_ping_button_real.clicked.connect(ping_custom_button)
        hbox4.addWidget(entry_any_1)
        hbox4.addWidget(entry_any_2)
        hbox4.addWidget(entry_any_3)
        hbox4.addWidget(entry_any_4)
        hbox4.addWidget(costom_ping_button_real)
        self.layout.addLayout(hbox4)

        # 第四行：表格
        #table = QtWidgets.QTableWidget(10, 10)
        table = f.table
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Emoji', 'IP', 'Result', 'Status', 'Tips'])
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 120)
        table.setColumnWidth(2, 80)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 130)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(table)