from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variables import BIG_FONT_SIZE, MINIMUM_WIDTH, TEXT_MARGIN


def isEmpty(text: str) -> bool:
    return not bool(text)


class Display(QLineEdit):
    eqRequested = Signal()
    delPressed = Signal()
    clearPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px;")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        text = self.text()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Delete, KEYS.Key_Backspace]
        isEsc = key == KEYS.Key_Escape

        if isEnter:
            print("Enter pressionado, sinal emitido", type(self).__name__)
            self.eqRequested.emit()
            return event.ignore()

        if isDelete:
            print("isDelete pressionado, sinal emitido", type(self).__name__)
            self.delPressed.emit()
            return event.ignore()

        if isEsc:
            print("isEsc pressionado, sinal emitido", type(self).__name__)
            self.clearPressed.emit()
            return event.ignore()

        if isEmpty(text) and not (isEnter or isDelete or isEsc):
            return event.ignore()

        super().keyPressEvent(event)

        print("Texto", text)
