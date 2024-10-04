import PySimpleGUI as sg
import io
import requests
from PIL import Image, UnidentifiedImageError
import base64
from PyFFRadio import process_tools
from PyFFRadio import settings

COVER_IMG_SIZE=(96,96)

class Player:

    def __init__(self):
        self.init_layout()
        self.window = sg.Window("Player", self.layout)
        self.runner = None
        self.settings = settings.Settings()
        self.station_button_color = '#CC8800'

    def run(self):
        self.window.finalize()
        self.window.set_min_size((400,150))
        #self.window['status'].update(value='Loading configuration')
        self.settings.read_settings('PyFFRadio.ini')

        # Add stations read from config to layout
        for stacja in self.settings.stations:
            self.window.extend_layout(self.window['-STATIONS-LIST-'], [self.row_item_station(1, stacja.name)])
            self.window.refresh()
            self.window['-STATIONS-LIST-'].contents_changed()
        # Download covers (images)
        self.download_stations_covers(self.settings.stations, COVER_IMG_SIZE)

        while True:
            self.event, self.values = self.window.read()
            #print('DEBUG: Event came in: ', self.event)
            if self.event in (sg.WIN_CLOSED, 'exit'):
                if self.runner != None:
                    self.runner.terminate()
                    self.runner = None
                break

            if isinstance(self.event, tuple):
                if self.event[0] == 'station selection':
                    station_name = self.event[1]
                    print("New station selected: ", station_name)
                    self.play_station(station_name)

        self.settings.write_settings('PyFFRadio.ini')
        self.window.close()

    def init_layout(self):
        self.layout = []
        info_layout = [sg.Push(), sg.Image(size=COVER_IMG_SIZE, key='current-station-cover'), sg.Push()], [sg.Push(), sg.Text('Title', key='current-station'), sg.Push()]
        lista_layout = sg.Column([], key='-STATIONS-LIST-', size=(200,120), scrollable=True, vertical_scroll_only=True) 
        bottom_buttons_layout = sg.Push(), sg.Button('Exit', key='exit', size=(15,1)), sg.Push()
        self.layout = [ [sg.Column(info_layout), sg.Push(), lista_layout], [bottom_buttons_layout] ]

    def row_item_station(self, row_num, station_name):
        item = [sg.Button(f'{station_name}', key=('station selection', station_name), 
                                      auto_size_button=False, 
                                      expand_x=True, 
                                      size=(25,1),
                                      pad=(4, 0), 
                                      use_ttk_buttons=True, 
                                      button_color=self.station_button_color)]
        return item

    def cleanup_player(self):
        if self.runner is not None:
            self.runner.terminate()
            del self.runner
            self.runner = None

    def play_station(self, which_station):
        if isinstance(which_station, int):
            self.cleanup_player()
            try:
                ffmpeg = self.settings.check_for_ffmpeg_binary()
            except NotADirectoryError:
                sg.popup_error('Given directory path cannot be found.', title='Error')
                return
            except FileExistsError:
                sg.popup_error('Cannot find ffplay in a given directory.', title='Error')
                return
            station_name = self.settings.stations[which_station].name
            station_url = self.settings.stations[which_station].url
            command = '"' + ffmpeg + '" -nodisp "' + station_url + '"'
            self.runner = process_tools.ProcessRunner()
            self.runner.run_command(f'{ffmpeg}', '-nodisp', f'{station_url}')
            self.window['current-station'].update(f'{self.runner.info.name}\n{self.runner.info.description}')
            raw_img = None
            if self.settings.stations[which_station].cover:
                raw_img = self.settings.stations[which_station].cover
            self.window['current-station-cover'].update(data=raw_img)
        elif isinstance(which_station, str):
            index = self.settings.stations.get_item_index_by_name(which_station)
            self.play_station(index)
        else:
            NotImplemented

    def get_base64_string_from_image(self, img: Image.Image) -> str:
        """Return PNG Base64 encoded string from an image"""
        imgbuff = io.BytesIO()
        img.save(imgbuff, format='PNG')
        return base64.b64encode(imgbuff.getbuffer())

    def resize_img_with_aspect_ratio(self, img: Image.Image, size: tuple, keep_aspect: bool) -> Image.Image:
        imgret = img
        if keep_aspect:
            aspect = img.width / img.height
            new_height = int(size[0] / aspect)
            imgret = img.resize((size[0],new_height))
        else:
            imgret = img.resize(size)
        return imgret

    def download_stations_covers(self, stations: settings.RadioStationsList, size: tuple):
        for stacja in stations:
            if stacja.cover_url not in (None, ''):
                req = requests.get(stacja.cover_url, stream=True)
                if req.status_code == 200:
                    buff = io.BytesIO(req.content)
                    try:
                        img = Image.open(buff)
                    except UnidentifiedImageError:
                        stacja.cover = None
                    else:
                        #img = img.resize(size=size)
                        img = self.resize_img_with_aspect_ratio(img, size, True)
                        stacja.cover = self.get_base64_string_from_image(img)
