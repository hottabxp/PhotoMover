from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar
from PyQt5.QtCore import Qt


def create_toolbar(instance):
    toolbar = QToolBar(instance)
    toolbar.setAttribute(Qt.WA_TranslucentBackground, True)

    toolbar.setStyleSheet("QToolBar { background-color: rgba(255, 255, 255, 2); }")

    prew = QAction(QIcon('assets/back.png'), "", instance)
    prew.triggered.connect(instance.prew_triggered)

    exit_button = QAction(QIcon('assets/exit.png'), "", instance)

    settings_button = QAction(QIcon('assets/setting.png'), "", instance)

    nxt = QAction(QIcon('assets/next.png'), '', instance)
    nxt.triggered.connect(instance.nxt_triggered)

    set_wlp = QAction(QIcon('assets/wallpaper.png'), '', instance)
    set_wlp.triggered.connect(instance.set_wallpaper)

    toolbar.addActions((prew, nxt, set_wlp, settings_button, exit_button))

    return toolbar
