from PyQt5.QtWidgets import QLabel
from unit_conversion import convert

class UnitLabel(QLabel):
    unit = 'pt'
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

    def update(self, value):
        display_value = round(value, 3)
        if UnitLabel.unit == 'pt':
            self.setText(f'{display_value} pt')
        else:
            display_value = round(convert(value, 'pt', UnitLabel.unit, self.parent.dpi), 3)
            self.setText(f'{display_value} {UnitLabel.unit}')
