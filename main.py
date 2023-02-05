import sys
from font_functions import *
from font_loader import *
from draw_functions import *
from grid_functions import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from splashscreen import *
import webbrowser
from file_handler import *
from sys import platform

# Adds title to MenuBar on OSX
if platform == 'darwin':
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = APP_TITLE


class Window(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE} | {APP_VERSION}")
        self.setGeometry(100, 100, 1000, 400)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.show_splash()
        self.init_menu()
        self.font_dict = create_font_dict()
        self.bottom_alignment_value = 0
        self.top_alignment_value = 0
        self.init_ui()
        self.resized.connect(self.update)
        self.column_gutter = self.update_column_gutter_value()

    def init_menu(self):
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu(' &File')
        help_menu = menuBar.addMenu(' &Help')

        reset_index_action = QAction(' Clear font index', self)
        reset_index_action.triggered.connect(self.reset_indexes)
        reset_index_action.setStatusTip('Resets the indexed fonts (Restarting the application is required)')
        help_menu.addAction(reset_index_action)

        about_action = QAction(f' About {APP_TITLE}', self)
        about_action.triggered.connect(self.show_splash)
        help_menu.addAction(about_action)

        help_action = QAction(' Visit the GitHub', self)
        help_action.triggered.connect(self.help_action)
        help_menu.addAction(help_action)

        open_file = QAction(' Open File', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open File')
        open_file.triggered.connect(self.file_open)
        file_menu.addAction(open_file)

        saveFile = QAction(' Save File', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        file_menu.addAction(saveFile)

    def file_save(self):
        file_path = QFileDialog.getSaveFileName(self, 'Save File')
        write_file(self, file_path[0])

    def file_open(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open File')
        read_file(self, file_path[0])

    def reset_indexes(self):
        os.remove('pickled_fonts.pkl')
        os.remove('pickled_paths.pkl')

    def help_action(self):
        webbrowser.open('https://github.com/CarlJKurtz/smart-grids', new=2)

    def resizeEvent(self, event):
            self.resized.emit()
            return super(Window, self).resizeEvent(event)

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.main_widget.setLayout(main_layout)
        left_column = QVBoxLayout()
        center_column = QVBoxLayout()
        right_column = QVBoxLayout()
        page_config = QFormLayout()
        type_config = QFormLayout()
        grid_config = QFormLayout()
        vertical_alignment = QHBoxLayout()
        top_alignment_layout = QVBoxLayout()
        bottom_alignment_layout = QVBoxLayout()
        output_layout = QFormLayout()

        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(center_column, 2)
        main_layout.addLayout(right_column, 1)

        self.canvas_label = QLabel()
        center_column.addWidget(self.canvas_label, alignment=Qt.AlignTop)
        self.canvas_width = self.canvas_label.frameGeometry().width()
        self.canvas_height = self.canvas_width
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)
        self.canvas = QPixmap(self.canvas_size)
        self.canvas.fill(Qt.black)
        self.canvas_label.setPixmap(self.canvas)

        page_config_group = QGroupBox("Page Configuration")
        left_column.addWidget(page_config_group, 2)
        page_config_group.setLayout(page_config)

        self.page_width_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=PAGE_WIDTH)
        self.page_width_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Page width:", self.page_width_spinbox)

        self.page_height_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=PAGE_HEIGHT)
        self.page_height_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Page height:", self.page_height_spinbox)

        self.top_margin_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=TOP_MARGIN)
        self.top_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Top margin", self.top_margin_spinbox)


        self.bottom_margin_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=BOTTOM_MARGIN)
        self.bottom_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Bottom margin:", self.bottom_margin_spinbox)

        self.left_margin_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=LEFT_MARGIN)
        self.left_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Left margin:", self.left_margin_spinbox)

        self.right_margin_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=RIGHT_MARGIN)
        self.right_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow("Right margin:", self.right_margin_spinbox)

        type_config_group = QGroupBox("Type Configuration")
        left_column.addWidget(type_config_group, 2)
        type_config_group.setLayout(type_config)

        self.font_dropdown = QComboBox()
        self.font_dropdown.setMaximumWidth(200)
        self.font_dropdown.addItems(list(self.font_dict.keys()))
        self.font_dropdown.currentTextChanged.connect(self.update)
        type_config.addRow("Font:", self.font_dropdown)

        self.font_size_spinbox = QDoubleSpinBox(suffix = " pt", maximum=100000, value=FONT_SIZE)
        self.font_size_spinbox.valueChanged.connect(self.update)
        type_config.addRow("Font size:", self.font_size_spinbox)

        self.leading_spinbox = QDoubleSpinBox(suffix = " pt", maximum=100000, minimum=0.01, value=LEADING)
        self.leading_spinbox.valueChanged.connect(self.update)
        type_config.addRow("Leading:", self.leading_spinbox)

        grid_config_group = QGroupBox("Grid Configuration")
        right_column.addWidget(grid_config_group, 2)
        grid_config_group.setLayout(grid_config)

        self.rows_spinbox = QSpinBox(minimum=1, maximum=100, value=ROWS)
        self.rows_spinbox.valueChanged.connect(self.update)
        grid_config.addRow("Amount of rows:", self.rows_spinbox)

        self.lines_in_gutter_spinbox = QSpinBox(maximum=100, minimum=1, value=LINES_IN_GUTTER)
        self.lines_in_gutter_spinbox.valueChanged.connect(self.update)
        grid_config.addRow("Lines in gutter:", self.lines_in_gutter_spinbox)

        self.columns_spinbox = QSpinBox(maximum=100, value=COLUMNS)
        self.columns_spinbox.valueChanged.connect(self.update)
        grid_config.addRow("Columns:", self.columns_spinbox)

        self.use_custom_gutter_checkbox = QCheckBox()
        self.use_custom_gutter_checkbox.stateChanged.connect(self.update)
        grid_config.addRow("Custom column gutter:", self.use_custom_gutter_checkbox)

        self.custom_gutter_spinbox = QDoubleSpinBox(suffix=" pt", maximum=100000, value=GUTTER)
        self.custom_gutter_spinbox.valueChanged.connect(self.update)
        grid_config.addRow("Gutter:", self.custom_gutter_spinbox)

        self.show_baseline_grid_checkbox = QCheckBox()
        self.show_baseline_grid_checkbox.stateChanged.connect(self.update)
        grid_config.addRow("Show baseline grid:", self.show_baseline_grid_checkbox)

        self.grid_start_position_value = QLabel(str(get_grid_start_position(self)))
        output_layout.addRow("Grid start position:", self.grid_start_position_value)

        self.baseline_shift_value = QLabel("0")
        output_layout.addRow("Baseline shift:", self.baseline_shift_value)

        self.possible_lines_value = QLabel(str(get_possible_lines(self)))
        output_layout.addRow("Total lines:", self.possible_lines_value)

        self.gutter_value = QLabel(str(round(gutter(self), 3)))
        output_layout.addRow("Row gutter:", self.gutter_value)

        self.lines_per_cell_value = QLabel(str(lines_in_cell(self)))
        output_layout.addRow("Lines per cell:", self.lines_per_cell_value)

        self.possible_divisions_value = QLabel("None")
        output_layout.addRow("Possible divisions:", self.possible_divisions_value)

        self.corrected_bottom_margin_value = QLabel(str(round(corrected_bottom_margin(self), 3)))
        output_layout.addRow("Corrected bottom margin:", self.corrected_bottom_margin_value)

        self.text_area_height_value = QLabel(str(get_text_area_height(self)))
        output_layout.addRow("Text area height:", self.text_area_height_value)

        self.ascender_value = QLabel(str(get_ascender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow("Ascender:", self.ascender_value)

        self.cap_height_value = QLabel(str(get_cap_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow("Cap-height:", self.cap_height_value)

        self.x_height_value = QLabel(
            str(get_x_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow("x-height:", self.x_height_value)
        self.descender_value = QLabel(str(round(font_functions.get_descender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3)))
        output_layout.addRow("Descender:", self.descender_value)

        vertical_alignment_group = QGroupBox("Vertical alignment")
        left_column.addWidget(vertical_alignment_group, 1)
        vertical_alignment_group.setLayout(vertical_alignment)
        self.top_alignment_group = QGroupBox("Upper alignment")
        self.top_alignment_group.setLayout(top_alignment_layout)
        self.bottom_alignment_group = QGroupBox("Bottom alignment")
        self.bottom_alignment_group.setLayout(bottom_alignment_layout)
        vertical_alignment.addWidget(self.top_alignment_group)
        vertical_alignment.addWidget(self.bottom_alignment_group)

        self.ascender_radio = QRadioButton("Ascender")
        self.ascender_radio.toggled.connect(self.update)
        self.cap_height_radio = QRadioButton("Cap-Height")
        self.cap_height_radio.toggled.connect(self.update)
        self.xheight_radio = QRadioButton("x-Height")
        self.xheight_radio.toggled.connect(self.update)

        self.baseline_radio = QRadioButton("Baseline")
        self.baseline_radio.toggled.connect(self.update)
        self.descender_radio = QRadioButton("Descender")
        self.descender_radio.toggled.connect(self.update)

        self.cap_height_radio.setChecked(True)
        self.baseline_radio.setChecked(True)

        top_alignment_layout.addWidget(self.ascender_radio)
        top_alignment_layout.addWidget(self.cap_height_radio)
        top_alignment_layout.addWidget(self.xheight_radio)
        bottom_alignment_layout.addWidget(self.baseline_radio)
        bottom_alignment_layout.addWidget(self.descender_radio)

        output_group = QGroupBox("Output")
        right_column.addWidget(output_group, 2)
        output_group.setLayout(output_layout)

        self.resized.connect(self.update)

    def preview(self):
        self.update()

    def update_canvas_size(self):
        self.canvas_width = self.canvas_label.frameGeometry().width()
        self.canvas_height = self.canvas_width
        self.canvas = self.canvas.scaled(self.canvas_width, self.canvas_height)
        self.canvas_label.setPixmap(self.canvas)

    def update_top_alignment_value(self):
        if self.ascender_radio.isChecked():
            top_alignment_value = font_functions.get_ascender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())
        elif self.cap_height_radio.isChecked():
            top_alignment_value = font_functions.get_cap_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())
        elif self.xheight_radio.isChecked():
            top_alignment_value = font_functions.get_x_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())

        return top_alignment_value

    def update_bottom_alignment_value(self):
        if self.baseline_radio.isChecked():
            bottom_alignment_value = 0
        elif self.descender_radio.isChecked():
            bottom_alignment_value = font_functions.get_descender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())
        else:
            bottom_alignment_value = 0

        return bottom_alignment_value

    def update_column_gutter_value(self):
        if self.use_custom_gutter_checkbox.isChecked():
            column_gutter = self.custom_gutter_spinbox.value()

        else:
            column_gutter = gutter(self)

        return column_gutter

    def display_possible_divisions(self):
        divisions = str(possible_divisions(self))[1:-1]
        divisions = divisions.replace(",", ", ")
        if len(divisions) > 0:
            self.possible_divisions_value.setText(divisions)
        
        else:
            self.possible_divisions_value.setText("None")

    def update(self):
        self.bottom_alignment_value = self.update_bottom_alignment_value()
        self.top_alignment_value = self.update_top_alignment_value()
        self.column_gutter = self.update_column_gutter_value()
        draw_page(self)
        self.display_possible_divisions()
        self.text_area_height_value.setText(str(round(get_text_area_height(self), 3)))
        self.cap_height_value.setText(str(round(font_functions.get_cap_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3)))
        self.ascender_value.setText(
            str(round(get_ascender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()),
                      3)))
        self.x_height_value.setText(str(round(get_x_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3)))
        self.grid_start_position_value.setText(str(round(get_grid_start_position(self), 3)))
        self.possible_lines_value.setText(str(round(get_possible_lines(self), 3)))
        self.corrected_bottom_margin_value.setText(str(round(corrected_bottom_margin(self), 3)))
        self.gutter_value.setText(str(round(gutter(self), 3)))
        self.lines_per_cell_value.setText(str(lines_in_cell(self)))
        self.descender_value.setText(str(round(font_functions.get_descender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3)))
        self.baseline_shift_value.setText(str(round(self.bottom_alignment_value, 3)))

        self.update_canvas_size()

    def throw_error(self, message):
        msg = QErrorMessage()
        msg.setWindowTitle("Error!")
        msg.showMessage(message)

        msg.exec_()

    def show_splash(self):
        self.splash = SplashScreen()
        self.splash.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/smart_grids-icon.png'))
    window = Window()
    window.show()
    window.show_splash()

    sys.exit(app.exec_())
