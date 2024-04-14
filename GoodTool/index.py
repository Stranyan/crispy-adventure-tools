import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

# 创建第零个页面
class index(QWidget):
    layout: QVBoxLayout
    def open_xshell(self):
        os.startfile(r'C:\\Program Files (x86)\NetSarang\Xmanager Enterprise 5\Xshell.exe')

    def open_navicat(self):
        os.startfile(r'D:\\El\Navicat Premium 12\navicat.exe')

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("All here is useful"))
        open_xshell_button = QtWidgets.QPushButton('Open Xshell')
        open_xshell_button.clicked.connect(self.open_xshell)
        self.layout.addWidget(open_xshell_button)
        open_navicat_button = QtWidgets.QPushButton('Open Navicat')
        open_navicat_button.clicked.connect(self.open_navicat)
        self.layout.addWidget(open_navicat_button)