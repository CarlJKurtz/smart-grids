from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore
from unit_conversion import convert
import re


class UnitLineEdit(QLineEdit):
    accepted_units = ['mm', 'px', 'pt', 'in', 'cm']
    unit = 'pt'
    upPressed = QtCore.pyqtSignal
    downPressed = QtCore.pyqtSignal

    def __init__(self, parent, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.stored_value = float(value)  # This will always be in pt
        self.editingFinished.connect(self.update)

        if UnitLineEdit.unit == 'pt':
            self.setText(f'{self.stored_value} pt')
        else:
            display_text = str(round(convert(self.stored_value, 'pt', UnitLineEdit.unit, self.parent.dpi), 3))
            self.setText(f'{display_text} {UnitLineEdit.unit}')

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Up:
            self.stored_value = self.stored_value + convert(1, UnitLineEdit.unit, 'pt', self.parent.dpi)
            display_value = round(convert(self.stored_value, 'pt', UnitLineEdit.unit, self.parent.dpi), 3)
            self.setText(f'{display_value} {UnitLineEdit.unit}')
            self.parent.update()

        elif event.key() == QtCore.Qt.Key_Down:
            self.stored_value = self.stored_value - convert(1, UnitLineEdit.unit, 'pt', self.parent.dpi)
            display_value = round(convert(self.stored_value, 'pt', UnitLineEdit.unit, self.parent.dpi), 3)
            self.setText(f'{display_value} {UnitLineEdit.unit}')
            self.parent.update()

    def value(self) -> float:
        return self.stored_value

    def setValue(self, value):
        self.stored_value = value
        if UnitLineEdit.unit == 'pt':
            display_value = round(value, 3)
            self.setText(f'{display_value} pt')
        else:
            display_value = round(convert(self.stored_value, 'pt', UnitLineEdit.unit, self.parent.dpi), 3)
            self.setText(f'{display_value} {UnitLineEdit.unit}')

    def update(self):
        validation = self.validate_input()
        value = validation[0]
        entered_unit = validation[1]

        if entered_unit == 'pt':
            self.stored_value = value
        else:
            self.stored_value = convert(value, entered_unit, 'pt', self.parent.dpi)

        if entered_unit == UnitLineEdit.unit:
            self.setText(f'{value} {UnitLineEdit.unit}')
        else:
            self.setText(f'{round(convert(value, entered_unit, UnitLineEdit.unit, self.parent.dpi), 3)} {UnitLineEdit.unit}')

        self.parent.update()

    def validate_input(self):
        try:
            input_text = str(self.text()).replace(",", ".")
            input_text = input_text.replace(' ', '')

            if input_text[-2:] in UnitLineEdit.accepted_units:
                unit = input_text[-2:]
            else:
                unit = UnitLineEdit.unit

            r = re.compile('[^\d\$\.]')
            value = float(r.sub('', input_text))

            return value, unit

        except ValueError:
            self.parent.throw_error('Invalid numeric value!')
            value = round(self.stored_value, 3)
            unit = 'pt'

            return value, unit
