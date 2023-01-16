import os
from pathlib import Path

home_path = str(Path.home())

APP_TITLE        = "SmartGrids"
APP_VERSION      = "1.2.3"

DEBUG            = True

CANVAS_WIDTH     = 10
CANVAS_HEIGHT    = 10

CANVAS_PADDING   = 10

# Default values
PAGE_WIDTH       = 1920.0
PAGE_HEIGHT      = 1080.0
TOP_MARGIN       = 50.0
BOTTOM_MARGIN    = 75.0
LEFT_MARGIN      = 100.0
RIGHT_MARGIN     = 30.0

FONT_SIZE        = 24.0
LEADING          = 27.0
CAP_HEIGHT       = 1.5

ROWS             = 6
LINES_IN_GUTTER  = 1
COLUMNS          = 9
GUTTER           = 50

FONT_DIRECTORIES = [
        os.path.join(home_path, "Library/Application Support/Adobe/CoreSync/plugins/livetype/.r"),
        os.path.join(home_path, "Library/Fonts"),
        os.path.join("/Library/Application Support/Adobe/Fonts"),
        "/System/Library/Fonts",
        os.path.join(home_path, 'Windows\Fonts'),
        os.path.join(home_path, 'AppData\Roaming\Adobe\CoreSync\plugins\livetype\r')

    ]