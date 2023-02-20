from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.app import MDApp

class MyCheckbox(MDCheckbox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.bind(active=self.on_checkbox_active)

    def on_checkbox_active(self, instance, value):
        if value:
            print('The checkbox', self, instance, 'is active', value)
        else:
            print('The checkbox', self, instance, 'is inactive', value)
