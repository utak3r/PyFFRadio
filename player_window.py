import PySimpleGUI as sg
import process_tools

class Player:

    def __init__(self):
        self.layout = [
            [sg.Button('Play', key='play')]
        ]
        self.window = sg.Window("Player", self.layout)
        self.runner = None

    def run(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, 'exit'):
                if self.runner != None:
                    self.runner.terminate()
                    self.runner = None
                break

            if self.event == 'play':
                self.play_station()

        self.window.close()

    def play_station(self):
        if self.runner != None:
            self.runner.terminate()
            self.runner = None
        ffmpeg = 'C:\\tools\\ffmpeg\\bin\\ffplay.exe'
        params = 'https://an.cdn.eurozet.pl/ant-waw.mp3'
        command = '"' + ffmpeg + '" -nodisp "' + params + '"'
        self.runner = process_tools.ProcessRunner()
        self.runner.run_command(command)