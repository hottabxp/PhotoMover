import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QGraphicsScene, QToolBar, QAction
from PyQt5.QtCore import Qt

import utils

import gui  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self, ccc):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле gui.py
        super().__init__()
        self.ccc = ccc
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        print(self.ccc)
        self.statusBar().hide()

        self.setFocus()
        self.graphicsView.setFocusPolicy(Qt.NoFocus)

        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphicsView.setGeometry(0, 0, self.width(), self.height())

        self.test = 0
        self.current_image = ''

        self.toolbar = QToolBar(self)
        self.toolbar.setAttribute(Qt.WA_TranslucentBackground, True)

        self.x = QAction('Hello', self)


        self.left_toolbar = QToolBar(self)
        self.left_toolbar.setFixedWidth(100)
        self.left_toolbar.addAction(self.x)
        self.addToolBar(Qt.LeftToolBarArea, self.left_toolbar)

        self.toolbar.setStyleSheet("QToolBar { background-color: rgba(255, 255, 255, 2); }")

        self.addToolBar(self.toolbar)

        self.scene = QGraphicsScene(self)

        # Создаем действия для панели инструментов
        prew = QAction(QIcon('assets/back.png'), "", self)
        prew.triggered.connect(self.prew_triggered)

        nxt = QAction(QIcon('assets/next.png'), '', self)
        nxt.triggered.connect(self.nxt_triggered)

        set_wlp = QAction(QIcon('assets/wallpaper.png'), '', self)
        set_wlp.triggered.connect(self.set_wallpaper)

        self.toolbar.addActions((prew, nxt, set_wlp))

        directory = "/home/sergey/Рабочий стол/images/"
        image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]

        self.imgs = utils.find_files(directory, image_patterns)

        self.set_image(self.imgs[0])

        self.current_image = self.imgs[0]
        self.setWindowTitle(self.current_image.split('/')[-1])

    def set_wallpaper(self):
        print(self.current_image)
        # utils.set_walpaper(self.current_image)
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

    def keyPressEvent(self, event):
        key = event.key()
        print(key)

        if key == Qt.Key_Right:
            self.next_image()
            print('Right')
        elif key == Qt.Key_Left:
            self.prew_image()
        elif key == Qt.Key_A:
            self.prew_image()
        elif key == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            # В противном случае разворачиваем окно на полный экран
            else:
                self.showFullScreen()
        elif key == Qt.Key_Escape:
            self.close()
        else:
            pass

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
    window = ExampleApp('www')  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    # window.showFullScreen()
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
