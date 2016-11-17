'''
Author: Aleksandr Spiridonov
This is a quick example of an app that will be modified for
mirroring to an HDMI driven screen with interactive UI on
a Raspberry Pi touchscreen.
'''

import os

os.environ["KIVY_BCM_DISPMANX_ID"] = "4"

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import operator


class ButtonDIPO(Button):
    def __init__(self,dictionary,key_string,in_place_operator,IPO_value,**kwargs):
        super(ButtonDIPO, self).__init__(**kwargs)
        self.dictionary = dictionary
        self.key_string = key_string
        self.IPO = in_place_operator
        self.IPO_value = IPO_value

    def on_press(self):
        self.dictionary[self.key_string] = self.IPO(self.dictionary[self.key_string],self.IPO_value)

class LabelD(Label):
    def __init__(self,dictionary,key_string,**kwargs):
        super(LabelD, self).__init__(**kwargs)
        self.dictionary = dictionary
        self.key_string = key_string
        Clock.schedule_interval(self.update, 1 / 30.)

    def update(self, *args):
        self.text = str(self.dictionary[self.key_string])



class MyApp(App):
    def __init__(self,dictionary):
        App.__init__(self)
        self.dict_local = dictionary

    def build(self):
        layout1 = BoxLayout(orientation='horizontal',spacing=10)
        layout1.add_widget(LabelD(self.dict_local,'counter',font_size=200))
        layout2 = BoxLayout(orientation='vertical', spacing=10)
        layout2.add_widget(ButtonDIPO(self.dict_local,'counter',operator.add,1,text="+1",font_size=200))
        layout2.add_widget(ButtonDIPO(self.dict_local, 'counter', operator.mul, 0, text="Reset",font_size=200))
        layout1.add_widget(layout2)

        return layout1



if __name__ == '__main__':
    dict_global = {}
    dict_global['counter'] = 0
    app = MyApp(dict_global)
    app.run()

