from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem.dropdownitem import MDDropDownItem
from kivymd.app import MDApp

MONTHS = ['Any', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


class MonthsDropDownItem(MDDropDownItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": month,
                "viewclass": "OneLineListItem",
                "height": dp(54),
                "on_release": lambda x=month: self.menu_callback(x),
            } for month in MONTHS
        ]
        self.menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
        )

    def menu_callback(self, text_item):
        app = MDApp.get_running_app()
        print(text_item)
        self.text = text_item
        app.all_filters['flower_month'] = text_item
        self.menu.dismiss()
