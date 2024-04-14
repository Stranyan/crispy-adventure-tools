import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTabWidget, QMainWindow
from index import index
from PingTool import pingtool
from ChangeIP import changeip
#from PingAlwaysTool import pingalwaystool

app = QtWidgets.QApplication(sys.argv)
window = QMainWindow()
window.resize(640, 640)
window.setWindowTitle('Good Tool')
tab_widget = QTabWidget() # 创建一个QTabWidget对象

index = index()
pingtool = pingtool()
changeip = changeip()
#pingalwaystool = pingalwaystool()
tab_widget.addTab(index, 'Index')
tab_widget.addTab(pingtool, 'Ping Tool')
tab_widget.addTab(changeip, 'Change IP')
#tab_widget.addTab(pingalwaystool, 'Ping Always Tool')

window.setCentralWidget(tab_widget)
window.show()
sys.exit(app.exec_())
