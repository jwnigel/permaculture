from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image


class MyLayout(Widget):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.tree_btn = self.ids.tree_btn

    def add_tree(self, touch):
        self.img = Image(source='images/tree1.png', pos=touch.pos)
        self.add_widget(self.img)
        self.img.pos = touch.pos

    def on_touch_move(self, touch):
        try:
            self.img.pos = touch.pos
        except AttributeError:   # if image hasn't been created yet (button not pressed)
            pass


class MainApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MainApp().run()
