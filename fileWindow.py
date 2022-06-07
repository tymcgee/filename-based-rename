# Tynan McGee
# 6/5/2022
# Main window UI
# Using material design icons and symbols from 
# https://fonts.google.com/icons

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from customList import customList

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html#module-PySide6.QtWidgets


# todo:
# - create preview of what rename will do
# - build the actual rename functionality

class FileWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filename-based File Rename")

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.compactSizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        ###############
        ## SETTINGS
        maxTargetFiles = 10
        self.settingsLayout = QtWidgets.QVBoxLayout()
        self.spinboxLayout = QtWidgets.QHBoxLayout()
        self.spinboxLayout.setContentsMargins(0, 0, 0, 0)
        self.spinboxFrame = QtWidgets.QFrame()
        self.spinboxFrame.setLayout(self.spinboxLayout)
        self.spinboxFrame.setSizePolicy(self.compactSizePolicy)
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
            suffixLayout = QtWidgets.QHBoxLayout()
            suffixLayout.setContentsMargins(0, 0, 0, 0)
            suffixFrame = QtWidgets.QFrame()
            suffixFrame.setLayout(suffixLayout)
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
        ## FILE BUTTONS, TOOLBAR BUTTONS, LIST BOXES
        self.leftFileBtn = QtWidgets.QPushButton('Choose Template Files')
        self.rightFileBtn = QtWidgets.QPushButton('Choose Files to Rename')
        self.leftFileBtn.clicked.connect(lambda: self.openFileDialog(0))
        self.rightFileBtn.clicked.connect(lambda: self.openFileDialog(1))
        self.leftList = customList()
        self.rightList = customList()
        self.lists = [self.leftList, self.rightList]
        self.leftListBtns = self.createListBtns(0)
        self.rightListBtns = self.createListBtns(1)

        ###############
        ## LIST GRID
        self.listsGrid = QtWidgets.QGridLayout()
        self.listsGrid.addWidget(self.leftListBtns, 0, 0, 2, 1)
        self.listsGrid.addWidget(self.leftFileBtn, 0, 1)
        self.listsGrid.addWidget(self.leftList, 1, 1)
        self.listsGrid.addWidget(self.rightFileBtn, 0, 2)
        self.listsGrid.addWidget(self.rightList, 1, 2)
        self.listsGrid.addWidget(self.rightListBtns, 0, 3, 2, 1)

        ###############
        ## BOTTOM BUTTON
        self.execButton = QtWidgets.QPushButton('Rename')
        self.execButton.clicked.connect(self.rename)

        ###############
        ## FINAL SETUP
        self.mainLayout.addLayout(self.settingsLayout)
        self.mainLayout.addLayout(self.listsGrid)
        self.mainLayout.addWidget(self.execButton)


    def createListBtns(self, n):
        listLayout = QtWidgets.QVBoxLayout()
        # Don't add any margins to the frame
        listLayout.setContentsMargins(0, 0, 0, 0)
        # Use a frame instead of a layout in order to use a size policy
        listFrame = QtWidgets.QFrame()
        listFrame.setLayout(listLayout)
        listFrame.setSizePolicy(self.compactSizePolicy)
        upBtn = QtWidgets.QToolButton()
        sortBtn = QtWidgets.QToolButton()
        downBtn = QtWidgets.QToolButton()
        delBtn = QtWidgets.QToolButton()
        clearBtn = QtWidgets.QToolButton()
        buttons = [upBtn, downBtn, sortBtn, delBtn, clearBtn]
        l = self.lists[n]
        icons = ['keyboard_up.svg', 'keyboard_down.svg',
                 'sort.svg', 'close.svg', 'delete_forever.svg']
        tooltips = ['Move item up', 'Move item down',
                    'Sort Items', 'Remove selected item', 'Remove all items']
        functions = [lambda: l.move(-1), lambda: l.move(1),
                     lambda: l.sortItems(), lambda: l.remove(),
                     lambda: l.clear()]
        for btn,icn,tltip,fcn in zip(buttons, icons, tooltips, functions):
            btn.setIcon(QtGui.QIcon(f'icons/{icn}'))
            btn.setIconSize(QtCore.QSize(25,25))
            btn.setToolTip(tltip)
            btn.clicked.connect(fcn)
            listLayout.addWidget(btn)
        return listFrame

    def openFileDialog(self, n):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        files = dialog.getOpenFileNames()[0]
        self.lists[n].addFilenames(files)

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
