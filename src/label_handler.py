from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


def show_label(instance, text):
    if instance.label:
        instance.label.hide()
        instance.timer.stop()

    instance.label = QtWidgets.QLabel(text, instance)
    instance.label.move(10, instance.height() - 35)
    print(instance.width(), instance.height())
    instance.label.setStyleSheet("font: 16pt; color: red")
    instance.label.setFixedWidth(instance.width())

    instance.timer = QTimer()
    instance.timer.timeout.connect(lambda: hide_label(instance))
    instance.timer.start(3000)

    instance.label.show()


def hide_label(instance):
    instance.label.hide()
    instance.timer.stop()
