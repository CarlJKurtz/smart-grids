from PIL import ImageFont


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Returns the cap-height of a font
def get_cap_height(font_dict, font: str, font_size: float) -> float:
    cap_height = font_dict[font].cap_height * font_size

    return cap_height


# Returns the x-height of a font
def get_x_height(font_dict, font: str, font_size: float) -> float:
    x_height = font_dict[font].x_height * font_size

    return x_height


# Returns the ascender length of a font
def get_ascender(font_dict, font: str, font_size: float) -> float:
    ascender = font_dict[font].ascender * font_size

    return ascender


# Returns the descender length of a font
def get_descender(font_dict, font: str, font_size: float) -> float:
    descender = font_dict[font].descender * font_size

    return descender
