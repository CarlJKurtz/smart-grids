from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore
from unit_conversion import convert
import re


class Unit_Spinbox(QLineEdit):
    accepted_units = ['mm', 'px', 'pt']
    upPressed = QtCore.pyqtSignal
    downPressed = QtCore.pyqtSignal

    def __init__(self, parent, unit, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.stored_value = float(value)  # This will always be in pt
        self.unit = unit
        self.editingFinished.connect(self.update)

        self.setText(f'{self.stored_value} {self.unit}')

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Up:
            self.setText(self.value_to_text(self.text_to_value(self.text()) + 1))
            self.update()
        elif event.key() == QtCore.Qt.Key_Down:
            self.setText(self.value_to_text(self.text_to_value(self.text()) - 1))
            self.update()

    def value(self) -> float:
        return self.stored_value

    def update(self):
        value = self.validate_input()[0]
        entered_unit = self.validate_input()[1]

        if entered_unit == 'pt':
            self.stored_value = value
        else:
            self.stored_value = convert(value, entered_unit, 'pt')

        if entered_unit == self.unit:
            self.setText(f'{value} {self.unit}')
        else:
            self.setText(f'{round(convert(value, entered_unit, self.unit), 3)} {self.unit}')

        self.parent.update()
        # print(f'    Stored value: {self.stored_value} pt')
        # print(f'    Text:         {self.text()}')

    def validate_input(self):
        try:
            input_text = str(self.text()).replace(",", ".")
            input_text = input_text.replace(' ', '')

            if input_text[-2:] in Unit_Spinbox.accepted_units:
                unit = input_text[-2:]
            else:
                unit = self.unit

            r = re.compile('[^\d\$\.]')
            value = float(r.sub('', input_text))

            return value, unit

        except ValueError:
            print('Error while reading input!')
            value = 10
            unit = 'pt'

            return value, unit




'''

    def point(self):
        return self.stored_value

    def text_to_value(self, text):
        try:
            text = str(text).replace(",", ".")
            text = text.replace(' ', '')

            if text[-2:] in Unit_Spinbox.accepted_units and text[-2:] != self.parent.unit:
                value = self.convert_to_unit(float(text[:-2]), text[-2:], self.parent.unit)
                text = str(value)

            r = re.compile('[^\d\$\.]')
            text = r.sub('', text)
            text = str(text)

            return float(text)

        except ValueError:
            return 100

    def value_to_text(self, value):
        text = f'{round(float(value), 3)} {self.parent.unit}'
        return text

    def update_text(self):
        self.stored_value = self.convert_to_point(self.text_to_value(self.text()))
        value = self.text_to_value(self.text())
        self.setText(self.value_to_text(value))
        return

    def convert_to_unit(self, value, unit, des_unit):
        if unit == "mm" and des_unit == 'pt':
            value = value / 0.353
        elif unit == "px" and des_unit == 'pt':
            value = value
        elif unit == "pt" and des_unit == 'mm':
            value = value * 0.353
        elif unit == "px" and des_unit == 'mm':
            value = value * 25.4 / self.parent.dpi, 3
        elif unit == 'mm' and des_unit == 'px':
            value = self.parent.dpi * value / 25.4, 3
        elif unit == "pt" and des_unit == 'px':
            value = value
        elif unit == "pt" and des_unit == 'pt':
            value = value

        return value

    def convert_to_point(self, value):
        try:
            text = str(self.text()).replace(",", ".")
            text = text.replace(' ', '')

            if text[-2:] in Unit_Spinbox.accepted_units and text[-2:] != 'pt':
                value = self.convert_to_unit(value, text[-2:], 'pt')

            text = str(value)

            r = re.compile('[^\d\$\.]')
            text = r.sub('', text)
            text = str(text)

            return float(text)

        except ValueError:
            return 100
'''