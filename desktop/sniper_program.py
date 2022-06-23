import kivy
from kivy.app import App
from kivy.uix.widget import Widget

#
# class MyWidget(Widget):
#     pass


class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()

# class MyApp(App):
#     def build(self):
#         return MyWidget()


if __name__ == '__main__':
    PongApp().run()
