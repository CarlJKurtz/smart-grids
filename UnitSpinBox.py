from PyQt5.QtWidgets import QDoubleSpinBox


class UnitSpinBox(QDoubleSpinBox):
    def __init__(self, unit, *args, **kwargs):
        self.unit = unit
        super().__init__(*args, **kwargs)
        self.setSuffix(f" {unit}")

    def textFromValue(self, value):
        return str(value)

    def valueFromText(self, text):
        text = self.cleanText().replace(",", ".")
        print(text)
        try:
            value, unit = text.split()

        except:
            value = text
            unit = self.unit

        if unit != self.unit:
            value = self.convert_to_default_unit(value, unit)
        return float(value)

    def convert_to_default_unit(self, value, unit):
        if unit == "m":
            value = value * 1000

        return value
