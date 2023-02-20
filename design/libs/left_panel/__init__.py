from kivy.uix.tabbedpanel import TabbedPanel

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