import os
from pathlib import Path

# Get correct path
import sys
import os
if getattr(sys, 'frozen', False):
    cur_path = os.path.dirname(sys.executable)
else:
    cur_path = str(os.path.dirname(__file__))

home_path = str(Path.home())

APP_TITLE        = "SmartGrids"
APP_VERSION      = "1.3.0"
FILE_TYPE        = '.grid'
DEBUG            = False

# Default values
PAGE_WIDTH       = 210
PAGE_HEIGHT      = 210
TOP_MARGIN       = 10.0
BOTTOM_MARGIN    = 20.0
LEFT_MARGIN      = 10.0
RIGHT_MARGIN     = 10.0

FONT_SIZE        = 10.0
LEADING          = 12.0
CAP_HEIGHT       = 1.5

ROWS             = 8
LINES_IN_GUTTER  = 1
COLUMNS          = 9
GUTTER           = 50

# Font directories
# To include new font into the dropdown list, add the path to the directory to the list
# All paths which don't contain fontfiles or do not exist will be ignored

FONT_DIRECTORIES = [
        os.path.join(home_path, "Library/Application Support/Adobe/CoreSync/plugins/livetype/.r"),
        #os.path.join(home_path, "Library/Fonts"),
        os.path.join("/Library/Application Support/Adobe/Fonts"),
        #"/System/Library/Fonts",
        #os.path.join(home_path, 'Windows\Fonts'),
        #os.path.join(home_path, 'AppData\Roaming\Adobe\CoreSync\plugins\livetype\r'),

    ]