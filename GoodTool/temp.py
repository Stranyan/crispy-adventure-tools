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


now = time.time()
timestamp = datetime.fromtimestamp(now)

formatted_timestamp = timestamp.strftime('%Y%m%d%H%M%S')
print(formatted_timestamp)
