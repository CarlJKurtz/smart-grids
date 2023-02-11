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
from unitlineedit import UnitLineEdit
from unitlabel import UnitLabel
from settings_window import Settings
from presets import *

# Adds title to MenuBar on OSX
try:
    if platform == 'darwin':
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        if bundle:
            info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            if info and info['CFBundleName'] == 'Python':
                info['CFBundleName'] = APP_TITLE

except ModuleNotFoundError:
    print(f'{Colors.FAIL}[!]{Colors.ENDC} Module foundation is missing. This can happen in brew environments.')

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

class Window(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dpi = 300
        self.setWindowTitle(f'{APP_TITLE} | {APP_VERSION}')
        self.setGeometry(100, 100, 1000, 400)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.splash = SplashScreen()
        self.show_splash()
        self.init_menu()
        self.font_dict = create_font_dict()
        self.preset_dict = list(PRESETS.keys())
        self.bottom_alignment_value = 0
        self.top_alignment_value = 0
        self.init_ui()
        self.resized.connect(self.update)
        self.column_gutter = self.update_column_gutter_value()
        self.window = Settings(self)
        self.change_unit(UNIT)

    def open_settings(self):
        self.window.show()

    def change_unit(self, new_unit):
        UnitLabel.unit = new_unit
        UnitLineEdit.unit = new_unit

        self.page_width_spinbox.update()
        self.page_height_spinbox.update()
        self.top_margin_spinbox.update()
        self.bottom_margin_spinbox.update()
        self.left_margin_spinbox.update()
        self.right_margin_spinbox.update()
        self.custom_gutter_spinbox.update()

    def init_menu(self):
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu(' &Edit')
        file_menu = menu_bar.addMenu(' &File')
        help_menu = menu_bar.addMenu(' &Help')

        settings_action = QAction(' Preferences', self)
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)

        reset_index_action = QAction(' Clear font index', self)
        reset_index_action.triggered.connect(self.reset_indexes)
        reset_index_action.setStatusTip('Resets the indexed fonts (Restarting the application is required)')
        edit_menu.addAction(reset_index_action)

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
        file_path = QFileDialog.getSaveFileName(self, 'Save As')
        if file_path:
            write_file(self, file_path[0])

    def file_open(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open File')
        read_file(self, file_path[0])

    @staticmethod
    def reset_indexes():
        os.remove(f'{cur_path}/pickled_fonts.pkl')
        os.remove(f'{cur_path}/pickled_paths.pkl')

    @staticmethod
    def help_action():
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

        page_config_group = QGroupBox('Page Configuration')
        left_column.addWidget(page_config_group, 2)
        page_config_group_v_layout = QVBoxLayout()
        page_config_group.setLayout(page_config_group_v_layout)
        page_config_group_v_layout.addLayout(page_config)

        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(self.preset_dict)
        self.preset_dropdown.setFixedWidth(120)
        self.preset_dropdown.currentTextChanged.connect(self.load_preset)
        page_config.addRow('Preset:', self.preset_dropdown)

        self.page_width_spinbox = UnitLineEdit(parent=self, value=PAGE_WIDTH)
        page_config.addRow('Page width:', self.page_width_spinbox)

        self.page_height_spinbox = UnitLineEdit(parent=self, value=PAGE_HEIGHT)
        page_config.addRow('Page height:', self.page_height_spinbox)

        self.top_margin_spinbox = UnitLineEdit(parent=self, value=TOP_MARGIN)
        page_config.addRow('Top margin:', self.top_margin_spinbox)


        self.bottom_margin_spinbox = UnitLineEdit(parent=self, value=BOTTOM_MARGIN)
        page_config.addRow('Bottom margin:', self.bottom_margin_spinbox)

        self.left_margin_spinbox = UnitLineEdit(parent=self, value=LEFT_MARGIN)
        page_config.addRow('Left margin:', self.left_margin_spinbox)

        self.right_margin_spinbox = UnitLineEdit(parent=self, value=RIGHT_MARGIN)
        page_config.addRow('Right margin:', self.right_margin_spinbox)

        grid = QGridLayout()
        page_config_group_v_layout.addLayout(grid)

        rotate_ccw_icon = QIcon(os.path.abspath(os.path.join(bundle_dir, 'assets/rotate_ccw.svg')))
        self.rotate_ccw_button = QPushButton(icon=rotate_ccw_icon)
        self.rotate_ccw_button.setFixedWidth(50)
        self.rotate_ccw_button.clicked.connect(self.rotate_ccw)

        rotate_cw_icon = QIcon(os.path.abspath(os.path.join(bundle_dir, 'assets/rotate_cw.svg')))
        self.rotate_cw_button = QPushButton(icon=rotate_cw_icon)
        self.rotate_cw_button.setFixedWidth(50)
        self.rotate_cw_button.clicked.connect(self.rotate_cw)

        mirror_vertical_icon = QIcon(os.path.abspath(os.path.join(bundle_dir, 'assets/mirror_vertical.svg')))
        self.mirror_vertical_button = QPushButton(icon=mirror_vertical_icon)
        self.mirror_vertical_button.setFixedWidth(50)
        self.mirror_vertical_button.clicked.connect(self.mirror_vertical)

        mirror_horizontal_icon = QIcon(os.path.abspath(os.path.join(bundle_dir, 'assets/mirror_horizontal.svg')))
        self.mirror_horizontal_button = QPushButton(icon=mirror_horizontal_icon)
        self.mirror_horizontal_button.setFixedWidth(50)
        self.mirror_horizontal_button.clicked.connect(self.mirror_horizontal)

        grid.addWidget(self.rotate_ccw_button, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.rotate_cw_button, 0, 1)
        grid.addWidget(self.mirror_vertical_button, 1, 0)
        grid.addWidget(self.mirror_horizontal_button, 1, 1)


        type_config_group = QGroupBox('Type Configuration')
        left_column.addWidget(type_config_group, 2)
        type_config_group.setLayout(type_config)

        self.font_dropdown = QComboBox()
        self.font_dropdown.setMaximumWidth(200)
        self.font_dropdown.addItems(list(self.font_dict.keys()))
        self.font_dropdown.currentTextChanged.connect(self.update)
        type_config.addRow('Font:', self.font_dropdown)

        self.font_size_spinbox = QDoubleSpinBox(suffix=' pt', maximum=100000, value=FONT_SIZE)
        self.font_size_spinbox.valueChanged.connect(self.update)
        type_config.addRow('Font size:', self.font_size_spinbox)

        self.leading_spinbox = QDoubleSpinBox(suffix=' pt', maximum=100000, minimum=0.01, value=LEADING)
        self.leading_spinbox.valueChanged.connect(self.update)
        type_config.addRow('Leading:', self.leading_spinbox)

        grid_config_group = QGroupBox('Grid Configuration')
        right_column.addWidget(grid_config_group, 2)
        grid_config_group.setLayout(grid_config)

        self.rows_spinbox = QSpinBox(minimum=1, maximum=100, value=ROWS)
        self.rows_spinbox.valueChanged.connect(self.update)
        grid_config.addRow('Amount of rows:', self.rows_spinbox)

        self.lines_in_gutter_spinbox = QSpinBox(maximum=100, minimum=1, value=LINES_IN_GUTTER)
        self.lines_in_gutter_spinbox.valueChanged.connect(self.update)
        grid_config.addRow('Lines in gutter:', self.lines_in_gutter_spinbox)

        self.columns_spinbox = QSpinBox(maximum=100, value=COLUMNS)
        self.columns_spinbox.valueChanged.connect(self.update)
        grid_config.addRow('Columns:', self.columns_spinbox)

        self.use_custom_gutter_checkbox = QCheckBox()
        self.use_custom_gutter_checkbox.stateChanged.connect(self.update)
        grid_config.addRow('Custom column gutter:', self.use_custom_gutter_checkbox)

        self.custom_gutter_spinbox = UnitLineEdit(parent=self, value=GUTTER)
        grid_config.addRow('Gutter:', self.custom_gutter_spinbox)

        self.show_baseline_grid_checkbox = QCheckBox()
        self.show_baseline_grid_checkbox.stateChanged.connect(self.update)
        grid_config.addRow('Show baseline grid:', self.show_baseline_grid_checkbox)

        self.resolution_output = QLabel(f'{self.dpi} dpi')
        output_layout.addRow('Document resolution:', self.resolution_output)

        self.grid_start_position_value = UnitLabel(parent=self, text=str(round(get_grid_start_position(self), 3)))
        output_layout.addRow('Grid start position:', self.grid_start_position_value)

        self.baseline_shift_value = QLabel(text=f'0 pt')
        output_layout.addRow('Baseline shift:', self.baseline_shift_value)

        self.possible_lines_value = QLabel(str(get_possible_lines(self)))
        output_layout.addRow('Total lines:', self.possible_lines_value)

        self.gutter_value = UnitLabel(parent=self, text=str(round(gutter(self), 3)))
        output_layout.addRow('Row gutter:', self.gutter_value)

        self.lines_per_cell_value = QLabel(str(lines_in_cell(self)))
        output_layout.addRow('Lines per cell:', self.lines_per_cell_value)

        self.possible_divisions_value = QLabel('None')
        output_layout.addRow('Possible divisions:', self.possible_divisions_value)

        self.corrected_bottom_margin_value = UnitLabel(parent=self, text=str(round(corrected_bottom_margin(self), 3)))
        output_layout.addRow('Corrected bottom margin:', self.corrected_bottom_margin_value)

        self.text_area_height_value = UnitLabel(parent=self, text=str(round(get_text_area_height(self), 3)))
        output_layout.addRow('Corrected text area height:', self.text_area_height_value)

        self.ascender_value = UnitLabel(parent=self, text=str(get_ascender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow('Ascender:', self.ascender_value)

        self.cap_height_value = UnitLabel(parent=self, text=str(get_cap_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow('Cap-height:', self.cap_height_value)

        self.x_height_value = UnitLabel(parent=self, text=str(get_x_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow('x-height:', self.x_height_value)

        self.descender_value = UnitLabel(parent=self, text=str(get_descender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value())))
        output_layout.addRow('Descender:', self.descender_value)

        vertical_alignment_group = QGroupBox('Vertical alignment')
        left_column.addWidget(vertical_alignment_group, 1)
        vertical_alignment_group.setLayout(vertical_alignment)
        self.top_alignment_group = QGroupBox('Upper alignment')
        self.top_alignment_group.setLayout(top_alignment_layout)
        self.bottom_alignment_group = QGroupBox('Bottom alignment')
        self.bottom_alignment_group.setLayout(bottom_alignment_layout)
        vertical_alignment.addWidget(self.top_alignment_group)
        vertical_alignment.addWidget(self.bottom_alignment_group)

        self.ascender_radio = QRadioButton('Ascender')
        self.ascender_radio.toggled.connect(self.update)
        self.cap_height_radio = QRadioButton('Cap-Height')
        self.cap_height_radio.toggled.connect(self.update)
        self.xheight_radio = QRadioButton('x-Height')
        self.xheight_radio.toggled.connect(self.update)

        self.baseline_radio = QRadioButton('Baseline')
        self.baseline_radio.toggled.connect(self.update)
        self.descender_radio = QRadioButton('Descender')
        self.descender_radio.toggled.connect(self.update)

        self.cap_height_radio.setChecked(True)
        self.baseline_radio.setChecked(True)

        top_alignment_layout.addWidget(self.ascender_radio)
        top_alignment_layout.addWidget(self.cap_height_radio)
        top_alignment_layout.addWidget(self.xheight_radio)
        bottom_alignment_layout.addWidget(self.baseline_radio)
        bottom_alignment_layout.addWidget(self.descender_radio)

        output_group = QGroupBox('Output')
        right_column.addWidget(output_group, 2)
        output_group.setLayout(output_layout)

        self.resized.connect(self.update)

    def rotate_cw(self):
        page_width = self.page_width_spinbox.text()
        page_height = self.page_height_spinbox.text()
        top_margin = self.top_margin_spinbox.text()
        bottom_margin = self.bottom_margin_spinbox.text()
        left_margin = self.left_margin_spinbox.text()
        right_margin = self.right_margin_spinbox.text()

        self.page_width_spinbox.setText(page_height)
        self.page_width_spinbox.update()
        self.page_height_spinbox.setText(page_width)
        self.page_height_spinbox.update()

        self.top_margin_spinbox.setText(left_margin)
        self.top_margin_spinbox.update()
        self.right_margin_spinbox.setText(top_margin)
        self.right_margin_spinbox.update()
        self.bottom_margin_spinbox.setText(right_margin)
        self.bottom_margin_spinbox.update()
        self.left_margin_spinbox.setText(bottom_margin)
        self.left_margin_spinbox.update()

    def rotate_ccw(self):
        page_width = self.page_width_spinbox.text()
        page_height = self.page_height_spinbox.text()
        top_margin = self.top_margin_spinbox.text()
        bottom_margin = self.bottom_margin_spinbox.text()
        left_margin = self.left_margin_spinbox.text()
        right_margin = self.right_margin_spinbox.text()

        self.page_width_spinbox.setText(page_height)
        self.page_width_spinbox.update()
        self.page_height_spinbox.setText(page_width)
        self.page_height_spinbox.update()

        self.top_margin_spinbox.setText(right_margin)
        self.top_margin_spinbox.update()
        self.right_margin_spinbox.setText(bottom_margin)
        self.right_margin_spinbox.update()
        self.bottom_margin_spinbox.setText(left_margin)
        self.bottom_margin_spinbox.update()
        self.left_margin_spinbox.setText(top_margin)
        self.left_margin_spinbox.update()

    def mirror_horizontal(self):
        left_margin = self.left_margin_spinbox.text()
        right_margin = self.right_margin_spinbox.text()

        self.right_margin_spinbox.setText(left_margin)
        self.right_margin_spinbox.update()
        self.left_margin_spinbox.setText(right_margin)
        self.left_margin_spinbox.update()

    def mirror_vertical(self):
        top_margin = self.top_margin_spinbox.text()
        bottom_margin = self.bottom_margin_spinbox.text()

        self.top_margin_spinbox.setText(bottom_margin)
        self.top_margin_spinbox.update()
        self.bottom_margin_spinbox.setText(top_margin)
        self.bottom_margin_spinbox.update()

    def load_preset(self):
        preset = self.preset_dropdown.currentText()
        preset_data = PRESETS[preset]

        self.change_unit(preset_data[6])  # Change unit

        self.page_width_spinbox.setText(str(preset_data[0]))
        self.page_width_spinbox.update()
        self.page_height_spinbox.setText(str(preset_data[1]))
        self.page_height_spinbox.update()
        self.top_margin_spinbox.setText(str(preset_data[2]))
        self.top_margin_spinbox.update()
        self.bottom_margin_spinbox.setText(str(preset_data[3]))
        self.bottom_margin_spinbox.update()
        self.left_margin_spinbox.setText(str(preset_data[4]))
        self.left_margin_spinbox.update()
        self.right_margin_spinbox.setText(str(preset_data[5]))
        self.right_margin_spinbox.update()

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
        divisions = divisions.replace(',', ', ')
        if len(divisions) > 0:
            self.possible_divisions_value.setText(divisions)
        
        else:
            self.possible_divisions_value.setText('None')

    def update(self):
        self.bottom_alignment_value = self.update_bottom_alignment_value()
        self.top_alignment_value = self.update_top_alignment_value()
        self.column_gutter = self.update_column_gutter_value()
        draw_page(self)
        self.display_possible_divisions()
        self.text_area_height_value.update(get_text_area_height(self))
        self.cap_height_value.update(font_functions.get_cap_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()))
        self.ascender_value.update(round(get_ascender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3))
        self.x_height_value.update(round(get_x_height(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3))
        self.grid_start_position_value.update(round(get_grid_start_position(self), 5))
        self.possible_lines_value.setText(str(round(get_possible_lines(self), 3)))
        self.corrected_bottom_margin_value.update(corrected_bottom_margin(self))
        self.gutter_value.update(round(gutter(self), 5))
        self.lines_per_cell_value.setText(str(lines_in_cell(self)))
        self.descender_value.update(round(font_functions.get_descender(self.font_dict, self.font_dropdown.currentText(), self.font_size_spinbox.value()), 3))
        baseline_shift = round(self.bottom_alignment_value, 3)
        self.baseline_shift_value.setText(f'{baseline_shift} pt')
        self.text_area_height_value.update(corrected_text_area_height(self))

        self.update_canvas_size()

    @staticmethod
    def throw_error(message, icon=QMessageBox.Warning):
        msg = QMessageBox()
        msg.setWindowTitle(APP_TITLE)
        msg.setText(message)
        msg.setIcon(icon)

        msg.exec_()

    def show_splash(self):
        self.splash.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setWindowIcon(QIcon('assets/smart_grids-icon.png'))
    window = Window()
    window.show()
    window.show_splash()

    sys.exit(app.exec_())
