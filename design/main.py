from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized') # Maximize window on startup

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.graphics.vertex_instructions import Ellipse
from kivy.graphics.context_instructions import Color
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons
from kivy.uix.tabbedpanel import TabbedPanel


BACKGROUND_IMAGE = 'images/largefield1.png'

class MyScreenManager(ScreenManager):
    pass

class DesignScreen(Screen):
    pass

class PlantsScreen(Screen):
    pass

class MasterLayout(MDBoxLayout):
    pass

class LeftPanel(TabbedPanel):
    pass

class DesignPanel(MDRelativeLayout):
    def area_text(self):
        if self.plot_length.text and self.plot_width.text:
            return int(self.plot_length.text) * int(self.plot_width.text)

    # def __init__(self, **kwargs):
    #     super(DesignPanel, self).__init__(**kwargs)
    #     self.background = BACKGROUND_IMAGE

    # def add_plant(self, size, pos):
    #     plant = DraggableImage(size=size,
    #                           pos=pos)
    #     # tree.on_motion(me=True, etype='begin') #This didn't work to make drag default
    #     self.add_widget(plant)

    # def activate_drag(self, instance):
    #     # to-do
    #     pass

class Tab(MDFloatLayout, MDTabsBase):
    pass

class DraggableImage(DragBehavior, Image):
    pass

class TreeButton(Button):
    pass

class UnitSelection(GridLayout):
    def units_selected(self, instance, value):
        if value == True:
            return 'meters'
        else:
            return 'feet'


class LeftPanelDropdown(FloatLayout):
    def dropdown(self):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'Example 1',
                'on_release': lambda x = 'Example 1': self.test1()
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'Example 2',
                'on_release': lambda x = 'Example 2': self.test2()
            }
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.menu,
            items = self.menu_list,
            width_mult = 3
        )
        self.menu.open()

    def test1(self):
        print('Function test1 activated.')

    def test2(self):
        print('Function test2 activated.')

    # Builder.load_file('left_dropdown.kv')

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        sm=ScreenManager()
        sm.add_widget(DesignScreen(name='design'))
        sm.add_widget(PlantsScreen(name='plants'))
        return sm

if __name__ == '__main__':
    MainApp().run()
