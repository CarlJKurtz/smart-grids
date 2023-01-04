from config import *
from grid_functions import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

BLACK = QColor(0, 0, 0)
WHITE = QColor(255, 255, 255)
MAGENTA = QColor(255, 0, 255)
LIGHT_GRAY = QColor(230, 230, 230)
CYAN = QColor(0, 255, 255)


class Page():
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
            page_width_displayed = self.window.canvas_width - CANVAS_PADDING * 2
            scale = page_width_displayed / self.width
            return scale
        else:
            page_height_displayed = self.window.canvas_height - CANVAS_PADDING * 2
            scale = page_height_displayed / self.height
            return scale

    def get_pos(self):
        if self.width > self.height:
            page_is_wider = True
        else:
            page_is_wider = False

        if page_is_wider:
            y = self.window.canvas_height / 2 - (self.height * self.scale) / 2
            x = CANVAS_PADDING
        else:
            x = self.window.canvas_width / 2 - (self.width * self.scale) / 2
            y = CANVAS_PADDING

        return x, y

    def draw(self):
        painter = QPainter(self.window.canvas)
        painter.setPen(QPen(WHITE, Qt.SolidPattern))
        painter.setBrush(QBrush(WHITE, Qt.SolidPattern))
        painter.drawRect(self.x_pos, self.y_pos, self.width * self.scale, self.height * self.scale)

    def draw_text_area(self):
        painter = QPainter(self.window.canvas)
        painter.setPen(QPen(MAGENTA, Qt.SolidPattern))
        painter.drawRect(self.x_pos + (self.window.left_margin_spinbox.value() * self.scale), self.y_pos + (self.window.top_margin_spinbox.value() * self.scale),  text_area_width(self.window) * self.scale, corrected_text_area_height(self.window) * self.scale)

    def draw_baseline_grid(self):
        if self.window.show_baseline_grid_checkbox.isChecked() and self.window.leading_spinbox.value() >= 0.1:
            painter = QPainter(self.window.canvas)
            painter.setPen(QPen(LIGHT_GRAY, Qt.SolidPattern))
            y_pos = self.y_pos + grid_start_position(self.window) * self.scale + self.window.leading_spinbox.value() * self.scale
            line_x = self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)
            line_x2 = line_x + (text_area_width(self.window) * self.scale)
            while y_pos < (text_area_height(self.window) * self.scale + self.y_pos + self.window.top_margin_spinbox.value() * self.scale):
                painter.drawLine(line_x, y_pos, line_x2, y_pos)
                y_pos = y_pos + (self.window.leading_spinbox.value() * self.scale)

    def draw_grid(self):
        if is_grid_valid(self.window, self.window.rows_spinbox.value()):
            painter = QPainter(self.window.canvas)
            painter.setPen(QPen(CYAN, Qt.SolidPattern))
            line_x = self.x_pos + (self.window.left_margin_spinbox.value() * self.scale)
            line_x2 = line_x + (text_area_width(self.window) * self.scale)
            y_start = self.y_pos + (self.window.top_margin_spinbox.value() * self.scale) - (dif_capheight_leading(self.window) * self.scale)
            y = y_start

            for i in range(self.window.rows_spinbox.value() - 1):
                y = y + self.window.leading_spinbox.value() * self.scale * lines_in_cell(self.window)
                painter.drawLine(line_x, y, line_x2, y)
                for j in range(self.window.lines_in_gutter_spinbox.value()):
                    y = y + self.window.leading_spinbox.value() * self.scale
                y = y + (dif_capheight_leading(self.window) * self.scale)
                painter.drawLine(line_x, y, line_x2, y)
                j = j+1
                y = y - (dif_capheight_leading(self.window) * self.scale)
                i = i+1
                pass



def refresh_canvas(window):
    window.canvas.fill(BLACK)


def draw_page(window):
    refresh_canvas(window)
    page = Page(window)
    page.draw()
    page.draw_baseline_grid()
    page.draw_grid()
    page.draw_text_area()
