from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized') # Maximize window on startup
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.chip import MDChip
from kivymd.uix.selectioncontrol import MDCheckbox
from libs.components.my_checkbox import MyCheckbox
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.lang.builder import Builder
import os
import pandas as pd
from plantdata import PlantData

# How can I avoid instantiating class here? I should be able to use it within class later...
# I think I want to combine PlantsDB and PlantData classes...
plant_data = PlantData()


class PlantsDB(AnchorLayout, PlantData):
    def __init__(self, **kwargs):
        super(PlantsDB, self).__init__(**kwargs)
        # Why doesn't self.data work below if the class inherits from PlantData?
        column_data, row_data = self.get_data_table()
        column_data = [(x, dp(60)) for x in column_data]
        table = MDDataTable(
            column_data = column_data,
            row_data = row_data,
            use_pagination=True,
            check=True,
            rows_num = 25
        )
        self.add_widget(table)


class TreeButton(Button):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    # allow deselection ***How can I make this clear plant_attr text?
    touch_deselect_last = BooleanProperty(True)


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class MainApp(MDApp, PlantData):

    def __init__(self):
        super(MainApp, self).__init__()
        # Because App inherits from PlantData I can manage all database functionality there
        self.all_filters = {'hardiness_zone': [],
                            'form': [],
                            'foliage': [],
                            'pollinators': [],
                            'growth_rate': [],
                            'flower_month': 'Any'
                            }

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.load_kvs()
        return Builder.load_file("main.kv")

    def process_rb(self, widget, state, value, category):
        if state == 'down':
            self.all_filters[category] = value
        else:
            self.all_filters[category] = 'Any'

    def process_checkbox(self, widget, state, value, category):
        if state == 'down':
            self.all_filters[category].append(value)
        else:
            self.all_filters[category].remove(value)
        print(self.all_filters)

    def process_slider(self, *args):
        category = args[0]
        value = args[2]
        self.all_filters[category] = value

    def load_kvs(self):
        # load components
        path_prefix = "libs/components/"
        for component in os.listdir(path_prefix):
            Builder.load_file(f"{path_prefix}{component}/{component}.kv")
        # load screens
        path_prefix = "libs/screens/"
        for screen in os.listdir(path_prefix):
            Builder.load_file(f"{path_prefix}{screen}/{screen}.kv")
        # load left screens
        path_prefix = "libs/left_screens/"
        for left_screen in os.listdir(path_prefix):
            Builder.load_file(f"{path_prefix}{left_screen}/{left_screen}.kv")
        # load layouts
        Builder.load_file("libs/center_display/center_display.kv")
        Builder.load_file("libs/left_panel/left_panel.kv")


    # for chips on filter
    def removes_marks_all_chips(self):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip.active:
                instance_chip.active = False


if __name__ == '__main__':
    MainApp().run()
