import pytest
import pathlib
from PyFFRadio.settings import RadioStation, RadioStationsList, Settings

class TestRadioStation:

    def test_constructor(self):
        stacja1 = RadioStation()
        assert stacja1.name == 'no name'
        assert stacja1.url == 'http://127.0.0.1'
        stacja2 = RadioStation('That is a nice name!')
        assert stacja2.name == 'That is a nice name!'
        assert stacja2.url == 'http://127.0.0.1'
        stacja3 = RadioStation('That is a nice name!', 'http://somewhere.in.a.web/')
        assert stacja3.name == 'That is a nice name!'
        assert stacja3.url == 'http://somewhere.in.a.web/'
        stacja4 = RadioStation('Another name...', 'http://link.to.radio/', 'http://link.to/logo.png')
        assert stacja4.name == 'Another name...'
        assert stacja4.url == 'http://link.to.radio/'
        assert stacja4.cover_url == 'http://link.to/logo.png'

    def test_set_name(self):
        name = 'Very Nice Name'
        stacja = RadioStation()
        assert stacja.name == 'no name'
        stacja.set_name(name)
        assert stacja.name == name

    def test_set_url(self):
        url = 'http://notso.local.host/here'
        stacja = RadioStation()
        assert stacja.url == 'http://127.0.0.1'
        stacja.set_url(url)
        assert stacja.url == url
    
    def test_set_cover_url(self):
        url = 'http://here.is.some/logo.png'
        stacja = RadioStation()
        assert stacja.cover_url == ''
        stacja.set_cover_url(url)
        assert stacja.cover_url == url

    def test_operator_eq(self):
        stacja1 = RadioStation()
        stacja2 = RadioStation()
        some_name = 'Compared Name'

        stacja1.set_name('name 1')
        stacja2.set_name('name 2')
        assert stacja1 != stacja2
        assert stacja1 != some_name
        assert stacja2 != some_name

        stacja1.set_name(some_name)
        assert stacja1 != stacja2
        assert stacja1 == some_name

        stacja2.set_name(some_name)
        assert stacja1 == stacja2
    
    def test_operator_str(self):
        stacja = RadioStation('Great station')
        assert f'{stacja}' == 'RadioStation(Name: Great station, URL: http://127.0.0.1)'

class TestRadioStationsList:

    def test_clear(self):
        lista = RadioStationsList()
        num = len(lista)
        stacja = RadioStation()
        lista.add(stacja)
        assert len(lista) == num + 1
        lista.clear()
        assert len(lista) == 0

    def test_add(self):
        lista = RadioStationsList()
        num = len(lista)
        stacja = RadioStation()
        test_name = 'this is it!'
        stacja.set_name(test_name)
        lista.add(stacja)
        assert len(lista) == num + 1
        assert lista[num].name == test_name

    def test_get_item_index_by_name(self):
        lista = RadioStationsList()
        num = 5
        for x in range(0, num):
            stacja = RadioStation()
            stacja.set_name('stacja %d' % (x))
            lista.add(stacja)
        assert len(lista) == num
        assert lista[2] == f'stacja {2}'
        assert lista[4] == f'stacja {4}'

        assert lista.get_item_index_by_name(f'stacja {2}') == 2
        assert lista.get_item_index_by_name(f'stacja {4}') == 4
        with pytest.raises(ValueError):
            lista.get_item_index_by_name('No such name...')

    def test_operator_iadd(self):
        lista = RadioStationsList()
        stacja = RadioStation()
        name = 'stacja 1'
        stacja.set_name(name)
        lista += stacja
        assert len(lista) == 1
        assert lista[0].name == name

    def test_operator_len(self):
        lista = RadioStationsList()
        for x in range(0, 5):
            stacja = RadioStation()
            lista.add(stacja)
            assert len(lista) == x+1
    
    def test_operator_getitem(self):
        lista = RadioStationsList()
        num = 5
        for x in range(0, num):
            stacja = RadioStation()
            stacja.set_name('stacja %d' % (x))
            lista.add(stacja)
        
        assert lista[1].name == 'stacja 1'
        assert lista[3].name == 'stacja 3'

    def test_iterator(self):
        lista = RadioStationsList()
        num = 100
        for x in range(0, num):
            stacja = RadioStation()
            stacja.set_name('stacja %d' % (x))
            lista.add(stacja)
        i = 0
        for stacja in lista:
            assert stacja.name == f'stacja {i}'
            i += 1

