from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from plantdata import PlantData


plant_data = PlantData()

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


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
        app = App.get_running_app()
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            app.root.ids.plant_attrs.text = rv.data[index]['text']


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.results = []
        self.data = [{'text': res} for res in range(len(self.results))]

class MainLayout(BoxLayout):

    def search(self, value):
        results = plant_data.call_plant(value.text)
        if len(results) > 0:
            self.ids.rv.data = [{'text': res} for res in results]
        print(f'search results: {results}')
        print(self.ids.rv.data)

class SearchApp(App):
    def build(self):
        return MainLayout()




if __name__ == '__main__':
    SearchApp().run()
