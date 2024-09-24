import PySimpleGUI as sg
from PyFFRadio import process_tools
from PyFFRadio import settings

class Player:

    def __init__(self):
        self.init_layout()
        self.window = sg.Window("Player", self.layout)
        self.runner = None
        self.settings = settings.Settings()

    def run(self):
        self.window.finalize()
        self.window['status'].update(value='Loading configuration')
        self.settings.read_settings()
        self.window['status'].update('Ready')
        while True:
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, 'exit'):
                if self.runner != None:
                    self.runner.terminate()
                    self.runner = None
                break

            if self.event == 'play':
                self.play_station()

        self.settings.write_settings()
        self.window.close()

    def init_layout(self):
        self.layout = []
        info_layout = sg.Text('Title', key='title')
        lista_layout = sg.Text('Station {i}', key='station') 
        bottom_buttons_layout = sg.Button('Play', key='play'), sg.Button('Exit', key='exit')
        status_layout = sg.StatusBar('status', key='status')
        self.layout = [ [info_layout, lista_layout], [bottom_buttons_layout], [status_layout] ]

    def play_station(self):
        # As of now, second try not working, to say at least.
        # Need to work on cleaning up previous playback.
        if self.runner is not None:
            del self.runner
            self.runner = None
        ffmpeg = self.settings.ffmpeg() + '\\ffplay.exe'
        station_url = self.settings.stations[0].url
        command = '"' + ffmpeg + '" -nodisp "' + station_url + '"'
        self.runner = process_tools.ProcessRunner()
        self.runner.run_command(command)
        self.window['status'].update('Playing')