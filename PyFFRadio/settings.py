import configparser
import os
import platform

class RadioStation:

    # Of course, Python is incapable of overloading methods (and thus construcotrs)...
    # Let's hack it then.
    def __init__(self, *args):
        self.name = 'no name'
        self.url = 'http://127.0.0.1'
        self.cover_url = ''
        self.cover = None

        if len(args) == 3:
            self.name = args[0]
            self.url = args[1]
            self.cover_url = args[2]
        if len(args) == 2:
            self.name = args[0]
            self.url = args[1]
        elif len(args) == 1:
            self.name = args[0]
    
    def set_name(self, new_name: str):
        self.name = new_name
    
    def set_url(self, new_url: str):
        self.url = new_url
    
    def set_cover_url(self, new_url: str):
        self.cover_url = new_url
        self.cover = None
    
    def __eq__(self, other):
        if isinstance(other, RadioStation):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented
    
    def __str__(self):
        return "RadioStation(Name: {}, URL: {})".format(self.name, self.url)


class RadioStationsList:

    def __init__(self):
        self.stations_list = []

    def clear(self):
        self.stations_list.clear()

    def add(self, station: RadioStation):
        self.stations_list.append(station)
    
    def get_item_index_by_name(self, name: str) -> int:
        index = self.stations_list.index(name)
        return index

    def __iadd__(self, station: RadioStation):
        self.stations_list.append(station)
        return self

    def __len__(self) -> int:
        return len(self.stations_list)
    
    def __getitem__(self, key):
        return self.stations_list[key]
    
    def __iter__(self):
        self.iter_pos = 0
        return self
    
    # No, this iterator is NOT safe ;) especially, when it comes to multithreading.
    def __next__(self):
        if self.iter_pos < len(self.stations_list):
            station = self.stations_list[self.iter_pos]
            self.iter_pos += 1
            return station
        else:
            raise StopIteration


class Settings:
    """This class holds all the settings for the app."""

    def __init__(self):
        self.ffmpeg_ = "."
        self.stations = RadioStationsList()


    def ffmpeg(self) -> str:
        return self.ffmpeg_
    
    def set_ffmpeg(self, new_path: str):
        self.ffmpeg_ = new_path

    # Prepare config object
    def prepare_settings_object(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.optionxform = str # make it case sensitive
        return config

    # Read config from file.
    def read_settings_file(self, path) -> configparser.ConfigParser:
        config = self.prepare_settings_object()
        config.read(path, encoding="utf-8")
        return config
    
    # Write config to a file
    def write_settings_file(self, config:configparser.ConfigParser, path: str):
        with open(path, mode='w', encoding="utf-8") as configfile:
            config.write(configfile)

    # Take care of default FFMPEG path and at least one radio station.
    def provide_defaults(self, config: configparser.ConfigParser) -> configparser.ConfigParser:
        try:
            ffmpeg = config['GENERAL']['FFMPEG_Path']
        except KeyError:
            config['GENERAL'] = {}
            config['GENERAL']['FFMPEG_Path'] = 'C:\\tools\\ffmpeg\\bin'
        if not config.has_section('STATIONS'):
            config['STATIONS'] = {}
            config['STATIONS']['Radio 357'] = 'https://live.r357.eu'
        return config

    def read_settings(self, config_file_path: str):
        config = self.read_settings_file(config_file_path)
        config = self.provide_defaults(config)
        self.ffmpeg_ = config['GENERAL']['FFMPEG_Path']
        self.stations.clear()
        for stacja in config['STATIONS']:
            station = RadioStation()
            station.set_name(stacja)
            station.set_url(config['STATIONS'][stacja])
            self.stations.add(station)
        # for stacja in self.stations:
        #     print(stacja.name + " : " + stacja.url)
        if config.has_section('COVERS'):
            for stacja in config['COVERS']:
                if stacja in self.stations.stations_list:
                    self.stations[self.stations.get_item_index_by_name(stacja)].set_cover_url(config['COVERS'][stacja])
        return
    
    def write_settings(self, config_file_path: str):
        config = self.prepare_settings_object()
        config['GENERAL'] = { 'FFMPEG_Path': self.ffmpeg_ }
        config['STATIONS'] = {}
        config['COVERS'] = {}
        for stacja in self.stations:
            try:
                config['STATIONS'][stacja.name] = stacja.url
                config['COVERS'][stacja.name] = stacja.cover_url
            except KeyError:
                print("Error while writing list of radio stations into config file.")

        self.write_settings_file(config, config_file_path)
        return
    
    def select_os_binary(self, binary: str) -> str:
        """Add system platform dependent / or \\ and eventually .exe"""
        file = binary
        system = platform.system()
        if system == 'Windows':
            file = '\\' + file + '.exe'
        else:
            file = '/' + file
        return file
    
    def construct_full_binary_path(self, dir: str, binary: str) -> str:
        bin = self.select_os_binary(binary)
        return f'{dir}{bin}'

    def check_for_ffmpeg_binary(self) -> str:
        full_path = ''
        dirpath = self.ffmpeg()
        if os.path.isdir(dirpath):
            path = self.construct_full_binary_path(dirpath, 'ffplay')
            if os.path.isfile(path):
                full_path = path
            else:
                raise FileExistsError
        else:
            raise NotADirectoryError
        return full_path
