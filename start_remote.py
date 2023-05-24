from PySide2 import QtWidgets
from remote_controller import RemoteWindow_controller

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	window = RemoteWindow_controller()
	window.show()
	sys.exit(app.exec_())