import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

import requests
import json
import asyncio
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class CalculateScreen(GridLayout):
    def __init__(self, **kwargs):
        super(CalculateScreen, self).__init__(**kwargs)
        self.data = {}
        self.cols = 2
        self.add_widget(Label(text='Enter your API key:'))
        self.api_key = TextInput(multiline=False)
        self.add_widget(self.api_key)
        self.add_widget(Label(text='Enter your private key:'))
        self.private_key = TextInput(multiline=False)
        self.add_widget(self.private_key)
        self.button = Button(text='Calculate')
        self.add_widget(self.button)
        self.button.bind(on_press=self.calculate)
        self.result = Label(text='Result:')
        self.add_widget(self.result)
        self.progress = ProgressBar(value=0, max=100)

    def calculate(self, instance):
        self.button.text = 'Calculating...'
        self.button.disabled = True
        self.api_key.disabled = True
        self.private_key.disabled = True
        self.button.background_color = (0.5, 0.5, 0.5, 1)
        self.progress.value = 0
        self.add_widget(self.progress)
        self.result.text = str({'api_key': self.api_key.text, 'private_key': self.private_key.text})
        print(self.result.text)
        # asyncio.ensure_future(self.calculate_async())


class MyDesktop(Widget):
    def __init__(self, **kwargs):
        super(MyDesktop, self).__init__(**kwargs)

    def build(self):
        return Label(text='Hello world')
    # def __init__(self, **kwargs):

    """def __init__(self):
        self.label = Label(text='Hello World', textwrap=True, font_size=50)
        self.submit_btn = Button(text='Submit', font_size=50)
        self.progress = ProgressBar(max=100, value=10)
        self.submit_btn.bind(on_press=self.submit_pressed)
        super(MyDesktop, self).__init__()
        
    def build(self):
        self.add_widget(self.label)
        self.add_widget(self.submit_btn)
        self.add_widget(self.progress)
        return self"""


class MyApp(App):
    def build(self):
        return CalculateScreen()


if __name__ == '__main__':
    MyApp().run()
