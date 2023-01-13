from config import *
from PyQt5.QtWidgets import QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        background_image = QPixmap('assets/splashscreen.png')
        self.setPixmap(background_image)
        self.setMask(background_image.mask())

        logo = QPixmap('assets/smart_grids-icon.png').scaledToWidth(80)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo)
        logo_label.move(20, 20)

        app_name_label = QLabel(APP_TITLE, self)
        app_name_label.setFont(QFont('Default', 42, weight=QFont.Bold))
        app_name_label.move(108, 25)

        version_label = QLabel(f'v. {APP_VERSION}', self)
        version_label.setFont(QFont('Courier', 14))
        version_label.move(113, 75)
        version_label.setStyleSheet("color: grey;")

        copyright_label = QLabel(f'{APP_TITLE} was created by Carl J.  Kurtz in 2022\n'
                           f'It is maintained by him and the GitHub community.\n'
                           f'\n'
                           f'\n'
                           f'Visit SmartGrids on GitHub.com for more information.', self)
        copyright_label.setFont(QFont('Default', 14))
        copyright_label.move(25, 140)
        copyright_label.setStyleSheet("color: lightgrey;")

        QTimer.singleShot(10000, self.close)
