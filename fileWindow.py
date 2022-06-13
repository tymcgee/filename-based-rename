# Tynan McGee
# 6/5/2022
# Main window UI
# Using material design icons and symbols from
# https://fonts.google.com/icons
# Code formatted using black

import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from customList import CustomList

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html#list-of-classes


# todo:
# - add an option to specify destination path? so files are copied instead of
#   renamed in place
# - progress bar?
# - add a tick box to the warning message to give the option of never showing it again

# recently done:
# - add a warning about moving files being dangerous
# - code changes:
# -- long strings split into multiple lines
# -- single quotes '' to double quotes ""
# -- some code formatting changes
# -- some more comments and docstrings


class FileWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filename-based File Rename")

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        # Don't stretch at all
        maxs = QtWidgets.QSizePolicy.Maximum
        mins = QtWidgets.QSizePolicy.Minimum
        self.compactSizePolicy = QtWidgets.QSizePolicy(maxs, maxs)
        # Only stretch horizontally
        self.compactVertSizePolicy = QtWidgets.QSizePolicy(mins, maxs)
        previewIcon = QtGui.QIcon("icons/preview.svg")
        # Filenames can't contain certain characters
        filenameRegex = QtCore.QRegularExpression(r'[^<>:"/\\\|\?\*]*')
        filenameValidator = QtGui.QRegularExpressionValidator(filenameRegex)

        ###############
        # SETTINGS
        boxesPerRow = 2
        numOfBoxCols = 5
        maxTargetFiles = boxesPerRow * numOfBoxCols
        self.settingsLayout = QtWidgets.QVBoxLayout()
        # Use a frame in order to set size policy
        self.spinboxFrame = QtWidgets.QFrame()
        self.spinboxFrame.setSizePolicy(self.compactSizePolicy)
        self.spinboxLayout = QtWidgets.QHBoxLayout(self.spinboxFrame)
        self.spinboxLayout.setContentsMargins(0, 0, 0, 0)
        self.targetFilesLabel = QtWidgets.QLabel(
            "Number of files to rename per template file:"
        )
        self.targetFilesLabel.setAlignment(QtCore.Qt.AlignRight)
        self.numOfTargetFiles = QtWidgets.QSpinBox()
        self.numOfTargetFiles.setRange(1, maxTargetFiles)
        self.numOfTargetFiles.setValue(1)
        self.numOfTargetFiles.valueChanged.connect(self.updateSuffixBoxes)
        self.spinboxPrevValue = 1
        self.spinboxLayout.addWidget(self.targetFilesLabel)
        self.spinboxLayout.addWidget(self.numOfTargetFiles)
        self.settingsLayout.addWidget(self.spinboxFrame)

        ###############
        # SUFFIX INPUT BOXES
        # Using/keeping track of frames so that we can set visibility later
        self.suffixFrames = []
        # Keep track of boxes so we can get the text from them later
        self.suffixBoxes = []
        self.suffixBoxFrame = QtWidgets.QFrame()
        self.suffixBoxFrame.setSizePolicy(self.compactVertSizePolicy)
        self.suffixBoxLayout = QtWidgets.QGridLayout(self.suffixBoxFrame)
        self.suffixBoxLayout.setContentsMargins(0, 0, 0, 0)
        for i in range(maxTargetFiles):
            # Create suffix input boxes and store them in suffixBoxes
            suffixFrame = QtWidgets.QFrame()
            suffixLayout = QtWidgets.QHBoxLayout(suffixFrame)
            suffixLayout.setContentsMargins(0, 0, 0, 0)
            suffix = QtWidgets.QLineEdit()
            suffix.setValidator(filenameValidator)
            suffixLabel = QtWidgets.QLabel(f"File {i+1} Suffix:")
            suffixLayout.addWidget(suffixLabel)
            suffixLayout.addWidget(suffix)
            self.suffixBoxLayout.addWidget(
                suffixFrame, i // boxesPerRow, i % boxesPerRow
            )
            self.suffixFrames.append(suffixFrame)
            self.suffixBoxes.append(suffix)
        for s in self.suffixFrames[1:]:
            # Hide them all except the first one
            s.setVisible(False)
        self.settingsLayout.addWidget(self.suffixBoxFrame)

        ###############
        # TOOLBAR BUTTONS, LIST BOXES
        # left
        self.leftBox = QtWidgets.QGroupBox("Template files")
        self.leftLayout = QtWidgets.QGridLayout(self.leftBox)
        self.leftList = CustomList()
        self.leftListBtns = self.createListBtns(self.leftList)
        # right
        self.rightBox = QtWidgets.QGroupBox("Files to be renamed")
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)
        self.rightList = CustomList()
        self.rightListBtns = self.createListBtns(self.rightList)

        ###############
        # LIST LAYOUTS
        self.leftLayout.addWidget(self.leftListBtns, 1, 0)
        self.leftLayout.addWidget(self.leftList, 1, 1, 1, 2)
        self.rightLayout.addWidget(self.rightListBtns, 1, 3)
        self.rightLayout.addWidget(self.rightList, 1, 0, 1, 2)
        self.listSplitter = QtWidgets.QSplitter()
        self.listSplitter.setChildrenCollapsible(False)
        self.listSplitter.addWidget(self.leftBox)
        self.listSplitter.addWidget(self.rightBox)

        ###############
        # BOTTOM BUTTON
        self.execButton = QtWidgets.QPushButton("Preview Rename")
        self.execButton.setIcon(previewIcon)
        self.execButton.setIconSize(QtCore.QSize(25, 25))
        self.execButton.clicked.connect(self.previewRename)

        ###############
        # FINAL SETUP
        self.mainLayout.addLayout(self.settingsLayout)
        self.mainLayout.addWidget(self.listSplitter)
        self.mainLayout.addWidget(self.execButton)

    ###############
    # TOOLBAR BUTTONS
    def createListBtns(self, l):
        # Use a frame in order to control sizePolicy
        buttonFrame = QtWidgets.QFrame()
        buttonFrame.setSizePolicy(self.compactSizePolicy)
        buttonLayout = QtWidgets.QVBoxLayout(buttonFrame)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        addFilesBtn = QtWidgets.QToolButton()
        addFolderBtn = QtWidgets.QToolButton()
        upBtn = QtWidgets.QToolButton()
        sortBtn = QtWidgets.QToolButton()
        downBtn = QtWidgets.QToolButton()
        delBtn = QtWidgets.QToolButton()
        clearBtn = QtWidgets.QToolButton()
        buttons = [
            addFilesBtn,
            addFolderBtn,
            upBtn,
            downBtn,
            sortBtn,
            delBtn,
            clearBtn,
        ]
        icons = [
            "add.svg",
            "folder_open.svg",
            "keyboard_up.svg",
            "keyboard_down.svg",
            "sort.svg",
            "close.svg",
            "delete_all.svg",
        ]
        tooltips = [
            "Add file(s)",
            "Add file(s) from directory recursively",
            "Move item up",
            "Move item down",
            "Sort items",
            "Remove selected item",
            "Remove all items",
        ]
        functions = [
            l.openFileDialog,
            l.openRecursiveDirDialog,
            lambda: l.move(-1),
            lambda: l.move(1),
            l.sortItems,
            l.remove,
            l.clear,
        ]
        for btn, icn, tltip, fcn in zip(buttons, icons, tooltips, functions):
            btn.setIcon(QtGui.QIcon(f"icons/{icn}"))
            btn.setIconSize(QtCore.QSize(25, 25))
            btn.setToolTip(tltip)
            btn.clicked.connect(fcn)
            buttonLayout.addWidget(btn)
        return buttonFrame

    def updateSuffixBoxes(self, n):
        if self.spinboxPrevValue < n:
            # Spinbox increased, show next box
            self.suffixFrames[n - 1].setVisible(True)
        else:
            # Spinbox decreased, remove previous box
            self.suffixFrames[n].setVisible(False)
        self.spinboxPrevValue = n

    def previewRename(self):
        raise NotImplementedError()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    win = FileWindow()
    win.show()

    sys.exit(app.exec())
