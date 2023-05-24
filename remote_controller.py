from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Signal

from enum import Enum
from threading import Thread, Lock
from time import sleep
import socket

from remote_window import Ui_RemoteWindow

class ElevatorState(Enum):
    MAINTAIN = 0
    TO_MAINTAIN = 1
    WORKING = 2

class RemoteWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RemoteWindow()
        self.ui.setupUi(self)
        self.running = True
        self.sendAva = Lock()
        self.elv1_stat = ElevatorState.WORKING
        self.ui.stat1.setText('Working')
        self.elv2_stat = ElevatorState.WORKING
        self.ui.stat2.setText('Working')
        self.ui.floor1.setText('')
        self.ui.floor2.setText('')
        self.ui.btn_ctr1.setText('Stop\nElevator 1')
        self.ui.btn_ctr2.setText('Stop\nElevator 2')
        self.rmt_sock_thread = Thread(target=self.setupRemote)
        self.rmt_sock_thread.daemon = True
        self.rmt_sock_thread.start()
        self.ui.btn_ctr1.clicked.connect(lambda: self.sendCmd(1))
        self.ui.btn_ctr2.clicked.connect(lambda: self.sendCmd(2))

    def sendCmd(self, elv):
        if elv == 1:
            if self.elv1_stat == ElevatorState.WORKING:
                self.elv1_stat = ElevatorState.TO_MAINTAIN
                self.ui.stat1.setText('Maintenance scheduled')
                with self.sendAva:
                    _ = self.sock.send(bytes('stop1', 'utf-8')) 
                self.ui.btn_ctr1.setText('Restart\nElevator 1')
            elif self.elv1_stat == ElevatorState.MAINTAIN:
                with self.sendAva:
                    _ = self.sock.send(bytes('restart1', 'utf-8'))
                self.ui.stat1.setText('Working')
                self.ui.btn_ctr1.setText('Stop\nElevator 1')
        elif elv == 2:
            if self.elv2_stat == ElevatorState.WORKING:
                self.elv2_stat = ElevatorState.TO_MAINTAIN
                self.ui.stat2.setText('Maintenance scheduled')
                with self.sendAva:
                    _ = self.sock.send(bytes('stop2', 'utf-8')) 
                self.ui.btn_ctr2.setText('Restart\nElevator 2')
            elif self.elv2_stat == ElevatorState.MAINTAIN:
                with self.sendAva:
                    _ = self.sock.send(bytes('restart2', 'utf-8'))
                self.ui.stat2.setText('Working')
                self.ui.btn_ctr2.setText('Stop\nElevator 2')

    def setupRemote(self):
        host, port = '127.0.0.1', 8000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
            self.rmt_thread = Thread(target=self.getStat)
            self.rmt_thread.start()
        except socket.error:
            print('Remote connection failed.')
    
    def getStat(self):
        while self.running:
            with self.sendAva:
                _ = self.sock.send(bytes('stat', 'utf-8'))
            try:
                msg = self.sock.recv(1024).decode()
                stat1, flr1, stat2, flr2 = msg.split(',')
                if stat1 == 'True':
                    self.elv1_stat = ElevatorState.MAINTAIN
                    self.ui.stat1.setText('Maintenance')
                elif self.elv1_stat == ElevatorState.TO_MAINTAIN:
                    self.elv1_stat = ElevatorState.WORKING
                self.ui.floor1.setText(flr1)
                if stat2 == 'True':
                    self.elv2_stat = ElevatorState.MAINTAIN
                    self.ui.stat2.setText('Maintenance')
                elif self.elv2_stat == ElevatorState.TO_MAINTAIN:
                    self.elv2_stat = ElevatorState.WORKING
                self.ui.floor2.setText(flr2)
            except:
                break
            sleep(0.1)

    def closeEvent(self, event):
        self.running = False
        self.sock.close()
        self.rmt_sock_thread.join()
        try:
            self.rmt_thread.join()
        except:
            pass
