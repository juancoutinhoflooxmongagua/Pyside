from display import Display
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isEmpty, isNumOrDot
from variables import MEDIUM_FONT_SIZE


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        self.setCheckable(True)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["", "0", ".", "="],
        ]
        self.display = display
        self._makeGrid()

    def _makeGrid(self):

        for row_number, row_data in enumerate(self._gridMask):
            for col_number, button_text in enumerate(row_data):
                if isEmpty(button_text):
                    placeholder = QPushButton("")
                    placeholder.setDisabled(True)
                    self.addWidget(placeholder, row_number, col_number)
                    continue

                button = Button(button_text)

                if not isNumOrDot(button_text):
                    button.setProperty("cssClass", "specialButton")

                self.addWidget(button, row_number, col_number)

                if button_text == "C":
                    slot = self._makeSlot(self._clearDisplay)
                elif button_text == "◀":
                    slot = self._makeSlot(self._backspace)
                elif button_text == "=":
                    slot = self._makeSlot(self._calculate)
                else:
                    slot = self._makeSlot(self._insertButtonTextToDisplay, button)

                button.clicked.connect(slot)

    def _makeSlot(self, func, *args, **kwargs):

        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _insertButtonTextToDisplay(self, button: Button):
        """Insere o texto do botão no display."""
        button_text = button.text()
        self.display.insert(button_text)

    def _clearDisplay(self):
        """Limpa o display."""
        self.display.clear()

    def _backspace(self):
        self.display.backspace()

    def _calculate(self):

        expression = self.display.text()
        if not expression:
            return

        expression = expression.replace("^", "**")

        try:
            result = str(eval(expression))
            self.display.setText(result)
        except Exception:
            self.display.setText("Error")
