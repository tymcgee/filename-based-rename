# Tynan McGee
# 6/5/2022
# Main renaming functionality

import sys
from PySide6 import QtCore, QtGui, QtWidgets
from fileWindow import FileWindow


class MainWindow(FileWindow):
    def __init__(self):
        super().__init__()
    
    def rename(self):
        print('show preview of rename with prompt to continue or cancel')
        for suffixBox in self.suffixBoxes:
            if suffixBox.isVisible():
                print(suffixBox.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
