from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized') # Maximize window on startup
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivymd.uix.textfield import MDTextField
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.chip import MDChip
from kivy.animation import Animation
from kivy.metrics import dp
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
            rows_num = 25
        )
        self.add_widget(table)

class MyChip(MDChip):
    icon_check_color = (0, 0, 0, 1)
    text_color = (0, 0, 0, 0.5)
    _no_ripple_effect = False
    # elevation = 1
    # md_bg_color = (56/255, 71/255, 11/255, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.set_chip_bg_color)
        self.bind(active=self.set_chip_text_color)

    def set_chip_bg_color(self, instance_chip, active_value: int):
        '''
        Will be called every time the chip is activated/deactivated.
        Sets the background color of the chip.
        '''

        self.md_bg_color = (
            (0, 0, 0, 0.4)
            if active_value
            else (
                self.theme_cls.bg_darkest
                if self.theme_cls.theme_style == "Light"
                else (
                    self.theme_cls.bg_light
                    if not self.disabled
                    else self.theme_cls.disabled_hint_text_color
                )
            )
        )

    def set_chip_text_color(self, instance_chip, active_value: int):
        Animation(
            color=(0, 0, 0, 1) if active_value else (0, 0, 0, 0.5), d=0.2
        ).start(self.ids.label)


class SearchTextField(MDTextField):
    pass


class LeftPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super(LeftPanel, self).__init__(**kwargs)
        self.bind(current_tab=self.contentChanged_cb)

    # Used for chips
    def contentChanged_cb(self, obj, value):
        print(f'Change -- obj: {obj} \nvalue: {value}')

    def print_ids(self):
        for id in self.ids:
            print(id)


class CenterDisplay(MDRelativeLayout):
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
        app = MDApp.get_running_app() # Better way to bind to this function in kivy?
        if len(self.layout_manager.selected_nodes) > 0:
            all_attrs = app.root.results[self.data[self.layout_manager.selected_nodes[-1]]['text']]
            attrs_label = app.root.ids['plant_attrs']
            # Probably the best way to do this would be to put each attribute (there are many more) on its own line or list item
            attrs_label.text = f"Height: {str(all_attrs['Height'])} \n\n Habitat: {str(all_attrs['Habitat'])}"
        else:
            return ''


class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    # for chips on filter
    def removes_marks_all_chips(self):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip.active:
                instance_chip.active = False


class MainApp(MDApp):
    # Colors are temporary
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Main()


if __name__ == '__main__':
    MainApp().run()
