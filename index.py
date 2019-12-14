from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
import sys

ui, _ = uic.loadUiType("view.ui")


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handels_Buttons()

    def InitUI(self):
        # Contain all ui change
        self.statusBar().showMessage('Ready')

        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Youtube downloader')
        self.show()

    def Handels_Buttons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        # Calculate progress bar
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()

    def Download(self):
        #  downloadin any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, 'Ошибка', 'Provide valid URL or save location path')
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)
                QMessageBox.information(self, 'Загузка завершена', 'Загузка успешно завершена')
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                self.progressBar.setValue(0)

            except Exception:
                QMessageBox.warning(self, 'Ошибка загрузки', 'Provide valid URL or save location path')

    def Handle_Browse(self):
        # enable browseing in os, pick location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".")

        self.lineEdit_2.setText(str(save_location[0]))

    def Save_Browse(self):
        # save location in the line edit
        pass


def main():
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
