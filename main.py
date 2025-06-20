import sys

from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Define o íconeAdd commentMore actions
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info("2.0 ^ 10.0 = 1024")
    window.addToVLayout(info)

    display = Display()
    window.addToVLayout(display)

    button = Button("Texto do botão")
    window.addToVLayout(button)

    button2 = Button("Texto do botão")
    window.addToVLayout(button2)

    window.adjustFixedSize()
    window.show()
    app.exec()
