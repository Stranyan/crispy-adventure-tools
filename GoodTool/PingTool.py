import colorsys, os, sys, subprocess, time, sqlite3, re
from ping3 import ping
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
from queue import Queue
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
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

        def get_ip_db(self, sheet_name, ip_column_name='IP', tips_column_name='Tips', db_url='d:\SQLite\IP-Data.db'):
            with sqlite3.connect(db_url) as conn:
                cursor = conn.cursor()
                ip_query = 'SELECT {} FROM {}'.format(ip_column_name, sheet_name)
                tips_query = 'SELECT {} FROM {}'.format(tips_column_name, sheet_name)
                cursor.execute(ip_query)
                ip_rows = cursor.fetchall()
                cursor.execute(tips_query)
                tips_rows = cursor.fetchall()
                ip_list = [row[0] for row in ip_rows]
                tips_list = [row[0] for row in tips_rows]
            return ip_list, tips_list

        def save_ping_results_to_database(self, ping_results):
            # 获取当前时间戳
            now = time.time()
            timestamp = datetime.fromtimestamp(now)
            #formatted_timestamp = timestamp.strftime('%Y%m%d%H%M%S')
            formatted_timestamp = timestamp.strftime('%Y%m%d%H%M%S')

            # 计算 ping_results 字典中的 IP 总数量
            total_ips = len(ping_results)

            # 构建表格名字
            table_name = str(formatted_timestamp) + '_' + str(total_ips)
            table_name = table_name.replace('-', '_').replace(':', '_')

            # 连接到数据库（如果数据库不存在，将会自动创建）
            conn = sqlite3.connect('d:\SQLite\ping_results.db')

            # 创建表格（如果表格不存在，将会自动创建）
            conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    ip TEXT PRIMARY KEY,
                    tip TEXT,
                    result TEXT
                )
            ''')

            # 插入数据
            for ip, data in ping_results.items():
                result = data.get('result', 'NO! FAIL!!!')
                tip = data.get('tip', '')

                conn.execute(f'INSERT INTO {table_name} (ip, result, tip) VALUES (?, ?, ?)',
                            (ip, result, tip))

            # 提交更改
            conn.commit()
            print('结果已提交SQLite数据库')

            # 关闭连接
            conn.close()

        def ping(self, ip):
            result = ping(ip,timeout=2,unit='ms',size=56)
            return result

        def get_ping_results(self, ips, tips):
            start = time.time()
            result_queue = Queue()
            ping_results = {}

            def set_ping_result(index, ip):
                result = 'NO! FAIL!!!'
                result = function_pingtool.Worker.ping(self, ip)
                rank = 'NO! FAIL!!!'
                if isinstance(result, float):
                    result = f'{result:.2f}毫秒'
                    rank = 1
                    #print('if', result)
                elif result is None:
                    result = 'NO! FAIL!!!'
                    rank = 'NO! FAIL!!!'
                    #print('elif', result)
                else:
                    result = 'NO! FAIL!!!'
                    rank = 'NO! FAIL!!!'
                    #print('else', result)

                ping_results[ip] = {
                    'result': result,
                    'tip': tips[index] if index < len(tips) else '',
                    'rank': rank
                }
                return

            threads = []
            if len(ips) < 10000:
                print('\n')
                print('>>>>>>>>>>')
                # 处理全部IP地址
                for index, ip in enumerate(ips):
                    thread = Thread(target=lambda i=index, ip=ip: set_ping_result(i, ip))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
            else:
                # 每次处理一万个IP地址
                print('\n')
                print('>>>>>>>>>>')
                print('有%s个IP！太多了！' % (len(ips)))

                num_ips = len(ips)
                num_batches = num_ips // 10000
                remaining_ips = num_ips % 10000
                
                for batch in range(num_batches):
                    temp_start_time = time.time()
                    start_index = batch * 10000
                    end_index = (batch + 1) * 10000
                    batch_ips = ips[start_index:end_index]

                    for index, ip in enumerate(batch_ips):
                        thread = Thread(target=lambda i=index, ip=ip: set_ping_result(i, ip))
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()

                    threads.clear()

                    now = time.time()
                    running_time = now - temp_start_time
                    dt_now = datetime.fromtimestamp(now)
                    finished_ip = num_ips - remaining_ips
                    print('第%s批完成%s个IP！耗时:%.3f秒！还剩余%s' % (batch+1, finished_ip, running_time, remaining_ips))
                    print('现在时间:%s' % dt_now)

                if remaining_ips > 0:
                    last_temp_start_time = time.time()
                    start_index = num_batches * 10000
                    end_index = num_ips
                    remaining_batch_ips = ips[start_index:end_index]

                    for index, ip in enumerate(remaining_batch_ips):
                        thread = Thread(target=lambda i=index, ip=ip: set_ping_result(i, ip))
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()

                    threads.clear()
                    # 调用函数保存 ping_results 到数据库中
                    self.save_ping_results_to_database(ping_results)

                    now = time.time()
                    running_time = now - last_temp_start_time
                    dt_now = datetime.fromtimestamp(now)
                    print('最后一批完成%s个IP！耗时:%.3f秒' % (remaining_ips, running_time))
                    print('现在时间:%s' % dt_now)


            # 根据result值的大小对ping_results进行排序
            # 定义用于排序的辅助函数
            def sort_key(item):
                if item[1]['result'] != bool:
                    if item[1]['result'] != 'NO! FAIL!!!':
                        return float(item[1]['result'][:-2])
                    elif type(item[1]['result']) == bool:
                        return item[1]['result']
                    else:
                        return float('inf')

            # 对 ping_results 进行排序
            sorted_results = sorted(ping_results.items(), key=sort_key, reverse=False)
            # 为每个IP分配对应的排序值
            for i, (ip, data) in enumerate(sorted_results):
                data['rank'] = i + 1
                ping_results[ip]['rank'] = data['rank']

            now = time.time()
            running_time = now - start
            dt_now = datetime.fromtimestamp(now)

            print('完成{}个IP！耗时:{:.3f}秒'.format(len(ips), running_time))
            print('现在时间:%s' % dt_now)
            print('>>>>>>>>>>')
            return ping_results

        def display_data_in_treeview(self, ping_results, table):
            def change_color(table, row, background_color):
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        item.setBackground(QtGui.QColor(background_color))

                        background_rgb = QtGui.QColor(background_color).getRgb()[:3]
                        background_hsv = colorsys.rgb_to_hsv(background_rgb[0] / 255.0, background_rgb[1] / 255.0, background_rgb[2] / 255.0)
                        V = background_hsv[2]
                        ori_text_color = 1 - V
                        if 0.5 < ori_text_color <= 0.9:
                            ori_text_color = 0.9
                        elif 0.1 <= ori_text_color <= 0.5:
                            ori_text_color = 0.1
                        c = map_range(ori_text_color, 0, 1, -45, 255)
                        i = int(c)
                        text_color = rgb_to_hex(i ,i, i)

                        item.setForeground(QtGui.QColor(text_color))
                    else:
                        item.setBackground(QtGui.QColor(background_color))
                return

            def rgb_to_hex(r, g, b):
                hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
                return hex_color

            def map_range(value, min_value, max_value, new_min, new_max):
                #min_value = 0  # 原始值的最小范围
                #max_value = 500  # 原始值的最大范围
                #new_min = 255  # 目标映射值的最小范围
                #new_max = 0  # 目标映射值的最大范围
                return (value - min_value) * (new_max - new_min) / (max_value - min_value) + new_min

            def set_table_item(row, column, item, number=False):
                item_data = QtWidgets.QTableWidgetItem(item)
                if number:
                    item_data.setData(QtCore.Qt.DisplayRole, item)
                item_data.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, column, item_data)

            table.clearContents()
            table.setRowCount(0)
            if ping_results:
                table.setRowCount(len(ping_results))

            sorting_enabled = table.isSortingEnabled()  # 保存排序状态

            table.setSortingEnabled(False)  # 禁用排序

            if ping_results:
                for row, (ip, data) in enumerate(ping_results.items()):
                    status = data.get('result', 'NO! FAIL!!!')
                    tip = data.get('tip', '')
                    rank = data.get('rank')

                    set_table_item(row, 1, ip)
                    set_table_item(row, 3, status)
                    set_table_item(row, 4, tip)
                    set_table_item(row, 5, rank, True)

                    if status == 'NO! FAIL!!!':
                        set_table_item(row, 2, status)
                        set_table_item(row, 0, '💀')

                        origin_value = int(rank)
                        value = int(map_range(origin_value, len(ping_results), 1, 30, 0))
                        r = value + 30
                        g = value *0.3
                        b = value * 0.5
                        no_hex_color = rgb_to_hex(int(r), int(g), int(b))
                        #change_color(table, row, "#681313")
                        change_color(table, row, no_hex_color)
                    else:
                        set_table_item(row, 2, 'SUCCESSFUL!')
                        set_table_item(row, 0, '🤩')

                        origin_value = int(float(status[:-2]))
                        value = int(map_range(origin_value, 0, 500, 255, 0))
                        r = value * 0.25
                        g = value
                        b = value * 0.5
                        yes_hex_color = rgb_to_hex(int(r), int(g), int(b))
                        change_color(table, row, yes_hex_color)
            table.setSortingEnabled(sorting_enabled)  # 恢复排序状态
            table.setSortingEnabled(True)
            return

        def ping_button(self, entry):
            text = entry.text()
            ip_get = text.split(',')
            ips = []
            tips = []
            for ip in ip_get:
                self.ping(ip)
                ips.append(ip)

            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

        def ping_custom_button(self, entry_any_1, entry_any_2, entry_any_3, entry_any_4):
            ip_1 = entry_any_1.text()
            ip_2 = entry_any_2.text()
            ip_3 = entry_any_3.text()
            ip_4 = entry_any_4.text()

            def if_ip(ip):
                if ip == '':
                    ip = '0-255'
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
            ips = result
            tips = []

            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

        def ping_local_button(self):
            name = 'LOCAL_IP'
            ips, tips = self.get_ip_db(name)
            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

        def ping_local_0_255_button(self):
            ips = [f"192.168.20.{i}" for i in range(0, 255)]
            tips = []
            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

        def ping_lan_button(self):
            name = 'LAN_IP'
            ips, tips = self.get_ip_db(name)
            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

        def ping_internet_button(self):
            name = 'INTERNET_IP'
            ips, tips = self.get_ip_db(name)
            ping_result_list = self.get_ping_results(ips, tips)
            self.display_data_in_treeview(ping_result_list, self.table)
            return

class pingtool(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Let's Ping Tool"))
        entry1 = QtWidgets.QLineEdit()
        entry_any_1 = QtWidgets.QLineEdit()
        entry_any_2 = QtWidgets.QLineEdit()
        entry_any_3 = QtWidgets.QLineEdit()
        entry_any_4 = QtWidgets.QLineEdit()
        fp = function_pingtool()
        f = fp.Worker()
        ping_button = partial(f.ping_button, entry1)
        ping_custom_button = partial(f.ping_custom_button, entry_any_1, entry_any_2, entry_any_3, entry_any_4)
        ping_local_button = partial(f.ping_local_button)
        ping_lan_button = partial(f.ping_lan_button)
        ping_internet_button = partial(f.ping_internet_button)
        ping_local_0_255_button = partial(f.ping_local_0_255_button)

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
        buttons2 = [("Ping 0-255", ping_local_0_255_button),
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
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(['Emoji', 'IP', 'Result', 'Status', 'Tips', 'Rank'])
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 120)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 130)
        table.setColumnWidth(5, 50)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(table)