from kivymd.uix.screen import MDScreen

class FirstScreen(MDScreen):
    def area_text(self):
        if self.plot_length.text and self.plot_width.text:
            return int(self.plot_length.text) * int(self.plot_width.text)