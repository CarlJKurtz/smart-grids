from collections import OrderedDict
from config import *
from fontTools import ttLib
from PIL import ImageFont
from ttc_conversion import *
import pickle
import time


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


class Font:
    def __init__(self, path):
        self.path = path
        if self.path[len(self.path) - 4:] == '.otc' or self.path[len(self.path) - 4:] == '.ttc':
            self.cap_height = None
            self.x_height = None
            self.ascender = None
            self.descender = None
            self.name = short_name(self.path)
            self.status = self.status()
            if DEBUG:
                self.print_info()

        else:
            self.cap_height = self.cap_height()
            self.x_height = self.x_height()
            self.ascender = self.ascender()
            self.descender = self.descender()
            self.name = short_name(self.path)
            self.status = self.status()
            if DEBUG:
                self.print_info()

        # returns cap_height at 1pt
    def cap_height(self):
        try:
            font = ImageFont.truetype(self.path, 1000, encoding="utf-8")
            cap_height = (-font.getbbox('E', anchor="ls")[1] / 1000)

            return cap_height
        except:
            return None

    def x_height(self) -> float:
        try:
            font = ImageFont.truetype(self.path, 1000, encoding="utf-8")
            x_height = (-font.getbbox('x', anchor="ls")[1] / 1000)

            return x_height
        except:
            return None

    def ascender(self) -> float:
        try:
            font = ImageFont.truetype(self.path, 1000, encoding="utf-8")
            ascender = (-font.getbbox('h', anchor="ls")[1] / 1000)

            return ascender
        except:
            return None

    def descender(self) -> float:
        try:
            font = ImageFont.truetype(self.path, 1000, encoding="utf-8")
            height_baseline_p = (-font.getbbox('p', anchor="ls")[1] / 1000)
            height_p = (-font.getbbox('p', anchor="lb")[1] / 1000)
            descender = height_p - height_baseline_p

            return descender
        except:
            return None

    def print_info(self):
        if type(self.x_height) == float and type(self.cap_height) == float and type(self.ascender) == float and type(self.descender) == float:
            status_color = Colors.OKGREEN
            status = 'Success'
        else:
            status_color = Colors.FAIL
            status = 'Failed'

        print(f'{status_color}[!]{Colors.ENDC} {self.name}')
        print(f'    x-height:    {self.x_height}')
        print(f'    cap-height:  {self.cap_height}')
        print(f'    ascender:    {self.ascender}')
        print(f'    descender:   {self.descender}')
        print(f'    path:        {self.path}')
        print()
        print(f'    load-status: {status_color}{status}{Colors.ENDC}')
        print()

    def status(self):
        if type(self.x_height) == float and type(self.cap_height) == float and type(self.ascender) == float and type(self.descender) == float and type(self.name) == str:
            return 'Success'
        else:
            return 'Failed'


# Loads all font-files in a directory into a giver dictionary
def add_fonts_to_dict(directory_path: str, font_dict: dict, indexed_fonts: dict) -> None:
    try:
        list_of_fonts = os.listdir(directory_path)
    except:
        list_of_fonts = {}
        print(f"{Colors.FAIL}[!]{Colors.ENDC} Failed to access {directory_path}. It might not exist on your system.")

    if len(list_of_fonts) != 0:
        for font in list_of_fonts:
            font_path = os.path.join(directory_path, font)
            if font_path not in indexed_fonts:
                if os.path.isdir(font_path):
                    add_fonts_to_dict(font_path, font_dict, indexed_fonts)
                indexed_fonts.append(font_path)
                if font[len(font) - 4:] == '.otc' or font[len(font) - 4:] == '.ttc':
                    ttc_to_ttf(font_path)
                    list_of_fonts = os.listdir('converted_fonts')
                    for font in list_of_fonts:
                        font_obj = Font('converted_fonts/'+font)
                        os.remove('converted_fonts/'+font)
                        if font_obj.status == 'Success':
                            font_dict.update({font_obj.name: font_obj})

                else:
                        font_obj = Font(font_path)
                        if font_obj.status == 'Success':
                                font_dict.update({font_obj.name: font_obj})
            else:
                if DEBUG:
                    print(f'{Colors.OKCYAN}[!]{Colors.ENDC} {font_path} was already indexed.')


# Loads all fonts into a dictionary from the directories given in config.py
def create_font_dict() -> OrderedDict:
    start_time = time.time()
    print(f'{Colors.OKCYAN}[!]{Colors.ENDC} Populating font dictionary. This may take a minute …')
    if not os.path.isfile('pickled_paths.pkl'):
        indexed_fonts = []
        pickle.dump(indexed_fonts, open('pickled_paths.pkl', 'wb'))
        installed_fonts = {}
        pickle.dump(installed_fonts, open('pickled_fonts.pkl', 'wb'))
    else:
        indexed_fonts = pickle.load(open('pickled_paths.pkl', 'rb'))

    if not os.path.isfile('pickled_fonts.pkl'):
        installed_fonts = {}
        pickle.dump(installed_fonts, open('pickled_fonts.pkl', 'wb'))
        indexed_fonts = []
        pickle.dump(indexed_fonts, open('pickled_paths.pkl', 'wb'))
        installed_fonts = {}
    else:
        installed_fonts = pickle.load(open('pickled_fonts.pkl', 'rb'))

    for path in FONT_DIRECTORIES:
        add_fonts_to_dict(path, installed_fonts, indexed_fonts)

    installed_fonts = OrderedDict(sorted(installed_fonts.items()))
    pickle.dump(indexed_fonts, open('pickled_paths.pkl', 'wb'))
    pickle.dump(installed_fonts, open('pickled_fonts.pkl', 'wb'))
    print()
    print(f'{Colors.OKGREEN}[!]{Colors.ENDC} Finished in {Colors.BOLD}{round(time.time() - start_time, 3)}{Colors.ENDC} seconds!')
    print()

    return installed_fonts


# Returns the display name of the font
def short_name(font) -> str:
    try:
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

        if name[0] == '.':
            name = name[1:]

        return name
    except:
        return None
