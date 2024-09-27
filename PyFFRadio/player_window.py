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
        #self.window['status'].update(value='Loading configuration')
        self.settings.read_settings('PyFFRadio.ini')

        # Add stations read from config to layout
        for stacja in self.settings.stations:
            self.window.extend_layout(self.window['-STATIONS-LIST-'], [self.row_item_station(1, stacja.name)])

        #self.window['status'].update('Ready')
        while True:
            self.event, self.values = self.window.read()
            #print('DEBUG: Event came in: ', self.event)
            if self.event in (sg.WIN_CLOSED, 'exit'):
                if self.runner != None:
                    self.runner.terminate()
                    self.runner = None
                break

            if self.event == 'play':
                self.play_station(0)
            
            if isinstance(self.event, tuple):
                if self.event[0] == 'station selection':
                    station_name = self.event[1]
                    print("New station selected: ", station_name)
                    self.play_station(station_name)

        self.settings.write_settings('PyFFRadio.ini')
        self.window.close()

    def init_layout(self):
        self.layout = []
        info_layout = sg.Text('Title', key='title')
        lista_layout = sg.Column([], key='-STATIONS-LIST-') 
        bottom_buttons_layout = sg.Button('Play', key='play'), sg.Button('Exit', key='exit')
        #status_layout = sg.StatusBar('status', key='status', auto_size_text=True, expand_x=True, justification='left')
        #self.layout = [ [info_layout, lista_layout], [bottom_buttons_layout], [status_layout] ]
        self.layout = [ [info_layout, lista_layout], [bottom_buttons_layout] ]

    def row_item_station(self, row_num, station_name):
        item = [sg.Column([[sg.Text(f'{station_name}', key=('station selection', station_name), enable_events=True)]], key=('-ROW-', row_num))]
        return item

    def cleanup_player(self):
        if self.runner is not None:
            self.runner.terminate()
            del self.runner
            self.runner = None

    def play_station(self, which_station):
        if isinstance(which_station, int):
            self.cleanup_player()
            ffmpeg = self.settings.ffmpeg() + '\\ffplay.exe'
            station_name = self.settings.stations[which_station].name
            station_url = self.settings.stations[which_station].url
            command = '"' + ffmpeg + '" -nodisp "' + station_url + '"'
            self.runner = process_tools.ProcessRunner()
            self.runner.run_command(f'{ffmpeg}', '-nodisp', f'{station_url}')
            # For now I have some issue with status bar not showing the full string
            # will solve it later...
            #status_text = 'Now playing: quite long station name' + station_name
            #self.window['status'].update(value=station_name)
        elif isinstance(which_station, str):
            index = self.settings.stations.get_item_index_by_name(which_station)
            self.play_station(index)
        else:
            NotImplemented

