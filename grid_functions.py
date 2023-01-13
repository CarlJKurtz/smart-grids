import font_functions
import math


def text_area_height(window) -> float:
    text_area_height = window.page_height_spinbox.value() - window.top_margin_spinbox.value() - window.bottom_margin_spinbox.value()

    return text_area_height


def text_area_width(window) -> float:
    text_area_width = window.page_width_spinbox.value() - window.left_margin_spinbox.value() - window.right_margin_spinbox.value()

    return text_area_width


def cap_height_of_selected(window) -> float:
    cap_height = font_functions.cap_height(window.font_dict.get(window.font_dropdown.currentText()), window.font_size_spinbox.value())

    return cap_height


def grid_start_position(window) -> float:
    try:
        grid_start_position = window.top_margin_spinbox.value() - (window.leading_spinbox.value() - window.top_alignment_value) + window.bottom_alignment_value
        return grid_start_position
    except:
        grid_start_position = window.top_margin_spinbox.value() - (
                    window.leading_spinbox.value() - cap_height_of_selected(window))

        return grid_start_position


def possible_lines(window) -> float:
    try:
        possible_lines = (text_area_height(window) + (window.leading_spinbox.value() - window.top_alignment_value)) / window.leading_spinbox.value()

        return possible_lines


    except:
        possible_lines = (text_area_height(window) + (window.leading_spinbox.value() - cap_height_of_selected(window))) / window.leading_spinbox.value()

        return possible_lines


def dif_capheight_leading(window) -> float:
    try:
        dif_capheight_leading = window.leading_spinbox.value() - window.top_alignment_value

        return dif_capheight_leading
    except:
        dif_capheight_leading = window.leading_spinbox.value() - cap_height_of_selected(window)

        return dif_capheight_leading


def corrected_text_area_height(window) -> float:
    try:
        new_text_area_height = window.leading_spinbox.value() * math.floor(possible_lines(window)) - dif_capheight_leading(window) + window.bottom_alignment_value
    except:
        new_text_area_height = window.leading_spinbox.value() * math.floor(
            possible_lines(window)) - dif_capheight_leading(window)

    return new_text_area_height


def corrected_bottom_margin(window) -> float:
    new_text_area_height = corrected_text_area_height(window)
    corrected_bottom_margin = window.page_height_spinbox.value() - new_text_area_height - window.top_margin_spinbox.value()

    return corrected_bottom_margin


def gutter(window) -> float:
    try:
        gutter = window.leading_spinbox.value() * window.lines_in_gutter_spinbox.value() + dif_capheight_leading(window) - window.bottom_alignment_value
    except:
        gutter = window.leading_spinbox.value() * window.lines_in_gutter_spinbox.value() + dif_capheight_leading(
            window)

    return gutter


def is_grid_valid(window, cells) -> bool:
    if cells > 0:
        lines_per_cell = (math.floor(possible_lines(window)) - (cells - 1) * window.lines_in_gutter_spinbox.value()) / cells
        if lines_per_cell.is_integer() and lines_per_cell > 0:
            is_valid = True
        else:
            is_valid = False

        return is_valid


def lines_in_cell(window) -> int:
    if is_grid_valid(window, window.rows_spinbox.value()):
        lines_in_cell = int((possible_lines(window) - (window.rows_spinbox.value() - 1) * window.lines_in_gutter_spinbox.value()) / window.rows_spinbox.value())
        return lines_in_cell

    else:
        return 0


def possible_divisions(window) -> list:
    list_of_possible_divisions = []
    for i in range(100):
        if is_grid_valid(window, i):
            if i != 1:
                list_of_possible_divisions.append(i)

    return list_of_possible_divisions
