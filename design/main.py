from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout


class DraggableImage(DragBehavior, Image):
    pass

class IconButton(ButtonBehavior, Image):

    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)

class MasterLayout(BoxLayout):
    pass

class MapLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(MapLayout, self).__init__(**kwargs)

    def add_tree(self, size, pos):
        tree = DraggableImage(source='images/tree1.png',
                              size_hint=(None, None),
                              size=size,
                              pos=pos)
        # tree.on_motion(me=True, etype='begin') #This didn't work to make drag default
        self.add_widget(tree)

class MainApp(App):
    def build(self):
        return MasterLayout()


if __name__ == '__main__':
    MainApp().run()
