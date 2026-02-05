import os
import sys

if hasattr(sys, "_MEIPASS"):
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

import japanize_kivy


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition

import csv

import search
import check_rhymes

if hasattr(sys, "_MEIPASS"):
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_kanji_data(filepath: str) -> list[dict]:
    kanji_data = []
    filepath = resource_path(filepath)
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kanji_data.append(row)
    return kanji_data

def load_rhyme_names(filepath: str) -> dict:
    rhyme_names = []
    filepath = resource_path(filepath)
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rhyme_names.append(row)
    return rhyme_names[0]

def get_color_by_pingze(pingze: str) -> tuple:
    if pingze.startswith('p'):
        return (1, 1, 0, 1)  
    else:
        return (0.2, 0.2, 1, 1)  
    
class DummyScreen(Screen):
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.kanji_list = [{'kanji': '', 'rhyme': ''} for _ in range(28)]
        self.selected_index = -1

    def on_enter(self):
        layout = self.ids.kanji_layout
        layout.clear_widgets()
        kanji_color = check_rhymes.get_color_by_checked_rhyme(self.kanji_list)
        i = 0
        for kanji_info in self.kanji_list:
            kanji_char = kanji_info.get('kanji', '')
            btn = InputButton(
                text = kanji_char,
                background_color=kanji_color[i]
            )
            btn.number = i
            i += 1
            layout.add_widget(btn)
    def show_string(self, orientation = True):
        app = App.get_running_app()
        result = ''
        if orientation:
            for i in range(7):
                for j in range(4):
                    result += self.kanji_list[i + j * 7]['kanji']
                    result += ' '
                result += '\n'
        else:
            for i in range(3, -1, -1):
                for j in range(7):
                    result += self.kanji_list[j + i * 7]['kanji']
                result += '\n\n'
        self.manager.get_screen('export').ids.export.text = result
        app.root.switch_to_Export()




class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.results = []
        self.radicals = ""


    def on_kv_post(self, base_widget):
        self.ids.r_all.active = True
        self.ids.r_ping.active = False
        self.ids.r_ze.active = False
        with open(resource_path('all_groups.txt'), 'r', encoding='utf-8-sig') as f:
            self.radicals = f.read()
        for radical in self.radicals:
            btn = Button(text=radical, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn_instance: self.get_result_by_radical(btn_instance.text))
            self.ids.radicals.add_widget(btn)

        self.rhyme_names = load_rhyme_names('rhyme_name.csv')
        for key, rhyme in self.rhyme_names.items():
            btn = Button(text=rhyme, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn_instance: self.get_result_by_rhyme(btn_instance.text))
            self.ids.rhymes.add_widget(btn)


    def get_result_by_reading(self, reading):
        self.results = search.search_kanji_by_reading(self.manager.kanji_data, reading)
        if (not self.ids.r_all.active):
            pingze = self.ids.r_ping.active
            self.results = search.filter_kanji_by_pingze(self.results, pingze)
        self.display_results()
    
    def get_result_by_radical(self, radical):
        self.results = search.search_kanji_by_radical(self.manager.kanji_data, radical)
        if (not self.ids.r_all.active):
            pingze = self.ids.r_ping.active
            self.results = search.filter_kanji_by_pingze(self.results, pingze)
        self.display_results()
    def get_result_by_kanji(self, kanji_char):
        self.results = search.lookup_kanji(self.manager.kanji_data, kanji_char)
        if (not self.ids.r_all.active):
            pingze = self.ids.r_ping.active
            self.results = search.filter_kanji_by_pingze(self.results, pingze)
        self.display_results()

    def get_result_by_rhyme(self, rhyme):
        rhyme_key = [key for key, value in self.rhyme_names.items() if value == rhyme][0]
        self.results = search.search_kanji_by_rhymes(self.manager.kanji_data, rhyme_key)
        if (not self.ids.r_all.active):
            pingze = self.ids.r_ping.active
            self.results = search.filter_kanji_by_pingze(self.results, pingze)
        self.display_results()
        
    def display_results(self):
        result_layout = self.ids.result_reading
        result_layout.clear_widgets()
        i = 0
        for single_kanji in self.results:
            kanji_char = single_kanji.get('kanji', '?')
            btn = ResultButton(text=kanji_char, background_color=get_color_by_pingze(single_kanji.get('rhyme', '')))
            btn.number = i
            result_layout.add_widget(btn)
            i += 1


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.rhyme = ''
    
    def send_kanji_to_main(self):
        app = App.get_running_app()
        main_screen = app.root.get_screen('main')
        detail_screen = app.root.get_screen('detail')
        kanji_char = detail_screen.ids.kanji_char.text
        rhyme = detail_screen.rhyme
        main_screen.kanji_list[main_screen.selected_index] = {'kanji': kanji_char, 'rhyme': rhyme}
        app.root.switch_to_main()