class TestSettings:

    def write_file(self, path, text):
        file = open(path, mode='w', encoding='utf-8')
        file.write(text)
        file.close()
    
    def remove_file(self, path):
        pathlib.Path('./' + path).unlink()

    def test_read_settings_file(self):
        file = 'test_config_file.ini'
        default_ffmpeg_path = 'C:\\tools\\ffmpeg\\bin'
        default_station_name = 'Radio 357'

        config_test_1_src = '' # empty file
        self.write_file(file, config_test_1_src)

        settings = Settings()
        assert settings.ffmpeg() == '.'
        assert len(settings.stations) == 0
        settings.read_settings(file)
        assert settings.ffmpeg() == default_ffmpeg_path
        assert len(settings.stations) == 1
        assert settings.stations[0].name == default_station_name

        # remove file
        self.remove_file(file)

        config_test_2_src = '[GENERAL]\nFFMPEG_Path = C:\\Program Files\\ffmpeg\\bin' # no radio stations provided
        self.write_file(file, config_test_2_src)

        settings = Settings()
        assert settings.ffmpeg() == '.'
        assert len(settings.stations) == 0
        settings.read_settings(file)
        assert settings.ffmpeg() == 'C:\\Program Files\\ffmpeg\\bin'
        assert len(settings.stations) == 1
        assert settings.stations[0].name == default_station_name

        # remove file
        self.remove_file(file)

        # full config with 2 stations
        config_test_3_src = '[GENERAL]\nFFMPEG_Path = C:\\Strange path\\ffmpeg\\bin\n\n[STATIONS]\nSuperFM = https://stream.super.fm:8443/superfm.mp3?1727132225114\nAntyradio = https://an.cdn.eurozet.pl/ant-web.mp3' 
        self.write_file(file, config_test_3_src)

        settings = Settings()
        assert settings.ffmpeg() == '.'
        assert len(settings.stations) == 0
        settings.read_settings(file)
        assert settings.ffmpeg() == 'C:\\Strange path\\ffmpeg\\bin'
        assert len(settings.stations) == 2
        assert settings.stations[0].name == 'SuperFM'
        assert settings.stations[0].url == 'https://stream.super.fm:8443/superfm.mp3?1727132225114'
        assert settings.stations[1].name == 'Antyradio'
        assert settings.stations[1].url == 'https://an.cdn.eurozet.pl/ant-web.mp3'

        # remove file
        self.remove_file(file)

    def test_write_settings(self):
        file = 'test_config_file.ini'
        settings = Settings()
        settings.set_ffmpeg('C:\\Program Files\\ffmpeg\\bin')
        settings.stations.add(RadioStation('Super Station', 'https://super.station/web.mp3', 'http://logos.com/logo1.png'))
        settings.stations.add(RadioStation('Fantastic Station', 'https://fantastic.station/stream.mp3', 'http://logos.com/logo2.png'))
        settings.write_settings(file)

        read_file = open(file, mode='r', encoding='utf-8').read()
        assert read_file == '[GENERAL]\nFFMPEG_Path = C:\\Program Files\\ffmpeg\\bin\n\n[STATIONS]\nSuper Station = https://super.station/web.mp3\nFantastic Station = https://fantastic.station/stream.mp3\n\n[COVERS]\nSuper Station = http://logos.com/logo1.png\nFantastic Station = http://logos.com/logo2.png\n\n'

        # remove file
        self.remove_file(file)
       