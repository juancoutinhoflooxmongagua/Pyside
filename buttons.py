import math
from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import converToNumber, isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        # Corrected typo: MEDIUM_FONT_FONT_SIZE -> MEDIUM_FONT_SIZE
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
        self, display: Display, info: Info, window: MainWindow, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self._equationInitialValue = "Sua conta"
        self.equation = self._equationInitialValue
        self._left = None
        self._right = None
        self._op = None

        self.display = display
        self.info = info
        self.window = window

        self._gridMask = [
            ["C", "D", " ", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["", "0", ".", "="],
            ["N", "0", ".", "="],
        ]
        self._makeGrid()

        self.display.eqRequested.connect(
            self.vouApagarVocê
        )  # Changed from eqPressed to eqRequested
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self.vouApagarVocê)

    def _makeGrid(self):
        for row_number, row_data in enumerate(self._gridMask):
            for col_number, button_text in enumerate(row_data):
                if isEmpty(button_text) or button_text == " ":
                    placeholder = QPushButton("")
                    placeholder.setDisabled(True)
                    self.addWidget(placeholder, row_number, col_number)
                    continue

                button = Button(button_text)

                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty("cssClass", "specialButton")
                    if button_text == "N":
                        self._connectButtonClicked(button, self._invertNumber)

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
        elif text == "D":
            self._connectButtonClicked(button, self.display.backspace)
        elif text == "=":
            self._connectButtonClicked(button, self._eq)
        elif text in "+-/*":
            self._connectButtonClicked(
                button, self._makeSlot(self._operatorClicked, button)
            )

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = converToNumber(displayText) * -1
        self.display.setText(str(number))

    def vouApagarVocê(self):
        print('Signal recebido por "vouApagarVocê" em', type(self).__name__)
        # Clear everything when C or Esc is pressed
        self._clear()

    def _insertButtonTextToDisplay(self, button):
        button_text = button.text()
        self.display.insert(button_text)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.info.setText(self.equation)
        self.display.clear()

    def _backspace(self):
        self.display.backspace()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("Você não digitou nada.")
            return

        if self._left is None:
            try:
                self._left = float(displayText)
            except ValueError:
                self._clear()
                return

        self._op = buttonText
        self.equation = f"{self._left} {self._op} ??"
        self.info.setText(self.equation)

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError("Conta incompleta.")
            return

        if self._left is None or self._op is None:
            return

        try:
            self._right = float(displayText)
        except ValueError:
            self._clear()
            return

        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            # Using math.isclose for float comparison to avoid precision issues
            if self._op == "/" and self._right == 0:
                raise ZeroDivisionError

            result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("Divisão por zero.")
        except OverflowError:
            self._showError("Essa conta não pode ser realizada.")
        except Exception as e:
            self._showError(f"Erro inesperado: {e}")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self.display.insert(str(result))

        if result == "error":
            self._left = None
        else:
            self._left = result

        self._right = None

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