class ExportScreen(Screen):
    pass

class InputButton(Button):
    def __init__(self, **kwargs):
        super(InputButton, self).__init__(**kwargs)
        self.number = 0
    
    def input_kanji(self):
        app = App.get_running_app()
        main_screen = app.root.get_screen('main')
        main_screen.selected_index = self.number
        app.root.switch_to_search()
    

class ResultButton(Button):
    number = 0
    def show_detail(self):
        # SearchScreenを正確に取得
        current_screen = self.parent
        while current_screen and not isinstance(current_screen, SearchScreen):
            current_screen = current_screen.parent
        
        if not current_screen:
            print("Error: SearchScreen not found")
            return
        
        search_screen = current_screen
        kanji_data = search_screen.results
        kanji_info = kanji_data[self.number]
        manager = search_screen.manager
        rhyme_names = manager.rhyme_names
        detail_screen = manager.get_screen('detail')
        
        detail_screen.ids.kanji_char.text = kanji_info.get('kanji', '?')
        detail_screen.ids.kanji_char.background_color = get_color_by_pingze(kanji_info.get('rhyme', ''))
        detail_screen.ids.kanji_onyomi.text = kanji_info.get('onyomi', '不明')
        detail_screen.ids.kanji_kunyomi.text = kanji_info.get('kunyomi', '不明')

        rhyme = kanji_info.get('rhyme', '不明')
        if rhyme and len(rhyme) > 0 and rhyme[0] == 'p':
            detail_screen.ids.kanji_rhyme.text = '平声' + rhyme_names.get(rhyme, '')
        else:
            detail_screen.ids.kanji_rhyme.text = '仄声'
        detail_screen.rhyme = rhyme
        
        manager.switch_to_detail()

class MainLayout(ScreenManager):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.add_widget(DummyScreen(name='dummy'))  # ダミースクリーンを追加
        self.add_widget(MainScreen(name='main'))
        self.add_widget(SearchScreen(name='search'))
        self.add_widget(DetailScreen(name='detail'))
        self.add_widget(ExportScreen(name='export'))
        self.current = 'main'
        self.kanji_data = load_kanji_data('kanji_data_modified.csv')
        self.rhyme_names = load_rhyme_names('rhyme_name.csv')
    
    def switch_to_search(self, direction='left'):
        self.transition = SlideTransition(direction=direction)
        self.current = 'search'

    def switch_to_detail(self):
        self.transition = SlideTransition(direction='left')
        self.current = 'detail'

    def switch_to_Export(self):
        self.transition = SlideTransition(direction='left')
        self.current = 'export'

    def switch_to_main(self):
        self.transition = SlideTransition(direction='right')
        self.current = 'main'
    def start_main(self):
        self.transition = NoTransition()
        self.current = 'main'



class KanshiApp(App):

    def build(self):
        return MainLayout()
    
    
if __name__ == '__main__':
    KanshiApp().run()