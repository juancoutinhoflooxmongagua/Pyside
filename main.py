import sys
from pathlib import Path

FILE_DIR = Path(__file__).parent
sys.path.append(str(FILE_DIR))

from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH

from display import Display
from info import Info
from buttons import ButtonsGrid

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info("Sua conta")
    window.addWidgetToVLayout(info)

    display = Display()
    window.addWidgetToVLayout(display)

    buttonsGrid = ButtonsGrid(display, info, window)
    window.v_layout.addLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()
