from grid_functions import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

BLACK = QColor(0, 0, 0)
WHITE = QColor(255, 255, 255)
MAGENTA = QColor(255, 0, 255)
LIGHT_GRAY = QColor(230, 230, 230)
CYAN = QColor(0, 255, 255)

canvas_width     = 10
canvas_height    = 10
canvas_padding   = 10


class Page:
    def __init__(self, window):
        self.window = window
        self.width = window.page_width_spinbox.value()
        self.height = window.page_height_spinbox.value()
        self.scale = self.get_scale()
        self.x_pos, self.y_pos = self.get_pos()

    def get_scale(self) -> float:
        if self.width > self.height:
            page_is_wider = True
        else:
            page_is_wider = False

        if page_is_wider:
            page_width_displayed = self.window.canvas_width - canvas_padding * 2
            scale = page_width_displayed / self.width
            return scale
        else:
            page_height_displayed = self.window.canvas_height - canvas_padding * 2
            scale = page_height_displayed / self.height
            return scale

    def get_pos(self):
        if self.width > self.height:
            page_is_wider = True
        else:
            page_is_wider = False

        if page_is_wider:
            y = self.window.canvas_height / 2 - (self.height * self.scale) / 2
            x = canvas_padding
        else:
            x = self.window.canvas_width / 2 - (self.width * self.scale) / 2
            y = canvas_padding

        return x, y

    def draw(self):
        painter = QPainter(self.window.canvas)
        painter.setPen(QPen(WHITE, Qt.SolidPattern))
        painter.setBrush(QBrush(WHITE, Qt.SolidPattern))
        painter.drawRect(int(self.x_pos), int(self.y_pos), int(self.width * self.scale), int(self.height * self.scale))

    def draw_text_area(self):
        painter = QPainter(self.window.canvas)
        painter.setPen(QPen(MAGENTA, Qt.SolidPattern))
        painter.drawRect(int(self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)), int(self.y_pos + (self.window.top_margin_spinbox.value() * self.scale)), int(get_text_area_width(self.window) * self.scale), int(corrected_text_area_height(self.window) * self.scale))

    def draw_baseline_grid(self):
        if self.window.show_baseline_grid_checkbox.isChecked() and self.window.leading_spinbox.value() >= 0.1:
            painter = QPainter(self.window.canvas)
            painter.setPen(QPen(LIGHT_GRAY, Qt.SolidPattern))
            y_pos = self.y_pos + get_grid_start_position(self.window) * self.scale + self.window.leading_spinbox.value() * self.scale
            line_x = self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)
            line_x2 = line_x + (get_text_area_width(self.window) * self.scale)
            while y_pos < (get_text_area_height(self.window) * self.scale + self.y_pos + self.window.top_margin_spinbox.value() * self.scale):
                painter.drawLine(int(line_x), int(y_pos), int(line_x2), int(y_pos))
                y_pos = y_pos + (self.window.leading_spinbox.value() * self.scale)

    def draw_rows(self):
        if is_grid_valid(self.window, self.window.rows_spinbox.value()):
            painter = QPainter(self.window.canvas)
            painter.setPen(QPen(CYAN, Qt.SolidPattern))
            line_x = self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)
            line_x2 = line_x + (get_text_area_width(self.window) * self.scale)
            y = self.y_pos + (self.window.top_margin_spinbox.value() * self.scale) - (dif_capheight_leading(self.window) * self.scale)

            for i in range(self.window.rows_spinbox.value() - 1):
                y = y + self.window.leading_spinbox.value() * self.scale * lines_in_cell(self.window)
                painter.drawLine(int(line_x), int(y), int(line_x2), int(y))
                for j in range(self.window.lines_in_gutter_spinbox.value()):
                    y = y + self.window.leading_spinbox.value() * self.scale
                y = y + (dif_capheight_leading(self.window) * self.scale)
                painter.drawLine(int(line_x), int(y), int(line_x2), int(y))
                j = j+1
                y = y - (dif_capheight_leading(self.window) * self.scale)
                i = i+1

    def draw_columns(self):
        if (self.window.columns_spinbox.value() - 1) * self.window.column_gutter < get_text_area_width(self.window) and self.window.columns_spinbox.value() > 0:
            painter = QPainter(self.window.canvas)
            painter.setPen(QPen(CYAN, Qt.SolidPattern))
            x = self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)
            y1 = self.y_pos + self.window.top_margin_spinbox.value() * self.scale
            y2 = self.y_pos + (self.height - corrected_bottom_margin(self.window)) * self.scale
            column_width = (get_text_area_width(self.window) - (self.window.columns_spinbox.value() - 1) * self.window.column_gutter) / self.window.columns_spinbox.value()

            for i in range(self.window.columns_spinbox.value() - 1):
                x = x + column_width * self.scale
                painter.drawLine(int(x), int(y1), int(x), int(y2))
                x = x + self.window.column_gutter * self.scale
                painter.drawLine(int(x), int(y1), int(x), int(y2))


def refresh_canvas(window):
    window.canvas.fill(BLACK)


def draw_page(window):
    refresh_canvas(window)
    page = Page(window)
    page.draw()
    page.draw_baseline_grid()
    page.draw_rows()
    page.draw_columns()
    page.draw_text_area()
