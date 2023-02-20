from kivy.uix.gridlayout import GridLayout

class UnitSelection(GridLayout):
    def units_selected(self, instance, value):
        if value == True:
            return 'meters'
        else:
            return 'feet'