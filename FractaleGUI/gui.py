import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class NestedFloatLayout(FloatLayout):
    pass


class FractaleGUI(App):

    def build(self):
        return NestedFloatLayout()

a = FractaleGUI()
a.run()
