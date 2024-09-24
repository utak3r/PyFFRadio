import configparser

class RadioStation:

    def __init__(self):
        self.name = 'no name'
        self.url = 'http://127.0.0.1'

    def set_name(self, new_name: str):
        self.name = new_name
    
    def set_url(self, new_url: str):
        self.url = new_url


class RadioStationsList:

    def __init__(self):
        self.stations_list = []

    def clear(self):
        self.stations_list.clear()

    def add(self, station: RadioStation):
        self.stations_list.append(station)
    
    def __iadd__(self, station: RadioStation):
        self.stations_list.append(station)

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

    def read_settings(self):
        config = configparser.ConfigParser()
        # Below line changes the default behaviour of ConfigParser
        # making the keys to be case sensitive :)
        config.optionxform = str
        config.read('PyFFRadio.ini')
        try:
            self.ffmpeg_ = config['PATHS']['FFMPEG_Path']
        except KeyError:
            print("Error: Couldn't find a FFMPEG_Path entry in config file.")
        self.stations.clear()
        for stacja in config['STATIONS']:
            station = RadioStation()
            station.set_name(stacja)
            station.set_url(config['STATIONS'][stacja])
            self.stations.add(station)
        for stacja in self.stations:
            print(stacja.name + " : " + stacja.url)
        return
    
    def write_settings(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['PATHS'] = { 'FFMPEG_Path': self.ffmpeg_ }
        config['STATIONS'] = {}
        for stacja in self.stations:
            try:
                config['STATIONS'][stacja.name] = stacja.url
            except KeyError:
                print("Error while writing list of radio stations into config file.")

        with open('PyFFRadio.ini', mode='w', encoding="utf-8") as configfile:
            config.write(configfile)
        return
    
