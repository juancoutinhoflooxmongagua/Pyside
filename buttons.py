import math
from display import Display
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isEmpty, isNumOrDot, isValidNumber
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


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._equationInitialValue = "Sua conta"
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue

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

                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty("cssClass", "specialButton")

                self._configSpecialButton(button)
                self.addWidget(button, row_number, col_number)

                if isNumOrDot(button_text):
                    slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                    self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == "C":
            self._connectButtonClicked(button, self._clear)
        elif text == "◀":
            self._connectButtonClicked(button, self._backspace)
        elif text == "=":
            self._connectButtonClicked(button, self._eq)
        elif text in "+-/*^":
            self._connectButtonClicked(
                button, self._makeSlot(self._operatorClicked, button)
            )

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _insertButtonTextToDisplay(self, button):
        button_text = button.text()
        self.display.insert(button_text)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    def _backspace(self):
        self.display.backspace()

    def _operatorClicked(self, button):
        buttonText = button.text()  # +-/* (etc...)
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f"{self._left} {self._op} ??"

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None or self._op is None:
            return

        self._right = float(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            if "^" in self.equation:
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            print("Zero Division Error")
        except OverflowError:
            print("Numero muito grande")

        self.display.clear()
        self.display.insert(str(result))

        if result == "error":
            self._left = None
        else:
            self._left = result

        self._right = None
