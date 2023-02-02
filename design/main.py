from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized') # Maximize window on startup

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle

BACKGROUND_IMAGE = 'images/largefield1.png'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = MasterLayout()
        self.add_widget(self.layout)

class MasterLayout(MDBoxLayout):
    pass

class LeftPanel(BoxLayout):
    pass

class DesignPanel(MDRelativeLayout):

    def __init__(self, **kwargs):
        super(DesignPanel, self).__init__(**kwargs)
        self.background = BACKGROUND_IMAGE

    def add_plant(self, size, pos):
        plant = DraggableImage(source='images/tree1.png',
                              size_hint=(None, None),
                              size=size,
                              pos=pos)
        # tree.on_motion(me=True, etype='begin') #This didn't work to make drag default
        self.add_widget(plant)

    def activate_drag(self, instance):
        # to-do
        pass

class DraggableImage(DragBehavior, Image):
    pass

class IconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        root=ScreenManager()
        root.add_widget(MainScreen(name='main'))
        return root

if __name__ == '__main__':
    MainApp().run()
