import pytest
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