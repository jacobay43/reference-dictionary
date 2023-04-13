import json
import random
from kivy.app import App
from kivy.properties import StringProperty,BooleanProperty
from navigationdrawer import NavigationDrawer
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label

class SelectableRecycleBoxLayout(FocusBehavior,LayoutSelectionBehavior,RecycleBoxLayout):
    def on_touch_down(self,touch):
        view_index = self.get_view_index_at(touch.pos)
        selected_word = self.parent.data[view_index]['text']
        self.parent.root.lookup_word(selected_word)
        self.parent.root.toggle_state()
class WordListLabel(RecycleDataViewBehavior,Label): 
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super().refresh_view_attrs(rv, index, data)
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch) #only word at the touched index is selected
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
class RV(RecycleView):
    umpth = 500
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with open('dictionary.json','r') as fh:
            dictionary = json.load(fh)
            self.data = ({'text':word} for word in list(dictionary.keys())[::self.umpth]) #list every umpteenth word in the dictionary
            self.data = sorted(self.data, key=lambda x: x['text']) #sort the words a-z
class Dictionary(NavigationDrawer): #in NavigationDrawer only 2 widgets are added, 1st becomes the side panel, second the main panel
    search_result = StringProperty()
    def lookup_word(self,word):
        with open('dictionary.json','r') as fh:
            dictionary = json.load(fh)
            result = dictionary.get(word.lower(),'')
            if result:
                self.search_result = f'[u][b]{word.capitalize()}[/b][/u]\n{result}'
            else:
                self.search_result = 'No Definition Found'
    def display_random_word(self):
        with open('dictionary.json','r') as fh:
            dictionary = json.load(fh)
            word = random.choice(list(dictionary.keys())) #select and display a random word from the dictionary
            self.search_result = f'[u][b]{word.capitalize()}[/b][/u]\n{dictionary.get(word)}'
            self.toggle_state() #hide the NavigationDrawer
    def display_definition(self):
        self.display_random_word()
class DictionaryApp(App):
    def build(self):
        self.title = 'Reference Dictionary'
        self.icon = 'dictionary_icon.jpg'
        return Dictionary()
if __name__ == '__main__':
    DictionaryApp().run() #Window.clearcolor isn't needed since kivy-garden-navigationdrawer has been modified globally to white for this app's use, consider building before changing the rgb values in site-packages