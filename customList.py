# Tynan McGee
# 6/5/2022
# QListWidget with ability for files to be drag/dropped in and with items being
# deselected when you click in a blank area. Includes functions which can be
# attached to buttons allowing for moving, removing, and clearing selected
# items, as well as for adding items using file and directory browsing.

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html

import os
from PySide6 import QtCore, QtWidgets, QtGui


class CustomList(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAlternatingRowColors(True)

    def addFilenames(self, filePaths):
        """filePaths has to be a list."""
        fnames = []
        for f in filePaths:
            bn = os.path.basename(f)
            if os.path.isdir(f):
                bn = bn + "/"
            fnames.append(bn)
        items = [QtWidgets.QListWidgetItem(f) for f in fnames]
        for i, fullPath in zip(items, filePaths):
            # Store the full path of the item in its tooltip
            i.setToolTip(fullPath)
            self.addItem(i)

    def dragEnterEvent(self, event):
        # If dragging a file, accept it, otherwise do default behavior
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        # If dropping a file, add it to the list, otherwise do default behavior
        if event.mimeData().hasUrls():
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            self.addFilenames(files)
        else:
            super().dropEvent(event)

    def mousePressEvent(self, event):
        # Deselect currently selected item if the click wasn't on an item
        pos = event.position()
        pt = QtCore.QPoint(pos.x(), pos.y())
        idx = self.indexAt(pt)
        super().mousePressEvent(event)
        if not idx.isValid():
            self.setCurrentRow(-1)
            self.setCurrentItem(None)

    def openFileDialog(self):
        files = QtWidgets.QFileDialog.getOpenFileNames()[0]
        self.addFilenames(files)

    def openRecursiveDirDialog(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory()
        fileList = []
        for root, dirs, files in os.walk(dir):
            for filename in files:
                fileList.append(os.path.join(root, filename))
        fileList.sort()
        self.addFilenames(fileList)

    def move(self, dir):
        """dir is 1 if moving down and -1 if moving up, so bool(dir+1) is
        true if moving down and false if moving up."""
        n = self.count()
        items = self.selectedItems()
        if len(items) > 0:
            rows = []
            # Placed keeps track of the items which have already moved. If an
            # item tries to move into one of the ones that has already moved
            # then it's at one of the edges and it shouldn't keep going.
            placed = []
            # Get rows of selected items
            for i in items:
                idx = self.indexFromItem(i)
                rows.append(idx.row())
            # Sort them so not to mess up indices during the move.
            # Reverse or not depending on direction of move
            rows.sort(reverse=bool(dir + 1))
            for row in rows:
                if row + dir >= 0 and row + dir < n and row + dir not in placed:
                    new = row + dir
                else:
                    new = row
                itm = self.takeItem(row)
                self.insertItem(new, itm)
                placed.append(new)
                # Keep all the items selected after they're moved
                itm.setSelected(True)
            self.setCurrentItem(itm)

    def remove(self):
        items = self.selectedItems()
        for i in items:
            idx = self.indexFromItem(i)
            self.takeItem(idx.row())

    def clear(self):
        for _ in range(self.count()):
            self.takeItem(0)
