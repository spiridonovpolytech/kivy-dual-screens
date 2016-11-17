'''
Author: Aleksandr Spiridonov
This is a quick example of an app that will be modified for
mirroring to an HDMI driven screen with interactive UI on
a Raspberry Pi touchscreen.
'''

from multiprocessing import Process, Manager, Event

def display_process(dict_global, is_master, exit_event):

    import os

    if is_master:
        os.environ["KIVY_BCM_DISPMANX_ID"] = "4"
    else:
        os.environ["KIVY_BCM_DISPMANX_ID"] = "5"

    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.clock import Clock
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label

    import operator


    class ButtonDIPO(Button):
        def __init__(self,key_string,in_place_operator,IPO_value,**kwargs):
            super(ButtonDIPO, self).__init__(**kwargs)
            #dictionary is now global
            #self.dictionary = dictionary
            self.key_string = key_string
            self.IPO = in_place_operator
            self.IPO_value = IPO_value

        if is_master:
            def on_press(self):
                dict_global[self.key_string] = self.IPO(dict_global[self.key_string],self.IPO_value)

    class LabelD(Label):
        def __init__(self,key_string,**kwargs):
            super(LabelD, self).__init__(**kwargs)
            # dictionary is now global
            # self.dictionary = dictionary
            self.key_string = key_string
            Clock.schedule_interval(self.update, 1 / 30.)

        def update(self, *args):
            self.text = str(dict_global[self.key_string])



    class MyApp(App):
        def __init__(self):
            App.__init__(self)
            # dictionary is now global
            # self.dict_local = dictionary
            if is_master:
                self.title = 'Master display'
            else:
                self.title = 'Slave display'
            Clock.schedule_interval(self.update, 1 / 30.)


        def build(self):
            layout1 = BoxLayout(orientation='horizontal',spacing=10)
            layout1.add_widget(LabelD('counter',font_size=200))
            layout2 = BoxLayout(orientation='vertical', spacing=10)
            layout2.add_widget(ButtonDIPO('counter',operator.add,1,text="+1",font_size=200))
            layout2.add_widget(ButtonDIPO('counter', operator.mul, 0, text="Reset",font_size=200))
            layout1.add_widget(layout2)

            return layout1

        def update(self, *args):
            if exit_event.is_set():
                exit()

        def on_stop(self):
            exit_event.set()

    app = MyApp()
    app.run()



if __name__ == '__main__':
    m = Manager()
    dict_main = m.dict()
    ev = Event()
    dict_main['counter'] = 0
    proc_master = Process(target=display_process, args=(dict_main,True, ev))
    proc_slave = Process(target=display_process, args=(dict_main, False, ev))
    proc_master.start()
    proc_slave.start()
    proc_master.join()
    proc_slave.join()

