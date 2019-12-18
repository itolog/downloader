from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
import pafy
import humanize
import sys
import os
import ffmpeg
import shutil

ui, _ = uic.loadUiType("view.ui")


class CloneThread(QThread, ui):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.video_path = os.path.join(os.getcwd(), 'a.mp4')
        self.audio_path = os.path.join(os.getcwd(), 'a.mp3')

    # run method gets called when we start the thread3
    def run(self):
        input_video = ffmpeg.input(self.video_path)
        added_audio = ffmpeg.input(self.audio_path)
        ffmp = ffmpeg.output(added_audio, input_video, 'out.mp4').run()
        # git clone done, now inform the main thread with the output
        self.signal.emit(ffmp)


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.location_path = ''
        self.audio_location_path = ''
        self.final_path = ''
        self.setupUi(self)
        self.InitUI()
        self.Handels_Buttons()
        # Thread
        self.ffmp_thread = CloneThread()
        self.ffmp_thread.signal.connect(self.finished)

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
        self.pushButton_5.clicked.connect(self.Get_Video)
        self.pushButton_4.clicked.connect(self.DownloadVideo)
        self.pushButton_3.clicked.connect(self.Save_Browse)

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

    # def Save_Browse(self):
    #     # save location in the line edit
    #     pass

    # DOWNLOAD YOUTUBE VIDEO SINGLE
    def Save_Browse(self):
        # save location in the line edit
        # enable browseing in os, pick location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".")

        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video(self):
        video_url = self.lineEdit_3.text()
        if video_url == '':
            QMessageBox.warning(self, 'Ошибка', 'Provide valid Video URL')
        else:
            try:
                video = pafy.new(video_url)
                video_stream = video.videostreams

                for streams in video_stream:
                    size = humanize.naturalsize(streams.get_filesize())
                    data = f'{streams.mediatype} {streams.extension} {streams.quality} {size}'
                    self.comboBox.addItem(data)

            except Exception:
                QMessageBox.warning(self, 'Ошибка', 'Provide valid Video URL')

    def DownloadVideo(self):
        video_url = self.lineEdit_3.text()
        self.location_path = os.path.join(os.getcwd(), 'a.mp4')
        self.audio_location_path = os.path.join(os.getcwd(), 'a.mp3')
        self.final_path = self.lineEdit_4.text() + 'final.mp4'

        if video_url == '' or self.location_path == '':
            QMessageBox.warning(self, 'Ошибка', 'Provide valid Video URL or save location path')
        else:
            try:
                video = pafy.new(video_url)
                video_stream = video.videostreams
                audio_stream = video.audiostreams
                quality = self.comboBox.currentIndex()

                download = video_stream[quality].download(filepath=self.location_path, callback=self.Video_Progress)
                download_audio = audio_stream[1].download(filepath=self.audio_location_path)

                self.ffmp_thread.start()

            except BaseException as e:
                print(e)

    def finished(self):
        final_path = os.path.normpath(self.lineEdit_4.text() + '.mp4')
        current_path = os.path.join(os.getcwd(), 'out.mp4')

        shutil.move(current_path, final_path)

        os.remove(os.path.join(os.getcwd(), 'a.mp4'))
        os.remove(os.path.join(os.getcwd(), 'a.mp3'))

        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.progressBar_2.setValue(0)
        self.comboBox.clear()
        QMessageBox.information(self, 'Загузка завершена', 'Загузка успешно завершена')

    def Video_Progress(self, total, recived, ratio, rate, time):
        read_data = recived
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(int(download_percentage))
            remaining_time = round(time / 60, 2)

            self.label_5.setText(str(f'{remaining_time} осталось минут'))

            QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
