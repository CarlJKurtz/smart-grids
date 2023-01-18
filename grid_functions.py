import font_functions
import math


# Return the height of the textarea
def get_text_area_height(window: object) -> float:
    page_height = window.page_height_spinbox.value()
    top_margin = window.top_margin_spinbox.value()
    bottom_margin = window.bottom_margin_spinbox.value()

    text_area_height = page_height - top_margin - bottom_margin

    return text_area_height


# Returns the width of the textarea
def get_text_area_width(window) -> float:
    page_width = window.page_width_spinbox.value()
    left_margin = window.left_margin_spinbox.value()
    right_margin = window.right_margin_spinbox.value()

    text_area_width = page_width - left_margin - right_margin

    return text_area_width


# Returns cap-height of currently selected font
def cap_height_of_selected(window) -> float:
    font_path = window.font_dict.get(window.font_dropdown.currentText())
    font_size = window.font_size_spinbox.value()

    cap_height = font_functions.get_cap_height(font_path, font_size)

    return cap_height


# Returns the distance from top-of-page to the top of the first line of text
def get_grid_start_position(window) -> float:
    top_margin = window.top_margin_spinbox.value()
    leading = window.leading_spinbox.value()
    top_alignemnt = window.top_alignment_value
    bottom_alignment = window.bottom_alignment_value

    grid_start_position = top_margin - leading - top_alignemnt + bottom_alignment

    return grid_start_position


# Returns the amount of lines that can fit into the text-area
def get_possible_lines(window) -> float:
    text_area_height = get_text_area_height(window)
    leading = window.leading_spinbox.value()
    difference_leading_top_alignment = dif_capheight_leading(window)

    possible_lines = (text_area_height + difference_leading_top_alignment) / leading

    return possible_lines


# Returns the difference between leading and the selected height (Cap-height, x-height etc.)
def dif_capheight_leading(window) -> float:
    leading = window.leading_spinbox.value()
    top_alignment = window.top_alignment_value

    difference_leading_top_alignment = leading - top_alignment

    return difference_leading_top_alignment



def corrected_text_area_height(window) -> float:
    try:
        new_text_area_height = window.leading_spinbox.value() * math.floor(get_possible_lines(window)) - dif_capheight_leading(window) + window.bottom_alignment_value
    except:
        new_text_area_height = window.leading_spinbox.value() * math.floor(
            get_possible_lines(window)) - dif_capheight_leading(window)

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
        lines_per_cell = (math.floor(get_possible_lines(window)) - (cells - 1) * window.lines_in_gutter_spinbox.value()) / cells
        if lines_per_cell.is_integer() and lines_per_cell > 0:
            is_valid = True
        else:
            is_valid = False

        return is_valid


def lines_in_cell(window) -> int:
    if is_grid_valid(window, window.rows_spinbox.value()):
        lines_in_cell = int((get_possible_lines(window) - (window.rows_spinbox.value() - 1) * window.lines_in_gutter_spinbox.value()) / window.rows_spinbox.value())
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
