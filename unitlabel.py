from PyQt5.QtWidgets import QLabel
from unit_conversion import convert

class UnitLabel(QLabel):
    def __init__(self, unit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit

    def update(self, value):
        display_value = round(value, 3)
        if self.unit == 'pt':
            self.setText(f'{display_value} pt')
        else:
            display_value = round(convert(value, 'pt', self.unit), 3)
            self.setText(f'{display_value} {self.unit}')
