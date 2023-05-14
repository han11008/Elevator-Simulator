from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Signal

from func import Elevator, Computer, PassengerState
from threading import Thread

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
        