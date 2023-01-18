from config import *
from fontTools import ttLib
from PIL import ImageFont
from collections import OrderedDict


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
def get_cap_height(font_path: str, font_size: float) -> float:
    text = "E"
    relative_size = int(font_size * 1000)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    cap_height = (-font.getbbox(text, anchor="ls")[1] / 1000)

    return cap_height


# Returns the x-height of a font
def get_x_height(font_path: str, font_size: float) -> float:
    text = "x"
    relative_size = int(font_size * 1000)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    x_height = (-font.getbbox(text, anchor="ls")[1] / 1000)

    return x_height


# Returns the ascender length of a font
def get_ascender(font_path: str, font_size: float) -> float:
    text = "h"
    relative_size = int(font_size * 1000)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    ascender = (-font.getbbox(text, anchor="ls")[1] / 1000)

    return ascender


# Returns the descender length of a font
def get_descender(font_path: str, font_size: float) -> float:
    text = "p"
    relative_size = int(font_size * 1000)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    height_baseline_p = (-font.getbbox(text, anchor="ls")[1] / 1000)
    height_p = (-font.getbbox(text, anchor="lb")[1] / 1000)
    descender = height_p - height_baseline_p

    return descender


# Loads all font-files in a directory into a giver dictionary
def add_fonts_to_dict(directory_path: str, font_dict: dict) -> None:
    try:
        list_of_fonts = os.listdir(directory_path)
        for font in list_of_fonts:
            try:
                font_path = os.path.join(directory_path, font)
                font_name = short_name(font_path)

                if font_name[0] == '.':
                    font_name = font_name[1:]

                font_dict.update({font_name: font_path})
                if DEBUG:
                    print(f"{Colors.OKGREEN}[!]{Colors.ENDC} Loaded {font_name}.")

            finally:
                print(f"{Colors.FAIL}[!]{Colors.ENDC} Failed to load font from {directory_path}.")

    except:
        print(f"{Colors.FAIL}[!]{Colors.ENDC} Failed to access {directory_path}. It might not exist on your system.")


# Loads all fonts into a dictionary from the directories given in config.py
def create_font_dict() -> OrderedDict:
    installed_fonts = {}

    for path in FONT_DIRECTORIES:
        add_fonts_to_dict(path, installed_fonts)

    installed_fonts = OrderedDict(sorted(installed_fonts.items()))

    return installed_fonts


# Returns the display name of the font
def short_name(font) -> str:
    tt = ttLib.TTFont(font)
    name = ''
    for record in tt['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')

        else:
            name_str = record.string.decode('latin-1')

        if record.nameID == 4 and not name:
            name = name_str

        if name:
            break

    return name
