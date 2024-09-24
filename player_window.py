import PySimpleGUI as sg
import process_tools
import settings

class Player:

    def __init__(self):
        self.layout = [
            [sg.Button('Play', key='play')]
        ]
        self.window = sg.Window("Player", self.layout)
        self.runner = None
        self.settings = settings.Settings()

    def run(self):
        self.settings.read_settings()
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