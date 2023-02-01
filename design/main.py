from kivy.config import Config
# Config.set('graphics', 'window_state', 'maximized') # Maximize window on startup

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle

from kivy.uix.stencilview import StencilView


class DraggableImage(DragBehavior, Image):
    pass

class IconButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)

class MasterLayout(BoxLayout):
    pass

class BackgroundImage(Image):
    def adjust_image_size(self, stencil):
        stencil_ratio = stencil.width / float(stencil.height)
        if self.image_ratio > stencil_ratio:
            self.width = stencil.height * self.image_ratio
            self.height = stencil.height
        else:
            self.width = stencil.width
            self.height = stencil.width / self.image_ratio

class MyStencilView(RelativeLayout, StencilView):

    def __init__(self, **kwargs):
        super(MyStencilView, self).__init__(**kwargs)

    def on_size(self, *args):
        self.children[0].adjust_image_size(self)

    def add_tree(self, size, pos):
        tree = DraggableImage(source='images/tree1.png',
                              size_hint=(None, None),
                              size=size,
                              pos=pos)
        # tree.on_motion(me=True, etype='begin') #This didn't work to make drag default
        self.add_widget(tree)

    def activate_drag(self, instance):
        # to-do
        pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return MasterLayout()


if __name__ == '__main__':
    MainApp().run()
