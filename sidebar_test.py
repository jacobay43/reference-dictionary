from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class A(App):
    def build(self):
        return GridLayout(SideBar())