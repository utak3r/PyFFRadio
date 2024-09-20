import PySimpleGUI as sg
import player_window

TRAY_APP = False

if TRAY_APP:
    tray_menu = ['BLANK', ['&Open', '---', 'E&xit']]
    tray = sg.SystemTray(menu=tray_menu, filename=r'PyFFRadio.ico')

    while True:
        menu_item = tray.read()
        print(menu_item)
        if menu_item == 'Exit':
            break
        elif menu_item == 'Open':
            player = player_window.Player()
            player.run()

else:
    player = player_window.Player()
    player.run()

