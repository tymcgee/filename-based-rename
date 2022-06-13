# Tynan McGee
# 6/8/2022
# Popup window to display two columns of text in a table.
# Not using a QDialog because it seems too restrictive for this case (can't
# resize the window easily, can't add my own widgets to it easily)

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/QDialog.html
# https://doc.qt.io/qtforpython/PySide6/QtWidgets/QTableWidget.html

import sys
from PySide6 import QtCore, QtWidgets, QtGui


class PreviewDialog(QtWidgets.QDialog):
    def __init__(self, left, right):
        super().__init__()
        okIcon = QtGui.QIcon("icons/check_circle.svg")
        cancelIcon = QtGui.QIcon("icons/cancel.svg")
        maxs = QtWidgets.QSizePolicy.Maximum
        self.compactSizePolicy = QtWidgets.QSizePolicy(maxs, maxs)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainTable = QtWidgets.QTableWidget(len(left), 2)
        self.mainTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        # Set header names and sizes
        leftHeader = QtWidgets.QTableWidgetItem("Original Filename")
        rightHeader = QtWidgets.QTableWidgetItem("New Filename")
        self.mainTable.setHorizontalHeaderItem(0, leftHeader)
        self.mainTable.setHorizontalHeaderItem(1, rightHeader)
        header = self.mainTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # Create two columns of table items containing the items in the left
        # and right lists
        for i, (l, r) in enumerate(zip(left, right)):
            li = QtWidgets.QTableWidgetItem(l)
            ri = QtWidgets.QTableWidgetItem(r)
            self.mainTable.setItem(i, 0, li)
            self.mainTable.setItem(i, 1, ri)
        # Set the table items to be read only
        self.mainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Create the "ok" and "cancel" buttons
        self.ok = QtWidgets.QPushButton("Rename!")
        self.ok.setIcon(okIcon)
        self.ok.setIconSize(QtCore.QSize(20, 20))
        self.ok.setAutoDefault(False)
        self.cancel = QtWidgets.QPushButton("Cancel")
        self.cancel.setIcon(cancelIcon)
        self.cancel.setIconSize(QtCore.QSize(20, 20))
        self.cancel.setDefault(True)
        self.btns = QtWidgets.QDialogButtonBox()
        self.btns.addButton(self.ok, QtWidgets.QDialogButtonBox.AcceptRole)
        self.btns.addButton(self.cancel, QtWidgets.QDialogButtonBox.RejectRole)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)

        self.mainLayout.addWidget(self.mainTable)
        self.mainLayout.addWidget(self.btns)

    def accept(self):
        # Show warning box and then do default behavior
        ret = QtWidgets.QMessageBox.warning(
            self,
            self.windowTitle(),
            "Warning: renaming files can be a dangerous operation. To avoid data loss, "
            "it may be a good idea to back up your files before proceeding.",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel,
        )
        if ret == QtWidgets.QMessageBox.Ok:
            super().accept()
