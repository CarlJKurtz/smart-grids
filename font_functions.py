import os
from fontTools import ttLib
from pathlib import Path
from PIL import ImageFont
from collections import OrderedDict


def cap_height(font_path: str, font_size: float) -> float:
    text = "E"
    relative_size = int(font_size * 100)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    cap_height = (-font.getbbox(text, anchor="ls")[1] / 100)
    return cap_height


def x_height(font_path: str, font_size: float) -> float:
    text = "x"
    relative_size = int(font_size * 100)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    x_height = (-font.getbbox(text, anchor="ls")[1] / 100)
    return x_height


def ascender(font_path: str, font_size: float) -> float:
    text = "h"
    relative_size = int(font_size * 100)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    ascender = (-font.getbbox(text, anchor="ls")[1] / 100)
    return ascender


def descender(font_path: str, font_size: float) -> float:
    text = "p"
    relative_size = int(font_size * 100)
    font = ImageFont.truetype(font_path, relative_size, encoding="utf-8")
    height_baseline_p = (-font.getbbox(text, anchor="ls")[1] / 100)
    height_p = (-font.getbbox(text, anchor="lb")[1] / 100)
    descender = height_p - height_baseline_p
    return descender


def font_dict() -> OrderedDict:
    installed_fonts = {}
    home_path = str(Path.home())
    adobe_fonts_path = os.path.join(home_path, "Library/Application Support/Adobe/CoreSync/plugins/livetype/.r")
    system_fonts_path = os.path.join(home_path, "Library/Fonts")
    adobe_test_font_path = os.path.join("/Library/Application Support/Adobe/Fonts")

    list_of_adobe_fonts = os.listdir(adobe_fonts_path)
    list_of_system_fonts = os.listdir(system_fonts_path)
    list_of_adobe_test_fonts = os.listdir(adobe_test_font_path)

    for font in list_of_system_fonts:
        try:
            installed_fonts.update(
                {short_name(os.path.join(system_fonts_path, font)): os.path.join(system_fonts_path, font)})

        except:
            pass

    for font in list_of_adobe_fonts:
        try:
            installed_fonts.update(
                {short_name(os.path.join(adobe_fonts_path, font)): os.path.join(adobe_fonts_path, font)})

        except:
            pass

    for font in list_of_adobe_test_fonts:
        try:
            installed_fonts.update(
                {short_name(os.path.join(adobe_test_font_path, font)): os.path.join(adobe_test_font_path, font)})

        except:
            pass

    installed_fonts = OrderedDict(sorted(installed_fonts.items()))

    return installed_fonts


def short_name(font):
    tt = ttLib.TTFont(font)
    name = ""
    family = ""
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
