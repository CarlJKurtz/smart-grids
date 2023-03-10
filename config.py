from pathlib import Path

# Get correct path
import sys
import os
if getattr(sys, 'frozen', False):
    cur_path = os.path.dirname(sys.executable)
else:
    cur_path = str(os.path.dirname(__file__))

home_path = str(Path.home())

APP_TITLE        = 'SmartGrids'
APP_VERSION      = '1.3.1'
FILE_TYPE        = '.grid'
DEBUG            = True

# Default values in pt
UNIT             = 'mm'  # Supported units: mm, pt, in, px, cm
PAGE_WIDTH       = 595.276
PAGE_HEIGHT      = 841.89
TOP_MARGIN       = 56.693
BOTTOM_MARGIN    = 170.079
LEFT_MARGIN      = 141.732
RIGHT_MARGIN     = 56.693

FONT_SIZE        = 9
LEADING          = 11.5
CAP_HEIGHT       = 1.5

ROWS             = 6
LINES_IN_GUTTER  = 1
COLUMNS          = 5
GUTTER           = 28.346

# Font directories
# To include new font into the dropdown list, add the path to the directory to the list
# All paths which don't contain fontfiles or do not exist will be ignored

FONT_DIRECTORIES = [
        os.path.join(home_path, 'Library/Application Support/Adobe/CoreSync/plugins/livetype/.r'),
        os.path.join(home_path, 'Library/Fonts'),
        os.path.join('/Library/Application Support/Adobe/Fonts'),
        '/System/Library/Fonts',
        os.path.join(home_path, 'Windows\Fonts'),
        os.path.join(home_path, 'AppData\Roaming\Adobe\CoreSync\plugins\livetype\r'),

    ]