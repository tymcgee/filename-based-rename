# Tynan McGee
# 6/5/2022
# Get filenames from the lists and rename them

import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from fileWindow import FileWindow
from previewWindow import PreviewDialog

DEBUG_MODE = False


class MainWindow(FileWindow):
    def __init__(self):
        super().__init__()

    def getLists(self):
        basenames = []
        sources = []
        suffixes = []
        # Left list contains template filenames
        for i in range(self.leftList.count()):
            item = self.leftList.item(i)
            name = item.text()
            # Remove extension
            basename = os.path.splitext(name)[0]
            basenames.append(basename)
        # Right list contains target files
        for i in range(self.rightList.count()):
            item = self.rightList.item(i)
            itemPath = item.toolTip()
            sources.append(itemPath)
        for suffixBox in self.suffixBoxes:
            if suffixBox.isVisible():
                suffixes.append(suffixBox.text())
        return basenames, sources, suffixes

    def checkInputs(self, basenames, sources, suffixes):
        if len(sources) == 0:
            # No input
            self.showError('There is nothing to rename.')
            return False
        elif len(sources) != len(basenames)*len(suffixes):
            # Bad input
            self.showError(
                'The number of files on the left must be the same as the number of files on the right times the number of files to rename per template file (specified at the top left).')
            return False
        elif not all(suffixes):
            # There is at least one empty suffix
            ret = self.showWarning(
                'At least one suffix is empty. Be careful that your files don\'t overwrite each other!')
            if ret == QtWidgets.QMessageBox.Cancel:
                return False
        elif len(suffixes) != len(set(suffixes)):
            # There are duplicate suffixes
            ret = self.showWarning(
                'At least two of the suffixes are the same. Be careful that your files don\'t overwrite each other!')
            if ret == QtWidgets.QMessageBox.Cancel:
                return False
        return True

    def getDests(self, basenames, sources, suffixes):
        dests = []
        n = len(suffixes)  # Num of renames per basename
        for base_num in range(len(basenames)):
            b = basenames[base_num]
            for i in range(n):
                suf = suffixes[i]
                src = sources[base_num*n + i]
                srcDir = os.path.dirname(src)
                ext = os.path.splitext(src)[1]
                newName = f'{b}{suf}{ext}'
                dest = os.path.join(srcDir, newName)
                dests.append(dest)
        return dests

    def previewRename(self):
        basenames, sources, suffixes = self.getLists()
        if not self.checkInputs(basenames, sources, suffixes):
            return
        dests = self.getDests(basenames, sources, suffixes)
        srcNames = [os.path.basename(s) for s in sources]
        dstNames = [os.path.basename(d) for d in dests]

        self.msgBox = PreviewDialog(srcNames, dstNames)
        self.msgBox.setWindowTitle(self.windowTitle())
        ret = self.msgBox.exec()
        if ret == QtWidgets.QDialog.Accepted:
            self.rename(sources, dests)

    def rename(self, sources, dests):
        for src, dst in zip(sources, dests):
            if DEBUG_MODE:
                print(f'{src} got moved to {dst}')
            else:
                try:
                    os.rename(src, dst)
                except FileNotFoundError:
                    self.showError(
                        'Something went wrong! One of the files you\'re trying to rename seems to not exist.')
        # Change the items in the right list to reflect the new filenames
        self.rightList.clear()
        self.rightList.addFilenames(dests)
        QtWidgets.QMessageBox.information(self, self.windowTitle(),
                                          'Files renamed!',
                                          QtWidgets.QMessageBox.Ok)

    def showError(self, text):
        QtWidgets.QMessageBox.critical(self, self.windowTitle(), text,
                                       QtWidgets.QMessageBox.Ok)

    def showWarning(self, text):
        ret = QtWidgets.QMessageBox.warning(self, self.windowTitle(), text,
                                            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                            QtWidgets.QMessageBox.Cancel)
        return ret


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
