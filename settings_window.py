from config import *
from PyQt5.QtWidgets import *
class Settings(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle(f"Preferences")
        self.init_ui()
        self.parent = parent
        self.change_unit()

    def init_ui(self):
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create a tab widget
        tab = QTabWidget(self)

        unit_list = ['pt', 'mm', 'in', 'px']

        # personal page
        unit_tab = QWidget(self)
        layout = QFormLayout()
        unit_tab.setLayout(layout)

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItems(unit_list)
        self.unit_dropdown.currentTextChanged.connect(self.change_unit)
        layout.addRow('Units:', self.unit_dropdown)


        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setRange(0, 1000)
        self.dpi_spinbox.setValue(300)
        self.dpi_spinbox.valueChanged.connect(self.change_dpi)
        layout.addRow('Resolution:', self.dpi_spinbox)


        font_tab = QWidget(self)
        layout = QVBoxLayout()
        font_tab.setLayout(layout)
        label = QLabel('Resetting the font index will remove all the font information that SmartGrids has collected.\n'
                       'This will not remove any font files from your system. This can fix errors after fonts were '
                       'uninstalled and reinstalled on the system.')
        label.setWordWrap(True)
        layout.addWidget(label)

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.reset_indexes)
        layout.addWidget(reset_button)

        tab.addTab(unit_tab, 'Units')
        tab.addTab(font_tab, 'Font-loading')

        main_layout.addWidget(tab, 0, 0, 2, 1)

    def reset_indexes(self):
        os.remove(f'{cur_path}/pickled_fonts.pkl')
        os.remove(f'{cur_path}/pickled_paths.pkl')

    def change_unit(self):
        self.parent.change_unit(self.unit_dropdown.currentText())

    def change_dpi(self):
        self.parent.dpi = self.dpi_spinbox.value()
