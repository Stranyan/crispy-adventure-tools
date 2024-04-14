import os, sys, subprocess, pyuac
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

# 创建第二个页面
class changeip(QWidget):
    layout: QVBoxLayout
    def change_IP_with_admin(self, ip, mask, gateway):
        adapter_name = '以太网'
        def run_netsh():
            cmd_IP = f'netsh interface ip set address name="{adapter_name}" static {ip} {mask} {gateway}'
            cmd_DHCP = f'netsh interface ip set address name="{adapter_name}" source=dhcp'
            print(f'Running command: {cmd_IP if ip else cmd_DHCP}')
            if ip:
                subprocess.run(cmd_IP)
            else:
                subprocess.run(cmd_DHCP)
        if not pyuac.isUserAdmin():
            print("Not an admin, re-launching as admin")
            pyuac.runAsAdmin()
            print("After calling runAsAdmin")
            subprocess.Popen([sys.executable, __file__])
            print("subprocess")
            os._exit(0)
        else:
            print("Already an admin, running netsh")
            run_netsh()
    def change_DHCP(self):
        ip = ''
        mask = ''
        gateway = ''
        self.change_IP_with_admin(ip, mask, gateway)
    def change_IP_local(self):
        ip = '192.168.20.244'
        mask = '255.255.255.0'
        gateway = '192.168.20.254'
        self.change_IP_with_admin(ip, mask, gateway)
    def change_IP_dtn(self):
        ip = '10.75.165.101'
        mask = '255.255.255.248'
        gateway = '10.75.165.97'
        self.change_IP_with_admin(ip, mask, gateway)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel('这是第二个页面，被计划用来做修改IP设置的功能'))
        # 第一行：三个更改IP按钮
        change_DHCP_button = QtWidgets.QPushButton('Change DHCP')
        change_DHCP_button.clicked.connect(self.change_DHCP)
        self.layout.addWidget(change_DHCP_button)
        change_IP_local_button = QtWidgets.QPushButton('Change IP to 192.168.20.244')
        change_IP_local_button.clicked.connect(self.change_IP_local)
        self.layout.addWidget(change_IP_local_button)
        change_IP_dtn_button = QtWidgets.QPushButton('Change IP to dtn')
        change_IP_dtn_button.clicked.connect(self.change_IP_dtn)
        self.layout.addWidget(change_IP_dtn_button)