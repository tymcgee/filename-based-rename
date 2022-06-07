# Tynan McGee
# 6/5/2022
# Main window UI
# Using material design icons and symbols from 
# https://fonts.google.com/icons

import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from customList import customList

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html#module-PySide6.QtWidgets


# todo:
# - when adding items to list, store their full path somewhere (likely
#   necessary for renaming functionality)
# - create preview of what rename will do
# - build the actual rename functionality

# recently done:
# - add directory choose button
# - move file and directory choosing buttons to the side toolbar
# - use icons for file/dir choosing buttons
# - rounded icons instead of sharp ones
# - put left and right lists in groupboxes with labels
# - use a splitter between the left and right list
# - move file/directory opening functions to customList


class FileWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filename-based File Rename")

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.compactSizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        openFileIcon = QtGui.QIcon('icons/file_open.svg')
        openDirIcon = QtGui.QIcon('icons/folder_open.svg')

        ###############
        ## SETTINGS
        maxTargetFiles = 10
        self.settingsLayout = QtWidgets.QVBoxLayout()
        # Use a frame in order to set size policy
        self.spinboxFrame = QtWidgets.QFrame()
        self.spinboxFrame.setSizePolicy(self.compactSizePolicy)
        self.spinboxLayout = QtWidgets.QHBoxLayout(self.spinboxFrame)
        self.spinboxLayout.setContentsMargins(0, 0, 0, 0)
        self.targetFilesLabel = QtWidgets.QLabel('Number of files to rename per template file:')
        self.targetFilesLabel.setAlignment(QtCore.Qt.AlignRight)
        self.numOfTargetFiles = QtWidgets.QSpinBox()
        self.numOfTargetFiles.setRange(1, maxTargetFiles)
        self.numOfTargetFiles.setValue(1)
        self.numOfTargetFiles.valueChanged.connect(self.updateSuffixBoxes)
        self.spinboxPrev = 1
        self.spinboxLayout.addWidget(self.targetFilesLabel)
        self.spinboxLayout.addWidget(self.numOfTargetFiles)
        self.settingsLayout.addWidget(self.spinboxFrame)

        ###############
        ## SUFFIX INPUT BOXES
        # Using/keeping track of frames so that we can set visibility later
        self.suffixFrames = []
        # Keep track of boxes so we can get the text from them later
        self.suffixBoxes = []
        self.suffixBoxLayout = QtWidgets.QGridLayout()
        for i in range(maxTargetFiles):
            # Create ten suffix input boxes and store them in suffixBoxes
            suffixFrame = QtWidgets.QFrame()
            suffixLayout = QtWidgets.QHBoxLayout(suffixFrame)
            suffixLayout.setContentsMargins(0, 0, 0, 0)
            suffix = QtWidgets.QLineEdit()
            suffixLabel = QtWidgets.QLabel(f'File {i+1} Suffix:')
            suffixLayout.addWidget(suffixLabel)
            suffixLayout.addWidget(suffix)
            self.suffixBoxLayout.addWidget(suffixFrame, i//2, i%2)
            self.suffixFrames.append(suffixFrame)
            self.suffixBoxes.append(suffix)
        for s in self.suffixFrames[1:]:
            # Hide them all except the first one
            s.setVisible(False)
        self.settingsLayout.addLayout(self.suffixBoxLayout)

        ###############
        ## TOOLBAR BUTTONS, LIST BOXES
        # left
        self.leftBox = QtWidgets.QGroupBox('Template files')
        self.leftLayout = QtWidgets.QGridLayout(self.leftBox)
        self.leftList = customList()
        self.leftListBtns = self.createListBtns(self.leftList)
        # right
        self.rightBox = QtWidgets.QGroupBox('Files to be renamed')
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)
        self.rightList = customList()
        self.rightListBtns = self.createListBtns(self.rightList)

        ###############
        ## LIST LAYOUTS
        self.leftLayout.addWidget(self.leftListBtns, 1, 0)
        self.leftLayout.addWidget(self.leftList, 1, 1, 1, 2)
        self.rightLayout.addWidget(self.rightListBtns, 1, 3)
        self.rightLayout.addWidget(self.rightList, 1, 0, 1, 2)
        self.listSplitter = QtWidgets.QSplitter()
        self.listSplitter.setChildrenCollapsible(False)
        self.listSplitter.addWidget(self.leftBox)
        self.listSplitter.addWidget(self.rightBox)

        ###############
        ## BOTTOM BUTTON
        self.execButton = QtWidgets.QPushButton('Rename')
        self.execButton.clicked.connect(self.rename)

        ###############
        ## FINAL SETUP
        self.mainLayout.addLayout(self.settingsLayout)
        self.mainLayout.addWidget(self.listSplitter)
        self.mainLayout.addWidget(self.execButton)


    def createListBtns(self, l):
        # Use a frame in order to control sizePolicy
        buttonFrame = QtWidgets.QFrame()
        buttonFrame.setSizePolicy(self.compactSizePolicy)
        buttonLayout = QtWidgets.QVBoxLayout(buttonFrame)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        fileBtn = QtWidgets.QToolButton()
        dirBtn = QtWidgets.QToolButton()
        upBtn = QtWidgets.QToolButton()
        sortBtn = QtWidgets.QToolButton()
        downBtn = QtWidgets.QToolButton()
        delBtn = QtWidgets.QToolButton()
        clearBtn = QtWidgets.QToolButton()
        buttons = [fileBtn, dirBtn, upBtn, downBtn, sortBtn, delBtn, clearBtn,]
        icons = ['file_open.svg', 'folder_open.svg', 'keyboard_up.svg',
                 'keyboard_down.svg', 'sort.svg', 'close.svg',
                 'delete_forever.svg']
        tooltips = ['Open file(s)', 'Open directory', 'Move item up',
                    'Move item down', 'Sort Items', 'Remove selected item',
                    'Remove all items']
        functions = [lambda: l.openFileDialog(), lambda: l.openDirDialog(),
                     lambda: l.move(-1), lambda: l.move(1),
                     lambda: l.sortItems(), lambda: l.remove(),
                     lambda: l.clear()]
        for btn,icn,tltip,fcn in zip(buttons, icons, tooltips, functions):
            btn.setIcon(QtGui.QIcon(f'icons/{icn}'))
            btn.setIconSize(QtCore.QSize(25,25))
            btn.setToolTip(tltip)
            btn.clicked.connect(fcn)
            buttonLayout.addWidget(btn)
        return buttonFrame

    def updateSuffixBoxes(self, n):
        if self.spinboxPrev < n:
            # Spinbox increased, show next box
            self.suffixFrames[n-1].setVisible(True)
        else:
            # Spinbox decreased, remove previous box
            self.suffixFrames[n].setVisible(False)
        self.spinboxPrev = n
        
    def rename(self):
        raise NotImplementedError()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = FileWindow()
    win.show()

    sys.exit(app.exec())
