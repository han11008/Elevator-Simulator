from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Signal

from func import Elevator, Computer, PassengerState
from threading import Thread
import socket

from main_window import Ui_MainWindow
from pop_window import Ui_Form

def formatFlr(flr: int) -> str:
    return f'<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">{flr}</span></p></body></html>'

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.move(100, 100)
        self.ui.callElvBtn.clicked.connect(self.addPsg)
        self.com = Computer()
        self.com_thread = Thread(target=self.com.get_tasks)
        self.com_thread.start()
        self.ui.elv1ShowFlr.setText(f'{formatFlr(self.com.elevator1.display_floor())}')
        self.ui.elv2ShowFlr.setText(f'{formatFlr(self.com.elevator2.display_floor())}')
        self.task_monitor = Thread(target=self.update)
        self.task_monitor.start()
        self.rmt_sock_thread = Thread(target=self.setupRemote)
        self.rmt_sock_thread.daemon = True
        self.rmt_sock_thread.start()

    def setupRemote(self):
        host, port = '127.0.0.1', 8000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((host, port))
            self.sock.listen(1)
            self.conn, self.conn_addr = self.sock.accept()
            self.rmt_thread = Thread(target=self.rcvCmd)
            self.rmt_thread.start()
        except socket.error:
            print('Remote connection failed.')

    def rcvCmd(self):
        while self.com.running:
            try:
                msg = self.conn.recv(1024).decode()
                if msg == 'stat':
                    stat1 = (not self.com.elevator1.running) and (not self.com.elevator1.moving)
                    stat2 = (not self.com.elevator2.running) and (not self.com.elevator1.moving)
                    _ = self.conn.send(bytes(f'{stat1},{self.com.elevator1.display_floor()},{stat2},{self.com.elevator2.display_floor()}', 'utf-8'))
                elif msg == 'stop1':
                    self.com.elv_to_maintain(1)
                elif msg == 'stop2':
                    self.com.elv_to_maintain(2)
                elif msg == 'restart1':
                    self.com.elv_restart(1)
                elif msg == 'restart2':
                    self.com.elv_restart(2)
            except:
                break
        if self.com.running:
            self.rmt_sock_thread.join()
            self.rmt_sock_thread = Thread(target=self.setupRemote)
            self.rmt_sock_thread.daemon = True
            self.rmt_sock_thread.start()

    def ctrlCom(self, info):
        _from, _to = info
        row_i = self.ui.waitingPsg.rowCount()
        self.ui.waitingPsg.insertRow(row_i)
        fromItem = QTableWidgetItem(_from); fromItem.setTextAlignment(QtCore.Qt.AlignCenter)
        toItem = QTableWidgetItem(_to); toItem.setTextAlignment(QtCore.Qt.AlignCenter)
        finItem = QTableWidgetItem(''); finItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.ui.waitingPsg.setItem(row_i, 0, fromItem)
        self.ui.waitingPsg.setItem(row_i, 1, toItem)
        self.ui.waitingPsg.setItem(row_i, 2, finItem)
        self.com.tasks.put((row_i, int(_from), int(_to)), block=False)

    def addPsg(self):
        self.childWindow = PopWindow_controller()
        self.childWindow.returnInfo.connect(self.ctrlCom)
        self.childWindow.show()
    
    def closeEvent(self, event):
        self.com.running = False
        self.com_thread.join()
        self.task_monitor.join()
        self.sock.close()
        self.rmt_sock_thread.join()
        try:
            self.rmt_thread.join()
        except:
            pass
    
    def update(self):
        while self.com.running:
            self.ui.elv1ShowFlr.setText(f'{formatFlr(self.com.elevator1.display_floor())}')
            self.ui.elv2ShowFlr.setText(f'{formatFlr(self.com.elevator2.display_floor())}')
            copy_state = self.com.task_state.copy()
            for tid, state in copy_state.items():
                if state[0] == PassengerState.ARRIVED:
                    finItem = self.ui.waitingPsg.item(tid, 2)
                    finItem.setText('v')

class PopWindow_controller(QtWidgets.QWidget):
    returnInfo = Signal(tuple)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.endInput)

    def endInput(self):
        self.returnInfo.emit((self.ui.comboBoxFrom.currentText(), self.ui.comboBoxTo.currentText()))
        self.close()
        