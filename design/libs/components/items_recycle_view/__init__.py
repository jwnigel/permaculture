from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def get_selected(self):
        app = MDApp.get_running_app() # Better way to bind to this function in kivy?
        if len(self.layout_manager.selected_nodes) > 0:
            all_attrs = app.results_dict[self.data[self.layout_manager.selected_nodes[-1]]['text']]
            attrs_label = app.root.ids.left_panel.ids.second_screen.ids['plant_attrs']
            # Probably the best way to do this would be to put each attribute (there are many more) on its own line or list item
            attrs_label.text = f"Height: {str(all_attrs['Height'])} \n\n Habitat: {str(all_attrs['Habitat'])}"
        else:
            return ''
