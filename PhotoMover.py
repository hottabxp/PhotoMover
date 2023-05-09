import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, QTimer

import configparser

from src import gui, utils
from src.key_events import handle_key_event
from src.toolbar import create_toolbar


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле gui.py
        super().__init__()
        self.conf_confirm_exit = None
        self.timer = None
        self.label = None
        self.config = None
        self.conf_last_directory = None

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.statusBar().hide()

        ################################################
        self.scene = QGraphicsScene(self)
        self.load_config()

        # Вызываем функцию create_toolbar и присваиваем результат переменной self.toolbar
        self.toolbar = create_toolbar(self)

        self.addToolBar(self.toolbar)

        ################################################

        self.setFocus()
        self.graphicsView.setFocusPolicy(Qt.NoFocus)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphicsView.setGeometry(0, 0, self.width(), self.height())

        self.test = 0
        self.current_image = ''

        image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]

        self.imgs = utils.find_files(self.conf_last_directory, image_patterns)

        self.set_image(self.imgs[0])

        self.current_image = self.imgs[0]
        self.setWindowTitle(self.current_image.split('/')[-1])

    def show_label(self, text):
        if self.label:
            self.label.hide()
            self.timer.stop()

        self.label = QtWidgets.QLabel(text, self)
        self.label.move(10, self.height() - 35)
        print(self.width(), self.height())
        self.label.setStyleSheet("font: 16pt; color: red")
        self.label.setFixedWidth(self.width())

        self.timer = QTimer()
        self.timer.timeout.connect(self.hide_label)
        self.timer.start(3000)

        self.label.show()

        # width - ширина

    def hide_label(self):
        self.label.hide()
        self.timer.stop()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.conf_confirm_exit = self.config['Core']['Confirm_exit']
        self.conf_last_directory = self.config['Core']['last_directory']
        print(self.conf_confirm_exit)

    def set_wallpaper(self):

        self.show_label(self.current_image)
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graphicsView.setGeometry(0, 0, self.width(), self.height())
        self.set_image(self.imgs[self.test])
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

        print(self.test)
        self.test += 1
        if self.test == len(self.imgs):
            self.test = 0
        self.set_image(self.imgs[self.test])
        self.current_image = self.imgs[self.test]
        self.setWindowTitle(self.current_image.split('/')[-1])

    def prew_image(self):

        print(self.test)
        self.test -= 1
        if self.test == len(self.imgs):
            self.test = 0
        self.set_image(self.imgs[self.test])
        self.current_image = self.imgs[self.test]
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
