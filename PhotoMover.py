import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, QTimer

import configparser

from src import main_ui, utils
from src.key_events import handle_key_event
from src.toolbar import create_toolbar
from src.label_handler import show_label
# from src.ui_utils import confirm_exit


class ExampleApp(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()
        self.conf_confirm_exit = None
        self.timer = None
        self.label = None
        self.config = None
        self.conf_last_directory = None
        self.curren_image_index = 0
        self.current_image = ''
        image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]

        self.setupUi(self)
        self.statusBar().hide()

        ################################################
        self.scene = QGraphicsScene(self)
        self.load_config()
        self.toolbar = create_toolbar(self)
        self.addToolBar(self.toolbar)

        ################################################

        self.setFocus()
        self.graphicsView.setFocusPolicy(Qt.NoFocus)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setGeometry(0, 0, self.width(), self.height())

        self.imgs = utils.find_files(self.conf_last_directory, image_patterns)
        self.set_image(self.imgs[0])
        self.current_image = self.imgs[0]
        self.setWindowTitle(self.current_image.split('/')[-1])


    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.conf_confirm_exit = self.config['Core']['Confirm_exit']
        self.conf_last_directory = self.config['Core']['last_directory']
        print(self.conf_confirm_exit)

    def set_wallpaper(self):
        show_label(self, self.current_image)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graphicsView.setGeometry(0, 0, self.width(), self.height())
        self.set_image(self.imgs[self.curren_image_index])
        self.setFocus()

    def prew_triggered(self):
        self.prew_image()
        pass

    def nxt_triggered(self):
        self.next_image()

    def confirm_exit(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Exit",
            "Закрыть приложение?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.close()

    def keyPressEvent(self, event):
        handle_key_event(event, self)

    def next_image(self):

        print(self.curren_image_index)
        self.curren_image_index += 1
        if self.curren_image_index == len(self.imgs):
            self.curren_image_index = 0
        self.set_image(self.imgs[self.curren_image_index])
        self.current_image = self.imgs[self.curren_image_index]
        self.setWindowTitle(self.current_image.split('/')[-1])

    def prew_image(self):
        self.curren_image_index -= 1
        if self.curren_image_index == -1:
            self.curren_image_index = len(self.imgs) - 1
        self.set_image(self.imgs[self.curren_image_index])
        self.current_image = self.imgs[self.curren_image_index]
        self.setWindowTitle(self.current_image.split('/')[-1])

    def click_prew(self):
        self.prew_image()

    def click_next(self):
        self.next_image()

    def set_image(self, image_path):
        pixmap = QPixmap(image_path).scaled(self.graphicsView.size())
        self.scene.addPixmap(pixmap)
        self.graphicsView.setScene(self.scene)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    # window.showFullScreen()
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
