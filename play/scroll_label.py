from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivy.properties import StringProperty

from kivy.base import runTouchApp
from kivy.lang import Builder

Builder.load_string('''
<ScrollableLabel>:
    text: str('This is the song that never ends, it just goes on and on my friends' * 50)
    Label:
        text: self.parent.text
        font_size: 50
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

runTouchApp(ScrollableLabel())
