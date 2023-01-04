import sys
from font_functions import *
from config import *
from grid_functions import *
from draw_functions import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.font_dict = font_dict()
        self.init_ui()
        self.resized.connect(self.update)
        self.top_alignment_value = self.update_top_alignment_value()
        self.bottom_alignment_value = self.update_bottom_alignment_value()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def init_ui(self):
        self.setWindowTitle(f"{APP_TITLE} | {APP_VERSION}")
        self.setGeometry(100, 100, 1000, 900)
        main_layout = QHBoxLayout()
        left_column = QVBoxLayout()
        self.center_column = QVBoxLayout()
        right_column = QVBoxLayout()
        page_config = QFormLayout()
        type_config = QFormLayout()
        grid_config = QFormLayout()
        vertical_alignment = QHBoxLayout()
        top_alignment_layout = QVBoxLayout()
        bottom_alignment_layout = QVBoxLayout()
        output_layout = QFormLayout()

        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(self.center_column, 2)
        main_layout.addLayout(right_column, 1)

        self.setLayout(main_layout)

        self.canvas_label = QLabel()
        self.center_column.addWidget(self.canvas_label, alignment=Qt.AlignTop)
        self.canvas_width = self.canvas_label.frameGeometry().width()
        self.canvas_height = self.canvas_width
        self.canvas_size = QSize(self.canvas_width, self.canvas_height)
        self.canvas = QPixmap(self.canvas_size)
        self.canvas.fill(Qt.black)
        self.canvas_label.setPixmap(self.canvas)

        page_config_group = QGroupBox("Page Configuration")
        left_column.addWidget(page_config_group)
        page_config_group.setLayout(page_config)

        self.page_width_label = QLabel("Page width:")
        self.page_width_spinbox = QDoubleSpinBox(maximum=100000, value=PAGE_WIDTH)
        self.page_width_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.page_width_label, self.page_width_spinbox)
        self.page_height_label = QLabel("Page height:")
        self.page_height_spinbox = QDoubleSpinBox(maximum=100000, value=PAGE_HEIGHT)
        self.page_height_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.page_height_label, self.page_height_spinbox)
        self.top_margin_label = QLabel("Top margin:")
        self.top_margin_spinbox = QDoubleSpinBox(maximum=100000, value=TOP_MARGIN)
        self.top_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.top_margin_label, self.top_margin_spinbox)
        self.bottom_margin_label = QLabel("Bottom margin:")
        self.bottom_margin_spinbox = QDoubleSpinBox(maximum=100000, value=BOTTOM_MARGIN)
        self.bottom_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.bottom_margin_label, self.bottom_margin_spinbox)
        self.left_margin_label = QLabel("Left margin:")
        self.left_margin_spinbox = QDoubleSpinBox(maximum=100000, value=LEFT_MARGIN)
        self.left_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.left_margin_label, self.left_margin_spinbox)
        self.right_margin_label = QLabel("Right margin:")
        self.right_margin_spinbox = QDoubleSpinBox(maximum=100000, value=RIGHT_MARGIN)
        self.right_margin_spinbox.valueChanged.connect(self.update)
        page_config.addRow(self.right_margin_label, self.right_margin_spinbox)

        type_config_group = QGroupBox("Type Configuration")
        left_column.addWidget(type_config_group)
        type_config_group.setLayout(type_config)

        self.font_label = QLabel("Font:")
        self.font_dropdown = QComboBox()
        self.font_dropdown.setMaximumWidth(200)
        self.font_dropdown.addItems(list(self.font_dict.keys()))
        self.font_dropdown.currentTextChanged.connect(self.update)
        type_config.addRow(self.font_label, self.font_dropdown)
        self.font_size_label = QLabel("Font size:")
        self.font_size_spinbox = QDoubleSpinBox(maximum=100000, value=FONT_SIZE)
        self.font_size_spinbox.valueChanged.connect(self.update)
        type_config.addRow(self.font_size_label, self.font_size_spinbox)
        self.leading_label = QLabel("Leading:")
        self.leading_spinbox = QDoubleSpinBox(maximum=100000, minimum=0.01, value=LEADING)
        self.leading_spinbox.valueChanged.connect(self.update)
        type_config.addRow(self.leading_label, self.leading_spinbox)
        self.use_custom_capheight_label = QLabel("Use custom cap-height:")
        self.use_custom_capheight_checkbox = QCheckBox()
        self.use_custom_capheight_checkbox.stateChanged.connect(self.update)
        type_config.addRow(self.use_custom_capheight_label, self.use_custom_capheight_checkbox)

        grid_config_group = QGroupBox("Grid Configuration")
        right_column.addWidget(grid_config_group, 2)
        grid_config_group.setLayout(grid_config)

        self.rows_label = QLabel("Amount of rows:")
        self.rows_spinbox = QSpinBox(maximum=100, value=ROWS)
        self.rows_spinbox.valueChanged.connect(self.update)
        grid_config.addRow(self.rows_label, self.rows_spinbox)
        self.columns_label = QLabel("Amount of columns:")
        self.columns_spinbox = QSpinBox(maximum=100, value=COLUMNS)
        self.columns_spinbox.valueChanged.connect(self.update)
        grid_config.addRow(self.columns_label, self.columns_spinbox)
        self.use_custom_gutter_label = QLabel("Use custom gutter:")
        self.use_custom_gutter_checkbox = QCheckBox()
        self.use_custom_gutter_checkbox.stateChanged.connect(self.update)
        grid_config.addRow(self.use_custom_gutter_label, self.use_custom_gutter_checkbox)
        self.custom_gutter_label = QLabel("Column gutter:")
        self.custom_gutter_spinbox = QDoubleSpinBox(maximum=100000, value=GUTTER)
        grid_config.addRow(self.custom_gutter_label, self.custom_gutter_spinbox)
        self.show_baseline_grid_label = QLabel("Show baseline-grid:")
        self.show_baseline_grid_checkbox = QCheckBox()
        self.show_baseline_grid_checkbox.stateChanged.connect(self.update)
        grid_config.addRow(self.show_baseline_grid_label, self.show_baseline_grid_checkbox)

        self.grid_start_position_label = QLabel("Grid start position:")
        self.grid_start_position_value = QLabel(str(grid_start_position(self)))
        output_layout.addRow(self.grid_start_position_label, self.grid_start_position_value)
        self.possible_lines_label = QLabel("Possible lines:")
        self.possible_lines_value = QLabel(str(possible_lines(self)))
        output_layout.addRow(self.possible_lines_label, self.possible_lines_value)
        self.gutter_label = QLabel("Row gutter:")
        self.gutter_value = QLabel(str(round(gutter(self), 3)))
        output_layout.addRow(self.gutter_label, self.gutter_value)
        self.lines_per_cell_label = QLabel("Lines per cell:")
        self.lines_per_cell_value = QLabel(str(lines_in_cell(self)))
        output_layout.addRow(self.lines_per_cell_label, self.lines_per_cell_value)
        output_layout.addRow(QLabel("Configurations:"), QLabel())
        self.corrected_bottom_margin_label = QLabel("Corrected bottom margin:")
        self.corrected_bottom_margin_value = QLabel(str(round(corrected_bottom_margin(self), 3)))
        output_layout.addRow(self.corrected_bottom_margin_label, self.corrected_bottom_margin_value)
        self.text_area_height_lable = QLabel("Height of text area:")
        self.text_area_height_value = QLabel(str(text_area_height(self)))
        output_layout.addRow(self.text_area_height_lable, self.text_area_height_value)
        self.ascender_label = QLabel("Ascender:")
        self.ascender_value = QLabel(str(ascender(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())))
        output_layout.addRow(self.ascender_label, self.ascender_value)
        self.cap_height_label = QLabel("Cap-height:")
        self.cap_height_value = QLabel(str(cap_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())))
        output_layout.addRow(self.cap_height_label, self.cap_height_value)
        self.x_height_label = QLabel("X-height:")
        self.x_height_value = QLabel(
            str(x_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())))
        output_layout.addRow(self.x_height_label, self.x_height_value)

        preview_button = QPushButton("Preview!")
        preview_button.clicked.connect(self.preview)
        output_layout.addWidget(preview_button)

        vertical_alignment_group = QGroupBox("Vertical alignment")
        right_column.addWidget(vertical_alignment_group, 1)
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
            top_alignment_value = font_functions.ascender(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())
        elif self.cap_height_radio.isChecked():
            top_alignment_value = font_functions.cap_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())
        elif self.xheight_radio.isChecked():
            top_alignment_value = font_functions.x_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value())

        return top_alignment_value

    def update_bottom_alignment_value(self):
        if self.baseline_radio.isChecked():
            bottom_alignment_value = 0
        elif self.descender_radio.isChecked():
            bottom_alignment_value = font_functions.descender(self.font_dict.get(self.font_dropdown.currentText()),
                                                            self.font_size_spinbox.value())
        else:
            bottom_alignment_value = 0

        return bottom_alignment_value

    def update(self):
        draw_page(self)
        self.top_alignment_value = self.update_top_alignment_value()
        self.bottom_alignment_value = self.update_bottom_alignment_value()
        self.text_area_height_value.setText(str(round(text_area_height(self), 3)))
        self.cap_height_value.setText(str(round(font_functions.cap_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value()), 3)))
        self.ascender_value.setText(
            str(round(ascender(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value()),
                      3)))
        self.x_height_value.setText(str(round(x_height(self.font_dict.get(self.font_dropdown.currentText()), self.font_size_spinbox.value()), 3)))
        self.grid_start_position_value.setText(str(round(grid_start_position(self), 3)))
        self.possible_lines_value.setText(str(round(possible_lines(self), 3)))
        self.corrected_bottom_margin_value.setText(str(round(corrected_bottom_margin(self), 3)))
        self.gutter_value.setText(str(round(gutter(self), 3)))
        self.lines_per_cell_value.setText(str(lines_in_cell(self)))

        if DEBUG:
            print(f"Top alignment: {self.top_alignment_value}")
            print(f"Bottom alignment: {self.bottom_alignment_value}")
            print()

        self.update_canvas_size()

    def throw_error(self, message):
        msg = QErrorMessage()
        msg.setWindowTitle("Error!")
        msg.showMessage(message)

        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())
