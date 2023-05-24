# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remote.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_RemoteWindow(object):
    def setupUi(self, RemoteWindow):
        RemoteWindow.setObjectName("RemoteWindow")
        RemoteWindow.resize(760, 440)
        self.centralwidget = QtWidgets.QWidget(RemoteWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.instr1_1 = QtWidgets.QLabel(self.centralwidget)
        self.instr1_1.setGeometry(QtCore.QRect(20, 60, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.instr1_1.setFont(font)
        self.instr1_1.setObjectName("instr1_1")
        self.instr2_1 = QtWidgets.QLabel(self.centralwidget)
        self.instr2_1.setGeometry(QtCore.QRect(20, 240, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.instr2_1.setFont(font)
        self.instr2_1.setObjectName("instr2_1")
        self.stat1 = QtWidgets.QLabel(self.centralwidget)
        self.stat1.setGeometry(QtCore.QRect(270, 60, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.stat1.setFont(font)
        self.stat1.setAlignment(QtCore.Qt.AlignCenter)
        self.stat1.setObjectName("stat1")
        self.stat2 = QtWidgets.QLabel(self.centralwidget)
        self.stat2.setGeometry(QtCore.QRect(270, 240, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.stat2.setFont(font)
        self.stat2.setAlignment(QtCore.Qt.AlignCenter)
        self.stat2.setObjectName("stat2")
        self.btn_ctr1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ctr1.setGeometry(QtCore.QRect(580, 80, 150, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.btn_ctr1.setFont(font)
        self.btn_ctr1.setObjectName("btn_ctr1")
        self.btn_ctr2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ctr2.setGeometry(QtCore.QRect(580, 260, 150, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.btn_ctr2.setFont(font)
        self.btn_ctr2.setObjectName("btn_ctr2")
        self.instr1_2 = QtWidgets.QLabel(self.centralwidget)
        self.instr1_2.setGeometry(QtCore.QRect(28, 120, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.instr1_2.setFont(font)
        self.instr1_2.setObjectName("instr1_2")
        self.floor1 = QtWidgets.QLabel(self.centralwidget)
        self.floor1.setGeometry(QtCore.QRect(260, 120, 40, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.floor1.setFont(font)
        self.floor1.setObjectName("floor1")
        self.floor2 = QtWidgets.QLabel(self.centralwidget)
        self.floor2.setGeometry(QtCore.QRect(260, 300, 40, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.floor2.setFont(font)
        self.floor2.setObjectName("floor2")
        self.instr2_2 = QtWidgets.QLabel(self.centralwidget)
        self.instr2_2.setGeometry(QtCore.QRect(28, 300, 220, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.instr2_2.setFont(font)
        self.instr2_2.setObjectName("instr2_2")
        RemoteWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RemoteWindow)
        QtCore.QMetaObject.connectSlotsByName(RemoteWindow)

    def retranslateUi(self, RemoteWindow):
        _translate = QtCore.QCoreApplication.translate
        RemoteWindow.setWindowTitle(_translate("RemoteWindow", "Remote Elevator Monitor"))
        self.instr1_1.setText(_translate("RemoteWindow", "Elevator 1 status:"))
        self.instr2_1.setText(_translate("RemoteWindow", "Elevator 2 status:"))
        self.stat1.setText(_translate("RemoteWindow", "Maintenance"))
        self.stat2.setText(_translate("RemoteWindow", "Maintenance scheduled"))
        self.btn_ctr1.setText(_translate("RemoteWindow", "Stop\n"
"Elevator 1"))
        self.btn_ctr2.setText(_translate("RemoteWindow", "Stop Elevator 2"))
        self.instr1_2.setText(_translate("RemoteWindow", "currently at floor:"))
        self.floor1.setText(_translate("RemoteWindow", "10"))
        self.floor2.setText(_translate("RemoteWindow", "10"))
        self.instr2_2.setText(_translate("RemoteWindow", "currently at floor:"))
