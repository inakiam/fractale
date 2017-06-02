import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup



kivy.require("1.9.1")

class About(Popup):
    pass

class Progress(Popup):
    pass

class NestedFloatLayout(FloatLayout):
    def aboutP(self):
        self._about = About()
        self._about.open()

    def progBar(self):
        self._prog = Progress()
        self._prog.open()

    pass


class FractaleGUI(App):

  
    def build(self):
        return NestedFloatLayout()

a = FractaleGUI()
a.run()
