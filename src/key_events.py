from PyQt5.QtCore import Qt



def handle_key_event(event, instance):
    key = event.key()
    print(key)

    if key == Qt.Key_Right:
        instance.next_image()
        print('Right')
    elif key == Qt.Key_Left:
        instance.prew_image()
    elif key == Qt.Key_A:
        instance.prew_image()
    elif key == Qt.Key_F11:
        if instance.isFullScreen():
            instance.showNormal()
        else:
            instance.showFullScreen()
    elif key == Qt.Key_Escape:
        if instance.conf_confirm_exit == "True":
            instance.confirm_exit()
        else:
            instance.close()
    else:
        pass
