from fontTools.ttLib import sfnt, TTFont
import os
import pathlib
from font_functions import *


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

# this code is based on afdkos otc2otf


def get_psname(font):
    if 'name' in font:
        psname = font['name'].getDebugName(6)
        if psname:
            return psname


def ttc_to_ttf(path):
    if not os.path.isdir('converted_fonts'):
        os.mkdir('converted_fonts')
    if len(os.listdir('converted_fonts')) > 0:
        print(f'{Colors.FAIL}[!]{Colors.ENDC} the directory converted_fonts is not empty!')
        return

    with open(path, 'rb') as fp:
        num_fonts = sfnt.SFNTReader(fp, fontNumber=0).numFonts

    for ft_idx in range(num_fonts):
        font = TTFont(path, fontNumber=ft_idx, lazy=True)

        psname = get_psname(font)
        if psname is None:
            ttc_name = os.path.splitext(os.path.basename(path))[0]
            psname = f'{ttc_name}-font{ft_idx}'

        ext = '.otf' if font.sfntVersion == 'OTTO' else '.ttf'
        font_filename = f'{psname}{ext}'
        font.save(f'{pathlib.Path(__file__).parent.resolve()}/converted_fonts/{font_filename}')

        font.close()
