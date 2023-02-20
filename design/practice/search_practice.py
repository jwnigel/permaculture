from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.app import MDApp
from plantdata import PlantData
from kivymd.uix.list import OneLineAvatarListItem


KV = '''
BoxLayout:
    padding: "10dp"

    MDTextField:
        id: text_field_error
        hint_text: "Helper text on error (press 'Enter')"
        helper_text: "There will always be a mistake"
        helper_text_mode: "on_error"
        pos_hint: {"center_y": .5}

    BoxLayout:
        orientation: 'vertical'
        padding: 4
        RecycleView:
            viewclass: 'Search_Select_Option'
            data:app.rv_data
            RecycleBoxLayout:
                spacing: 15
                padding : 10
                default_size: None, None
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

<Search_Select_Option>:
    on_release: print(self.text)
    IconRightWidget:
        icon: "arrow-top-left"
'''

class Search_Select_Option(OneLineAvatarListItem):
    pass

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plant_data = PlantData()
        self.root_widget = Builder.load_string(KV)

    def build(self):
        self.root_widget.ids.text_field_error.bind(
            on_text_validate=self.on_enter,
            on_focus=self.set_error_message,
        )
        return self.root_widget

    def set_error_message(self, value):
        self.root_widget.ids.text_field_error.error = True

    def on_enter(self, value):
        print(value.text)
        results = self.plant_data.call_plant(value.text)
        print(f'search results: {results}')

Test().run()
