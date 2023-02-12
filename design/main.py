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
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivymd.icon_definitions import md_icons
from kivy.uix.tabbedpanel import TabbedPanel
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.textfield import MDTextField
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from plantdata import PlantData

plant_data = PlantData()

class SearchTextField(MDTextField):
    pass

class LeftPanel(TabbedPanel):
    pass

class DesignPanel(MDRelativeLayout):
    def area_text(self):
        if self.plot_length.text and self.plot_width.text:
            return int(self.plot_length.text) * int(self.plot_width.text)

class TreeButton(Button):
    pass

class UnitSelection(GridLayout):
    def units_selected(self, instance, value):
        if value == True:
            return 'meters'
        else:
            return 'feet'


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    # allow deleselection ***How can I make this clear plant_attr text?
    touch_deselect_last = BooleanProperty(True)

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            rv.get_selected()
            return index

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def get_selected(self):
        app = MDApp.get_running_app()
        if len(self.layout_manager.selected_nodes) > 0:
            all_attrs = str(app.root.results[self.data[self.layout_manager.selected_nodes[-1]]['text']])
            attrs_label = app.root.ids['plant_attrs']
            attrs_label.text = all_attrs
        else:
            return ''

class Main(BoxLayout):

    def search(self, value): # called from TextInput on_text_validate (Enter)
        self.results = {plant_series[1]['CommonName'].split(',')[0]: plant_series[1].drop(columns='CommonName')\
            for plant_series in plant_data.call_plant(value.text).iterrows()}

        rv = self.ids.rv
        if len(self.results) > 0:
            rv.data = [{'text': plant} for plant in self.results.keys()]
        else:
            rv.data = [{'text': 'No results found'}]

        # Unselect RecycleView selection if selected
        try:
            rv.layout_manager.deselect_node(rv.layout_manager.selected_nodes[-1])
        except IndexError:
            pass

        # Clear plant attributes from previous search
        self.ids.plant_attrs.text = ''

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Main()


if __name__ == '__main__':
    MainApp().run()
