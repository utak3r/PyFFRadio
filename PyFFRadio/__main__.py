__version__ = "0.1.0"

import sys
import PySimpleGUI as sg
from PyFFRadio.player_window import Player

TRAY_APP = False

if __name__ == "__main__":
    if TRAY_APP:
        tray_menu = ['BLANK', ['&Open', '---', 'E&xit']]
        tray = sg.SystemTray(menu=tray_menu, filename=r'PyFFRadio.ico')

        while True:
            menu_item = tray.read()
            print(menu_item)
            if menu_item == 'Exit':
                break
            elif menu_item == 'Open':
                player = Player()
                player.run()

    else:
        player = Player()
        player.run()


    sys.exit(0)
